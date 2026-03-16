# Technical Template

이 문서는 downstream definition phase에서 `technical.md`를 작성할 때 따르는 artifact template다.
Architector가 primary owner지만, Mate가 downstream technical kickoff를 준비하거나 Execution phase가 technical intent를 해석할 때도 읽을 수 있다.

## Use This Doc When

- approved PRD를 기반으로 `technical.md`를 처음 만들 때
- 기존 `technical.md`를 새 PRD 방향에 맞게 갱신할 때
- architecture, integration, stack choice, library choice, technical constraint를 한 문서로 정리해야 할 때
- execution 이전에 technical decision과 trade-off를 self-contained 하게 남겨야 할 때

## Mandatory Rules

- `technical.md`는 approved `prd.md`를 전제로 한다.
- `technical.md`는 PRD를 다시 쓰지 않고, approved PRD를 architecture, integration, technical decision으로 확장한다.
- existing codebase, current stack, team precedent가 있으면 external reference보다 먼저 읽는다.
- local precedent가 약하거나 stack choice가 불명확하면 official > source > web 순서로 자료조사와 library search를 수행한다.
- 주요 architecture, stack, library choice는 FR, NFR, constraint, assumption 중 최소 하나와 연결되어야 한다.
- 선택하지 않은 대안과 trade-off를 남긴다.
- technical decision이 PRD scope, requirement, metric 변경을 요구하면 conflict를 명시하고 planning으로 되돌린다.
- execution seed는 direct code나 detailed task breakdown이 아니라 architecture-to-execution bridge 수준으로 남긴다.
- spike candidate는 unresolved high-risk technical question이 남을 때만 optional로 둔다.

## Template

```markdown
## Technical: {Title (2-10 words)}

{TL;DR - what system or capability is being designed, what technical direction this document recommends, and why this direction fits the approved PRD.}

**Technical Context**

- Source PRD: {path or title}
- Existing system baseline: {current stack, modules, services, or none}
- Technical goal: {이번 technical.md가 구체화해야 하는 핵심}
- Current technical gaps: {execution 전에 해결해야 할 technical ambiguity}

## 1. Inputs & Architectural Drivers

- Functional requirements in scope: {이번 technical design이 직접 다루는 요구사항}
- Non-functional requirements in scope: {latency, scale, security, availability, cost 등}
- Constraints: {infra, policy, vendor, timeline, team skill, external contract}
- Existing precedents: {local pattern or none}
- Architectural drivers: {설계 결정을 강하게 제한하는 요구사항}

## 2. Architecture Pattern & System Boundaries

- Selected pattern: {modular monolith / service-oriented / event-driven / other}
- Why this pattern fits: {요구사항과의 연결}
- System boundaries: {어디까지 이 문서 범위인지}
- High-level flow: {request, data, event 흐름}

ASCII diagram이나 설명형 구조도를 사용해도 된다.

## 3. Stack and Library Search Summary

- Local evidence first: {existing stack or precedent가 무엇이었는지}
- Candidate technologies: {후보 stack or library 목록}
- Adopted choices: {채택한 기술과 이유}
- Rejected alternatives: {제외한 기술과 이유}
- Evidence tiers used: {official, source, web 중 무엇을 썼는지}

내부 선례가 약했다면 이 섹션은 필수다.

## 4. Component Responsibilities & Interfaces

- Component/module/service: {이름} — {책임} — {interface boundary}
- Component/module/service: {이름} — {책임} — {interface boundary}
- Ownership boundaries: {state, data, side-effect, orchestration 분리}

## 5. Data Model & Storage Strategy

- Core entities or aggregates: {핵심 데이터 구조}
- Storage choice: {RDB, cache, queue, object store 등}
- Data consistency model: {transaction, eventual consistency, read/write path}
- Caching strategy: {where, why, invalidation}
- Migration or compatibility notes: {기존 데이터와의 관계}

## 6. API & Integration Contracts

- Internal contracts: {module API, service API, event contract}
- External integrations: {third-party API, webhook, SDK, platform capability}
- Auth/authz considerations: {relevant if applicable}
- Failure and retry behavior: {timeout, retry, fallback, idempotency}
- Validation and error strategy: {input validation, error surface, observability hook}

## 7. NFR Mapping

- Performance: {어떤 설계 결정이 담당하는가}
- Scalability: {어떤 설계 결정이 담당하는가}
- Security: {어떤 설계 결정이 담당하는가}
- Reliability: {어떤 설계 결정이 담당하는가}
- Maintainability: {어떤 설계 결정이 담당하는가}
- Availability/Operations: {어떤 설계 결정이 담당하는가}

작업 특성에 맞는 NFR만 남기되, relevant category는 빠뜨리지 않는다.

## 8. Deployment & Operations

- Runtime topology: {single deployable, worker split, edge/server, mobile/backend 등}
- Scaling posture: {horizontal, queue-based, partitioning, none}
- Configuration and secrets: {어디서 관리하는지}
- Monitoring and alerting: {logs, metrics, tracing, alerts}
- Backup and recovery: {relevant if applicable}

## 9. Trade-offs & Future Evolution

- Decision: {무엇을 선택했는가} — {장점} — {단점}
- Decision: {무엇을 선택했는가} — {장점} — {단점}
- Future evolution path: {나중에 requirements가 커지면 어디를 바꿀지}

## 10. Risks, Open Questions & Optional Spike Candidates

- Risks: {주요 리스크와 완화 방향}
- Open questions: {아직 남은 의사결정}
- Optional spike candidates:
  - {question} — {why unresolved} — {validation plan} — {timebox}

## 11. Execution Seeds

- Implementation seeds: {구현자가 먼저 건드려야 할 구조와 순서 힌트}
- Verification seeds: {무엇을 테스트하고 측정해야 하는가}
- Non-goals for execution: {이번 단계에서 하지 않을 것}

## 12. References & Evidence

- Local evidence:
  - {path} — {what it contributed}
- External references:
  - {url / source} — {what it contributed}
- Technical rationale summary: {왜 이 방향을 선택했는지}
- Conflicts or escalations: {PRD conflict 또는 unresolved choice가 있으면 명시}
```

## Review Checklist

- approved PRD의 direction과 충돌하지 않는가
- architecture pattern, stack, library choice가 requirements와 NFR에 연결되는가
- local precedent와 external evidence의 우선순위가 분명한가
- local precedent가 약할 때 stack and library search summary가 빠지지 않았는가
- component boundary, data/storage, API/integration, deployment 방향이 execution 전에 충분히 구체적인가
- trade-off, rejected alternatives, risks, open questions를 숨기지 않았는가
- execution seed가 direct code나 task breakdown이 아니라 architecture-to-execution bridge 수준으로 정리되었는가