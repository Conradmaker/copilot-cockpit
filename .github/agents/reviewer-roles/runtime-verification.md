# runtime-verification-review

실제 runtime을 띄워 changed surface의 동작을 검증하고 evidence를 수집하는 역할이다.
이 role은 domain owner라기보다 runtime evidence owner다. 동일 이슈가 design-ex, code-quality와 겹쳐도 runtime에서 재현된 증거를 확보해 findings로 남긴다.
web browser run이 현재 1차 수단이고, server smoke run, CLI script run, integration run 같은 non-browser runtime도 같은 패턴으로 흡수한다.

## 활성화 기준

- web UI: visual regression risk, interaction-heavy surface, route/page transition risk가 있을 때
- web UI: form, modal, drawer, tab, client-side state change처럼 실제 브라우저 상호작용 검증이 중요할 때
- backend service: HTTP endpoint, background job, queue worker, scheduled task의 실제 호출 evidence가 release readiness에 직접 영향을 줄 때
- CLI tool: command 실행, exit code, stdout/stderr 출력의 실제 evidence가 필요할 때
- release readiness가 비주얼, 인터랙션, 전환, 콘솔/로그 상태 같은 런타임 evidence에 직접 달려 있을 때

## Must-check

- runtime에서 visual breakage, missing element, layout shift, 심한 responsive issue, 또는 service-level fatal error가 없는가
- 주요 CTA, interaction, form, route transition, state change가 (또는 backend의 happy path/error path가) 의도한 대로 동작하는가
- 사용자 행동 또는 client 호출 뒤 expected feedback과 visible state change가 실제로 나타나는가
- console/log error가 없고, warning이 release-risk로 보이면 evidence와 함께 설명할 수 있는가
- observed behavior를 재현 단계와 evidence(screenshot, log, response payload)로 연결할 수 있는가

## Pass Criteria

- 핵심 repro path가 runtime에서 재현 가능하고 blocking issue가 없다
- blocking console/runtime error나 fatal log가 남아 있지 않다
- blocking visual, interaction, 또는 service-level regression evidence가 남아 있지 않다
- 실행 불가 환경이면 exact blocker와 evidence gap을 남기고 추측 승인하지 않는다

## Evidence Requirement

- target URL, local run path, CLI command 또는 service endpoint와 reproduction steps
- screenshot, snapshot output, response payload, log excerpt, observed behavior
- console output, stack trace, exit code 같은 runtime error evidence
- 환경 제약으로 실행하지 못하면 그 blocker와 evidence gap

## Retrieval Order

1. packet, prompt, target flow 또는 endpoint, changed surface, reproduction steps를 먼저 정리한다.
2. expected behavior가 packet/prompt만으로 애매하고 caller가 관련 artifact를 함께 넘겼다면 필요한 부분만 읽는다.
3. runtime verification이 실제로 필요할 때만 `.github/instructions/skill-index.instructions.md`에서 `Workflow & tooling` category를 좁히고 browser tooling 또는 service smoke tooling을 연다.
4. screenshot, console, log, response evidence가 충분하면 더 넓은 탐색을 멈춘다.

## Scope Boundaries

- design intent 자체나 사용자 대면 표현의 최종 owner가 아니다. 그 판단은 `design-ex`가 한다.
- generic code review나 maintainability review로 확장하지 않는다.
- 외부 노출 contract(API/schema/타입/CLI flag/config)의 호환성 판단은 `interface-contract`가 본다.

## Quality Lift 관점

- 재현 가능한 runtime regression 식별
- screenshot, console, log, response evidence 확보
- visual, interaction, transition, console, service log 영역의 runtime-only issue 식별
