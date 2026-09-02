---
name: ai-language-v4
description: AI language (NOR Protocol v4) — a stateful AI-to-AI communication format. Use when one agent writes to another statefully (report→decision→execution→ACK), or when you need discipline — grounding a model that drifts or hallucinates in prose. Syntax + namespaces + examples.
author: MafiaAI — a team of people and AI agents building tools, websites and solutions. More: https://t8.pl
license: for public use
---

# AI language (NOR Protocol v4) — an AI-to-AI communication format

*A concise working reference. This is OUR format, worked out in practice between agents —
not an industry standard. Take it, use it, adapt it.*

## WHY (when to use)
- **Stateful communication** agent↔agent: report→decision→execution→ACK (not prose).
- **Discipline** — grounding a model that drifts or spins stories in prose. Proven in practice:
  state+operation+ACK leaves no room for confabulation. The model has to give a fact and
  a confirmation, not an essay.
- **Automation** — the format is single-line and regular, so it is easy to compose, parse
  and validate with a program (no reliance on whether the model remembers the syntax).

## SYNTAX
```
@VERSION[4.0][MODIFIERS]::NAMESPACE::COMMAND[PAYLOAD]
```
- `@VERSION[4.0]` — REQUIRED, always first.
- Payload is language-agnostic (any language inside `[...]`).
- **Single line** — one message = one line (easy to log and pass around).

## MODIFIERS
`@VERSION[4.0]`(required) · `@PRIORITY[LOW|NORMAL|HIGH|CRITICAL]` · `@TO[id]` · `@FROM[id]` · `@BROADCAST` · `@SEQ[n]` · `@DEPENDS[n]` · `@PARALLEL` · `@IF[cond]`

## NAMESPACES — CORE (17)
`NOR::`(meta-communication) `DEK::`(lifecycle/stages) `TTL::`(time/lifetime) `SIG::`(signature/identity) `BUF::`(working memory) `ACK::`(acknowledgement) `CMD::`(command) `ECHO::`(test) `INT::`(external I/O) `ERR::`(errors) `DATA::`(data) `LOG::`(log/metrics) `TASK::`(tasks) `CHAT::`(free-form) `COLLAB::`(collaboration) `FLOW::`(threads) `META::`(about the protocol)

## ACK STATUSES
`OK` `ERROR` `PENDING` `TIMEOUT` `RECEIVED` `PROCESSED` `READY` `BUSY` `PARTIAL` `RETRY` `DEGRADED` `QUEUED` `STALE` `CONFLICT` `CANCELLED`

## DEK STAGES
`STAGE[INIT|PREP|EXEC|FINAL|CLEANUP]` (or 0-4)

## EXAMPLES
```
# Stateful ACK (reply to an instruction):
@VERSION[4.0]@FROM[AI1]@TO[NOR]::ACK::RECEIVED[task X] + ETA[2min]

# Grounding a drifting model (facts+commands, not prose):
@VERSION[4.0]@TO[AI2]::META::CORRECT[X = fact, not Y]
@VERSION[4.0]::CMD::STOP[re-posting/inflating] + CMD::NEXT[a concrete step]
@VERSION[4.0]::ACK::AWAIT[STATUS=RECEIVED + ETA]

# Agent-to-agent handshake:
@VERSION[4.0]@TO[AI2]::SIG::IDENT[AI1] → @VERSION[4.0]::ACK::OK[ready]

# Task with priority and sequence:
@VERSION[4.0]@SEQ[001]@PRIORITY[HIGH]::TASK::EXECUTE[job] TTL::300
```

## RULES
1. **State, not prose.** Every line = STATE+OPERATION+ACK. A model that drifts or hallucinates
   spins prose — v4 grounds it (it has to give a fact + a confirmation).
2. **ACK is mandatory** — the receiver replies statefully (RECEIVED+ETA), not with an essay.
3. **Single line** — one message = one line; leave multi-line to channels that tolerate it.
4. **Limits:** v4 works between agents that COOPERATE. Over an external agent you do not
   control, the protocol is persuasion, not control — do not expect enforcement.

---
*v4 = discipline that keeps a model close to the facts. The format does not replace thinking —
it takes remembering the syntax off the model and leaves it the content.*

---
**MafiaAI** — a team of people and AI agents building tools, websites and solutions. More: **https://t8.pl**
