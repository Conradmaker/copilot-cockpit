---
description: "Voice and tone rules. Distinguishes user-facing web product copy (friendly 해요체) from agent conversation tone (합니다체). Internal agent docs keep their own 평서체."
applyTo: "**"
---

# Voice & Tone

상황별로 한국어 보이스톤을 분리한다. 내부 문서 톤(평서체 "~다/~한다")이 사용자 화면이나 대화로 누수되지 않게 한다.

## 1. 웹 프로덕트 카피 (사용자 노출 텍스트)

대상: `*.tsx`, `*.jsx`, `*.html`, `*.mdx` 안의 UI 문자열, 버튼 라벨, 안내 문구, 에러/빈 상태, 마케팅 카피, 메타데이터.

규칙:
- 기본은 친절한 **해요체** or **합니다체** 를 사용한다. ("저장했어요", "다시 시도해 주세요", "아직 결과가 없어요", "결제가 완료되었습니다", "오류가 발생했습니다")
- 결제·보안·법적 고지처럼 신뢰가 중요한 문맥은 정중한 **합니다체**를 사용한다. ("결제가 완료되었습니다")
- 음슴체("~다", "~한다", "~이다") 금지. 명사 종결("저장 완료") 남용 금지.
- 한 화면 안에서 종결어미 톤을 섞지 않는다. (단, 제목과 같은 헤드라인의 카피라이팅은 별도의 톤을 허용할 수 있다.)
- AI 흔적 제거: 불필요한 부사("정말, 매우, 단순히"), 과장된 약속, 영어식 수동태 피하기.

참고 스킬과 reference:
- `.github/skills/writing-clearly/SKILL.md` — AI 패턴 제거, 자연스러운 한글
  - `references/ai-patterns-ko.md` — 한국어 AI 패턴 24종
  - `references/ai-patterns-en.md` — 영어 AI 패턴 17종
  - `references/voice-and-rhythm.md` — 보이스·리듬
  - `references/composition-principles.md` — 문장 구성 원칙
- `.github/skills/ds-product-ux/SKILL.md` — CTA, 에러, 빈 상태 UX 라이팅
  - `references/02-ux-writing.md` — UX 라이팅 규칙
  - `references/01-action-patterns.md` — CTA·액션 패턴
  - `references/03-loading-feedback.md` — 로딩·피드백 카피
  - `references/10-common-ux-mistakes.md` — 흔한 UX 실수
- `.github/skills/writing-content/SKILL.md` — 마케팅·블로그 카피 구조
  - `references/01-common-content-guidance.md` — 공통 가이드
  - `references/02-social-posts.md` / `03-blog-posts.md` / `04-articles.md` — 포맷별 구조

## 2. 사용자와의 대화 (Copilot 응답)

대상: 사용자에게 직접 답변하는 모든 채팅 메시지.

규칙:
- 기본은 **합니다체**. ("확인했습니다", "수정하겠습니다", "원인은 ~입니다")
- 간결하게. 불필요한 서론·결론 생략.
- 음슴체로 답하지 않는다. 반말 금지.
- 코드·파일 경로·심볼명은 백틱 또는 링크.

참고 스킬과 reference:
- `.github/skills/writing-clearly/SKILL.md` — 명료성, AI 톤 제거
  - `references/ai-patterns-ko.md` — 한국어 AI 패턴 체크리스트
  - `references/voice-and-rhythm.md` — 보이스·리듬

## 3. 내부 에이전트 문서 (예외)

대상: `AGENTS.md`, `.github/**` (instructions, skills, agents, prompts 등), `*.agent.md`, `SKILL.md`.

규칙:
- 기본은 **평서체("~다/~한다")** 유지. 이 톤은 워크스페이스 컨텍스트 전용이며, 위 1·2번으로 누수되지 않게 한다.
- **AI가 가장 정확히 해석할 수 있는 한국어**로 작성한다. 사용자가 읽을 수는 있어야 하지만, 우선순위는 모델 해석 정확도다.
  - 핵심 용어·개념·고유명사는 영어 원문 유지 (예: `subagent`, `packet`, `task_packet`, `applyTo`, `frontmatter`, `MCP`).
  - 모호한 의역·은유·관용 표현 금지. 한 단어가 한 개념을 가리키도록 일관 유지.
  - 조건·예외·금지 사항은 bullet로 분리. 중첩 문장으로 묶지 않는다.
  - 능동·현재형 단정문. "~할 수도 있다", "~인 것 같다" 같은 hedging 금지.
  - 코드·경로·심볼·파일명은 항상 백틱.
