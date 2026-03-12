# 메이트 워크플로우 시각화

이 문서는 [product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)의 워크플로우를 Mermaid 다이어그램으로 시각화한다.

---

## 1. 전체 워크플로우 개요

```mermaid
flowchart TB
    Start([사용자 요청]) --> Planning[Planning Phase]
    
    Planning -->|Quality Gate 통과| PlanBriefing[Approved Plan Briefing]
    Planning -->|Refinement Loop| Planning
    
    PlanBriefing --> ModeSelect{Mode 선택<br/>askQuestions}
    ModeSelect --> HandoffWrite[handoff.md 작성]
    HandoffWrite --> ExecutionMode{Handoff Surface 노출}
    
    ExecutionMode -->|Fleet Mode| FleetExecution[Fleet Mode Execution]
    ExecutionMode -->|Rush Mode| RushExecution[Rush Mode Execution]
    
    FleetExecution --> Review[Review Phase]
    RushExecution --> Review
    
    Review -->|approve| GitTail{Git Tail 필요?}
    Review -->|approve-with-risks| GitTail
    Review -->|rework-required| Rework{Rework 유형}
    
    Rework -->|Local Fix| FleetExecution
    Rework -->|Local Fix| RushExecution
    Rework -->|Spec Failure| Planning
    
    GitTail -->|Yes| GitMaster[Git Tail Phase]
    GitTail -->|No| MemoryTail{Memory Tail 필요?}
    
    GitMaster --> MemoryTail
    
    MemoryTail -->|Durable Signal 존재| MemorySynth[Memory Tail Phase]
    MemoryTail -->|No| End([완료])
    
    MemorySynth --> End
    
    style Planning fill:#e1f5fe
    style FleetExecution fill:#fff3e0
    style RushExecution fill:#fff3e0
    style Review fill:#f3e5f5
    style GitMaster fill:#e8f5e9
    style MemorySynth fill:#fce4ec
```

### Phase 전환 조건

| From | To | Entry Conditions |
|------|-----|------------------|
| Planning | Execution | approved plan, passed coordinator-reviewed quality gate, mode confirmed, handoff.md 완성, explicit user approval |
| Execution | Review | implementation 결과와 verification evidence 준비 |
| Review | Git Tail | review verdict가 승인 가능 수준 |
| Review | Memory Tail | validated work나 반복 가치가 있는 signal 존재 |
| Review | Planning | spec-level failure로 local fix로 덮으면 안 되는 경우 |

---

## 2. Planning Phase 상세

```mermaid
flowchart TB
    Start([사용자 요청]) --> Discovery[Discovery]
    
    Discovery --> |context/evidence gap| AskQ1{askQuestions 필요?}
    AskQ1 -->|Yes| UserInput[사용자 의도/선호 파악]
    AskQ1 -->|No| EARSCheck
    UserInput --> EARSCheck
    
    Discovery --> |reference need| ExploreLane[Explore 호출]
    Discovery --> |external evidence need| LibrarianLane[Librarian 호출]
    
    ExploreLane --> EARSCheck
    LibrarianLane --> EARSCheck
    
    EARSCheck[EARS 다차원 커버리지 체크<br/>functional/visual-design/UX/technical/content]
    EARSCheck --> |빠진 차원| AskQ2[askQuestions로 확인]
    AskQ2 --> SpecDraft
    EARSCheck --> |All covered| SpecDraft[Spec 초안 작성]
    
    SpecDraft --> CouncilCheckpoint[Council Checkpoint]
    
    CouncilCheckpoint --> |planning checkpoint| ParallelReview{병렬 리뷰}
    
    ParallelReview --> DynCoord1[동적 Coordinator Lane 1<br/>coord-types/type.md 로드]
    ParallelReview --> DynCoord2[동적 Coordinator Lane 2<br/>coord-types/type.md 로드]
    ParallelReview --> ExploreCheck[Explore<br/>추가 evidence]
    ParallelReview --> LibrarianCheck[Librarian<br/>external reference]
    
    DynCoord1 --> Verdict{Coordinator 개선 루프}
    DynCoord2 --> Verdict
    ExploreCheck --> Synthesis[Mate 합성]
    LibrarianCheck --> Synthesis
    
    Verdict -->|green| Synthesis
    Verdict -->|yellow| FixYellow[Fix 후 Mate 판단]
    Verdict -->|red| FixRed[Fix 후 재검토 필수]
    FixYellow --> Synthesis
    FixRed --> CouncilCheckpoint
    
    Synthesis --> Design[Design<br/>EARS execution-ready spec]
    
    Design --> Refinement[Refinement]
    
    Refinement --> QualityGate{Quality Gate}
    
    QualityGate -->|Total Score < 88<br/>Critical Blocker 존재| Refinement
    QualityGate -->|Pass| PlanBriefing[Approved Plan Briefing]
    
    PlanBriefing --> ModeAsk[askQuestions로 Mode 확인]
    ModeAsk --> HandoffWrite[handoff.md 작성]
    HandoffWrite --> HandoffSurface[Handoff Surface 노출]
    
    HandoffSurface --> UserApproval{User Approval}
    UserApproval -->|Approved| ExecutionMode{실행 모드}
    UserApproval -->|Clarification 필요| AskQ1
    
    style Discovery fill:#e3f2fd
    style EARSCheck fill:#e8eaf6
    style CouncilCheckpoint fill:#fff8e1
    style Verdict fill:#fff3e0
    style Design fill:#f1f8e9
    style QualityGate fill:#ffebee
    style HandoffSurface fill:#fce4ec
```

### Planning Quality Gate 조건

- Total Score 88 이상
- Critical Blocker 없음
- Latest revision이 coordinator-reviewed 상태
- Pass 후 askQuestions로 Mode 확인 → `handoff.md` 작성 → handoff surface 노출

---

## 3. Execution Phase 상세

### Execution Entry Conditions

1. Approved `plan.md`가 존재
2. Explicit user approval이 있음
3. Current `handoff.md`가 있음
4. Required planning lanes가 invalidated 상태가 아님

```mermaid
flowchart TB
    Start([Execution 시작]) --> ReadPlan[plan.md & handoff.md 읽기]
    
    ReadPlan --> Mode{실행 모드}
    
    Mode -->|Fleet Mode| Commander[Commander<br/>Orchestration Owner]
    Mode -->|Rush Mode| DeepAgent[Deep Execution Agent<br/>Single Implementer]
    
    %% Fleet Mode Flow
    Commander --> FleetStrategy[Execution Strategy 확정]
    FleetStrategy --> FleetContext{Context 보강 필요?}
    
    FleetContext -->|Yes| FleetExplore[Explore/Librarian 호출]
    FleetContext -->|No| WorkSplit
    
    FleetExplore --> WorkSplit[Work Unit Split/Merge]
    
    WorkSplit --> WorkerAssign[Deep Execution Agent Worker<br/>Coding Work 위임]
    
    WorkerAssign --> FleetMilestone{Major Milestone}
    
    FleetMilestone -->|No| WorkerAssign
    FleetMilestone -->|Yes| FleetCoordCheck[Coordinator Validation 요청]
    
    FleetCoordCheck --> FleetCoordVerdict{Coordinator Verdict}
    
    FleetCoordVerdict -->|Not Ready| FleetStrategy
    FleetCoordVerdict -->|Ready| FleetTodoSync[Todo Sync]
    
    FleetTodoSync --> FleetComplete{Implementation 완료?}
    
    FleetComplete -->|No| WorkerAssign
    FleetComplete -->|Yes| FleetReview[Reviewer Broad Review]
    
    %% Rush Mode Flow
    DeepAgent --> RushContext{Context 보강 필요?}
    
    RushContext -->|Yes| RushExplore[Explore/Librarian 호출]
    RushContext -->|No| RushImpl
    
    RushExplore --> RushImpl[직접 구현]
    
    RushImpl --> RushMilestone{Major Milestone}
    
    RushMilestone -->|No| RushImpl
    RushMilestone -->|Yes| RushCoordCheck[Coordinator Validation 요청]
    
    RushCoordCheck --> RushCoordVerdict{Coordinator Verdict}
    
    RushCoordVerdict -->|Not Ready| RushImpl
    RushCoordVerdict -->|Ready| RushTodoSync[Todo Sync]
    
    RushTodoSync --> RushComplete{Implementation 완료?}
    
    RushComplete -->|No| RushImpl
    RushComplete -->|Yes| RushReview[Reviewer Broad Review]
    
    %% Review 결과
    FleetReview --> ReviewResult{Review Verdict}
    RushReview --> ReviewResult
    
    ReviewResult -->|Rework Required| ReworkType{Rework 유형}
    
    ReworkType -->|Fleet| WorkerAssign
    ReworkType -->|Rush| RushImpl
    
    ReviewResult -->|Approve| Tail{Tail 필요?}
    
    Tail --> Git
    Tail --> Memory
    
    style Commander fill:#e8f5e9
    style DeepAgent fill:#fff3e0
    style FleetCoordCheck fill:#f3e5f5
    style RushCoordCheck fill:#f3e5f5
```

### Execution Mode 선택 기준

| Mode | Owner | 언제 선택 |
|------|-------|----------|
| Fleet Mode | Commander | Split/Merge orchestration이 품질에 의미 있게 도움이 될 때 |
| Rush Mode | Deep Execution Agent | Context continuity와 단일 implementer 흐름이 유리할 때 |

---

## 4. Review Phase 상세

```mermaid
flowchart TB
    Start([Implementation 완료]) --> Reviewer[Reviewer 호출]
    
    Reviewer --> ReadArtifacts[plan.md & handoff.md 확인]
    
    ReadArtifacts --> ChangedSurface[변경 영역 분석]
    
    ChangedSurface --> Validation[Validation Focus 검토]
    
    Validation --> CodeReview[Code Review<br/>Correctness, Regression, Security]
    
    CodeReview --> DesignReview[Design & Product Review<br/>Consistency, Impact]
    
    DesignReview --> ResidualRisk[Residual Risks 파악]
    
    ResidualRisk --> Verdict{Review Verdict}
    
    Verdict -->|Approve| ReleaseReady[Release Recommendation 작성]
    Verdict -->|Approve-with-Risks| RiskDocument[Residual Risk 명시]
    Verdict -->|Rework-Required| ReworkType{Rework 유형 판단}
    
    ReleaseReady --> TailDecision{Tail 작업 필요?}
    RiskDocument --> TailDecision
    
    ReworkType -->|Local Fix| Implementer[Implementer에게 Rework]
    ReworkType -->|Spec Failure| BackToPlanning[Back to Planning]
    
    Implementer --> Reviewer
    
    BackToPlanning --> PlanningPhase[Planning Phase 재시작]
    
    TailDecision -->|Git Tail| GitPhase[Git Tail Phase]
    TailDecision -->|Memory Tail| MemoryPhase[Memory Tail Phase]
    TailDecision -->|Both| BothTail[Git + Memory Tail]
    TailDecision -->|None| End([완료])
    
    GitPhase --> End
    MemoryPhase --> End
    BothTail --> End
    
    style Reviewer fill:#f3e5f5
    style Verdict fill:#ffebee
    style ReworkType fill:#fff8e1
```

### Review Outcomes

| Verdict | 의미 | 다음 단계 |
|---------|------|----------|
| `approve` | 승인 가능, residual risk 없음 | Git/Memory Tail 진행 |
| `approve-with-risks` | 승인 가능하지만 residual risk 존재 | Risk 명시 후 Tail 진행 |
| `rework-required` | 수정 필요 | Implementer rework 또는 back-to-planning |

---

## 5. Git Tail Phase 상세

### Git Tail Entry Conditions

1. Implementation과 review가 git workflow action을 할 정도로 validated됨
2. Review가 통과했거나 explicit exception이 승인됨

```mermaid
flowchart TB
    Start([Git Tail 시작]) --> TaskType{작업 유형 분류}
    
    TaskType -->|Branch| BranchOp[Branch 작업]
    TaskType -->|Commit| CommitOp[Commit 작업]
    TaskType -->|PR| PROp[Pull Request 작업]
    TaskType -->|Merge| MergeOp[Merge 작업]
    TaskType -->|Other GH| GHWorkflow[GitHub Workflow 작업]
    
    BranchOp --> ReadSkill[git-workflow skill 읽기]
    CommitOp --> ReadSkill
    PROp --> ReadSkill
    MergeOp --> ReadSkill
    GHWorkflow --> ReadSkill
    
    ReadSkill --> CheckState[현재 Git State 확인]
    
    CheckState --> CheckConvention[GitHub Flow 규칙 & 팀 Convention 확인]
    
    CheckConvention --> ValidateNaming[Branch Naming, Commit Message, PR Shape 검증]
    
    ValidateNaming --> Execute[작업 실행]
    
    Execute --> Verify[결과 검증]
    
    Verify --> FollowUp{Follow-up 필요?}
    
    FollowUp -->|Conflict| ConflictResolve[Conflict 해결]
    FollowUp -->|Auth Failure| AuthIssue[Auth 문제 해결]
    FollowUp -->|CI Blocker| CIWait[CI 대기/해결]
    FollowUp -->|None| End([Git Tail 완료])
    
    ConflictResolve --> End
    AuthIssue --> End
    CIWait --> End
    
    style TaskType fill:#e8f5e9
    style Execute fill:#fff8e1
    style Verify fill:#f3e5f5
```

### Git Tail Guardrails

- `main`에 직접 커밋하지 않는다
- 작업 전에 현재 상태를 확인한다
- 가능하면 커밋 전에 diff를 다시 본다
- 팀 convention과 GitHub Flow를 어기지 않는다

---

## 6. Memory Tail Phase 상세

### Memory Synthesizer Authority

`Memory-synthesizer`는 durable signal이 충분하면 **사용자 확인 없이 저장**할 수 있다.

```mermaid
flowchart TB
    Start([Memory Tail 시작]) --> AnalyzeSession[Session Context 분석]
    
    AnalyzeSession --> Classify{Memory 분류}
    
    Classify -->|Personal| PersonalMemory[Personal Memory<br/>User preferences, patterns]
    Classify -->|Project| ProjectMemory[Project Memory<br/>Codebase facts, conventions]
    
    PersonalMemory --> DurabilityCheck{Signal Durability}
    ProjectMemory --> DurabilityCheck
    
    DurabilityCheck -->|Weak/Temporary| Skip[Skip]
    DurabilityCheck -->|Strong/Durable| DuplicationCheck{Duplication 확인}
    
    DuplicationCheck -->|Existing| Update[기존 Memory 업데이트]
    DuplicationCheck -->|New| Save[새 Memory 저장]
    
    Update --> End([Memory Tail 완료])
    Save --> End
    Skip --> End
    
    style Classify fill:#e8f5e9
    style DurabilityCheck fill:#fff8e1
    style Save fill:#fce4ec
```

### Memory Tail Guardrails

- Secret, credential, sensitive data를 저장하지 않는다
- Temporary task state를 durable memory로 저장하지 않는다
- Low-confidence write보다 skip를 우선한다
- Memory pollution과 duplication을 피한다

---

## 7. 역할별 책임과 상호작용

```mermaid
flowchart LR
    subgraph Planning[Planning Phase]
        Mate[Mate<br/>Planning Owner]
        Explore1[Explore<br/>Local Evidence]
        Librarian1[Librarian<br/>External Research]
        Coord1[Coordinator<br/>Planning Council]
    end
    
    subgraph Execution[Execution Phase]
        Commander[Commander<br/>Fleet Orchestrator]
        DeepExec[Deep Execution Agent<br/>Implementer/Worker]
        Coord2[Coordinator<br/>Milestone Validator]
    end
    
    subgraph Review[Review Phase]
        Reviewer[Reviewer<br/>Quality Gate]
    end
    
    subgraph Tail[Tail Phases]
        GitMaster[Git Master<br/>Git Workflow]
        MemSynth[Memory Synthesizer<br/>Memory Tail]
    end
    
    Mate -->|planning_review_packet| Coord1
    Mate -->|explore request| Explore1
    Mate -->|research request| Librarian1
    Coord1 -->|verdict| Mate
    Explore1 -->|evidence| Mate
    Librarian1 -->|evidence| Mate
    
    Mate -->|handoff: Fleet Mode| Commander
    Mate -->|handoff: Rush Mode| DeepExec
    
    Commander -->|delegates coding| DeepExec
    DeepExec -->|milestone validation| Coord2
    Coord2 -->|verdict + todo sync| Commander
    Coord2 -->|verdict + todo sync| DeepExec
    
    Commander -->|review request| Reviewer
    DeepExec -->|review request| Reviewer
    
    Reviewer -->|approve| GitMaster
    Reviewer -->|approve| MemSynth
    
    style Mate fill:#e3f2fd
    style Commander fill:#e8f5e9
    style DeepExec fill:#fff3e0
    style Reviewer fill:#f3e5f5
    style GitMaster fill:#e0f2f1
    style MemSynth fill:#fce4ec
```

### 역할별 Owner 책임

| Role | Phase | 책임 |
|------|-------|------|
| **Mate** | Planning | User intent를 execution-ready spec으로 변환, planning loop 주도 |
| **Coordinator** | Planning, Execution | Planning council 검토, milestone validation, todo sync |
| **Commander** | Execution (Fleet) | Fleet Mode orchestration, worker 관리, review orchestration |
| **Deep Execution Agent** | Execution | Rush Mode primary implementer, Fleet Mode coding worker |
| **Reviewer** | Review | Broad quality gate, correctness/security/design/product 검토 |
| **Git Master** | Git Tail | Validated change를 GitHub Flow에 맞게 정리 |
| **Memory Synthesizer** | Memory Tail | Durable signal만 memory에 저장 |
| **Explore** | Support | Local evidence, reusable pattern, symbol flow 탐색 |
| **Librarian** | Support | Official docs, external research, version 검증 |

---

## 8. 재진입 루프 상세

```mermaid
flowchart TB
    subgraph Loops[재진입 루프]
        RefinementLoop[Refinement Loop<br/>Planning 안에서 반복]
        ReworkLoop[Rework Loop<br/>Execution/Review 안에서 반복]
        BackToPlanning[Back-to-Planning Loop<br/>Spec failure 시 Planning 복귀]
    end
    
    Start([시작]) --> Planning
    
    subgraph Planning[Planning Phase]
        P1[Discovery] --> P2[Council Checkpoint]
        P2 --> P3[Design]
        P3 --> P4[Refinement]
        P4 --> P5{Quality Gate}
        P5 -->|Fail| P4
        P5 -->|Pass| P6{User Gate}
        P6 -->|Reject| P4
        P6 -->|Approve| Execution
    end
    
    subgraph Execution[Execution Phase]
        E1[Read Plan/Handoff] --> E2[Implementation]
        E2 --> E3{Milestone}
        E3 -->|Continue| E2
        E3 -->|Complete| Review
    end
    
    subgraph Review[Review Phase]
        R1[Code Review] --> R2[Design Review]
        R2 --> R3{Verdict}
        R3 -->|Rework| R4{Rework Type}
        R4 -->|Local| E2
        R4 -->|Spec Failure| P1
        R3 -->|Approve| Tail[Tail Phases]
    end
    
    style P4 fill:#fff8e1
    style R4 fill:#ffebee
    style BackToPlanning fill:#ffebee
```

### 루프 발생 조건

| 루프 | 발생 조건 | 범위 |
|------|----------|------|
| **Refinement Loop** | Quality gate 미통과, user feedback, new evidence | Planning Phase 내부 |
| **Rework Loop** | Review verdict = rework-required | Execution ↔ Review |
| **Back-to-Planning** | Spec-level failure, scope expansion 필요 | Review → Planning |

---

## 9. Quality Gate 체크리스트

```mermaid
flowchart TB
    subgraph PlanningGate[Planning Quality Gate - 통과 조건]
        PG1[Total Score ≥ 88]
        PG2[No Critical Blocker]
        PG3[Coordinator-Reviewed]
        
        PG1 --> PG2 --> PG3
    end
    
    subgraph PostGateActions[Post-Gate Actions]
        PGA1[handoff.md 생성/갱신]
        PGA2[User Approval]
        
        PGA1 --> PGA2
    end
    
    subgraph ExecutionGate[Execution Quality Gate]
        EG1[Milestone Validation = Ready]
        EG2[Todo Sync 최신 상태]
        EG3[Verification Completeness]
        
        EG1 --> EG2 --> EG3
    end
    
    subgraph ReviewGate[Review Quality Gate]
        RG1[Verdict = Approve/approve-with-risks]
        RG2[Residual Risk 명시]
        RG3[Release Recommendation]
        
        RG1 --> RG2 --> RG3
    end
    
    subgraph GitGate[Git Tail Quality Gate]
        GG1[Workflow Safety]
        GG2[Rule Compliance]
        
        GG1 --> GG2
    end
    
    subgraph MemoryGate[Memory Tail Quality Gate]
        MG1[Durable Signal 충분]
        MG2[Duplication Avoidance]
        
        MG1 --> MG2
    end
    
    style PlanningGate fill:#e3f2fd
    style ExecutionGate fill:#fff3e0
    style ReviewGate fill:#f3e5f5
    style GitGate fill:#e8f5e9
    style MemoryGate fill:#fce4ec
```

---

## 10. 에스컬레이션 시그널

```mermaid
flowchart TB
    subgraph PlanningEscalation[Planning Escalation Signals]
        PE1[Unresolved user choice가<br/>quality gate를 막음]
        PE2[External contract/version<br/>evidence 충돌]
        PE3[Previously passed lane<br/>invalidation]
        PE4[Verification contract가<br/>scope를 커버 못함]
    end
    
    subgraph ExecutionEscalation[Execution Escalation Signals]
        EE1[Scope expansion 필요]
        EE2[Local evidence만으로<br/>blocker 해결 불가]
        EE3[User choice 필요]
        EE4[Milestone validation =<br/>not-ready or severe drift]
    end
    
    subgraph ReviewEscalation[Review Escalation Signals]
        RE1[Spec failure requiring<br/>planning rework]
        RE2[Residual risk가<br/>release를 block]
    end
    
    subgraph GitEscalation[Git Tail Escalation Signals]
        GE1[Merge conflict]
        GE2[Permission/auth failure]
        GE3[CI blocker]
        GE4[Branch strategy conflict]
    end
    
    subgraph MemoryEscalation[Memory Tail Escalation Signals]
        ME1[Personal vs project<br/>classification 모호]
        ME2[Candidate가 current task에만<br/>묶여 있음]
        ME3[Signal strength 약함]
    end
    
    style PlanningEscalation fill:#e3f2fd
    style ExecutionEscalation fill:#fff3e0
    style ReviewEscalation fill:#f3e5f5
    style GitEscalation fill:#e8f5e9
    style MemoryEscalation fill:#fce4ec
```

---

## 참조

- [product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md) — 워크플로우 상세 정의
- [subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md) — 서브에이전트 호출 계약
- [AGENTS.md](AGENTS.md) — 전역 불변식과 역할 경계
