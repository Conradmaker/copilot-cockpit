# Reviewer Role Index

Reviewer가 단일 `ROLE`을 받으면 이 디렉토리에서 해당 `{role}.md`를 읽어 role-specific 검토 기준을 로드한다.

## Role 활성화 기준

| role | 언제 선택하는가 | 관점 |
| --- | --- | --- |
| board | 병렬 reviewer 결과를 합성하고 final gate를 닫아야 할 때 | broad quality gate |
| design | visual/UX 표현, copy, layout, motion, responsive quality, design-level accessibility가 중요할 때 | visual quality와 UX expression |
| code-quality | UI implementation, state/render flow, maintainability, implementation-level accessibility가 중요할 때 | implementation quality와 reliability |
| security | auth, input, secret, persistence, file/network I/O, privileged action이 바뀔 때 | exploitability와 security control |
| performance | hot path, data access, caching, bundle, latency risk가 있을 때 | performance와 scalability |
| product-integrity | 핵심 사용자 플로우, acceptance criteria, product outcome alignment risk가 중요할 때 | implementation acceptance와 product outcome |
| browser | 실제 브라우저 실행 evidence, visual regression, interaction/transition, console risk가 중요할 때 | runtime verification과 browser evidence |

## 사용 규칙

- Commander는 changed surface와 hotspot을 보고 필요한 role만 병렬 호출한다.
- `board`는 병렬 reviewer가 아니라 final synthesis and gate role이다.
- role 문서는 activation logic, must-check, pass criteria, retrieval order, scope boundary를 담는다.
- 파일이 없는 role이 요청되면 Reviewer는 범용 기준으로 검토하되 누락을 명시한다.
