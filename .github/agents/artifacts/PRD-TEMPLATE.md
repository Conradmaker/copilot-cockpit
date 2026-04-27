# PRD Template

이 문서는 planning phase의 최종 산출물인 PRD artifact 구조와 필수 규칙을 정의하는 on-demand template reference다.
Mate가 primary owner지만, PRD를 직접 검토하거나 downstream 문서를 만드는 다른 agent도 필요할 때 읽을 수 있다.

## Use This Doc When

- approved PRD를 새로 작성할 때
- PRD 구조가 충분한지 검토할 때
- planning artifact format을 agent file 밖에서 유지보수하고 싶을 때
- PRD에서 Design, Technical, execution-planning phase로 넘길 seed를 정리할 때

## Mandatory Rules

- PRD는 PM-oriented source of truth다. detailed design spec이나 task breakdown으로 흘러가지 않는다.
- PRD는 downstream Design 및 Technical work가 채팅을 다시 읽지 않고도 시작할 수 있을 만큼 self-contained 해야 한다.
- askQuestions는 planning 중 언제든 사용할 수 있지만, PRD 끝에 blocking question만 남기고 멈추는 방식으로 쓰지 않는다.
- session PRD file은 latest coordinator-reviewed version과 동기화한다.
- Quality Gate score는 planning Coordinator output의 `Scores`와 동기화한다. Coordinator score와 PRD score가 다르면 PRD를 approved로 닫지 않는다.
- PRD는 반드시 user에게 제시한다. file만 언급하고 끝내지 않는다.
- relevant dimension 식별과 requirement quality는 current workflow와 EARS coverage 기준을 따른다.
- requirements, constraints, assumptions, recommendations, open questions를 섞어 쓰지 않는다.
- unresolved uncertainty는 숨기지 말고 explicit하게 적는다.

## Template

```markdown
## PRD: {Title (2-10 words)}

{TL;DR - what problem is being solved, for whom, and the recommended product direction.}

**Executive Summary**

- Problem: {핵심 문제 1-2문장}
- Proposed solution: {제안 솔루션 1-2문장}
- Expected impact: {기대 효과 1-2문장}

**Problem Statement & Evidence**

- Who is affected: {누가 이 문제를 겪는가}
- What is happening: {현재 어떤 문제가 발생하는가}
- Why it matters now: {왜 지금 중요한가}
- Evidence:
  - {research, analytics, user quote, support signal 등}

**Target Users & Jobs**

- Primary user: {주 사용자}
- Secondary user: {보조 사용자 - 필요 시만}
- Jobs to be done: {사용자가 이루려는 일}
- Pain points: {사용자 관점의 주요 고통}

**Strategic Context**

- Why now: {우선순위 배경}
- Product or business goal: {연결되는 목표}
- Competitive or ecosystem context: {필요 시만}

**Solution Overview**

- Product direction: {무엇을 만들고 어떻게 풀 것인가}
- Core experience: {사용자가 경험하는 핵심 흐름}
- Release posture: {rough MVP / phased rollout / optional follow-up}

**Experience Goals & Design Intent**

- Desired user feeling: {예: guided, calm, confident, fast, focused}
- Interaction principles: {상호작용 원칙}
- Visual or brand direction: {분위기, 밀도, 시각 톤}
- Design non-goals: {지금 PRD에서 확정하지 않을 디자인 항목}

**Success Metrics**

- Primary metric: {핵심 성공 지표와 목표값}
- Secondary metrics: {보조 지표}
- Guardrail metrics: {악화되면 안 되는 지표}

**Requirements**

Dimensions: {해당 차원 — functional / visual-design / UX / technical / content}

- [REQ-N] The [system/component] shall [requirement]
- [REQ-N] WHEN [trigger], the [system/component] shall [response]
- [REQ-N] WHILE [state], the [system/component] shall [behavior]
- [REQ-N] IF [condition], THEN the [system/component] shall [response]
  {EARS가 더 명확할 때만 사용하고, 부자연스러우면 자유형 허용}

**Constraints, Assumptions & Edge Cases**

- Constraints: {하드 제약, 외부 계약, 정책}
- Assumptions: {현재 가정하고 있는 것}
- Edge cases: {놓치기 쉬운 경우}

**Scope**

- Included: {이번 PRD 범위}
- Out of scope: {이번에 하지 않는 것}
- Non-goals: {명시적으로 원하지 않는 것}

**Dependencies & Risks**

- Dependencies: {팀, 시스템, 외부 의존성}
- Risks: {주요 리스크}
- Mitigations: {완화 방법}

**Open Questions & Decisions**

- Open questions: {아직 결정되지 않은 항목}
- Decisions made: {이미 고정한 중요한 결정}

**Downstream Seeds**

- Design.md should elaborate: {화면/상호작용/분위기/UX seed}
- Technical.md should elaborate: {architecture/integration/constraint seed}
- Execution planning should elaborate: {task planning, sequencing, verification seed}

**References & Evidence**

- Key findings: {핵심 발견}
- Resource index:
  - {path/url} — {무엇을 다루는지}
- Related session artifact index: /memories/session/artifacts.md (generated docs only)

**Quality Gate**

- Problem clarity: {0-20}
- User & JTBD clarity: {0-20}
- Success metrics & scope discipline: {0-20}
- Requirements quality (including EARS where useful): {0-20}
- Risks, open questions, downstream readiness: {0-20}
- Total: {0-100}
```

## Quality Gate Anchors

- Problem clarity: 0 추측 위주 / 5 문제명만 있음 / 10 문제와 영향은 보이나 근거 약함 / 15 문제, 사용자, 영향이 대부분 연결됨 / 20 문제, 근거, 왜 지금 중요한지가 모두 명시됨
- User & JTBD clarity: 0 사용자 불명확 / 5 사용자명만 있음 / 10 primary user와 JTBD 일부만 보임 / 15 primary user, JTBD, pain point가 대부분 연결됨 / 20 target user, JTBD, pain point가 구체적이고 충돌이 없음
- Success metrics & scope discipline: 0 측정 불가 / 5 vague metric 또는 scope only / 10 metric이나 scope 중 하나가 약함 / 15 metric, included, out of scope가 대부분 선명함 / 20 measurable metric, guardrail, scope boundary, non-goal이 모두 분명함
- Requirements quality: 0 requirement 없음 / 5 generic bullet 위주 / 10 핵심 requirement는 있으나 testability 약함 / 15 대부분의 requirement가 조건과 반응을 설명함 / 20 relevant dimension이 빠지지 않고, requirement가 testable하며 ambiguity가 잘 bounded됨
- Risks, open questions, downstream readiness: 0 risk와 open issue 불명확 / 5 risk list만 존재 / 10 risk 또는 downstream seed가 약함 / 15 major risk, open question, downstream seed가 대부분 usable함 / 20 bounded risk, decision status, downstream seed가 모두 self-contained하게 정리됨

## Review Checklist

- 문제와 근거가 분명한가
- target user와 JTBD가 비어 있지 않은가
- success metrics가 measurable한가
- scope, out of scope, non-goals가 서로 구분되는가
- requirements와 constraints, assumptions가 뒤섞이지 않았는가
- PRD가 design spec이나 task plan으로 과도하게 내려가지 않았는가
- References & Evidence가 concise summary 수준을 유지하고, `/memories/session/artifacts.md`가 generated docs만 정확히 가리키는가
- downstream Design 및 Technical work가 시작할 seed가 충분한가
