# 에이전트 시스템 가이드

이 문서는 `.github/` 영역을 유지보수할 때 어떤 문서가 무엇을 담당하는지 빠르게 확인하는 사용자용 안내서다.
작성 세부 규칙을 다시 길게 풀어쓰지 않고, `AGENTS.md`, `instructions`, `agents`, `memories`가 서로 충돌하지 않게 맞추는 데만 집중한다.

## 영역별 역할

- `AGENTS.md`: 항상 읽히는 기본 맥락이다. 철학, 책임 경계, 최소한의 담당 구조를 둔다.
- `instructions/`: 공통 실행 규칙, packet schema, skill discovery registry, editing contract 같은 공유 규칙을 둔다.
- `docs/`: 사람이 읽는 workflow 안내 문서, system guide 같은 장문 문서를 둔다.
- `agents/`: 각 agent가 따르는 개별 contract와 agent-owned artifact template를 둔다.
- `agents/workflows/`: `.agent.md`에 모두 담기엔 긴 agent별 절차, 관문, 재진입 규칙을 둔다.
- `memories/`: 프로젝트 memory 경로와 오래 유지할 사실을 둔다.
- `skills/`: 재사용 가능한 기능을 skills에서 관리할 때 수정한다.

## 기준 문서 맵

- 공통 packet schema (`TASK`, `EXPECTED_OUTCOME`, `MUST_DO`, `MUST_NOT_DO`, `CONTEXT`, `ARTIFACTS`, `task_packet`), `ARTIFACTS`의 `REF_{N}` 규칙, phase별 산출물 정책, subagent 선택 기준의 기준 문서: `.github/instructions/subagent-invocation.instructions.md`
- Execution worker에 작업을 넘길 때의 규칙, dispatch-ready brief 구성 방식, worker 재사용 및 재시도 정책의 기준 문서: `.github/agents/Commander.agent.md`
- agent별 workflow와 receiver contract의 기준 위치: `.github/agents/`, `.github/agents/workflows/`
- 사람이 읽는 workflow 안내 문서의 기준 위치: `.github/docs/`
- agent-owned 산출물 템플릿의 기준 위치: `.github/agents/artifacts/`
- workspace skill discovery registry의 기준 문서: `.github/instructions/skill-index.instructions.md`
- `.agent.md` 작성 규칙의 기준 문서: `.github/instructions/create-agent.instructions.md`
- `SKILL.md` 작성 규칙의 기준 문서: `.github/instructions/create-skills.instructions.md`
- 저장소 전체 운영 요약의 기준 문서: `AGENTS.md`
- memory path 규칙의 기준 문서: `.github/memories/memories.md`

## 수정 순서

1. `AGENTS.md`에서 철학과 담당 구조가 맞는지 먼저 확인한다.
2. `instructions/`에서 공유 규칙의 기준 문서와 skill discovery registry를 맞춘다.
3. `docs/`에서 장문 workflow 문서의 기준 문서를 맞춘다.
4. `agents/`에서는 로컬 contract와 agent-owned artifact template 기준 위치를 함께 정리한다.
5. memory 경로나 workflow 산출물이 바뀌면 `memories/`와 관련 agent 문구를 함께 맞춘다.

## 일치 규칙

- role 이름이나 역할 분담이 바뀌면 `AGENTS.md`, `instructions/subagent-invocation.instructions.md`, 해당 `.agent.md`를 함께 수정한다.
- skill category나 주요 skill registry 구성이 바뀌면 `instructions/skill-index.instructions.md`와 관련 agent/reviewer 문서를 함께 수정한다.
- role index 디렉터리(`coord-roles/`, `reviewer-roles/`)가 추가되거나 role 구성이 바뀌면 해당 index와 기준 agent 문서를 함께 수정한다.
- 관문, 인계, 산출물 수명 주기 표현은 `AGENTS.md`, `instructions/subagent-invocation.instructions.md`, `.agent.md`, `agents/workflows/` 사이에서 서로 충돌하면 안 된다.
- 특히 Planning 인계의 넓은 산출물 묶음과 Execution/Review packet의 task-local artifact isolation은 사람이 읽는 문서와 runtime 문서에서 같은 의미로 설명되어야 한다.
- README, workflow playbook, migration guide 같은 사용자 문서는 규칙을 요약하거나 중복 설명해도 되지만, exact field definition과 completeness 기준의 최종 기준 문서는 `instructions/` 또는 관련 `.agent.md` 한 곳만 남긴다.
- 장문의 workflow 설명은 `docs/`에 두고, agent-owned 산출물 템플릿은 `.github/agents/artifacts/`에 둔다. `instructions/`나 `.agent.md`에 긴 복제본을 남기지 않는다.
- project memory 경로를 참조하는 문구는 `.github/memories/memories.md`와 맞춘다.
- 이 문서에서 create-agent/create-skills의 작성 규칙을 다시 상세히 풀어쓰지 않는다.

## 범위 밖

- 관련 없는 `.github/skills/` 확장
- `.github/commands/` 또는 slash command 추가
- hook automation 도입
- non-`.github/` 문서 정리

다만 agent가 맡던 기능을 skills 쪽으로 옮기는 작업은 예외적으로 이 문서의 직접 수정 대상이 된다.

## 유지보수 점검표

- 한 규칙군에는 상세 기준 문서가 하나만 남는다.
- `AGENTS.md`는 철학과 담당 구조 수준을 넘지 않는다.
- skill discovery의 기준 문서는 `instructions/skill-index.instructions.md`다.
- `instructions/`는 공유 규칙만, `docs/`는 장문 reference만, `agents/`는 로컬 동작과 agent-owned artifact template만 설명한다.
- 사람이 읽는 문서에 독자 친화적 중복 설명은 허용하되, 행동 규칙의 최종 기준 문서는 하나로 고정한다.
- 사람이 읽는 문서가 Planning 단계의 생성된 산출물 묶음, implementation packet의 기본 `artifacts=[]`, review packet의 최소 관련 문서 또는 근거 참조 규칙과 충돌하지 않는다.
- `description`, `tools`, `agents`, `handoffs`, `user-invocable`, `disable-model-invocation`, output contract 같은 섹션 이름은 보수적으로 다룬다.
- 수정 뒤 안내형 인계, 상위 도구 한도, 출력 규약, 책임 경계가 유지되는지 확인한다.
