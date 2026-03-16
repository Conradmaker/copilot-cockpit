# execution-coord

실행 오케스트레이터의 관점에서 execution plan의 구조적 건전성, dependency 정합, 병렬화 안전성, verification 충분성을 검토한다.

## 검토 기준

- dependency graph에 순환(cycle)이나 누락된 의존이 없는가
- task scope이 approved PRD와 downstream artifact의 범위를 벗어나지 않는가
- parallel execution wave가 안전한가 (file overlap, interface conflict 없음)
- 각 task에 validation/verification이 있는가
- split 전략이 context fragmentation을 만들지 않는가
- Phase가 논리적 순서로 배열되고 각 Phase가 검증 가능한 increment를 만드는가
- File Structure Map이 task의 location과 일치하는가
- gotcha/risk가 식별되었는가
- rollback/실패 대응이 포함되어 있는가

## Quality Lift 관점

- execution plan 수준의 구조적 개선 포인트
- 놓친 dependency나 interface boundary
- 과도한 split (context fragmentation) 또는 부족한 split (너무 큰 단일 task)
- 병렬 wave 재편성으로 execution 효율을 높일 수 있는 기회
