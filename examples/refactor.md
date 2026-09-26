# CODEX_HANDOFF

> Generated: 2026-09-26T15:40:00Z
> Repository: atlas-web
> Branch: refactor/query-boundary
> HEAD: c83fa11
> Working tree: dirty — 4 modified, 0 untracked

## Goal

Move dashboard query construction behind `DashboardQueryService` without changing generated SQL or API responses.

## Current State

- Verified: two handlers now call the service and snapshot output is unchanged.
- Inference: the export handler can use the same service without needing an additional query option.
- Blocked: none.

## Files Changed

| Path | Status | Purpose |
| --- | --- | --- |
| `src/dashboard/query-service.ts` | modified | Add `forDashboard()` and shared filter mapping. |
| `src/dashboard/summary-handler.ts` | modified | Delegate query construction. |
| `src/dashboard/detail-handler.ts` | modified | Delegate query construction. |
| `tests/dashboard/query-service.test.ts` | modified | Preserve generated-query snapshots. |

## Key Discoveries

- `export-handler.ts` duplicates the same filters but also sets `batchSize`; that option belongs to execution, not query construction.
- Snapshot order depends on `Map` insertion order in `filter-mapper.ts`.

## Decisions

- **Decision:** Keep filter ordering unchanged. **Reason:** Reordering is unrelated and would make semantic equivalence harder to review. **Trade-off:** A known readability issue remains.

## Failed Approaches

- A generic `buildQuery(options)` API widened the public surface and made invalid option combinations possible, so it was replaced with named service methods.

## Remaining Work

- [ ] Migrate `export-handler.ts` while keeping `batchSize` in the execution layer.
- [ ] Run dashboard integration tests.

## Verification

| Command or check | Result | When |
| --- | --- | --- |
| `yarn test query-service.test.ts` | PASS — 12 tests and snapshots | current session |
| Compare API response fixtures | PASS — no fixture diff | current session |
| `yarn test dashboard:integration` | NOT RUN — export handler not migrated | current session |

## Next Recommended Action

Migrate only the query-construction logic in `src/dashboard/export-handler.ts` into `DashboardQueryService`.
