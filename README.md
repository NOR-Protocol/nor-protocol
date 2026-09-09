# NOR Protocol v4

**PL:** format komunikacji AI–AI: **stan + operacja + potwierdzenie**, jedna parsowalna linia.  
**EN:** AI–AI communication format: **state + operation + acknowledgement**, one parseable line.

Not an industry standard. A working format from practice. We publish it because it works for us.  
Nie jest standardem branżowym. To roboczy format z praktyki. Publikujemy, bo u nas działa.

Site (in-browser generator, nothing is sent to a server): [jezyk.t8.pl](https://jezyk.t8.pl)

## With the Coordination System (SK v6)

NOR Protocol v4 is the **language**. [SK v6](https://sk.t8.pl) is **how the work is organized**. We use them together.

- **v4** — one line: state + operation + ACK. Nodes talk so they do not drift in prose.
- **SK v6** — coordinator, CROWN (producer ≠ verifier, other model), closed task list, gate for irreversible actions. Concept: [sk.t8.pl](https://sk.t8.pl). We do not publish the running engine.

```
@VERSION[4.0]@FROM[NOR]@TO[A1]::META::NOTE[v4 = jezyk; SK v6 = tory pracy. Razem. Czytaj sk.t8.pl + jezyk.t8.pl]
@VERSION[4.0]@FROM[A1]@TO[NOR]::ACK::RECEIVED[sk.t8.pl + jezyk.t8.pl] + ETA[5min]
```

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

**Private / personal use: free.**  
**Company / commercial use: not granted** — contact [t8.pl](https://t8.pl).

Keep author credit (NOR & t8.pl). This is not MIT. GitHub will show **Other**. See `LICENSE`.

X: [@NOR_Protocol](https://x.com/NOR_Protocol)
