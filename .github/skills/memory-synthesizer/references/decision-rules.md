# Memory Decision Rules

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 memory-synthesizer skill의 상세 판정 기준이다. SKILL.md에서 확신이 서지 않을 때만 읽는다.

## 1. Scope Map

| Target | 저장할 때 | 형식 | 저장하지 말 것 |
| --- | --- | --- | --- |
| `/memories/` | stable user preference, communication style, recurring instruction | 짧은 bullet 또는 단일 사실 | 현재 task에만 쓰는 요청, 일회성 감상 |
| `/memories/repo/` | stable project fact, convention, verified command, architecture/workflow fact | JSON object with `subject`, `fact`, `citations`, `reason`, `category` | 현재 patch에만 묶인 사실, 추측, merge 여부에 따라 바뀔 사실 |
| `/memories/session/` | 현재 대화의 plan, references, scratch | task-specific note | durable knowledge처럼 오래 남길 정보 |

## 2. Durability Test

아래 질문에 대부분 yes면 durable signal 후보다.

1. future coding이나 code review task에서 다시 도움이 되는가
2. 현재 대화나 현재 patch만으로 끝나는 정보가 아닌가
3. 시간이 지나도 쉽게 바뀌지 않을 가능성이 높은가
4. 짧은 코드 샘플만 보고는 항상 추론할 수 없는가
5. 민감정보 없이 안전하게 저장 가능한가

yes가 적으면 skip가 기본값이다.

## 3. Skip Rules

아래 항목이면 저장하지 않는다.

- temporary blocker
- unresolved speculation
- user가 곧 번복할 가능성이 큰 즉흥적 선호
- secrets, credentials, private data
- 현재 대화가 끝나면 가치가 사라지는 scratch state
- 기존 memory와 사실상 중복되는 항목

## 4. Repo Memory JSON Template

repo memory는 아래 필드를 모두 채운다.

```json
{
  "subject": "What the fact is about",
  "fact": "The stable repository fact to remember",
  "citations": ["Relevant file path or other concrete evidence"],
  "reason": "Why this will help future coding or review tasks",
  "category": "architecture|workflow|convention|pattern|tooling|other"
}
```

### Field guidance

- `subject`: 검색 가능한 짧은 주제명으로 쓴다.
- `fact`: 한 문장으로도 재사용 가능한 사실로 쓴다.
- `citations`: 실제로 다시 확인 가능한 근거를 넣는다.
- `reason`: 왜 durable memory로 남길 가치가 있는지 설명한다.
- `category`: `.github/memories/memories.md`의 분류와 최대한 맞춘다.

## 5. Category Hints

`.github/memories/memories.md`를 참고해 아래처럼 분류한다.

- architecture: 시스템 구조, 역할 분담, 설계 결정
- workflow: build/test/run/merge 같은 검증된 절차
- convention: naming, layout, authoring, formatting 규칙
- pattern: 반복해서 재사용되는 해결 방식
- tooling: 특정 도구 사용법, 검증된 명령, 환경 제약

## 6. Recommended Save Order

1. existing memory 확인
2. scope 분류
3. durability test
4. format 준비
5. 저장 또는 skip 이유 기록

저장보다 skip가 더 안전한 상황이 많다. 자신감이 낮으면 저장하지 않는다.
