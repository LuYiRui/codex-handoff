# CODEX_HANDOFF

> Generated: 2026-09-26T10:20:00Z
> Repository: acme-api
> Branch: fix/refresh-race
> HEAD: 7e41c2a
> Working tree: dirty — 2 modified, 0 untracked

## Goal

Stop intermittent `401` responses when two requests refresh the same expired access token.

## Current State

- Verified: `TokenManager.refresh()` now shares one in-flight refresh promise; the focused concurrency test passes.
- Inference: the original production symptom was caused by concurrent refresh calls overwriting each other's rotated refresh token.
- Blocked: none.

## Files Changed

| Path | Status | Purpose |
| --- | --- | --- |
| `src/auth/token-manager.ts` | modified | Deduplicate refresh calls in `TokenManager.refresh()`. |
| `tests/auth/token-manager.test.ts` | modified | Add a two-request regression test. |

## Key Discoveries

- `AuthClient.request()` can call `refresh()` concurrently from separate response interceptors.
- The refresh endpoint rotates refresh tokens, so the second call can invalidate the first response.

## Decisions

- **Decision:** Store and await one in-flight promise in `TokenManager`. **Reason:** It fixes the race at the shared boundary. **Trade-off:** All callers receive the same refresh failure and retry independently later.

## Failed Approaches

- Retrying every `401` once still produced two refresh calls and hid the race without fixing token rotation.

## Remaining Work

- [ ] Run the complete auth test suite and inspect the final diff for unrelated changes.

## Verification

| Command or check | Result | When |
| --- | --- | --- |
| `npm test -- token-manager.test.ts` | PASS — 18 tests | current session |
| `npm test -- auth` | NOT RUN — session paused before full suite | current session |

## Next Recommended Action

Run `npm test -- auth` and record the observed result.
