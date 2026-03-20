---
name: memory-synthesizer
description: "Synthesizes durable user preferences and repository facts into the correct memory scope while avoiding memory pollution. Use this skill after validated work when you need to decide whether something should be saved to persistent memory, repo memory, or skipped. Always consult this skill before writing to memory after a completed task, even if the user only says 'remember this', 'save this', or the session surfaced a useful project convention. Do not use this skill for temporary scratch notes, generic file creation, or one-off session bookkeeping; use normal memory tools . Triggers on: memory tail, remember this, save to memory, durable signal, user preference, project fact, repo memory, personal memory, memory pollution, 기억해, 메모리에 저장, 사용자 선호 저장, 프로젝트 사실 저장, 메모리 테일."
---

# 메모리 합성 가이드

## 목표

validated work 뒤에 나온 durable signal만 올바른 memory scope에 저장하고, 일회성 상태와 노이즈는 과감히 건너뛴다.

이 문서는 빠른 판단용 요약 가이드다. 저장 scope가 애매하거나 적격성 판단이 흔들리면 먼저 `references/decision-rules.md`를 직접 읽고 기준을 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 판단 단계

### 1. 저장 후보를 먼저 좁힌다

모든 회고를 memory로 만들지 않는다. 반복 가치가 있는 user preference, stable project fact, 팀 관례, architecture decision, 검증된 작업 방식만 후보로 본다.

#### 빠른 판단 기준

- 다음 세션이나 다른 task에서도 coding 또는 review 품질을 올릴 수 있으면 후보로 남긴다.
- 현재 task가 끝나면 의미가 사라지는 메모라면 저장하지 않는다.
- 추측, 임시 가정, 해결되지 않은 blocker는 저장하지 않는다.

→ 상세: `references/decision-rules.md`

### 2. memory scope를 먼저 분류한다

무엇을 저장할지보다 어디에 저장할지를 먼저 결정한다.

- user memory: stable user preference, 반복되는 커뮤니케이션 선호, 작업 스타일
- repo memory: stable project fact, convention, verified command, architecture or workflow fact
- session memory: 현재 대화에만 필요한 plan, references, scratch note

#### 빠른 판단 기준

- 사용자의 취향이나 선호면 user memory다.
- 저장소 전체에 재사용될 사실이면 repo memory다.
- 현재 대화가 끝나면 버려도 되는 상태면 session memory거나 skip다.

→ 상세: `references/decision-rules.md`

### 3. durable signal인지 검증한다

signal strength가 약하면 저장보다 skip가 낫다. memory pollution은 missing memory보다 더 비싸다.

#### 빠른 판단 기준

- 이미 코드나 짧은 파일 읽기만으로 항상 추론 가능한 사실이면 저장 우선순위를 낮춘다.
- 현재 patch가 merge되지 않아도 유효한 사실이어야 durable signal로 본다.
- 비밀정보, credential, 민감정보가 섞여 있으면 저장하지 않는다.

→ 상세: `references/decision-rules.md`

### 4. 저장 형식을 맞춘다

scope마다 포맷이 다르다. 특히 repo memory는 JSON 필드가 정확해야 한다.

#### 빠른 판단 기준

- user memory는 짧은 bullet 또는 단일 사실로 쓴다.
- repo memory는 `subject`, `fact`, `citations`, `reason`, `category`를 갖춘 JSON으로 쓴다.
- citations는 나중에 검증 가능한 근거여야 한다.

→ 상세: `references/decision-rules.md`

### 5. 저장 전 중복과 대안을 확인한다

새 메모를 만드는 것이 항상 최선은 아니다. 기존 memory가 이미 더 좋은 표현을 갖고 있으면 추가 저장보다 skip나 업데이트 판단이 낫다.

#### 빠른 판단 기준

- 같은 사실이 이미 더 명확한 wording으로 저장되어 있으면 새로 만들지 않는다.
- current session만 정리하면 충분한 내용이면 durable memory로 올리지 않는다.
- 확신이 낮으면 skip 이유를 남기고 저장하지 않는다.

→ 상세: `references/decision-rules.md`

---

## references 가이드

아래 문서는 실제 저장 결정을 내리기 전에 직접 읽어야 하는 기준 문서다.

| 파일 | 읽을 때 |
| --- | --- |
| `references/decision-rules.md` | scope 분류, skip 기준, repo memory JSON 포맷, 중복 방지 기준이 애매할 때 |
| `../../memories/memories.md` | project-level fact를 어떤 category로 볼지 감이 필요할 때 |

---

## 범위

- 현재 task용 plan, references, scratch 정리 → session memory inline flow
- 단순히 아무 메모나 많이 남기는 작업 → 이 skill의 범위가 아니다

이 skill은 validated work 뒤의 durable signal을 고르는 판단용 skill이다. 저장량보다 저장 품질을 우선한다.
