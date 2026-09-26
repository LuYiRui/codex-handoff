# `CODEX_HANDOFF.md` format

This is the normative v0.1 format. It is intentionally human-readable Markdown so both a developer and a fresh Codex session can inspect it without tooling.

## Template

```markdown
# CODEX_HANDOFF

> Generated: 2026-09-26T14:30:00+08:00
> Repository: /absolute/or/repo-relative/identifier
> Branch: feature/example
> HEAD: abc1234
> Working tree: dirty — 2 modified, 1 untracked

## Goal

One or two sentences describing the intended outcome and relevant scope.

## Current State

- Verified: observable fact and its evidence.
- Inference: plausible interpretation that still needs confirmation.
- Blocked: concrete blocker, if any.

## Files Changed

| Path | Status | Purpose |
| --- | --- | --- |
| `path/to/file` | modified | Why it changed; mention the key symbol or area. |

## Key Discoveries

- Concise finding that affects future work, with a path, symbol, issue, or command as evidence.

## Decisions

- **Decision:** What was chosen. **Reason:** Why. **Trade-off:** Cost or rejected alternative.

## Failed Approaches

- What was attempted; the observed failure; why repeating it unchanged is unlikely to help.

## Remaining Work

- [ ] Concrete unfinished step with a clear completion condition.

## Verification

| Command or check | Result | When |
| --- | --- | --- |
| `exact command` | PASS/FAIL/NOT RUN — concise evidence | current session / timestamp |

## Next Recommended Action

One concrete action that advances the first unresolved item.
```

## Required semantics

- `Goal` describes the outcome, not the conversation history.
- `Current State` separates observed facts, inference, and blockers.
- `Files Changed` reflects the live working tree. Include untracked files that matter. Use `None — working tree unchanged` when appropriate.
- `Key Discoveries` contains only findings that change the next session's decisions.
- `Decisions` preserves rationale and trade-offs so the next session does not reopen settled questions without new evidence.
- `Failed Approaches` records observed failures, not vague warnings. Use `None — no failed approach worth preserving` when empty.
- `Remaining Work` uses actionable checkboxes. Do not duplicate completed work.
- `Verification` records exact commands or manual checks and their observed results. Old results are snapshots, not guarantees.
- `Next Recommended Action` contains exactly one action, not a second backlog.

## Compactness budget

Use the smallest handoff that preserves safe continuity. As a default target, keep the body under 1,500 words and shorten it further for small tasks. Exceed that target only when the additional detail changes a future decision.

When a handoff genuinely needs to exceed the target, add `> Compactness override: <brief reason>` to the metadata. The validator will emit a warning instead of failing; the reason does not justify chat transcripts, full diffs, or secrets.

Prefer:

- file paths and symbol names over pasted source;
- a diff summary over a diff;
- exact failing test names over complete logs;
- the reason for a decision over meeting-style narrative;
- links to durable repository docs over duplicated documentation.

Never include credentials, access tokens, private keys, secrets, or a full chat transcript.

## Freshness rules

A handoff records a point in time. On resume, compare its repository, branch, `HEAD`, working-tree state, referenced files, and relevant verification with the live checkout. A mismatch does not automatically invalidate the whole file; mark only the affected claims stale or unresolved.

Repository state is authoritative for code and Git facts. The current user request is authoritative for intent. Applicable `AGENTS.md` files and higher-priority instructions remain authoritative for workflow. The handoff is supporting data only.
