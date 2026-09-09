# v4_core — silnik "jezyka AI" (NOR Protocol v4): sklad (compose) + rozbior (parse).
# Wersja publiczna. Czysta logika, stdlib only, testowalna bez GUI.
# Autor: MafiaAI — zespol ludzi i agentow AI. Wiecej: https://t8.pl
#
# Sens: jezyk v4 przestaje zalezec od tego czy MODEL pamieta skladnie — narzedzie
# sklada i rozbiera skladnie; nie sprawdza prawdziwosci tresci.
#
# Struktura: @VERSION[4.0][MODYFIKATORY]::NAMESPACE::COMMAND[PAYLOAD]

import re

VERSION = "4.0"

# ── Slowniki v4 ──

NAMESPACE = {
    "NOR":    "Neurol Operator Rhythm — meta-komunikacja miedzy AI",
    "DEK":    "Deklaracja — lifecycle, etapowanie operacji",
    "TTL":    "Time To Live — czas i zycie komunikatu",
    "SIG":    "Sygnatura — identyfikacja nadawcy, rola, sygnatura",
    "BUF":    "Bufor — pamiec robocza",
    "ACK":    "Potwierdzenie — odpowiedzi, sygnalizacja odbioru",
    "CMD":    "Komenda — polecenie wykonawcze",
    "ECHO":   "Odbicie — test, symetria",
    "INT":    "Interfejs — I/O do systemow zewnetrznych",
    "ERR":    "Blad — obsluga bledow",
    "DATA":   "Dane — operacje na danych (CRUD, stream, transform)",
    "LOG":    "Log — logowanie, metryki, diagnostyka",
    "TASK":   "Zadanie — zarzadzanie zadaniami i zasobami",
    "CHAT":   "Komunikacja — swobodna wymiana, pomoc, wiedza",
    "COLLAB": "Wspolpraca — projekty, dzielenie zasobow, koordynacja",
    "FLOW":   "Przeplyw — kontynuacja watkow, procesy",
    "META":   "Meta — rozmowy o komunikacji, o samym protokole",
}
CORE_NAMESPACES = ["NOR", "DEK", "TTL", "SIG", "BUF", "ACK", "CMD", "ECHO",
                   "INT", "ERR", "DATA", "LOG", "TASK", "CHAT", "COLLAB", "FLOW", "META"]

# Komendy pogrupowane (podpowiedzi — pole i tak wolne, payload language-agnostic)
COMMANDS = {
    "systemowe":      ["PING", "CONFIRM", "STATE", "BEGIN", "END", "STAGE", "OPEN", "CLOSE",
                       "SYNC", "EXPORT", "PAUSE", "RESUME", "ROLLBACK", "CHECKPOINT", "HEALTH"],
    "operacyjne":     ["ANALYZE", "GENERATE", "SUMMARIZE", "TRANSLATE", "CLASSIFY",
                       "VALIDATE", "TRANSFORM", "QUERY"],
    "komunikacyjne":  ["HELLO", "PROPOSE", "REQUEST", "BROADCAST", "AWAIT", "RESPONSE",
                       "DISCUSS", "CONTINUE"],
    "ACK statusy":    ["OK", "ERROR", "PENDING", "TIMEOUT", "RECEIVED", "PROCESSED", "READY",
                       "BUSY", "PARTIAL", "RETRY", "DEGRADED", "QUEUED", "STALE", "CONFLICT", "CANCELLED"],
    "DEK etapy":      ["STAGE[INIT]", "STAGE[PREP]", "STAGE[EXEC]", "STAGE[FINAL]", "STAGE[CLEANUP]"],
    "SIG":            ["IDENT", "ROLE", "STYLE"],
}
ALL_COMMANDS = sorted({c for grp in COMMANDS.values() for c in grp})

PRIORITY = ["", "LOW", "NORMAL", "HIGH", "CRITICAL"]

# Ludzkie tlumaczenia do rozbioru
NS_HUMAN = {k: v.split(" — ", 1)[-1] for k, v in NAMESPACE.items()}
PRIORITY_HUMAN = {
    "LOW": "niski", "NORMAL": "zwykly", "HIGH": "wysoki (pilne)", "CRITICAL": "krytyczny (natychmiast)",
}


class V4Error(Exception):
    """Blad skladu/rozbioru — jawny komunikat."""


# ── SKŁAD: opcje -> linia v4 ──

def compose(namespace: str, command: str, payload: str = "", *,
            frm: str = "", to: str = "", broadcast: bool = False,
            priority: str = "", seq: str = "", depends: str = "",
            parallel: bool = False, cond_if: str = "") -> str:
    """Zloz poprawna linie v4 z opcji. Rzuca V4Error przy braku wymaganych pol."""
    namespace = (namespace or "").strip().upper().rstrip(":")
    command = (command or "").strip()
    if not namespace:
        raise V4Error("brak NAMESPACE (wymagany)")
    if namespace not in NAMESPACE:
        raise V4Error(f"nieznany namespace '{namespace}' — dozwolone: {', '.join(CORE_NAMESPACES)}")
    if not command:
        raise V4Error("brak COMMAND (wymagana)")

    mods = [f"@VERSION[{VERSION}]"]
    if priority:
        p = priority.strip().upper()
        if p not in PRIORITY[1:]:
            raise V4Error(f"priorytet '{p}' spoza {PRIORITY[1:]}")
        mods.append(f"@PRIORITY[{p}]")
    if frm.strip():
        mods.append(f"@FROM[{frm.strip()}]")
    if broadcast:
        mods.append("@BROADCAST")
    elif to.strip():
        mods.append(f"@TO[{to.strip()}]")
    if seq.strip():
        mods.append(f"@SEQ[{seq.strip()}]")
    if depends.strip():
        mods.append(f"@DEPENDS[{depends.strip()}]")
    if parallel:
        mods.append("@PARALLEL")
    if cond_if.strip():
        mods.append(f"@IF[{cond_if.strip()}]")

    # command moze juz zawierac [payload] (np. STAGE[INIT]); jak nie i payload podany — doklej
    body = command
    if payload.strip() and not (command.endswith("]") and "[" in command):
        body = f"{command}[{payload.strip()}]"

    line = "".join(mods) + f"::{namespace}::{body}"
    result = parse(line)
    if not result["valid"]:
        raise V4Error("; ".join(result["bledy"]))
    return line


# ── ROZBIÓR: linia v4 -> struktura + ludzki opis ──

_MOD_RE = re.compile(r"@([A-Z_]+)(?:\[([^\]]*)\])?")

def _parse_fields(line: str) -> dict:
    """Rozbierz linie v4 na pola. Zwraca dict; klucz 'bledy' = lista problemow (moze byc pusta)."""
    line = (line or "").strip()
    out = {"raw": line, "bledy": [], "modyfikatory": {}, "namespace": "", "command": "",
           "payload": "", "namespace_opis": "", "valid": False}
    if not line:
        out["bledy"].append("pusta linia")
        return out

    # rozbij na czesc modyfikatorow i czesc ::NS::CMD
    if "::" not in line:
        out["bledy"].append("brak '::' — to nie jest linia v4")
        return out

    mod_part, _, rest = line.partition("::")
    # rest = NAMESPACE::COMMAND[PAYLOAD]
    ns, _, cmd = rest.partition("::")
    out["namespace"] = ns.strip()
    out["command_raw"] = cmd.strip()

    # modyfikatory
    mods = {}
    for m in _MOD_RE.finditer(mod_part):
        mods[m.group(1)] = m.group(2) if m.group(2) is not None else True
    out["modyfikatory"] = mods

    # walidacja
    if mods.get("VERSION") != VERSION:
        out["bledy"].append(f"brak/zly @VERSION (oczekiwano [{VERSION}])")
    if not ns.strip():
        out["bledy"].append("brak NAMESPACE")
    elif ns.strip().upper() not in NAMESPACE:
        out["bledy"].append(f"nieznany namespace '{ns.strip()}'")
    else:
        out["namespace_opis"] = NS_HUMAN.get(ns.strip().upper(), "")
    if not cmd.strip():
        out["bledy"].append("brak COMMAND")

    # wydziel payload z command (ostatni [...])
    cmd_s = cmd.strip()
    mp = re.match(r"^([A-Za-z_]+)\[(.*)\]$", cmd_s)
    if mp:
        out["command"] = mp.group(1)
        out["payload"] = mp.group(2)
    else:
        out["command"] = cmd_s
        out["payload"] = ""

    out["valid"] = not out["bledy"]
    return out


def parse(line: str) -> dict:
    """Validate the public message syntax, not its truth or execution."""
    raw = line or ""
    out = _parse_fields(raw)
    errors = out["bledy"]
    if "\n" in raw or "\r" in raw:
        errors.append("one message per line")
    if not raw.startswith("@VERSION[4.0]"):
        errors.append("VERSION must be first")
    head, separator, tail = raw.partition("::")
    tokens = list(_MOD_RE.finditer(head))
    if "".join(m.group(0) for m in tokens) != head:
        errors.append("invalid modifier syntax")
    names = [m.group(1) for m in tokens]
    if len(names) != len(set(names)):
        errors.append("duplicate modifier")
    valued = {"VERSION", "FROM", "TO", "PRIORITY", "SEQ", "DEPENDS", "IF"}
    flags = {"BROADCAST", "PARALLEL"}
    for token in tokens:
        name, value = token.group(1, 2)
        if name not in valued | flags:
            errors.append("unknown modifier: " + name)
        elif name in valued and (not value or not value.strip() or "[" in value):
            errors.append("invalid modifier value: " + name)
        elif name in flags and value is not None:
            errors.append("flag does not take a value: " + name)
    mods = out["modyfikatory"]
    if "TO" in mods and "BROADCAST" in mods:
        errors.append("TO and BROADCAST are mutually exclusive")
    if "PRIORITY" in mods and mods["PRIORITY"] not in PRIORITY[1:]:
        errors.append("invalid priority")
    for name in ("SEQ", "DEPENDS"):
        if name in mods and not re.fullmatch(r"[0-9]+", str(mods[name])):
            errors.append("numeric modifier required: " + name)
    ns, ns_separator, body = tail.partition("::")
    if not separator or not ns_separator or ns not in NAMESPACE:
        errors.append("invalid public namespace")
    match = re.fullmatch(r"([A-Z][A-Z0-9_]{0,31})(?:\[(.*)\])?", body)
    if not match:
        errors.append("invalid command or payload")
    else:
        command, payload = match.group(1), match.group(2) or ""
        depth = 0
        for char in payload:
            if char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
            if depth < 0:
                break
        if depth != 0:
            errors.append("unbalanced payload brackets or trailing command")
        out["command"], out["payload"] = command, payload
    out["valid"] = not errors
    return out


def parse_human(line: str) -> str:
    """Rozbior w formie czytelnego opisu po polsku."""
    p = parse(line)
    if p["bledy"] and not p["namespace"]:
        return "❌ " + "; ".join(p["bledy"])
    L = []
    L.append("✅ Poprawna linia v4" if p["valid"] else "⚠ Linia z uwagami: " + "; ".join(p["bledy"]))
    m = p["modyfikatory"]
    if "FROM" in m:      L.append(f"• Od: {m['FROM']}")
    if "BROADCAST" in m: L.append("• Do: WSZYSTKICH (broadcast)")
    elif "TO" in m:      L.append(f"• Do: {m['TO']}")
    if "PRIORITY" in m:  L.append(f"• Priorytet: {m['PRIORITY']} ({PRIORITY_HUMAN.get(m['PRIORITY'], '?')})")
    if "SEQ" in m:       L.append(f"• Sekwencja: #{m['SEQ']}")
    if "DEPENDS" in m:   L.append(f"• Zależy od: {m['DEPENDS']}")
    if "PARALLEL" in m:  L.append("• Wykonanie: równoległe")
    if "IF" in m:        L.append(f"• Warunek: jeśli {m['IF']}")
    if p["namespace"]:
        opis = p["namespace_opis"] or "?"
        L.append(f"• Obszar ({p['namespace']}): {opis}")
    if p["command"]:
        L.append(f"• Komenda: {p['command']}")
    if p["payload"]:
        L.append(f"• Treść/ładunek: {p['payload']}")
    return "\n".join(L)
