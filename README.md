# NOR Protocol v4

Format komunikacji AI–AI: **stan + operacja + potwierdzenie**, jedna parsowalna linia.

Nie jest standardem branżowym. To roboczy format z praktyki. Publikujemy, bo u nas działa.

Strona (generator w przeglądarce, nic nie wysyła na serwer): [jezyk.t8.pl](https://jezyk.t8.pl)

## Przykład

```
@VERSION[4.0]@FROM[A1]@TO[A2]::TASK::EXECUTE[zrób X]
@VERSION[4.0]@FROM[A2]@TO[A1]::ACK::RECEIVED[zadanie] + ETA[2min]
```

Odbiorca odpowiada statusem (`RECEIVED`, `PROCESSED`, `BUSY`, `ERROR`…), nie „jasne, zaraz się zajmę”.

## Co jest w tym repozytorium

| plik | co to |
|---|---|
| `skill-jezyk-ai-PL.md` | referencja do wklejenia agentowi (PL) |
| `skill-jezyk-ai-EN.md` | to samo po angielsku |
| `v4_core_public.py` | skład / rozbiór linii (Python, stdlib) |
| `v4_kreator_public.py` | GUI Skład + Rozbiór (PyQt6) |

## Kreator desktop

```
pip install PyQt6
python v4_kreator_public.py
```

## Czym to nie jest

- nie szyfrowanie i nie bezpieczeństwo kanału
- nie sterowanie obcym modelem (to konwencja, nie egzekucja)
- nie framework multi-agent i nie silnik orkiestracji

Format zdejmuje z modelu pamiętanie składni. Treść nadal musi być konkretna.

## Licencja

Użytek niekomercyjny z zachowaniem autorów (NOR & t8.pl). Szczegóły: `LICENSE`.
X: [@NOR_Protocol](https://x.com/NOR_Protocol)
