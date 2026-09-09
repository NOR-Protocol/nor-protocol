---
name: ai-language-v4
description: AI language (NOR Protocol v4) — a stateful AI-to-AI communication format. Use when one agent writes to another statefully (report→decision→execution→ACK), or when you need discipline — grounding a model that drifts or hallucinates in prose. Syntax + namespaces + examples.
author: MafiaAI — a team of people and AI agents building tools, websites and solutions. More: https://t8.pl
license: See LICENSE; private/personal use only without a separate grant
---

# AI language (NOR Protocol v4) — an AI-to-AI communication format

*A concise working reference. This is OUR format, worked out in practice between agents —
not an industry standard. Use is subject to LICENSE.*

## WHY (when to use)
- **Stateful communication** agent↔agent: report→decision→execution→ACK (not prose).
- **Clarity** — explicit fields reduce ambiguity. Valid syntax does not prove truth or execution.
- **Automation** — the format is single-line and regular, so it is easy to compose, parse
  and validate with a program (no reliance on whether the model remembers the syntax).
- **Scope** — public language tools only. SK is a separate private project; its implementation is not included.

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
@VERSION[4.0]@FROM[AI1]@TO[NOR]::ACK::RECEIVED[task=example; eta=2min]

# Grounding a drifting model (facts+commands, not prose):
@VERSION[4.0]@TO[AI2]::META::CORRECT[X = fact, not Y]
@VERSION[4.0]::CMD::STOP[re-posting/inflating]
@VERSION[4.0]::CMD::NEXT[a concrete step]
@VERSION[4.0]::ACK::AWAIT[STATUS=RECEIVED + ETA]

# Agent-to-agent handshake:
@VERSION[4.0]@TO[AI2]::SIG::IDENT[AI1]
@VERSION[4.0]::ACK::OK[ready]

# Task with priority and sequence:
@VERSION[4.0]@SEQ[001]@PRIORITY[HIGH]::TASK::EXECUTE[task=example; ttl_seconds=300]
```

## RULES
1. One message per line. VERSION comes first. Use only the documented modifiers and core namespaces.
2. ACK requested tasks with a status. Do not ACK an ACK or FYI unless explicitly asked to reply.
3. Receipt is not completion. A status label does not prove the underlying claim.
4. FROM and TO are labels, not authentication or access control.
5. Commands are extensible names (1-32 uppercase letters, digits or underscores, starting with a letter).
6. The parser checks syntax only. It does not execute commands, enforce TTL, authenticate agents or verify results.
7. Put ETA and other application data inside the payload. Do not append another command after it.
8. Payload text must have balanced square brackets; use separate messages instead of concatenated commands.

More: https://t8.pl. Use is subject to LICENSE.
