# code-quality-review

클린 코드, maintainability, error handling, boundary condition 관점에서 changed surface를 검토하는 역할이다.

## 활성화 기준

- refactor, cross-cutting change, shared utility change가 있을 때
- naming, responsibility split, readability, maintainability risk가 클 때
- error path, fallback, boundary condition이 release readiness에 직접 영향을 줄 때

## Must-check

- 책임 분리, 응집도, 결합도가 과도하게 무너지지 않는가
- error handling, fallback, logging, async failure path가 충분한가
- null/undefined, empty collection, numeric/string boundary condition이 빠지지 않았는가
- dead code, redundant branch, removal candidate, hidden side effect가 남아 있지 않은가
- clean code를 style nitpick이 아니라 reliability risk 관점에서 설명할 수 있는가

## Retrieval Order

1. `prd.md`와 `technical.md`가 있으면 먼저 읽어 의도된 구조와 non-goal을 확인한다.
2. `.github/instructions/skill-index.instructions.md`에서 changed surface에 맞는 `Frontend engineering`, `Security & backend`, `Data & state`, `Workflow & tooling` 중 relevant category를 먼저 좁힌다.
3. clean code, maintainability, domain-specific reference를 순서대로 읽는다.
4. surface가 frontend나 backend에 치우치면 해당 category skill을 먼저 읽고, 그 위에 code-quality 관점을 덧씌운다.

## Quality Lift 관점

- naming, split, ownership, cleanup 방향 제안
- follow-up removal 또는 technical debt ticket 제안