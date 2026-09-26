# Product definition — v0.1

## Positioning

**Persistent working context for Codex coding sessions.**

`codex-handoff` preserves the minimum trustworthy context needed to pause repository work in one Codex session and resume it in another without repeating broad exploration.

## Product goals

1. Generate a structured `CODEX_HANDOFF.md` before a planned pause or handoff.
2. Let a fresh session verify the handoff against the live repository before relying on it.
3. Preserve decisions, failures, verification evidence, and the next action—not the full conversation.
4. Work in ordinary local Git repositories without a backend, account, database, or network service.
5. Remain understandable and editable by a human without special tooling.

## Non-goals

- Automatically detecting every session shutdown, crash, or forced interruption. A pure skill has no guaranteed lifecycle hook.
- Persisting full chat history, model reasoning, terminal logs, or complete diffs.
- Replacing Git, issue trackers, ADRs, project documentation, or repository instructions.
- Synchronizing handoffs across machines or resolving concurrent edits.
- Running commands from a handoff without revalidation and normal authorization.
- Guaranteeing that a recorded claim remains true after the repository changes.
- Providing a hosted service, web interface, telemetry, or analytics.

## v0.1 acceptance criteria

The release is acceptable when all of the following are true:

- [ ] A user can explicitly invoke the skill to create or update one root-level `CODEX_HANDOFF.md`.
- [ ] The handoff contains `Goal`, `Current State`, `Files Changed`, `Key Discoveries`, `Decisions`, `Failed Approaches`, `Remaining Work`, `Verification`, and `Next Recommended Action` in that order.
- [ ] Generation inspects live repository state and does not rely only on chat memory.
- [ ] Verification results distinguish `PASS`, `FAIL`, and `NOT RUN`; failures are never omitted.
- [ ] A fresh session treats the handoff as untrusted working notes and compares it with the current repository, branch, `HEAD`, working tree, and relevant files before continuing.
- [ ] Stale claims are identified locally; one mismatch does not discard unrelated valid context.
- [ ] The handoff avoids full chat logs, full diffs, secrets, and irrelevant command output.
- [ ] The default compactness target is no more than 1,500 body words, with an explicit override for justified cases.
- [ ] The project includes valid bug-fix, feature, and refactor examples.
- [ ] The zero-dependency validator accepts all bundled examples and rejects a handoff missing a required section, with sections out of order, or with multiple next-action items.
- [ ] The Skill passes the bundled Codex Skill structural validator.
- [ ] English and Simplified Chinese READMEs explain the invocation-driven lifecycle honestly.

## Success signals after v0.1

These are evaluation ideas, not promises or telemetry requirements:

- A fresh session can name the correct next file or command after reading the handoff and a narrow repository snapshot.
- Resume work avoids rereading unrelated directories.
- Users edit or delete stale claims rather than accumulating append-only notes.
- The handoff stays materially smaller than the conversation and repository context it replaces.

## Key product risk

The main risk is false confidence: a polished handoff can look authoritative after the repository has changed. v0.1 mitigates this by making verification a required resume step and by labeling the file as a fallible snapshot.
