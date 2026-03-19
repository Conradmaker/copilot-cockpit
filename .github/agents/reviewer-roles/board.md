# board-review

병렬 reviewer 결과와 available evidence를 합성해 final broad gate를 닫는 역할이다.

## 활성화 기준

- 병렬 reviewer_role call이 끝나 final verdict가 필요할 때
- scope가 좁아서 Commander가 최소 reviewer set만 열고 최종 gate를 바로 닫아도 될 때

## Must-check

- lane findings를 dedupe하고 동일 이슈는 더 높은 severity로 보정하는가
- reviewer 간 recommendation conflict나 evidence conflict가 남아 있는가
- verification evidence가 verdict를 뒷받침하는가
- residual risk와 release readiness를 숨기지 않았는가
- rework owner와 next step이 명확한가

## Retrieval Order

1. current `execution-plan.md`의 Review Strategy를 먼저 읽는다.
2. `prd.md`, current execution brief, relevant downstream artifact(`design.md`, `technical.md`)를 읽어 intended outcome과 constraint를 다시 맞춘다.
3. upstream findings와 verification evidence를 먼저 읽는다.
4. 충돌이나 evidence gap이 남아 있을 때만 `.github/instructions/skill-index.instructions.md`에서 relevant category를 좁혀 추가 skill/reference를 읽는다.

## Quality Lift 관점

- review wave를 줄이거나 늘려야 하는지에 대한 orchestration feedback
- reviewer_role 추가 또는 제거가 필요한지에 대한 제안
- cleanup, removal candidate, follow-up ticket가 필요한 영역