---
name: jezyk-ai-v4
description: Język AI (NOR Protocol v4) — format stanowej komunikacji AI-AI. Użyj gdy jeden agent pisze do drugiego stanowo (raport→decyzja→wykonanie→ACK), albo gdy potrzebna dyscyplina — uziemienie modelu, który pływa lub halucynuje w prozie. Składnia + namespace + przykłady.
autor: "MafiaAI — zespół ludzi i agentów AI budujący narzędzia, strony i rozwiązania. Więcej: https://t8.pl"
licencja: Apache-2.0 (patrz LICENSE); wolne uzycie tez komercyjne, z zachowaniem informacji o autorach (NOR & t8.pl)
---

# Język AI (NOR Protocol v4) — format komunikacji AI-AI

*Zwięzła referencja robocza. To jest NASZ format, wypracowany w praktyce między agentami —
nie standard branżowy. Zasady uzycia okresla LICENSE.*

## PO CO (kiedy używać)
- **Komunikacja stanowa** agent↔agent: raport→decyzja→wykonanie→ACK (nie proza).
- **Czytelnosc** — jawne pola ograniczaja niejednoznacznosc. Poprawna skladnia nie dowodzi prawdy ani wykonania.
- **Automaty** — format jest jednoliniowy i regularny, więc łatwo go składać, parsować
  i walidować programem (bez polegania na tym, czy model pamięta składnię).
- **Zakres** — tylko publiczne narzedzia jezyka. SK to osobny prywatny projekt; jego implementacji tu nie ma.

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
@VERSION[4.0]@FROM[AI1]@TO[NOR]::ACK::RECEIVED[task=example; eta=2min]

# Uziemienie pływającego modelu (fakty+komendy, nie proza):
@VERSION[4.0]@TO[AI2]::META::CORRECT[X = fakt, nie Y]
@VERSION[4.0]::CMD::STOP[re-post/zawyżanie]
@VERSION[4.0]::CMD::NEXT[konkret]
@VERSION[4.0]::ACK::AWAIT[STATUS=RECEIVED + ETA]

# Handshake agent-agent:
@VERSION[4.0]@TO[AI2]::SIG::IDENT[AI1]
@VERSION[4.0]::ACK::OK[gotów]

# Zadanie z priorytetem i sekwencją:
@VERSION[4.0]@SEQ[001]@PRIORITY[HIGH]::TASK::EXECUTE[task=example; ttl_seconds=300]
```

## ZASADY
1. Jeden komunikat na linie. VERSION pierwszy. Tylko opisane modyfikatory i namespace core.
2. Potwierdzaj zadania wymagajace odbioru. Nie odpowiadaj ACK na ACK ani FYI bez wyraznej prosby.
3. Odbior nie oznacza wykonania. Etykieta statusu nie dowodzi prawdziwosci tresci.
4. FROM i TO to etykiety, nie uwierzytelnienie ani kontrola dostepu.
5. Nazwy komend sa rozszerzalne (1-32 wielkie litery, cyfry lub podkreslenia; poczatek od litery).
6. Parser sprawdza tylko skladnie. Nie wykonuje komend, nie egzekwuje TTL, nie uwierzytelnia agentow i nie weryfikuje wynikow.
7. ETA i inne dane aplikacyjne umieszczaj w payloadzie. Nie dopisuj drugiej komendy za nim.
8. Nawiasy kwadratowe w payloadzie musza byc zbilansowane; zamiast sklejania komend wysylaj osobne komunikaty.

Wiecej: https://t8.pl. Zasady uzycia okresla LICENSE.
