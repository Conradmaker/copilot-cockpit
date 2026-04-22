# Reviewer Role Index

Reviewer가 단일 `ROLE`을 받으면 이 디렉토리에서 해당 `{role}.md`를 읽어 role-specific 검토 기준을 로드한다.
role은 stack이 아니라 **무엇을 판단하는가**로 잘려 있다. 합집합으로 frontend, backend, persistence, contract surface, 사용자 대면 표현, 사용자 대면 문서, runtime/build evidence를 모두 커버한다.

## Role 활성화 기준

| role | 언제 선택하는가 | 관점 |
| --- | --- | --- |
| final-review | 병렬 reviewer 결과를 합성하고 final gate를 닫아야 할 때 | broad quality gate |
| design-ex | 사용자 대면 표면(visual, UX writing, layout, motion, responsive, copy tone)과 visual+interactive accessibility가 중요할 때 | 사용자가 보고/듣고/조작하는 표면의 quality |
| code-quality | 내부 코드의 구조, state/data flow, error handling, boundary, naming, composition, maintainability, in-code rationale가 중요할 때 (FE/BE/scripts/infra 공통) | implementation quality와 reliability |
| interface-contract | REST/GraphQL/RPC, DB schema, 공유 type, 공개 component API, CLI flag, config schema, event payload의 호환성과 그에 딸린 contract 문서 정합성이 중요할 때 | 외부 노출 contract surface의 호환성과 명세-구현-문서 정합성 |
| security | auth, input/secret/PII, privileged action, dependency/supply-chain, 보안 헤더 같은 exploitability surface가 바뀔 때 | exploitability와 security control |
| performance | hot path, latency, throughput, bundle size, query/IO/직렬화 비용 같은 performance surface가 바뀔 때 (FE/BE 공통) | performance와 scalability |
| runtime-verification | 실제 runtime 실행 evidence가 필요할 때 (web browser run이 1차, server smoke/CLI run/integration run으로 확장) | runtime evidence collection |
| build-verification | 코드 변경이 있어 full build, typecheck, lint, test suite의 실제 실행 evidence가 필요할 때 (코드 변경 plan의 default) | build/test의 release readiness evidence |

## 사용 규칙

- Commander는 changed surface와 hotspot을 보고 필요한 role만 병렬 호출한다.
- `final-review`는 병렬 reviewer가 아니라 final synthesis and gate role이다.
- role 문서는 activation logic, must-check, pass criteria, retrieval order, scope boundary를 담는다.
- 동일 변경에 여러 role이 자연스럽게 걸치면 (예: API endpoint 변경이 `interface-contract` + `security` + `code-quality`에 동시에 걸침) 각 role의 must-check 관점에서 병렬로 호출한다.
- 파일이 없는 role이 요청되면 Reviewer는 범용 기준으로 검토하되 누락을 명시한다.

## Documentation ownership 분배

documentation은 별도 role 없이 다음과 같이 분배한다.

- 사용자 대면 카피, README hero, marketing copy, in-product copy → `design-ex`
- spec, PRD, acceptance doc, public release note → 작성/유지는 Mate, release readiness 합성은 `final-review`
- API reference, schema doc, migration guide, changelog의 contract 부분 → `interface-contract`
- 내부 코드 주석, in-code rationale, ADR, 내부 dev README → `code-quality`
