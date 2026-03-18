# Reviewer Role Index

Reviewer가 단일 `reviewer_role`을 받으면 이 디렉토리에서 해당 `{role}.md`를 읽어 role-specific 검토 기준을 로드한다.

## Role 활성화 기준

| role | 언제 선택하는가 | 관점 |
|---|---|---|
| board | 병렬 reviewer 결과를 합성하고 final gate를 닫아야 할 때 | broad quality gate |
| security | auth, input, secret, persistence, file/network I/O, privileged action이 바뀔 때 | exploitability와 security control |
| frontend | React/UI implementation, state/render flow, shared UI surface가 바뀔 때 | frontend implementation quality |
| design | UX/UI, copy, layout, motion, responsive surface quality가 중요할 때 | UX/UI review |
| performance | hot path, data access, caching, bundle, latency risk가 있을 때 | performance와 scalability |
| code-quality | clean code, maintainability, error handling, boundary condition, refactor risk가 중요할 때 | code quality와 reliability |

## 사용 규칙

- Commander는 changed surface와 hotspot을 보고 필요한 role만 병렬 호출한다.
- `board`는 병렬 reviewer가 아니라 final synthesis and gate role이다.
- role 문서는 긴 checklist dump가 아니라 activation logic, must-check, retrieval order를 담는다.
- 파일이 없는 role이 요청되면 Reviewer는 범용 기준으로 검토하되 누락을 명시한다.