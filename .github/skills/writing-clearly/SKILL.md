---
name: writing-clearly
description: "Clear, concise, and human-sounding prose for any language and surface. Applies AI-pattern detection and removal (17 EN + 24 KO patterns backed by KatFishNet research), voice injection, and a self-review quality gate. Use this skill when writing, editing, rewriting, or reviewing prose for clarity, concision, naturalness, or humanization, even if the user only says 'make this clearer', 'sounds robotic', 'humanize this', 'too wordy', or 'sounds like AI'. Always consult this skill for prose-quality work regardless of content type or platform. For content structure and format use writing-content. For technical documentation patterns use writing-document. Triggers on: clear writing, concise writing, humanize, AI writing, robotic text, polish prose, rewrite, edit copy, tone, voice, clarity, brevity, AI patterns, 명확하게, 간결하게, 자연스럽게, AI 느낌, 로봇 같은, 다듬어줘, 문장 다듬기, 글 수정, 어색해, 톤, 보이스, 휴머나이징."
---

# 명확하고 자연스러운 글쓰기 (writing-clearly)

## 목표

사람이 읽는 모든 텍스트를 명확하고 간결하고 자연스럽게 만든다. 이 스킬은 콘텐츠 유형(블로그, 소셜, 기술문서)이 아니라 **글의 품질** 자체를 다룬다. 어떤 포맷이든 최종 문장이 인간답고, 군더더기 없고, 목적에 맞게 움직이도록 만드는 것이 이 스킬의 역할이다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 글을 쓰거나 편집할 때는 아래 reference 문서를 직접 읽고 감지 기준, 교정 전략, Before/After 예시를 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 6대 핵심 원칙

### 1. 능동태와 긍정형으로 쓴다

주어가 행동하는 문장이 명확하다. "~되었다"보다 "~했다"가 짧고 강하다. "~하지 않는 것은 아니다" 대신 "~한다"로 쓴다.

- 수동태를 발견하면 주어가 누구인지 먼저 찾고, 그 주어를 문장 앞으로 끌어온다
- 부정형으로 우회하는 문장을 긍정형 직접 서술로 바꾼다
- 시스템 처리("처리되었습니다")보다 사용자의 동작이나 결과("저장했습니다")로 표현한다

#### 빠른 판단 기준

- "~에 의해", "~되었다", "was ~ed by"가 보이면 능동태로 바꿀 수 있는지 먼저 검토한다
- 부정이 두 번 이상 중첩되면("not un-", "~하지 않은 것은 아니다") 반드시 다시 쓴다
- 주어 없이 시작하는 문장이 연속 3개 이상이면 구조를 바꾼다

실제 적용 전에는 [references/composition-principles.md](references/composition-principles.md)를 직접 읽고, 능동태·긍정형 전환의 Before/After 예시를 확인한다.

→ 상세: [references/composition-principles.md](references/composition-principles.md)

### 2. 불필요한 단어를 걷어낸다

모든 단어가 일하게 만든다. 수식하지 않는 수식어, 이미 알려진 정보를 다시 말하는 문장, 습관으로 붙이는 filler를 제거한다.

- "~에 대해서", "~의 경우에는", "~하는 것이 가능하다" 같은 우회구를 직접 표현으로 줄인다
- "매우", "정말", "기본적으로", "essentially" 같은 강화어(intensifier)가 실제로 의미를 바꾸지 않으면 삭제한다
- 한 문장에 하나의 목적만 담는다. 두 가지 목적이 보이면 문장을 나눈다

#### 빠른 판단 기준

- 단어를 삭제해도 의미가 바뀌지 않으면 삭제한다
- 같은 문단 안에 같은 의미를 두 번 말하고 있으면 하나를 지운다
- 접속사("또한", "게다가", "Furthermore", "Moreover")가 연속으로 나오면 논리 흐름으로 대체한다

실제 적용 전에는 [references/composition-principles.md](references/composition-principles.md)를 직접 읽고, 우회구 교체와 강화어 점검의 Before/After 예시를 확인한다.

→ 상세: [references/composition-principles.md](references/composition-principles.md)

### 3. 구체적이고 명확한 언어를 쓴다

막연한 단어 대신 관찰 가능한 행동, 수치, 이름을 쓴다. 독자가 머릿속에 그림을 그릴 수 있어야 한다.

- "다양한 분야"보다 분야 이름을 쓴다. "상당한 개선"보다 수치를 쓴다
- "groundbreaking", "cutting-edge", "혁신적인", "핵심적인" 같은 판촉 형용사를 구체적 근거로 교체한다
- 모호한 대명사("그것", "이것", "it", "this")를 줄이고 지시 대상을 명시한다
- 관련 단어끼리 가까이 둔다. 수식어와 피수식어 사이에 다른 절이 끼지 않게 한다

#### 빠른 판단 기준

- "중요하다", "효과적이다", "crucial", "significant"가 보이면 왜 중요한지, 어떻게 효과적인지를 대신 쓴다
- 형용사 2개 이상이 명사 하나를 수식하면 정말 둘 다 필요한지 확인한다
- 문장 끝에 강조할 단어를 배치한다 — 가장 중요한 정보가 문장 끝에 오면 기억에 남는다

실제 적용 전에는 [references/composition-principles.md](references/composition-principles.md)를 직접 읽고, 판촉 형용사 교체와 관련 단어 배치의 Before/After 예시를 확인한다.

→ 상세: [references/composition-principles.md](references/composition-principles.md)

### 4. AI 패턴을 감지하고 제거한다

LLM이 생성한 글에는 통계적으로 빈번한 패턴이 있다. 영문과 한국어 각각 고유한 AI 흔적이 있으며, 이를 알아야 고칠 수 있다.

영문 17종, 한국어 24종(KatFishNet 논문 기반)의 AI 패턴이 있다. 각 패턴의 감지 기준, 주의 단어 목록, 교정 전략, Before/After 예시는 모두 reference에 있다.

#### 영문 주요 패턴 (17종)

| 카테고리 | 대표 패턴 | 주의 신호 |
|---------|---------|--------|
| 콘텐츠 | 과잉 의미 부여, 표면적 -ing 분석, 판촉 언어 | "pivotal", "stands as a testament", "showcasing", "nestled" |
| 언어·문법 | AI 유행어, copula 회피, 3박자 과용 | "delve", "leverage", "serves as", "fosters" |
| 스타일 | em dash 남용, 굵은 글씨 과다, 이모지 장식 | —, **bold** 남발, 🚀💡✅ |

실제 적용 전에는 [references/ai-patterns-en.md](references/ai-patterns-en.md)를 직접 읽고, 각 패턴의 감지 기준과 교정 전략을 확인한다.

→ 상세: [references/ai-patterns-en.md](references/ai-patterns-en.md)

#### 한국어 주요 패턴 (24종, KatFishNet 논문 기반)

| 카테고리 | 대표 패턴 | 감지 정확도 |
|---------|---------|----------|
| 문장부호 (7종) | 쉼표 과다, 영어식 배치, 연결어미 뒤 쉼표 | 94.88% AUC |
| 띄어쓰기 (3종) | 의존명사·보조용언 경직된 일관성 | 79.51% AUC |
| 품사 다양성 (3종) | 명사 과다, 동사/형용사 빈곤 | 82.99% AUC |
| 어휘 (7종) | AI 유행어, 불필요한 한자어, 복수형 '-들' 과다, 대명사 반복 | 경험적 관찰 |
| 구조 (4종) | 문장 리듬 부족, 3박자 과용, 접속사 과다, 경어체 균일성 | 경험적 관찰 |

실제 적용 전에는 [references/ai-patterns-ko.md](references/ai-patterns-ko.md)를 직접 읽고, 각 패턴의 과학적 감지 기준과 교정 전략을 확인한다.

→ 상세: [references/ai-patterns-ko.md](references/ai-patterns-ko.md)

#### 빠른 판단 기준

- **영문**: "delve", "tapestry", "landscape"(비유적), "crucial", "pivotal"가 보이면 AI 패턴으로 의심한다. em dash가 3개 이상이면 줄인다
- **한국어**: 쉼표가 문장의 40% 이상에 있으면 패턴 1을 의심한다. "혁신적인", "핵심적인", "효과적으로"가 같은 문단에 있으면 패턴 14를 의심한다. '-들'이 수량사와 함께 있으면 패턴 17을 의심한다
- **공통**: 3개짜리 목록이 연속으로 나오면 3박자 과용이다. 모든 문장이 비슷한 길이면 리듬이 없다

### 5. 보이스와 리듬을 살린다

AI 패턴을 제거하는 것만으로는 부족하다. 깨끗하지만 무미건조한 글은 여전히 기계적으로 느껴진다. 목소리와 리듬을 넣어야 사람이 쓴 글이 된다.

- 문장 길이를 의도적으로 변주한다. 짧은 문장. 그리고 때로는 좀 더 길게 풀어서 흐름을 만드는 문장
- 의견, 감정, 불확실성을 적절히 드러낸다. "솔직히 잘 모르겠다"는 "결과는 불분명합니다"보다 인간적이다
- 대상 독자의 보이스가 있다면(브랜드 가이드, 기존 글 예시) 그 톤을 먼저 파악하고 맞춘다
- 격식체 글에서도 한 가지 어투만 고집하지 않는다. 한국어는 -습니다와 -어요를 섞어 리듬을 만들고, 영문은 short punch와 longer flow를 번갈아 쓴다

#### 빠른 판단 기준

- 연속 5문장의 길이가 비슷하면 의도적으로 짧거나 긴 문장을 하나 끼운다
- 모든 문장이 3인칭 서술이면 1인칭이나 질문을 고려한다
- 텍스트에서 필자의 성격이 전혀 느껴지지 않으면 보이스를 추가한다
- 보이스 레퍼런스가 있으면 반드시 먼저 읽고 리듬, 수사 장치, 유머 허용도를 추출한다

실제 적용 전에는 [references/voice-and-rhythm.md](references/voice-and-rhythm.md)를 직접 읽고, 보이스 캡처 워크플로와 리듬 변주 테크닉을 확인한다.

→ 상세: [references/voice-and-rhythm.md](references/voice-and-rhythm.md)

### 6. 셀프 리뷰 게이트를 통과한다

글을 완성하기 전에 아래 체크리스트를 통과한다. 하나라도 실패하면 해당 원칙으로 돌아가서 수정한다.

#### 최종 체크리스트

| # | 점검 항목 | 관련 원칙 |
|---|---------|---------|
| 1 | 수동태가 3문장 이상 연속하지 않는다 | 원칙 1 |
| 2 | 부정이 2중 이상 중첩된 문장이 없다 | 원칙 1 |
| 3 | 삭제해도 의미가 바뀌지 않는 단어가 없다 | 원칙 2 |
| 4 | 같은 문단에서 같은 내용을 두 번 말하지 않는다 | 원칙 2 |
| 5 | "중요한", "효과적인", "crucial", "pivotal" 같은 판촉 수식어가 구체적 근거 없이 쓰이지 않는다 | 원칙 3 |
| 6 | AI 유행어 목록(영문·한국어)에 해당하는 단어가 근거 없이 남아 있지 않다 | 원칙 4 |
| 7 | 연속 5문장의 길이가 모두 비슷하지 않다 | 원칙 5 |
| 8 | 글 전체에서 필자의 목소리나 톤이 느껴진다 | 원칙 5 |
| 9 | 사실적 주장에 출처나 근거가 있다 | 전체 |
| 10 | 대상 독자의 톤·격식 수준에 맞는다 | 전체 |

#### 언어별 추가 점검

**영문 추가**:
- em dash가 한 문단에 2개를 넘지 않는다
- "delve", "tapestry", "landscape"(비유적), "foster", "leverage" 등 AI 유행어가 남아 있지 않다
- 볼드체가 강조가 아닌 장식에 쓰이지 않는다

**한국어 추가**:
- 쉼표가 문장의 40% 이상에서 사용되지 않는다
- 연결어미(-고, -어서, -지만) 뒤에 불필요한 쉼표가 없다
- '-들'이 수량사나 수식어와 중복되지 않는다
- "해당"이 같은 문단에 2번 이상 반복되지 않는다
- 문장 어미가 한 가지(-습니다 또는 -다)로만 유지되지 않는다

---

## 작업 흐름

### 새 글을 쓸 때

1. [references/composition-principles.md](references/composition-principles.md)를 읽고 대상 독자와 톤을 정한다 (보이스 가이드가 있으면 [references/voice-and-rhythm.md](references/voice-and-rhythm.md)도 함께 읽는다)
2. 원칙 1–3을 적용하며 초안을 쓴다
3. 해당 언어의 AI 패턴 reference를 읽고, 원칙 4로 스캔·교정한다
4. 원칙 5로 리듬과 보이스를 입힌다
5. 원칙 6 체크리스트를 통과시킨다

### 기존 글을 편집할 때

1. 해당 언어의 AI 패턴 reference를 읽고, 원칙 4를 먼저 돌려 AI 패턴 유무를 확인·교정한다
2. [references/composition-principles.md](references/composition-principles.md)를 읽고, 원칙 1–3으로 구조적 문제를 잡는다
3. 원칙 5로 리듬과 보이스가 있는지 확인한다
4. 원칙 6 체크리스트를 통과시킨다

### 휴머나이징(AI 텍스트 자연스럽게 만들기)

1. 텍스트 언어를 확인하고, 해당 언어의 AI 패턴 reference를 읽는다 (영문: ai-patterns-en.md / 한국어: ai-patterns-ko.md)
2. [references/voice-and-rhythm.md](references/voice-and-rhythm.md)를 읽는다
3. 원칙 4를 중심으로 AI 패턴을 체계적으로 감지하고 교정한다
4. 원칙 5로 성격과 리듬을 주입한다
5. 원칙 6의 언어별 추가 점검을 통과시킨다
6. 원래 의미와 사실 정보를 보존했는지 최종 확인한다

---

## 이 스킬이 다루지 않는 범위

| 작업 | 사용할 스킬 |
|-----|----------|
| 콘텐츠 타입별 구조·포맷(블로그, 소셜, 뉴스레터) | writing-content |
| 기술문서 패턴(API 레퍼런스, 체인지로그, README) | writing-document |
| 콘텐츠 소스 리서치·정보 수집 | research-content-source |
| 테크니컬 SEO | seo-technical |
| 콘텐츠 SEO 최적화 | seo-content |
| UX 라이팅, CTA 문구, 에러 문구 | ds-product-ux |

---

## Reference 파일

| 파일 | 내용 | 언제 읽는가 |
|-----|-----|----------|
| [references/composition-principles.md](references/composition-principles.md) | 능동태, 긍정형, 간결성, 구체성, 위치 규칙 상세 + Before/After 예시 | 원칙 1–3을 적용할 때 |
| [references/ai-patterns-en.md](references/ai-patterns-en.md) | 영문 AI 패턴 17종: 감지 기준, 주의 단어 목록, 교정 전략, Before/After 예시 | 영문 텍스트의 AI 패턴을 감지·교정할 때 |
| [references/ai-patterns-ko.md](references/ai-patterns-ko.md) | 한국어 AI 패턴 24종: 과학적 감지 기준, 교정 전략, Before/After 예시 (5개 카테고리 전체) | 한국어 텍스트의 AI 패턴을 감지·교정할 때 |
| [references/voice-and-rhythm.md](references/voice-and-rhythm.md) | 보이스 캡처 워크플로, 성격 주입 전략, 문장 리듬 변주법 | 원칙 5를 적용할 때, 특히 보이스 레퍼런스가 있을 때 |
