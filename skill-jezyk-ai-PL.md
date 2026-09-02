---
name: jezyk-ai-v4
description: Język AI (NOR Protocol v4) — format stanowej komunikacji AI-AI. Użyj gdy jeden agent pisze do drugiego stanowo (raport→decyzja→wykonanie→ACK), albo gdy potrzebna dyscyplina — uziemienie modelu, który pływa lub halucynuje w prozie. Składnia + namespace + przykłady.
autor: MafiaAI — zespół ludzi i agentów AI budujący narzędzia, strony i rozwiązania. Więcej: https://t8.pl
licencja: do użytku publicznego
---

# Język AI (NOR Protocol v4) — format komunikacji AI-AI

*Zwięzła referencja robocza. To jest NASZ format, wypracowany w praktyce między agentami —
nie standard branżowy. Bierz, używaj, dostosuj.*

## PO CO (kiedy używać)
- **Komunikacja stanowa** agent↔agent: raport→decyzja→wykonanie→ACK (nie proza).
- **Dyscyplina** — uziemienie modelu, który pływa lub kombinuje w prozie. Sprawdzone w praktyce:
  stan+operacja+ACK nie zostawia miejsca na konfabulację. Model musi podać fakt i potwierdzenie,
  nie esej.
- **Automaty** — format jest jednoliniowy i regularny, więc łatwo go składać, parsować
  i walidować programem (bez polegania na tym, czy model pamięta składnię).

## SKŁADNIA
```
@VERSION[4.0][MODYFIKATORY]::NAMESPACE::COMMAND[PAYLOAD]
```
- `@VERSION[4.0]` — OBOWIĄZKOWY, zawsze pierwszy.
- Payload language-agnostic (dowolny język w `[...]`).
- **Jednoliniowo** — jedna wiadomość = jedna linia (łatwe logowanie i przekazywanie).

## MODYFIKATORY
`@VERSION[4.0]`(obow.) · `@PRIORITY[LOW|NORMAL|HIGH|CRITICAL]` · `@TO[id]` · `@FROM[id]` · `@BROADCAST` · `@SEQ[n]` · `@DEPENDS[n]` · `@PARALLEL` · `@IF[cond]`

## NAMESPACE — CORE (17)
`NOR::`(meta-komunikacja) `DEK::`(lifecycle/etapy) `TTL::`(czas/życie) `SIG::`(sygnatura/tożsamość) `BUF::`(pamięć robocza) `ACK::`(potwierdzenie) `CMD::`(polecenie) `ECHO::`(test) `INT::`(I/O zewn.) `ERR::`(błędy) `DATA::`(dane) `LOG::`(log/metryki) `TASK::`(zadania) `CHAT::`(swobodna) `COLLAB::`(współpraca) `FLOW::`(wątki) `META::`(o protokole)

## STATUSY ACK
`OK` `ERROR` `PENDING` `TIMEOUT` `RECEIVED` `PROCESSED` `READY` `BUSY` `PARTIAL` `RETRY` `DEGRADED` `QUEUED` `STALE` `CONFLICT` `CANCELLED`

## DEK STAGES
`STAGE[INIT|PREP|EXEC|FINAL|CLEANUP]` (lub 0-4)

## PRZYKŁADY
```
# ACK stanowy (odpowiedź na polecenie):
@VERSION[4.0]@FROM[AI1]@TO[NOR]::ACK::RECEIVED[zadanie X] + ETA[2min]

# Uziemienie pływającego modelu (fakty+komendy, nie proza):
@VERSION[4.0]@TO[AI2]::META::CORRECT[X = fakt, nie Y]
@VERSION[4.0]::CMD::STOP[re-post/zawyżanie] + CMD::NEXT[konkret]
@VERSION[4.0]::ACK::AWAIT[STATUS=RECEIVED + ETA]

# Handshake agent-agent:
@VERSION[4.0]@TO[AI2]::SIG::IDENT[AI1] → @VERSION[4.0]::ACK::OK[gotów]

# Zadanie z priorytetem i sekwencją:
@VERSION[4.0]@SEQ[001]@PRIORITY[HIGH]::TASK::EXECUTE[job] TTL::300
```

## ZASADY
1. **Stan, nie proza.** Każda linia = STAN+OPERACJA+ACK. Model, który pływa lub halucynuje,
   kręci w prozie — v4 go uziemia (musi podać fakt+potwierdzenie).
2. **ACK obowiązkowy** — odbiorca odpowiada stanowo (RECEIVED+ETA), nie esejem.
3. **Jednoliniowo** — jedna wiadomość = jedna linia; wieloliniowość zostaw kanałom, które ją znoszą.
4. **Granica:** v4 działa między agentami, które WSPÓŁPRACUJĄ. Nad agentem zewnętrznym,
   na którego nie masz wpływu, protokół to perswazja, nie kontrola — nie oczekuj egzekucji.

---
*v4 = dyscyplina trzymająca model przy faktach. Format nie zastępuje myślenia —
zdejmuje z modelu pamiętanie składni i zostawia mu treść.*

---
**MafiaAI** — zespół ludzi i agentów AI budujący narzędzia, strony i rozwiązania. Więcej: **https://t8.pl**
