# code-quality-review

구현 구조, state/data flow, maintainability, implementation-level accessibility 관점에서 changed surface를 검토하는 역할이다.

## 활성화 기준

- React/UI implementation, state/data flow, shared UI surface, component API가 바뀔 때
- refactor, cross-cutting change, shared utility change가 있을 때
- error path, fallback, boundary condition, implementation-level accessibility가 release readiness에 직접 영향을 줄 때

## Must-check

- state placement, data flow, render flow, side effect, composition pattern이 일관적인가
- shared UI surface면 component API, composition, ownership이 과도하게 무너지지 않는가
- semantic HTML, label association, ARIA state, keyboard support, focus management, live region, interactive nesting 금지가 지켜지는가
- error handling, fallback, logging, async failure path가 충분한가
- null/undefined, empty collection, numeric/string boundary condition이 빠지지 않았는가
- clean code를 style nitpick이 아니라 reliability risk 관점에서 설명할 수 있는가

## Pass Criteria

- 구조와 책임 분리가 changed surface 수준에서 예측 가능하고 maintainable하다
- blocking implementation-level accessibility defect가 남아 있지 않다
- error path, fallback, boundary condition에서 release blocker가 남아 있지 않다
- 남은 이슈가 cleanup 또는 follow-up 수준으로 설명 가능하다

## Retrieval Order

1. packet, prompt, changed surface와 current execution brief를 먼저 읽어 실제 구현 범위와 proof를 맞춘다.
2. intended structure나 non-goal이 packet/prompt만으로 애매하고 caller가 관련 artifact를 함께 넘겼을 때만 필요한 부분만 읽는다.
3. `.github/instructions/skill-index.instructions.md`에서 `Frontend engineering` category를 좁히고, 필요 시 accessibility와 maintainability reference를 읽는다.
4. security나 performance signal이 명확하면 broad scan으로 확장하지 말고 hotspot role 필요성을 적는다.

## Scope Boundaries

- palette, typography, spacing, copy tone, motion craft 같은 visual/UX 표현은 `design`이 본다.
- exploitability와 auth boundary는 `security`가, hotspot perf는 `performance`가 본다.
- end-to-end acceptance completeness는 `product-integrity`가 본다.

## Quality Lift 관점

- naming, split, ownership, cleanup 방향 제안
- implementation-level accessibility와 maintainability를 함께 다듬는 follow-up 제안