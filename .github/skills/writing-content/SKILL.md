---
name: writing-content
description: "Methods for drafting and structuring audience-facing content: social posts, blog posts, and articles. Use this skill when the user asks to write, outline, structure, repurpose, or polish drafts for LinkedIn, X, blogs, or thought-leadership pieces. Always consult this skill for decisions about hook, angle, structure, pacing, and CTA in publishable content, even if the user only says 'write a post', 'make this into a blog', or 'draft something for LinkedIn'. For sentence-level clarity or AI-pattern removal use writing-clearly. For product docs use writing-document. For SEO optimization use seo-content. Triggers on: social post, LinkedIn post, X thread, blog post, article, content draft, repurpose, thought leadership, 콘텐츠 작성, 소셜 글, 블로그 글, 아티클, 글 구조, 초안, 발행용 글."
disable-model-invocation: false
user-invocable: false
---

# 콘텐츠 작성 방법론 (writing-content)

## 목표

소셜 포스트, 블로그 포스트, 아티클 같은 대외 발행용 콘텐츠를 채널과 독자에 맞는 구조로 빠르게 설계하고 작성한다. 이 스킬의 중심은 문장을 예쁘게 다듬는 일이 아니라, 어떤 관점으로 시작하고 어떤 형식으로 전개하며 어디서 멈춰야 독자가 끝까지 읽는지를 판단하는 데 있다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 콘텐츠를 쓰기 전에는 공통 작성 원칙을 먼저 읽고, 그다음 현재 요청이 소셜인지 블로그인지 아티클인지에 맞는 포스트 타입 가이드를 추가로 읽은 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 6대 핵심 원칙

### 1. 목적과 독자를 먼저 고정한다

좋은 콘텐츠는 문장력보다 방향이 먼저 맞아야 한다. 같은 주제라도 독자가 누구인지, 읽은 뒤 무엇을 하길 원하는지에 따라 첫 문장과 전개 구조가 달라진다.

- 글을 시작하기 전에 독자, 채널, 목표 행동을 먼저 정한다
- 정보 전달, 관점 제시, 전환 유도, 관계 형성 중 무엇이 우선인지 분리한다
- 입력 정보가 부족하면 사실을 지어내지 말고 필요한 가정과 빈칸을 드러낸다

#### 빠른 판단 기준

- 이 글이 누구를 위한 글인지 한 문장으로 말할 수 없으면 쓰기 전에 정리한다
- 읽고 난 뒤 독자가 취할 행동이 흐리면 CTA보다 목적부터 다시 잡는다
- 사실 근거나 사례가 없는데 단정적으로 쓰고 있다면 조사 스킬이나 추가 입력이 필요하다고 본다

→ 상세: [references/01-common-content-guidance.md](references/01-common-content-guidance.md)

### 2. 채널에 맞는 형식을 먼저 고른다

LinkedIn 포스트, X 쓰레드, 블로그 포스트, 아티클은 읽히는 방식이 다르다. 같은 내용을 그대로 복붙하면 길이, 리듬, 단락 구조, 기대치가 어긋난다.

- 소셜은 첫 줄과 스캔성이 우선이다
- 블로그는 검색 유입과 체류를 고려해 섹션 구조가 분명해야 한다
- 아티클은 관점, 근거, 맥락의 밀도가 더 높아야 한다
- 하나의 원고를 여러 채널로 옮길 때는 길이만 줄이지 말고 형식을 다시 설계한다

#### 빠른 판단 기준

- 첫 두 문단을 읽기 전에 글 형식을 구분할 수 없다면 구조가 모호한 상태다
- 블로그인데 소셜처럼 단문 훅만 이어지면 정보 밀도가 부족하다
- 소셜인데 설명 문단이 길게 이어지면 스캔성이 무너진다

→ 상세: [references/02-social-posts.md](references/02-social-posts.md), [references/03-blog-posts.md](references/03-blog-posts.md), [references/04-articles.md](references/04-articles.md)

### 3. 도입부는 주제가 아니라 약속으로 시작한다

독자는 친절한 배경 설명보다 지금 읽을 이유를 먼저 찾는다. 도입부는 “무슨 글인가”보다 “읽으면 무엇을 얻는가”를 먼저 보여줘야 한다.

- 첫 문장은 사실, 긴장, 반전, 질문, 결과 중 하나로 시작한다
- 배경 설명은 독자가 계속 읽을 이유를 만든 뒤에 붙인다
- 제목과 첫 문장은 서로 다른 역할을 갖게 한다. 제목은 범위를, 도입부는 당기는 힘을 맡는다

#### 빠른 판단 기준

- 첫 줄이 일반론이나 업계 클리셰로 시작하면 다시 쓴다
- 도입부를 지웠을 때 글의 가치가 줄지 않으면 도입부가 비어 있는 상태다
- “왜 지금 이 글을 읽어야 하는가”가 첫 화면 안에 없으면 훅이 약하다

→ 상세: [references/01-common-content-guidance.md](references/01-common-content-guidance.md)

### 4. 주장 대신 근거와 사례로 전개한다

읽히는 콘텐츠는 추상적 의견보다 장면, 사례, 데이터, 관찰에서 힘이 나온다. 근거가 없는 확신은 금방 비어 보인다.

- 섹션마다 하나의 주장과 그것을 받치는 사례나 근거를 짝지어 둔다
- 실측 데이터, 실제 경험, 구체적 비교, 관찰 가능한 결과를 우선한다
- 근거가 부족하면 단정형 문장 대신 관찰형, 제안형, 아웃라인형으로 낮춘다

#### 빠른 판단 기준

- 큰 주장 뒤에 바로 예시나 증거가 붙지 않으면 설득력이 약하다고 본다
- 똑같은 형용사만 반복되고 장면이나 숫자가 없으면 밀도가 부족하다
- 출처가 필요한 내용인데 출처나 맥락이 빠져 있으면 발행 전 보완이 필요하다

→ 상세: [references/01-common-content-guidance.md](references/01-common-content-guidance.md)

### 5. 보이스는 화려함보다 일관성이 중요하다

좋은 보이스는 문장을 과장하는 기술이 아니라, 한 글 안에서 같은 사람이 말하는 것처럼 느껴지게 하는 일이다. 톤은 채널과 독자에 맞춰 달라질 수 있지만 리듬과 태도는 일관되어야 한다.

- 전문가처럼 쓰려 하지 말고, 현재 역할에 맞는 거리감을 유지한다
- 창업자, 실무자, 브랜드, 에디터 중 어떤 화자를 전제하는지 먼저 정한다
- 재치, 단정, 겸손, 직설의 비율을 섞더라도 한 글 안에서는 흔들리지 않게 한다

#### 빠른 판단 기준

- 문단마다 화자가 바뀐 것처럼 느껴지면 톤이 불안정하다
- 보이스를 만들기 위해 과장된 단어와 감탄을 덧붙이고 있다면 줄인다
- 개인 경험을 쓰는 글인데 지나치게 중립적이면 거리감이 멀어진 상태다

→ 상세: [references/01-common-content-guidance.md](references/01-common-content-guidance.md)

### 6. 발행 전에는 읽힘과 다음 행동을 같이 점검한다

초안이 완성됐다고 바로 발행 가능한 것은 아니다. 독자가 훑어 읽을 수 있는지, 마지막에 무엇을 해야 하는지, 불필요한 문단이 남아 있지 않은지까지 확인해야 한다.

- 제목, 첫 줄, 소제목, 마무리 CTA를 따로 떼어 읽어 본다
- 한 번에 스캔 가능한 길이와 단락 밀도로 조정한다
- 목적이 전환이 아니더라도 저장, 공유, 댓글, 문의 같은 다음 행동을 열어 둔다
- 채널별 금지 요소와 마감 전 체크리스트를 따로 확인한다

#### 빠른 판단 기준

- 굵은 구조만 읽어도 글 흐름이 보이지 않으면 재편집한다
- 마지막 문단이 요약만 하고 끝나면 다음 행동이 닫혀 있다
- 채널에 맞지 않는 길이, 링크 위치, 문단 밀도가 보이면 발행 전에 다시 맞춘다

→ 상세: [references/01-common-content-guidance.md](references/01-common-content-guidance.md), [references/02-social-posts.md](references/02-social-posts.md), [references/03-blog-posts.md](references/03-blog-posts.md), [references/04-articles.md](references/04-articles.md)

---

## references/ 가이드

아래 문서는 실제 작성 전에 읽어야 하는 작업 가이드다. 이 스킬 본문은 방향을 잡는 용도고, 공통 원칙과 포스트 타입별 디테일은 references에서 확인한다.

| 파일 | 읽을 때 |
| --- | --- |
| [references/01-common-content-guidance.md](references/01-common-content-guidance.md) | 공통 원칙, 보이스, 근거, 마무리 기준 + 섹션 8 (보이스 캡처 워크플로), 섹션 9 (콘텐츠 리패키징 시스템) |
| [references/02-social-posts.md](references/02-social-posts.md) | LinkedIn, X, founder post + Hook Formulas (4 가지 유형) |
| [references/03-blog-posts.md](references/03-blog-posts.md) | 설명형, 교육형, 비교형 블로그 포스트 |
| [references/04-articles.md](references/04-articles.md) | 관점형, 해설형 아티클 + 섹션 10 (유형별 구조 템플릿) |

### 추천 로드 순서

- 소셜 포스트 작성: `01 → 02`
- 블로그 초안 작성: `01 → 03`
- 아티클 아웃라인 작성: `01 → 04`
- 기존 글 리패키징: `01 (섹션 9) → 대상 포스트 타입 가이드`
- 보이스 정립이 필요한 경우: `01 (섹션 8)`

---

## 범위

- 문장 단위 명료화, 군더더기 제거, AI 말투 제거 → `writing-clearly`, `humanizer`, `korean-humanizer` 계열
- README, changelog, release notes, API reference 같은 제품/기술 문서 → `writing-document`, `writing-readme`, `write-api-reference`, `product-changelog` 계열
- 사실 검증, 자료 수집, 출처 조사, 최신 사례 확인 → `research-content-source`, `documentation-lookup`, `research-foundation` 계열
- 키워드 전략, 검색 의도 최적화, SERP 중심 구조화 → `seo-content`, `seo-technical` 계열

이 스킬은 콘텐츠를 더 잘 쓰기 위한 구조와 형식의 판단을 담당한다. 문장 교정, 조사, 기술문서화, SEO 최적화까지 한 스킬에 넣지 않는다.