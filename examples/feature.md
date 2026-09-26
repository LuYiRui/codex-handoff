# CODEX_HANDOFF

> Generated: 2026-09-26T12:05:00Z
> Repository: papertrail-cli
> Branch: feature/json-output
> HEAD: a91b430
> Working tree: dirty — 3 modified, 1 untracked

## Goal

Add `--format json` to the `list` command while preserving the existing table output by default.

## Current State

- Verified: argument parsing and JSON serialization are implemented; focused tests pass.
- Inference: downstream scripts will prefer newline-free JSON arrays, but this has not been confirmed with users.
- Blocked: help text example is still missing.

## Files Changed

| Path | Status | Purpose |
| --- | --- | --- |
| `src/commands/list.ts` | modified | Route records to table or JSON renderer. |
| `src/output/json.ts` | untracked | Serialize public record fields. |
| `tests/list.test.ts` | modified | Cover explicit JSON and default table formats. |
| `README.md` | modified | Document the new flag; example pending. |

## Key Discoveries

- Internal records contain `debugMetadata`, which must not appear in public JSON output.
- The command framework already rejects unknown `--format` values through its choices option.

## Decisions

- **Decision:** Emit one JSON array followed by a newline. **Reason:** It is valid for both terminals and redirected files. **Trade-off:** Streaming large result sets is outside v0.1 scope.

## Failed Approaches

- Serializing internal records directly exposed `debugMetadata`; the new renderer now maps an explicit public shape.

## Remaining Work

- [ ] Add one README example showing redirected JSON output.
- [ ] Run the full CLI test suite.

## Verification

| Command or check | Result | When |
| --- | --- | --- |
| `pnpm test -- list.test.ts` | PASS — 9 tests | current session |
| `pnpm test` | NOT RUN — session time limit | current session |

## Next Recommended Action

Add one redirected JSON example to `README.md`.
