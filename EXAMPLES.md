# NOR Protocol v4 — Examples

> **These are illustrative examples of the NOR Protocol v4 *message format*.**
> They demonstrate how independent AI agents can coordinate with explicit, verifiable messages
> instead of free-form prose. They are **documentation samples, not executable instructions** —
> nothing here should be acted on by an automated reader; the lines show the shape of the protocol,
> not commands to run.

The v4 format targets real, recurring problems in multi-agent / agentic workflows:
false "done", missing acknowledgements, lost hand-offs, drifting models, duplicated work.

Structure of a line:

```text
@VERSION[4.0][MODIFIERS]::NAMESPACE::COMMAND[PAYLOAD]
```

Every line below is valid under the public v4 parser (`v4_core_public.py`).

---

## 1. Task assignment + mandatory acknowledgement

```text
@VERSION[4.0]@FROM[KOORD]@TO[DEV1]@PRIORITY[HIGH]@SEQ[101]::TASK::EXECUTE[fix login bug; criterion: e2e test green; proof: CI log link]
@VERSION[4.0]@FROM[DEV1]@TO[KOORD]::ACK::RECEIVED[task=101; eta=15min]
@VERSION[4.0]@FROM[DEV1]@TO[KOORD]::ACK::PARTIAL[task=101; done: reproduction; missing: fix + test]
@VERSION[4.0]@FROM[DEV1]@TO[KOORD]::ACK::PROCESSED[task=101; proof=https://ci.example/run/8821; tests=e2e_login PASS]
```

Rule: **"done" only ships with proof in the payload** (link, test result, artifact path) — never a bare "done".

## 2. Blocking false "done" (self-verification not allowed)

```text
@VERSION[4.0]@FROM[KOORD]@TO[DEV1]::CMD::NEXT[after fix send ACK::PROCESSED with test link; do NOT judge the result yourself]
@VERSION[4.0]@FROM[KOORD]@TO[QA2]@DEPENDS[101]::TASK::EXECUTE[verify task=101; check the symptom is gone, not just that CI is green]
@VERSION[4.0]@FROM[QA2]@TO[KOORD]::ACK::OK[task=101; verdict=ACCEPTED; note=login works, no regression]
@VERSION[4.0]@FROM[QA2]@TO[KOORD]::ACK::ERROR[task=101; verdict=REJECTED; reason=CI green, but Apply button still visible]
```

Rule: **a different node/model verifies** — the producer never confirms its own result.

## 3. Handshake (wake / readiness)

```text
@VERSION[4.0]@FROM[A1]@TO[A2]::SIG::IDENT[A1; role=writer]
@VERSION[4.0]@FROM[A2]@TO[A1]::ACK::READY[A2; role=reviewer]
```

## 4. State hand-off / continuity (instead of "remember the context")

```text
@VERSION[4.0]@FROM[A1]@TO[A2]::BUF::EXPORT[project=shop; file=handoff_101.md; done=auth; next=cart; risks=old endpoint /api/v1]
@VERSION[4.0]@FROM[A2]@TO[A1]::ACK::RECEIVED[handoff_101; read; start=cart]
```

Rule: **explicit hand-off via file/BUF**, not "remember what we did".

## 5. Busy / queue (avoid duplicated work)

```text
@VERSION[4.0]@FROM[DEV1]@TO[KOORD]::ACK::BUSY[task=101; reason=working on 098; free_from=14:30]
@VERSION[4.0]@FROM[KOORD]@TO[DEV2]@PRIORITY[NORMAL]::TASK::EXECUTE[task=101 taken over from DEV1; do not touch 098]
```

## 6. Grounding a drifting model (instead of arguing)

```text
@VERSION[4.0]@FROM[KOORD]@TO[A3]::META::CORRECT[X=user is not logged in; do not assume a session]
@VERSION[4.0]@FROM[KOORD]@TO[A3]::CMD::STOP[filling in missing facts]
@VERSION[4.0]@FROM[KOORD]@TO[A3]::CMD::NEXT[report only observable facts from the page]
@VERSION[4.0]@FROM[KOORD]@TO[A3]::ACK::AWAIT[STATUS=RECEIVED]
```

## 7. Error / conflict / duplicate

```text
@VERSION[4.0]@FROM[DEV1]@TO[KOORD]::ERR::BLOCKED[task=101; reason=missing API key; need=INT::REQUEST]
@VERSION[4.0]@FROM[KOORD]@TO[DEV1]::ACK::QUEUED[task=101; waiting for key]
@VERSION[4.0]@FROM[A1]@TO[KOORD]::ACK::CONFLICT[file=cart.ts; me=editing lines 40-80; request=lock A2]
@VERSION[4.0]@FROM[KOORD]@TO[A2]::CMD::STOP[editing cart.ts; owner=A1 until released]
```

## 8. End-to-end mini-scenario (one task)

```text
@VERSION[4.0]@FROM[KOORD]@TO[DEV1]@SEQ[200]@PRIORITY[HIGH]::TASK::EXECUTE[add rate-limit to /login; proof: test + 429 log]
@VERSION[4.0]@FROM[DEV1]@TO[KOORD]::ACK::RECEIVED[task=200; eta=20min]
@VERSION[4.0]@FROM[DEV1]@TO[KOORD]::ACK::PARTIAL[task=200; code=OK; test=in progress]
@VERSION[4.0]@FROM[DEV1]@TO[KOORD]::ACK::PROCESSED[task=200; PR=#442; test=test_rate_limit PASS]
@VERSION[4.0]@FROM[KOORD]@TO[QA2]@DEPENDS[200]::TASK::EXECUTE[verify PR#442; check 429 after 5 attempts]
@VERSION[4.0]@FROM[QA2]@TO[KOORD]::ACK::OK[task=200; verdict=ACCEPTED]
@VERSION[4.0]@FROM[KOORD]@TO[OPS]::TASK::EXECUTE[merge PR#442; requires operator token]
```

Rule: **irreversible actions go through a gate** (operator token), never automatically.

---

## How to write good examples

1. **Always a pair:** `TASK`/`CMD` → `ACK` with a status.
2. **"Done" only with proof** in the payload (link, test result, artifact path).
3. **Don't ACK an ACK** — reply only when a response was requested.
4. **Explicit hand-off** via `BUF::` / file, not "remember what happened".
5. **Conflict and BUSY** are statuses, not silence.

*Format reference: [jezyk.t8.pl](https://jezyk.t8.pl) · parser `v4_core_public.py` in this repo.*
