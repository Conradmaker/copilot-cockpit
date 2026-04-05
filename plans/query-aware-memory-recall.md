# Query-aware Memory Recall

## 상태

- deferred after Dynamic skill activation and Commander playbook
- write owner는 이미 존재한다: `.github/skills/memory-synthesizer/SKILL.md`
- recall owner는 아직 명시적으로 분리되지 않았다

## 문제

현재 하네스는 memory 저장 판단은 비교적 엄격하지만, 조회는 정적이다.

- 현재 질문과 무관한 memory까지 같이 끌려올 위험이 있다
- current phase, current file, recent tool usage 같은 retrieval signal을 잘 쓰지 못한다
- 저장과 조회 책임이 한 문서/한 판단 흐름에 섞여 있어 memory pollution과 context overload를 따로 다루기 어렵다
- execution이나 review 단계에서 필요한 과거 사실이 있어도, 어떤 memory를 다시 꺼내야 하는지 규칙이 약하다

## 왜 지금은 후순위인가

즉각적인 execution quality 개선은 Commander -> Deep Execution handoff 품질에서 더 크게 나온다.
memory recall은 중요하지만, current execution failure의 주 원인은 아니다.

## 참고 앵커

- claw-code `src/memdir/findRelevantMemories.ts`
- 핵심 아이디어: 전체 preload 대신 query-time shortlist, recent-tools noise suppression, selective attach

## 옵션

### Option A. full preload 유지

- 장점: 구현이 가장 단순하다
- 단점: context density가 계속 나빠지고, query relevance가 낮다
- verdict: reject

### Option B. query-time shortlist

- 질문, current phase, recent tools, already surfaced memory를 기준으로 0~3개의 candidate memory만 고른다
- 장점: context 효율이 높고, claw-code 참고 포인트와 가장 가깝다
- 단점: shortlist quality를 위한 header discipline이 필요하다
- verdict: recommended

### Option C. hybrid index + shortlist

- `MEMORY.md` 또는 summary index는 유지하고, 실제 상세 memory는 shortlist로 붙인다
- 장점: orientation과 precision을 같이 확보한다
- 단점: index discipline이 무너지면 다시 비대해진다
- verdict: likely path after Option B

## 권장 방안

1. write owner와 recall owner를 분리한다.
2. memory-synthesizer는 write owner로 유지한다.
3. recall owner는 아래 신호를 기준으로 shortlist를 만든다.
	- current query
	- current phase
	- current file or changed surface
	- recent tools or active workflow
	- already surfaced memory
4. shortlist에 든 memory만 read하고, 필요한 부분만 합성한다.

## 설계 초안

### Recall input

- query or current subproblem summary
- current phase
- current file or changed surface
- recent tools
- already surfaced memory set

### Recall output

- selected memory list (0~3)
- 왜 이 memory가 relevant한지 한 줄 설명
- freshness가 중요하면 updated-at 또는 known currency note

### Guardrails

- tool usage reference와 active tool docs는 noise가 되기 쉬우므로 suppress candidate로 본다
- 같은 memory를 매 turn 반복 surface하지 않는다
- durability가 약한 임시 session note는 recall 대상 기본값에서 제외한다

## 선행 조건

- Dynamic skill activation 1차 반영 완료
- Commander playbook 1차 반영 완료

## 다음 구현 후보

1. recall owner를 어디에 둘지 결정
	- 별도 skill
	- memory-synthesizer의 companion reference
	- instructions-level rule
2. memory header 규약 정의
3. shortlist flow와 duplicate suppression 규칙 문서화

## 검증

- 같은 질문에 memory 전체 preload보다 shortlist 방식이 더 정확하고 짧은 context를 만드는지 확인
- recent tool noise suppression이 실제로 false positive를 줄이는지 확인
- write owner와 recall owner가 충돌하지 않는지 cross-review
