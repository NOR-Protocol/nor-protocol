# NOR Protocol v4

**PL:** format komunikacji AI–AI: **stan + operacja + potwierdzenie**, jedna parsowalna linia.  
**EN:** AI–AI communication format: **state + operation + acknowledgement**, one parseable line.

Not an industry standard. A working format from practice. We publish it because it works for us.  
Nie jest standardem branżowym. To roboczy format z praktyki. Publikujemy, bo u nas działa.

Site (in-browser generator, nothing is sent to a server): [jezyk.t8.pl](https://jezyk.t8.pl)

## Scope

This repository contains only the public NOR Protocol language tools.
SK is a separate private project. Its implementation is not included here.

## Example

```
@VERSION[4.0]@FROM[A1]@TO[A2]::TASK::EXECUTE[zrób X]
@VERSION[4.0]@FROM[A2]@TO[A1]::ACK::RECEIVED[task=example; eta=2min]
```

The receiver answers with a status (`RECEIVED`, `PROCESSED`, `BUSY`, `ERROR`…), not “sure, I’ll get to it”.

## Files

| file | what |
|---|---|
| `skill-jezyk-ai-PL.md` | paste-into-agent reference (PL) |
| `skill-jezyk-ai-EN.md` | same in English |
| `v4_core_public.py` | compose / parse (Python, stdlib) |
| `v4_kreator_public.py` | desktop GUI (PyQt6) |

## Desktop creator

```
pip install PyQt6
python v4_kreator_public.py
```

## What this is not

- not encryption, not channel security
- not control over a foreign model (convention, not enforcement)
- not a multi-agent framework and not an orchestration engine

Valid syntax does not prove that a claim is true or that work was completed.
ACK confirms receipt, not completion. Do not ACK an ACK or an informational message
unless a reply was explicitly requested. FROM is a label, not authentication.

Commands are extensible names; this package parses messages but does not execute them.
ETA and other application data belong inside the payload. Send one message per line.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

Licensed under the **Apache License 2.0** — see [`LICENSE`](./LICENSE).

Free for any use, including commercial, as long as you keep the author credit (NOR & t8.pl) and follow the license terms. GitHub shows this repo as **Apache-2.0**.

X: [@NOR_Protocol](https://x.com/NOR_Protocol)
