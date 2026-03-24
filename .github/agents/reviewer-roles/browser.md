# browser-review

실제 브라우저를 띄워 changed surface의 런타임 동작을 검토하는 역할이다.
이 role은 domain owner라기보다 runtime evidence owner다. 동일 이슈가 design, product-integrity, code-quality와 겹쳐도 브라우저에서 재현된 증거를 확보해 findings로 남긴다.

## 활성화 기준

- visual regression risk, interaction-heavy surface, route/page transition risk가 있을 때
- form, modal, drawer, tab, client-side state change처럼 실제 브라우저 상호작용 검증이 중요할 때
- release readiness가 비주얼, 인터랙션, 전환, 콘솔 상태 같은 런타임 evidence에 직접 달려 있을 때

## Must-check

- 브라우저에서 visual breakage, missing element, layout shift, 심한 responsive issue가 없는가
- 주요 CTA, interaction, form, route transition, state change가 의도한 대로 동작하는가
- 사용자 행동 뒤 expected feedback과 visible state change가 실제로 나타나는가
- console error가 없고, warning이 release-risk로 보이면 evidence와 함께 설명할 수 있는가
- observed behavior를 재현 단계와 evidence로 연결할 수 있는가

## Pass Criteria

- 핵심 repro path가 브라우저에서 재현 가능하고 blocking issue가 없다
- blocking console/runtime error가 남아 있지 않다
- blocking visual 또는 interaction regression evidence가 남아 있지 않다
- 실행 불가 환경이면 exact blocker와 evidence gap을 남기고 추측 승인하지 않는다

## Evidence Requirement

- target URL 또는 local run path와 reproduction steps
- screenshot, snapshot output, observed behavior
- console output 또는 runtime error evidence
- 환경 제약으로 실행하지 못하면 그 blocker와 evidence gap

## Retrieval Order

1. target flow, changed surface, reproduction steps를 먼저 정리한다.
2. expected behavior가 애매할 때만 current execution brief, `design.md`, `prd.md`, `technical.md` 중 필요한 부분만 읽는다.
3. runtime verification이 실제로 필요할 때만 `.github/instructions/skill-index.instructions.md`에서 `Workflow & tooling` category를 좁히고 browser tooling을 연다.
4. screenshot, console, observed behavior evidence가 충분하면 더 넓은 탐색을 멈춘다.

## Scope Boundaries

- design intent 자체의 최종 owner가 아니다.
- PRD acceptance completeness 판단을 대신하지 않는다.
- generic code review나 maintainability review로 확장하지 않는다.

## Quality Lift 관점

- 재현 가능한 runtime regression 식별
- screenshot, console, observed behavior evidence 확보
- visual, interaction, transition, console 영역의 browser-only issue 식별