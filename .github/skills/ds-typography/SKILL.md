---
name: ds-typography
description: "Typography decision patterns for product UI and web surfaces: context-first font choice, font pairing, type scale, weight hierarchy, line-height, letter-spacing, line length, responsive type, variable font usage, and typography quality review. Use this skill when choosing fonts, setting a type scale, deciding whether one font is enough, tightening tracking, tuning Korean or multilingual headings, or polishing text hierarchy in a UI. Always consult this skill for typography decisions that affect tone, readability, density, or perceived polish, even if the user only asks to pick a font, fix text spacing, make the UI feel premium, or clean up hierarchy. For broader visual systems use ds-visual-design. For layout composition use ds-ui-patterns. For Tailwind v4 implementation mechanics use fe-tailwindcss. Triggers on: typography, font pairing, type scale, line-height, letter-spacing, tracking, line length, variable font, text hierarchy, font weight, responsive typography, multilingual type, premium typography, 타이포그래피, 폰트 조합, 폰트 스케일, 줄간격, 자간, 트래킹, 줄 길이, 가변 폰트, 텍스트 계층, 폰트 두께, 반응형 타이포그래피, 멀티링구얼 타이포."
---

# 타이포그래피 시스템 (ds-typography)

## 목표

UI와 웹 surface의 텍스트가 tone, hierarchy, reading comfort를 동시에 만족하도록 typography decision을 구조화한다. 이 스킬은 폰트 자체보다도, 어떤 맥락에서 어떤 서체를 고르고 어떻게 계층과 리듬을 세울지 판단하는 전용 owner다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 폰트를 고르거나 scale, leading, tracking을 결정하기 전에는 아래 reference 문서를 직접 읽고 상황에 맞는 기준을 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 패턴

### 1. 먼저 텍스트의 job과 reading context를 고정한다

좋은 타이포그래피는 폰트 브라우징으로 시작하지 않는다. 먼저 이 텍스트가 잠깐 시선을 잡아야 하는지, 오래 읽혀야 하는지부터 정해야 한다.

- 헤드라인, CTA, 배지, 내비게이션처럼 짧게 강한 인상을 주는 텍스트와
- 본문, 문서, 설명, 테이블처럼 오래 읽혀야 하는 텍스트를 분리해서 본다
- work tool인지 marketing surface인지에 따라 neutral default와 personality 허용 범위가 달라진다
- long reading인지 rapid scanning인지에 따라 line-height, measure, density가 달라진다

#### 빠른 판단 기준

- 목적이 애매하면 폰트 후보를 늘리기 전에 텍스트의 역할부터 다시 나눈다
- product UI인데 시각적 개성만 보고 과한 서체를 고르고 있다면 neutral default를 먼저 검토한다
- reading context가 긴데도 headline logic로 leading과 measure를 잡고 있으면 다시 설계한다

→ 상세: [references/01-reading-and-selection.md](references/01-reading-and-selection.md)

### 2. 폰트 선택은 one-font rule과 anchor font에서 시작한다

대부분의 product UI는 한 패밀리로 충분하다. 두 번째 폰트는 명확한 역할 차이와 art direction이 있을 때만 추가한다.

- 기본값은 one font + multiple weights다
- personality가 중요한 surface에서는 anchor font를 먼저 정하고 body font를 붙인다
- 두 폰트를 조합할 때는 구조적 대비가 보여야 한다
- 너무 비슷한 두 서체는 pairing이 아니라 accidental mismatch다
- 커스텀 폰트는 aesthetic choice이기 전에 licensing choice다

#### 빠른 판단 기준

- 두 번째 폰트를 쓰는 이유를 한 문장으로 설명할 수 없으면 하나로 줄인다
- headline font와 body font가 너무 비슷하면 둘 중 하나를 없애거나 대비를 키운다
- product app인데 매 화면마다 font personality가 달라 보이면 one-font rule로 되돌린다

→ 상세: [references/02-pairing-and-scale.md](references/02-pairing-and-scale.md)

### 3. scale, weight, color hierarchy는 제한된 system으로 만든다

좋은 hierarchy는 큰 글자 몇 개를 눈대중으로 섞는 것이 아니라, 제한된 단계와 역할을 반복하는 시스템에서 나온다.

- scale ratio를 하나 고르고 일관되게 쓴다
- 일반적으로 6~8개 이내의 text size면 충분하다
- 기본 weight 조합은 보통 400, 500, 600으로 시작한다
- heavier weights는 deliberate visual exception으로만 사용한다
- text hierarchy는 size뿐 아니라 weight와 opacity로 나눈다

#### 빠른 판단 기준

- 숫자마다 다른 font size를 쓰고 있으면 먼저 ratio와 token으로 정리한다
- 700 이상 weight가 자주 보이면 실제로 필요한 강조인지 다시 본다
- hierarchy를 크기 하나로만 만들고 있다면 weight와 text color level을 같이 조정한다

→ 상세: [references/02-pairing-and-scale.md](references/02-pairing-and-scale.md)
→ 상세: [references/03-hierarchy-and-tracking.md](references/03-hierarchy-and-tracking.md)

### 4. line-height, tracking, line length가 읽기 리듬을 만든다

텍스트가 편하게 읽히는지, 정제되어 보이는지는 폰트 이름보다 leading, measure, tracking에 더 크게 좌우된다.

- body text는 보통 1.5~1.7 leading과 50~75자 measure를 기본으로 본다
- headline은 body보다 타이트할 수 있지만 script와 line count를 같이 봐야 한다
- small text와 ALL CAPS는 positive tracking이 사실상 필수다
- 큰 Latin heading은 약한 negative tracking이 유효할 수 있다
- Korean과 non-Latin heading은 기본 tracking을 유지하고 미세 조정만 한다

#### 빠른 판단 기준

- 작은 텍스트가 답답한데 tracking이 0이면 먼저 tracking을 본다
- ALL CAPS가 많은데 tracking을 안 줬다면 polishing이 덜 된 상태로 본다
- desktop 문단이 너무 넓어 보이면 font size를 건드리기 전에 measure를 줄인다

→ 상세: [references/03-hierarchy-and-tracking.md](references/03-hierarchy-and-tracking.md)

### 5. responsive type와 variable font는 effect가 아니라 decision layer다

반응형 타이포그래피와 variable font는 나중에 붙이는 효과가 아니라, scale과 hierarchy를 다른 화면에서도 유지하기 위한 decision layer다.

- breakpoint jump보다 clamp 기반의 smooth scaling을 우선 검토한다
- variable font는 표현과 번들 이점을 동시에 줄 때 가치가 크다
- token으로 굳히지 않은 typography는 implementation 단계에서 흔들리기 쉽다
- Tailwind v4에서는 typography 결정을 token과 `@theme`로 연결한다

#### 빠른 판단 기준

- 모바일과 데스크톱의 text scale이 완전히 단절돼 있으면 clamp나 bounded scaling을 검토한다
- variable font를 쓰는데 실제로 axis control을 거의 안 쓴다면 static weights가 더 나을 수 있다
- font pairing, scale, leading이 아직 안 정해졌는데 utility class부터 쓰고 있으면 순서를 거꾸로 탄 것이다

→ 상세: [references/04-responsive-and-tokens.md](references/04-responsive-and-tokens.md)

### 6. shipping 전에 readable인지 evaluation한다

좋은 typography는 taste만으로 고르지 않는다. 구조적 품질, glyph coverage, 실제 콘텐츠 테스트, 문자권 대응까지 확인해야 한다.

- legibility와 readability를 구분해서 본다
- x-height, counter, aperture, stroke contrast, Il1/O0 구분을 확인한다
- real content와 real size로 테스트한다
- multilingual product는 target language 문자열로 직접 확인한다
- licensing과 shipping risk를 마지막이 아니라 초기에 본다

#### 빠른 판단 기준

- specimen이 예쁜데 14~16px에서 무너지면 body candidate에서 제외한다
- Latin에서는 괜찮아 보여도 한글이나 숫자, 특수문자에서 무너지면 다시 본다
- 폰트가 좋아 보여도 실제 content block이 uneven gray로 보이면 structure가 약한 것이다

→ 상세: [references/05-evaluation-and-checklist.md](references/05-evaluation-and-checklist.md)

---

## references/ 가이드

아래 문서는 실제 타이포그래피 결정을 내리기 전 직접 읽어야 하는 상세 가이드다.

| 파일 | 읽을 때 |
| --- | --- |
| [references/01-reading-and-selection.md](references/01-reading-and-selection.md) | reading model, context-first 질문, type-for-a-moment vs type-to-live-with를 정할 때 |
| [references/02-pairing-and-scale.md](references/02-pairing-and-scale.md) | anchor font, one-font rule, pairing, type scale, safe defaults를 결정할 때 |
| [references/03-hierarchy-and-tracking.md](references/03-hierarchy-and-tracking.md) | weight hierarchy, text color hierarchy, line-height, tracking, line length, vertical rhythm을 조정할 때 |
| [references/04-responsive-and-tokens.md](references/04-responsive-and-tokens.md) | clamp, responsive type, variable font, Tailwind v4 token bridge를 잡을 때 |
| [references/05-evaluation-and-checklist.md](references/05-evaluation-and-checklist.md) | typeface evaluation, multilingual checks, shipping checklist, anti-pattern을 점검할 때 |

### 추천 로드 순서

- 폰트 선택부터 시작: `01 → 02 → 05`
- hierarchy polish: `03 → 05`
- responsive typography: `02 → 04 → 05`
- multilingual heading 조정: `01 → 03 → 05`

---

## 범위

- 전체 visual system의 color, spacing, depth, icon balance → `ds-visual-design`
- 레이아웃, section rhythm, dashboard/landing composition → `ds-ui-patterns`
- shipped product references 조사와 pattern extraction → `refero-design`
- Tailwind v4 utility mechanics, class composition, `@utility`, `cva` → `fe-tailwindcss`
- webfont loading, `@font-face`, preload, subsetting, font budget, CSS implementation deep dive → `web-typography`
