# Bundled Reference Pack

## 상태

- deferred after Dynamic skill activation and Commander playbook
- 현재 하네스에는 `references/` 관례는 있으나 progressive disclosure 표준은 약하다

## 문제

복합 skill과 orchestration 문서는 쉽게 비대해진다.

- SKILL.md 본문이 selection guide, workflow, examples, long reference를 모두 들고 있어 비대해지기 쉽다
- 어떤 reference를 언제 읽어야 하는지 명시적 로딩 규칙이 약하다
- 같은 reference가 여러 skill에 중복으로 복사되기 쉽다
- 긴 본문은 trigger quality와 reading cost를 함께 떨어뜨린다

## 왜 지금은 후순위인가

현재 가장 큰 품질 문제는 execution handoff ambiguity다.
bundled reference pack은 문서 품질과 확장성에는 중요하지만, immediate execution failure의 1순위 원인은 아니다.

## 참고 앵커

- claw-code `src/skills/bundledSkills.ts`
- 핵심 아이디어: skill 본문은 selection and workflow를 유지하고, reference resource는 lazy하게 availability를 연다

## 옵션

### Option A. everything in SKILL.md

- 장점: 파일 수가 적다
- 단점: context cost가 커지고 maintenance가 나빠진다
- verdict: reject

### Option B. references/ 분리 + loading rule

- SKILL.md는 selection guide와 loading rule만 들고, 긴 자료는 references/로 보낸다
- 장점: 현재 하네스 도구 ceiling에 맞고 progressive disclosure를 바로 얻을 수 있다
- 단점: reference navigation 품질이 나쁘면 오히려 찾기 어렵다
- verdict: recommended

### Option C. runtime extraction

- 비교 저장소와 가장 유사하지만, 현재 하네스에는 runtime support가 없다
- verdict: defer

## 권장 방안

1. SKILL.md는 아래 역할만 우선 보존한다.
	- 언제 읽을지
	- 어떤 판단을 내릴지
	- 어떤 순서로 진행할지
2. 긴 예시, 체크리스트, 비교표, 템플릿은 `references/`로 이동한다.
3. SKILL.md 초반에 `references 가이드` 또는 `추천 로드 순서`를 둔다.
4. reference는 언제 읽는지 trigger를 한 줄로 설명한다.

## Pilot 후보

- `.github/skills/kick-research/SKILL.md`
- 이유: orchestration 성격이 강하고, broad workflow + lane guidance + examples + references를 가장 잘 분리할 수 있다

## 설계 초안

### Skill body가 가져야 할 것

- goal
- workflow
- stop rule
- references guide
- output contract

### references/로 내려야 할 것

- 긴 예시
- detailed checklist
- domain별 variant guidance
- 비교표
- reusable template

## Guardrails

- reference 분리는 navigation clarity를 해치지 않아야 한다
- SKILL.md를 짧게 만드는 것이 목적이지, 찾기 어렵게 쪼개는 것이 목적이 아니다
- pilot 단계에서는 1개 skill만 먼저 바꾸고, pattern이 안정화된 뒤 확장한다

## 선행 조건

- Dynamic skill activation 1차 반영 완료
- Commander playbook 1차 반영 완료

## 다음 구현 후보

1. pilot skill 선정 확정
2. body vs reference cut line 정의
3. references guide 문구 템플릿 만들기
4. pilot 전후 context size와 navigability 비교

## 검증

- pilot skill에서 SKILL.md 본문 길이가 줄어도 decision quality가 유지되는지 확인
- references guide만 읽고도 다음 read target을 빠르게 고를 수 있는지 확인
- duplicate content가 줄었는지 확인
