---
description: "Guidelines for TypeScript Development targeting TypeScript 5.x and ES2022 output"
applyTo: "**/*.ts"
---

# TypeScript Development

이 지침은 TypeScript 5.x와 ES2022 출력을 기본으로 하는 프로젝트를 가정한다.
런타임이 더 낮은 target을 요구하면 그 제약을 먼저 확인한 뒤 조정한다.

## Core Intent

- 기존 아키텍처와 코딩 기준을 존중한다.
- 똑똑해 보이는 축약보다 읽기 쉬운 명시적 해법을 우선한다.
- 새 추상화를 만들기 전에 현재 추상화를 확장할 수 있는지 먼저 본다.
- 유지보수성과 명확성을 우선한다.

## General Guardrails

- TypeScript 5.x / ES2022를 기본으로 하고, 가능하면 polyfill보다 native feature를 우선한다.
- pure ES module을 사용하고 `require`, `module.exports`, CommonJS helper는 만들지 않는다.
- 특별한 요청이 없으면 저장소의 build, lint, test 스크립트를 따른다.
- 의도가 분명하지 않은 설계 trade-off는 결과 설명에 남긴다.

## Project Organization

- 새 코드는 저장소의 기존 folder와 responsibility layout을 따른다.
- 특별한 지시가 없으면 kebab-case 파일명을 사용한다.
- discovery에 도움이 되면 test, type, helper를 구현 가까이에 둔다.
- 새 utility를 만들기 전에 shared utility를 재사용하거나 확장할 수 있는지 먼저 본다.

## Naming And Style

- class, interface, enum, type alias는 PascalCase를 쓴다.
- 그 외 대부분은 camelCase를 쓴다.
- `IUser` 같은 interface prefix는 피하고 의미가 드러나는 이름을 쓴다.
- 이름은 구현 방식보다 행동이나 도메인 의미를 드러내야 한다.

## Formatting And Style

- 제출 전에는 가능한 한 저장소의 lint 또는 format 스크립트를 돌린다.
- 기존 들여쓰기, 따옴표, trailing comma 규칙을 따른다.
- 함수는 한 가지 책임에 집중하게 유지하고, 분기 복잡도가 커지면 helper를 추출한다.
- practical하다면 immutable data와 pure function을 우선한다.

## Type System Expectations

- implicit 또는 explicit `any`를 피한다.
- 필요하면 `unknown`과 narrowing을 사용한다.
- realtime event나 state machine에는 discriminated union을 우선 검토한다.
- 같은 shape를 여러 번 복제하지 말고 shared contract를 모은다.
- `Readonly`, `Partial`, `Record` 같은 utility type으로 의도를 드러낸다.

## Async, Events, And Error Handling

- `async/await`를 사용한다.
- `await` 주변에는 필요한 범위의 try/catch와 구조화된 error handling을 둔다.
- edge case는 early return으로 처리해 nesting을 줄인다.
- project logging 또는 telemetry utility가 있으면 그 경로로 에러를 보낸다.
- user-facing error는 저장소가 이미 쓰는 notification pattern을 따른다.
- configuration-driven update나 high-frequency event는 debounce와 deterministic dispose를 고려한다.

## Architecture And Patterns

- 저장소의 dependency injection 또는 composition pattern을 따른다.
- lifecycle에 연결할 때는 기존 initialize, dispose, cleanup 순서를 관찰한 뒤 맞춘다.
- transport, domain, presentation layer는 가능한 한 분리한다.
- service를 추가할 때는 lifecycle hook과 필요한 test도 함께 본다.

## External Integrations

- client는 hot path 밖에서 만들고 testability를 위해 injection 가능하게 둔다.
- secret을 하드코딩하지 않는다.
- network나 IO call에는 retry, backoff, cancellation 필요 여부를 검토한다.
- 외부 응답은 바로 노출하지 말고 domain shape로 정규화한다.

## Security Practices

- 외부 입력은 schema validator나 type guard로 검증한다.
- dynamic code execution과 untrusted template rendering을 피한다.
- HTML 렌더링에는 escaping이나 trusted type 같은 안전한 경로를 사용한다.
- query는 parameterized query나 prepared statement를 사용한다.
- secret은 secure storage에 두고 least privilege를 지킨다.
- sensitive data는 immutable flow와 defensive copy를 우선 고려한다.
- crypto는 검증된 library만 사용한다.
- dependency advisory를 확인하고 보안 패치를 미루지 않는다.

## Configuration And Secrets

- configuration은 shared helper를 통해 접근하고 schema나 validator로 검증한다.
- secret은 project의 secure storage 경로를 따르고 `undefined`와 error state를 다룬다.
- 새로운 config key를 추가하면 관련 test와 문서도 업데이트한다.

## UI And UX Components

- user input이나 external content는 렌더링 전에 sanitize한다.
- UI layer는 얇게 유지하고, 무거운 로직은 service나 state manager로 내린다.
- event나 message를 사용해 UI와 business logic를 느슨하게 결합한다.

## Testing Expectations

- 저장소가 쓰는 framework와 naming style에 맞춰 unit test를 추가하거나 갱신한다.
- 동작이 여러 module이나 platform API를 가로지르면 integration 또는 end-to-end coverage를 확장한다.
- 빠른 피드백을 위해 targeted test부터 돌린다.
- brittle timing assertion보다 fake timer나 injected clock을 우선한다.

## Performance And Reliability

- 무거운 dependency는 lazy-load를 검토하고, 사용이 끝나면 dispose한다.
- 비싼 계산이나 fetch는 실제로 필요할 때까지 미룬다.
- high-frequency event는 batch 또는 debounce를 검토한다.
- resource lifetime을 추적해 leak를 막는다.

## Documentation And Comments

- public API에는 필요한 JSDoc을 남긴다.
- `@remarks`, `@example`가 실제 사용을 설명하는 데 도움이 되면 추가한다.
- comment는 구현 설명보다 intent를 설명하게 쓴다.
- refactor 중 stale note는 함께 지운다.
- 중요한 패턴을 추가하면 architecture 또는 design 문서 업데이트도 검토한다.
