---
name: kick-init
description: "One-time design context bootstrap for a project. Explores the codebase for existing design decisions, asks targeted questions to fill gaps, and persists a Design Context document that all design and frontend skills can reference. Use when starting design work on a new project, onboarding to an unfamiliar codebase, or when no Design Context exists yet. Always consult this skill before first design or visual work on a fresh project. Triggers on: kick-init, design context setup, design onboarding, project design setup, 디자인 컨텍스트 설정, 디자인 온보딩, 프로젝트 디자인 시작, 디자인 초기 세팅."
user-invocable: true
disable-model-invocation: true
---

# 디자인 컨텍스트 부트스트랩 (kick-init)

Prefer retrieval-led reasoning over pre-training-led reasoning.

## 목표

프로젝트의 디자인 방향, 사용자 맥락, 브랜드 성격, 미적 기준을 한 번에 수집하고 문서화한다. 이 문서는 이후 모든 ds-*/fe-* 스킬이 참조하는 Design Context의 출발점이 된다.

---

## 워크플로

### Step 1: 코드베이스 탐색

질문하기 전에 프로젝트에서 추론할 수 있는 것을 먼저 수집한다.

**확인 대상:**

- `README`, 문서 — 프로젝트 목적, 대상 사용자, 명시된 목표
- `package.json`, 설정 파일 — 기술 스택, 디자인 라이브러리 의존성
- 기존 컴포넌트 — 현재 디자인 패턴, spacing, typography
- 브랜드 에셋 — 로고, 파비콘, 이미 정의된 색상값
- 디자인 토큰 / CSS 변수 — 색상 팔레트, 폰트 스택, spacing scale
- 스타일 가이드, 브랜드 문서

확인한 것과 아직 불분명한 것을 구분해서 기록한다.

### Step 2: 갭 질문

코드베이스에서 추론할 수 없는 것만 사용자에게 질문한다.

#### 사용자와 목적

- 누가 사용하는가? 사용 맥락은?
- 사용자가 해결하려는 Job은?
- 인터페이스가 불러일으켜야 할 감정은? (신뢰, 기쁨, 차분함, 긴급함 등)

#### 브랜드와 성격

- 브랜드 성격을 3단어로 표현한다면?
- 느낌이 맞는 레퍼런스 사이트나 앱이 있는가? 구체적으로 어떤 점?
- 안티 레퍼런스 — 절대 닮으면 안 되는 것은?

#### 미적 방향

- 시각적 방향에 대한 강한 선호가 있는가? (미니멀, 대담, 우아, 장난스러움, 기술적, 유기적 등)
- 라이트 모드, 다크 모드, 또는 둘 다?
- 반드시 쓰거나 반드시 피해야 할 색상은?

#### 접근성

- 특정 접근성 요구사항이 있는가? (WCAG 레벨, 알려진 사용자 니즈)
- 모션 감소, 색각 이상 등에 대한 고려가 필요한가?

코드베이스 탐색에서 이미 답이 나온 질문은 건너뛴다.

### Step 3: Design Context 문서 작성

탐색 결과와 사용자 답변을 합성해서 아래 구조로 작성한다.

```markdown
## Design Context

### Users
[누구인지, 사용 맥락, Job to be Done]

### Brand Personality
[보이스, 톤, 3단어 성격, 감정 목표]

### Aesthetic Direction
[시각적 톤, 레퍼런스, 안티 레퍼런스, 테마]

### Design Principles
[대화에서 도출된 3~5가지 디자인 원칙]
```

### Step 4: 저장

1. 프로젝트 루트에 `.design-context.md`로 저장한다
2. 사용자에게 `.github/copilot-instructions.md`에도 Design Context를 추가할지 확인한다
3. 핵심 디자인 원칙을 요약해서 완료를 확인한다

---

## 판단 기준

- 코드베이스에서 이미 알 수 있는 것은 질문하지 않는다
- 질문은 5~8개를 넘기지 않는다 — 핵심 갭에만 집중한다
- Design Principles는 구체적이고 검증 가능해야 한다 — "좋은 UX를 제공한다" 같은 추상적 원칙은 피한다

---

## 범위

### 포함

- 프로젝트 디자인 컨텍스트 수집과 문서화
- 기존 디자인 에셋과 토큰 탐색
- 사용자 인터뷰 기반 브랜드/미적 방향 확립

### 제외

- 디자인 비평이나 개선 제안 → `kick-design-booster`
- 구체적인 UI 구현 → `ds-ui-patterns`, `fe-*`
- 디자인 리서치 → `research-design`
