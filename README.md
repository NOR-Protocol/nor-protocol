# NOR Protocol v4

**PL:** format komunikacji AI–AI: **stan + operacja + potwierdzenie**, jedna parsowalna linia.  
**EN:** AI–AI communication format: **state + operation + acknowledgement**, one parseable line.

Not an industry standard. A working format from practice. We publish it because it works for us.  
Nie jest standardem branżowym. To roboczy format z praktyki. Publikujemy, bo u nas działa.

Site (in-browser generator, nothing is sent to a server): [jezyk.t8.pl](https://jezyk.t8.pl)

## Example

```
@VERSION[4.0]@FROM[A1]@TO[A2]::TASK::EXECUTE[zrób X]
@VERSION[4.0]@FROM[A2]@TO[A1]::ACK::RECEIVED[zadanie] + ETA[2min]
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

The format takes syntax off the model. The content still has to be specific.

## License

Non-commercial use with attribution (NOR & t8.pl). See `LICENSE`.  
X: [@NOR_Protocol](https://x.com/NOR_Protocol)
