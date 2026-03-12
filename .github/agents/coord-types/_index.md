# Coordinator Type Index

Coordinator가 `coordinator_type`을 받으면 이 디렉토리에서 해당 `{type}.md`를 로드한다.

## Lane 활성화 기준

| type | 언제 선택하는가 | 관점 |
|---|---|---|
| product | UI/UX, 사용자 흐름, 결과물 완성도가 중요할 때 | 디자이너, 개발자 |
| manager | 계획 구조, 순서, scope, risk, verification이 중요할 때 | 기획자, PM |
| visual-design | 색상, 타이포, 스페이싱, 시각적 계층이 중요할 때 | 비주얼 디자이너 |
| technical | 성능, 보안, 아키텍처, 비기능 요구사항이 중요할 때 | 테크 리드 |

## 사용 규칙

- Mate는 작업 성격에 맞는 type을 최소 2개 동적으로 선택한다.
- 파일이 없는 type이 요청되면 범용 기준으로 검토하되 누락을 명시한다.
- 새 type이 필요하면 이 디렉토리에 `{type}.md`를 추가한다.
