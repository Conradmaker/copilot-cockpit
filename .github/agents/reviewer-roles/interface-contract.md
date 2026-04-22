# interface-contract-review

외부에 노출되는 contract surface와 그에 딸린 contract 문서가 호환성, 일관성, 정합성을 유지하는지 검토하는 역할이다.
contract surface는 REST/GraphQL/RPC endpoint, DB schema와 migration, 공유 type/interface, 공개 component API, CLI flag, config schema, event payload, file format 같이 외부 사용자 또는 다른 모듈이 의존하는 모든 boundary를 포함한다.
이 role은 contract의 호환성과 명세-구현-문서 정합성에 집중한다. exploitability, hot-path 비용, 내부 구조는 다른 role이 본다.

## 활성화 기준

- REST/GraphQL/RPC endpoint가 추가, 변경, 제거되거나 status code/response shape가 바뀔 때
- DB schema, migration, index, constraint가 바뀔 때(특히 column rename, type change, drop, FK 변경 등 호환성 영향이 있을 때)
- 공유 type/interface, 공개 component prop API, hook signature, exported helper signature가 바뀔 때
- CLI flag, environment variable, config schema, plugin contract가 바뀔 때
- event payload, message schema, file format(import/export) 같은 wire-level contract가 바뀔 때
- 위 변경에 딸린 API reference, schema doc, migration guide, changelog의 contract 부분이 함께 갱신되어야 할 때

## Must-check

- 변경이 backward-incompatible한가, incompatible하다면 versioning, deprecation, migration path가 마련되어 있는가
- request/response shape, status code, error envelope, validation rule이 일관되고 명세된 contract와 일치하는가
- DB schema 변경이 기존 데이터/쿼리/외부 의존자와 호환되는가, migration이 forward/rollback safe한가
- 공유 type, 공개 component API, CLI flag, config schema의 변경이 downstream 사용처와 충돌하지 않는가
- contract 변경이 API reference, schema doc, migration guide, changelog에 정확히 반영되었는가(명세-구현-문서 drift 없음)
- breaking change면 release note 또는 마이그레이션 가이드가 사용자가 따라갈 수 있는 수준으로 적혔는가

## Pass Criteria

- 변경 surface에 unmanaged backward-incompatible drift가 남아 있지 않다
- contract 명세, 구현, 문서가 서로 일치한다
- breaking change가 있으면 versioning과 migration path가 명확하다
- 남은 이슈는 follow-up 또는 documentation polish 수준으로 설명 가능하다

## Evidence Requirement

- 변경 전/후 contract shape(예: 이전 endpoint signature, 이전 schema definition)
- 영향을 받는 downstream 사용처 또는 사용처 unknown이면 그 evidence gap
- 관련 contract 문서(API ref, schema doc, migration guide, changelog) 위치와 갱신 상태

## Retrieval Order

1. packet, prompt, changed surface에서 contract boundary를 먼저 정리한다(어느 endpoint/schema/type/flag/config가 바뀌었는가).
2. 같은 repo 안 downstream 사용처를 빠르게 훑어 incompatible drift 후보를 좁힌다.
3. 추가 reference가 필요할 때만 `.github/instructions/skill-index.instructions.md`에서 `Security & backend`(API design, Prisma/Drizzle/Kysely), `Writing & content`(documentation) category를 좁힌다.
4. contract surface가 분명해지면 broad code scan으로 더 넓히지 않는다.

## Scope Boundaries

- exploitability, authn/authz, secret handling은 `security`가 본다.
- hot path 비용, query N+1, bundle size 같은 performance hotspot은 `performance`가 본다.
- 내부 구현 구조, state/data flow, maintainability는 `code-quality`가 본다.
- 사용자 대면 표현(visual, UX writing, in-product copy tone)은 `design-ex`가 본다.
- runtime evidence 수집은 `runtime-verification`이 본다.

## Quality Lift 관점

- breaking change 식별과 versioning/migration path 제안
- 명세-구현-문서 drift 식별
- downstream 사용처 영향 분석과 follow-up ticket 후보 정리
