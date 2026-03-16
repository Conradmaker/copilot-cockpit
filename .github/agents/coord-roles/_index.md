# Coordinator Role Index

Coordinator가 `coordinator_role`을 받으면 이 디렉토리에서 해당 `{role}.md`를 로드한다.

## Lane 활성화 기준

| role | 언제 선택하는가 | 관점 |
|---|---|---|
| manager | PRD 문서의 품질, completeness, 구조적 readiness, scope, metrics가 중요할 때 | 기획자, PM |
| product | PRD가 암시하는 product outcome 완성도, 코어 경험 흐름, downstream(UI/Tech) 전개 필요성이 중요할 때 | 프로덕트 오너 |

## 사용 규칙

- Mate는 작업 성격에 맞는 role을 최소 2개 동적으로 선택한다.
- 파일이 없는 role이 요청되면 범용 기준으로 검토하되 누락을 명시한다.
- 새 role이 필요하면 이 디렉토리에 `{role}.md`를 추가한다.
