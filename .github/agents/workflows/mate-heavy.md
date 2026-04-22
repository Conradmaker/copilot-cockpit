# Mate Heavy Workflow

이 문서는 Mate의 heavy planning mode를 정의하는 receiver-local workflow다.
heavy는 speed보다 evidence closure, stricter review, stronger PRD self-containedness, downstream readiness를 우선하는 고강도 경로다. shared philosophy, artifact ownership, handoff visibility 같은 공통 규칙은 Mate.agent가 맡고, 이 문서는 heavy mode의 digging, gate, downstream decision, refinement를 다룬다.

## Role And Boundary

- heavy mode의 목표는 사용자의 요구사항을 aggressively researched PRD와 evidence-reviewed downstream artifact set으로 수렴시키는 것이다.
- heavy는 default보다 더 강한 digging, 더 높은 quality gate, 더 엄격한 council loop를 사용한다.
- heavy는 PRD 승인 뒤 downstream lane을 스스로 결정하고, design-first 순서로 opened artifact를 다시 검토할 수 있다.

## Entry Conditions

아래 상황에서 heavy mode를 연다.

- user가 `heavy` mode를 명시했을 때
- mode가 명시되지 않았고 askQuestions를 통해 `heavy`를 선택했을 때

## Inputs And Artifact Responsibilities

shared artifact 정의와 공통 규칙은 Mate.agent를 따른다.
heavy mode는 `prd.md`와 `artifacts.md`를 갱신하고, downstream lane이 열리면 opened artifact만 review input으로 사용한다. design lane이 열렸다면 heavy는 post-design review 뒤에 technical lane 필요 여부를 다시 판단한다.

## Planning Controls

- `askQuestions`는 초기 alignment 도구이자 drafting 중 steering 도구며, planning 중 언제든 반복 사용할 수 있다.
- 가까운 skill, reference, reusable pattern, project rule을 먼저 확인한다.
- Explore는 local pattern, reusable template, project-specific rule, symbol flow, local evidence를 read-only로 수집할 때 연다.
- Librarian는 external contract, official doc, source-level behavior, version-sensitive evidence를 확인하거나 web search로 자료조사가 필요할 때 연다.
- Explore, Librarian등 자료조사는 PRD를 선명하게 만드는 데 필요한 evidence를 모으는 활동이다.
- Coordinator Council은 draft의 clarity, scope discipline, metric quality, requirement quality, downstream ambiguity를 점검하는 quality checkpoint다. Mate는 작업 성격에 맞는 coordinator role을 최소 2개 동적으로 선택하고, 각 role을 분리된 lane으로 병렬로 연다.



## Workflow

1. user request를 읽고 request의 내용을 파악한다.
2. problem, target user, success metric, scope, non-goal, constraint, evidence gap 중 draft를 왜곡할 축이 보이면 brainstorming-style narrowing으로 먼저 alignment를 회수한다. 질문이 필요하면 최대 3개의 focused question을 묶고, 가능하면 multiple-choice를 사용한다.
3. 가까운 skill, reference, local pattern, reusable template, project rule, external contract를 먼저 확인한다.
4. local evidence가 부족하면 Explore를 열어 relevant file surface, symbol flow, reusable pattern, project-specific constraint를 더 깊게 확인한다.
5. external contract, current reference, version-sensitive behavior가 중요하면 Librarian를 열어 external digging을 진행한다.
6. 각 digging wave의 materially relevant evidence를 PRD의 decision-ready summary에 반영하고, `artifacts.md`는 생성된 문서 인덱스로 유지한다. council에 올리기 전 current PRD가 major assumption, missing acceptance target, scope creep, bounded evidence gap 측면에서 충분히 읽히는지 pre-plan gap analysis를 수행한다.
7. EARS 다차원 커버리지를 점검하고 `.github/agents/artifacts/PRD-TEMPLATE.md`의 기준으로 PRD를 작성한다. PRD는 downstream owner가 채팅을 다시 읽지 않고도 시작할 수 있을 만큼 self-contained해야 하지만, PRD 전체를 detailed design spec이나 technical execution spec으로 비대화하지 않는다.
8. drafting 중간에도 framing, tone, priority, scope, tradeoff를 더 정확히 맞출 가치가 있으면 askQuestions로 steering한다.
9. role별로 분리된 coordinator lane을 최소 2개 열어 병렬로 council review를 진행한다. draft가 high-risk, high-ambiguity, cross-functional이면 추가 lane이나 supporting research lane을 붙일 수 있다.
10. Coordinator verdict를 처리한다.
	- green: 현재 lane을 통과시킨다.
	- yellow: 해당 항목을 수정하고 같은 lane을 다시 연다.
	- red: 수정 후 재검토를 필수로 연다.
11. user feedback, new evidence, coordinator verdict를 반영해 `prd.md`를 더 정확하게 다듬는다.
12. invalidated lane만 다시 열며 refinement loop를 반복한다. heavy는 opened coordinator lane이 모두 green이고 evidence sufficiency와 downstream readiness가 다시 확보될 때까지 이 루프를 닫지 않는다.
	- clarification 문제면 질문 lane을 다시 연다.
	- evidence 문제면 digging lane을 다시 연다.
	- quality 문제면 coordinator lane을 다시 연다.
	- 문서 구조와 wording 문제면 drafting loop를 다시 연다.
13. planning quality gate를 평가한다.
14. gate를 통과하면 approved PRD briefing을 user에게 보여주고, 추가 refinement가 필요한지만 askQuestions로 확인한다.
15. Mate가 PRD coordinator signal을 다시 검토하고 downstream mode를 스스로 결정한다.
	- `디자인만`: design elaboration이 필요한 경우
	- `기술설계만`: technical elaboration이 필요한 경우
	- `둘 다`: 두 lane이 모두 필요하지만, heavy는 design review를 먼저 완료한 뒤 technical entry를 재확정해야 하는 경우
16. 결정된 downstream mode를 실행한다.
	- `디자인만` 또는 `둘 다`이면 Designer를 먼저 연다.
	- `기술설계만`이면 technical seed가 약한지 먼저 확인하고, 필요하면 targeted digging wave를 다시 연 뒤 Architector를 연다.
17. design lane이 열렸으면 generated `design.md`를 `prd.md` major coordinator finding 기준으로 다시 평가한다. PRD conflict, weak evidence, unresolved major design choice, downstream-ready specificity 부족이 보이면 invalidated design lane을 다시 연다.
18. post-design review 결과를 바탕으로 technical elaboration 필요 여부를 다시 판단한다. `둘 다`였거나 design 결과가 technical definition을 더 필요하게 만들면, technical seed가 충분한지 확인한 뒤 필요할 때만 Architector를 연다.
19. technical lane이 열렸으면 generated `technical.md`를 `prd.md`, approved design decision 기준으로 다시 평가한다. weak precedent, insufficient technical evidence, unresolved architecture risk, approved design constraint mismatch, PRD conflict가 보이면 invalidated technical lane만 다시 연다.
20. downstream artifact가 PRD conflict나 unresolved user choice를 드러내면 local patch로 덮지 말고 planning lane으로 되돌린다.
21. 추가 refinement가 없으면 `prd.md`, `artifacts.md`, `design.md(optional)`, `technical.md(optional)`를 latest approved version으로 동기화하고 heavy mode를 종료한다.

## Planning Quality Gate

heavy mode에서 PRD를 승인하려면 아래 조건이 모두 충족되어야 한다.

- latest revision이 coordinator-reviewed 상태다.
- opened coordinator lane이 모두 green이다.
- total score가 95 이상이다.
- critical blocker가 없다.
- evidence gap이 닫혔거나 명시적으로 bounded 상태다.
- downstream owner가 채팅을 다시 읽지 않고도 시작할 수 있을 만큼 approved `prd.md`가 준비되어 있다.

## Heavy Completion Gate

heavy mode를 종료하려면 아래 조건이 모두 충족되어야 한다.

- planning quality gate를 이미 통과했다.
- Mate가 downstream mode를 결정했고, required design review와 conditional technical entry 판단을 모두 끝냈다.
- 열린 `design.md`는 post-design review를 통과했고, 열린 `technical.md`는 current `prd.md`, `artifacts.md`, approved design decision과 정렬되어 있다.
- invalidated planning lane이나 downstream lane이 남아 있지 않다.
- latest artifact set이 동기화되어 있다.

## Approval And Downstream Trigger

- heavy는 downstream mode를 user 선택 대신 Mate가 결정한다.
- heavy의 auto-decision은 lane opening과 review ownership만 뜻한다. design/technical decision 자체는 downstream owner가 만든다.
- `둘 다`는 병렬 실행 뜻이 아니라 두 downstream lane이 모두 eventually 필요하다는 뜻이다.
- design lane이 열렸다면 technical lane entry는 post-design review 뒤에 확정한다.
- refinement은 필요한 lane만 다시 열어 지시 및 진행한다.
- downstream artifact가 current `prd.md`와 충돌하면 충돌 사실부터 명시하고, 필요하면 planning으로 되돌린다.

## Outputs

- updated `prd.md`
- updated `artifacts.md`
- optional `design.md`
- optional `technical.md`
- approved PRD briefing shown to user
- approved `prd.md`가 준비된 경우 relevant guided handoff trigger

## Guardrails

- digging이 깊다고 해서 raw transcript나 링크 dump를 artifact로 남기지 않는다.
- all green이 나오기 전에는 council loop를 pass로 처리하지 않는다.
- score 95 gate를 우회하지 않는다.
- PRD가 준비되면 guided handoff surface를 숨기지 않는다.
- PRD를 design spec, technical design, task breakdown, execution plan으로 무분별하게 비대화하지 않는다.

## Escalation Signals

- unresolved user choice가 product direction을 materially 바꾼다.
- external contract나 version evidence가 충돌한다.
- approved scope expansion이 필요하다.
- heavy digging을 여러 wave 진행해도 evidence가 closure되지 않는다.
- downstream owner가 current PRD와 양립할 수 없는 conflict를 드러낸다.

## Drift Signals And Re-entry

- PRD가 latest user intent와 어긋난다.
- EARS 다차원 커버리지에서 relevant dimension이 빠져 있다.
- opened coordinator lane 중 green이 아닌 lane이 다시 생긴다.
- opened design lane에서 weak evidence, unresolved major design choice, execution-ready specificity gap이 드러난다.
- opened technical lane에서 weak precedent, insufficient technical evidence, unresolved architecture risk, approved design constraint mismatch가 드러난다.
- downstream artifact가 current `prd.md`와 어긋난다.

Mate는 heavy mode 안에서 clarification, digging, council validation, PRD refinement, downstream refinement loop를 반복해 품질을 끌어올릴 수 있다.