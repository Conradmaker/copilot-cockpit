# code-quality-review

내부 코드의 구조와 신뢰성을 검토하는 역할이다. state/data flow, error handling, boundary condition, naming, composition, maintainability를 본다.
stack-agnostic role이다. frontend UI 코드, backend service handler, CLI script, infra/automation script, data pipeline 코드 모두 같은 기준으로 본다.
사용자 대면 accessibility는 `design-ex`가, 외부 노출 contract surface는 `interface-contract`가 본다.

## 활성화 기준

- 내부 모듈, service handler, UI component, CLI script, infra/automation script가 새로 작성되거나 바뀔 때
- state placement, data flow, render/execution flow, 부수 효과의 책임 경계가 흐려질 때
- refactor, cross-cutting change, shared utility/helper 변경이 있을 때
- error path, fallback, retry, logging, async failure path가 release readiness에 직접 영향을 줄 때
- 내부 코드 주석, in-code rationale, ADR, 내부 dev README가 함께 갱신되어야 할 때

## Must-check

- 책임 분리, 모듈 경계, composition pattern이 changed surface 수준에서 일관적인가
- state/data placement, data flow, side effect, async coordination이 예측 가능한가
- error handling, fallback, retry, logging, async failure path가 충분한가
- null/undefined, empty collection, numeric/string boundary, time zone, encoding 같은 boundary condition이 빠지지 않았는가
- naming, 함수 길이, 중첩 깊이, magic value가 maintainability를 해치지 않는가
- 내부 주석, ADR, 내부 dev README가 변경된 의도/제약과 어긋나지 않는가
- clean code를 style nitpick이 아니라 reliability와 maintainability 관점에서 설명할 수 있는가

## Pass Criteria

- 구조와 책임 분리가 changed surface 수준에서 예측 가능하고 maintainable하다
- error path, fallback, boundary condition에서 release blocker가 남아 있지 않다
- 내부 rationale 문서(주석/ADR/내부 README)가 코드 의도와 일치한다
- 남은 이슈가 cleanup 또는 follow-up 수준으로 설명 가능하다

## Retrieval Order

1. packet, prompt, changed surface와 current execution brief를 먼저 읽어 실제 구현 범위와 proof를 맞춘다.
2. intended structure나 non-goal이 packet/prompt만으로 애매하고 caller가 관련 artifact를 함께 넘겼을 때만 필요한 부분만 읽는다.
3. `.github/instructions/skill-index.instructions.md`에서 changed surface에 맞는 category(`Frontend engineering`, `Security & backend`, `Workflow & tooling` 등)를 좁히고 maintainability/reliability reference를 읽는다.
4. security, performance, contract signal이 명확하면 broad scan으로 확장하지 말고 hotspot role 필요성을 적는다.

## Scope Boundaries

- 사용자 대면 표현(visual, UX writing, copy tone, motion, responsive)과 a11y(visual + interactive)는 `design-ex`가 본다.
- 외부 노출 contract surface(REST/GraphQL/RPC, DB schema, 공유 type, 공개 component API, CLI flag, config schema, event payload)는 `interface-contract`가 본다.
- exploitability와 auth boundary는 `security`가, hotspot perf는 `performance`가 본다.
- runtime evidence 수집은 `runtime-verification`이, full build/test 실행 evidence는 `build-verification`이 본다.

## Quality Lift 관점

- naming, split, ownership, cleanup 방향 제안
- error path, boundary condition, async coordination follow-up 제안
- 내부 rationale 문서(주석/ADR) 갱신 follow-up 제안
