# Web Image Prompt Template

웹 개발에 쓰이는 에셋을 AI 이미지 생성 툴(Midjourney, Firefly, DALL-E 3, Flux 등)로
AI 느낌 없이 고퀄리티로 뽑아내기 위한 프롬프트 구조 템플릿.

이 문서는 Painter가 prompt를 조립할 때 읽는 primary reference다.
Designer는 image requirement에 최소 필드만 남긴다: `asset_id`, `output_path`, `placement`, `ratio`.
Painter는 그 최소 필드와 `design.md` 전체 tone and manner를 함께 읽고 실제 prompt를 확장한다.

---

## Painter Defaults

Designer가 최소 필드만 남겼고 추가 cue가 없을 때 Painter는 아래 기본값을 우선 검토한다.

| placement cue | default style | default background | default ratio |
|---|---|---|---|
| hero / landing / primary hero | `3D Abstract` 또는 `Stylized CGI` | `minimal clean background` 또는 `dark background` | `16:9` |
| article cover / campaign cover / editorial | `Editorial Illustration` | `minimal clean background` | `16:9` |
| onboarding / empty state / support visual | `Flat Illustration` | `white background, isolated subject` 또는 `transparent background` | `1:1` |
| background / decorative plate | `3D Abstract` | `dark background` 또는 `minimal clean background` | `16:9` |

사용자 prompt가 더 구체적이면 위 default보다 prompt를 우선한다.

---

## 7-Layer Framework

모든 프롬프트는 아래 7개 레이어로 구성된다. ①②③⑦은 필수, 나머지는 권장.

```
[① STYLE ANCHOR], [② SUBJECT], [③ COLOR PALETTE],
[④ LIGHTING & MOOD], [⑤ TEXTURE & FINISH],
[⑥ TECHNICAL SPECS]
--no [⑦ NEGATIVE PROMPT]
```

---

### ① STYLE ANCHOR `필수`

**역할:** AI 기본값(과포화, 미드저니 느낌)을 덮어쓰는 핵심 레이어.
구체적인 매체명·아트 무브먼트를 명시한다.

**패턴:** `[medium] style, [reference aesthetic]`

| 스타일 | Style Anchor 예시 |
|---|---|
| Flat Illustration | `flat vector illustration, minimalist line art style, Monocle magazine aesthetic` |
| Editorial | `editorial illustration, risograph print style, NYT magazine aesthetic` |
| 3D Abstract | `high-end 3D render, CGI artwork, Octane render quality` |
| Stylized CGI | `stylized photography, high-end commercial CGI, shot on Hasselblad` |

---

### ② SUBJECT `필수`

**역할:** 무엇을 그릴지 명확하게 지정. 캐릭터 수·동작·구도를 함께 기술.

**패턴:** `[캐릭터/오브젝트 묘사], [동작/상태], [구도 or 시점]`

**예시:**
- `a young woman running joyfully, long flowing black hair, dynamic side-view pose, single subject`
- `floating glossy spheres and geometric shapes, various sizes scattered in space, frosted glass panel in center`
- `a man and woman jogging together in a city park, both wearing black athletic wear, side view running pose`

---

### ③ COLOR PALETTE `필수`

**역할:** 일관성 확보의 핵심. HEX 코드까지 지정하면 시리즈 작업 시 색상이 고정된다.
최대 3~4색으로 제한할수록 AI 느낌이 사라진다.

**패턴:** `[색상 설명], [HEX 코드 나열]`

**예시:**
- `monochrome black and white only, solid black fills`
- `deep purple #1A0A2E background, hot pink #FF3CAC accent, violet #7B2FBE mid-tone`
- `limited palette: cobalt blue #1B4FD8 sky, grass green #2D7D46, hot pink #FF3CAC accent, warm beige #F5E6C8 path`

---

### ④ LIGHTING & MOOD `권장`

**역할:** 분위기와 퀄리티를 결정. 특히 3D·배경 이미지에서 효과가 크다.

| 상황 | 표현 |
|---|---|
| Flat / 일러스트 | `flat even lighting` |
| Editorial | `bright daylight lighting` |
| 3D 제품/배경 | `cinematic studio lighting with bloom and subtle lens flare` |
| 야외 장면 | `soft golden hour lighting` |
| 다크/테크 | `dramatic rim lighting, deep shadows` |

---

### ⑤ TEXTURE & FINISH `권장`

**역할:** 매체감 표현. 이 레이어가 AI 이미지와 수작업 이미지를 구분하는 포인트.

| 스타일 | 텍스처 표현 |
|---|---|
| Flat | `clean closed linework, no textures, solid fills` |
| Editorial | `grain texture overlay, halftone dot texture on surfaces` |
| 3D | `PBR glossy materials, subsurface scattering, bokeh depth of field` |
| Risograph | `risograph print texture, slight ink misregistration` |
| Stylized Photo | `film grain, subtle chromatic aberration` |

---

### ⑥ TECHNICAL SPECS `권장`

**역할:** 웹 사용 목적에 맞는 포맷을 지정.

**배경 처리:**
- `white background, isolated subject` — UI 컴포넌트, 아이콘
- `transparent background` — 오버레이 용도
- `minimal clean background` — 히어로 일러스트
- `dark background` — SaaS 랜딩, 테크 배경

**비율:**
- `square format 1:1` — SNS, 썸네일
- `landscape format 16:9` — 히어로 배너
- `portrait format 9:16` — 모바일, 스토리
- `wide banner format 3:1` — 헤더 배너

---

### ⑦ NEGATIVE PROMPT `필수`

**역할:** AI가 기본적으로 만들어내는 이상함을 방어. 없으면 AI 느낌을 벗어날 수 없다.

#### 공통 (모든 스타일)
```
photorealistic rendering, midjourney style, oversaturated colors, uncanny valley,
oversmoothed skin, generic stock photo aesthetic, watermark, signature, text overlay,
deformed hands, extra limbs, extra fingers, anatomically incorrect
```

#### Flat Illustration 추가
```
shading, 3d render, gradient fill, complex texture, drop shadow, multiple light sources,
photorealistic, lens flare, depth of field
```

#### Editorial Illustration 추가
```
smooth digital painting, 3d render, too many colors, overdetailed background,
clean flat vector, plastic sheen
```

#### 3D Abstract 추가
```
cartoon, flat 2d, hand-drawn, people, characters, text, logo,
plastic cheap look, overexposed, blown highlights
```

#### 웹 사용 공통
```
cropped subject, cut off edges, cluttered composition, busy background,
multiple subjects when single needed, low resolution, jpeg artifact
```

---

## 완성 템플릿 (복사용)

### Flat Illustration

```
flat vector illustration, minimalist line art style, [SUBJECT],
[COLOR PALETTE],
flat even lighting,
clean closed linework, solid fills, no gradients or textures,
[BACKGROUND], [RATIO],
Monocle magazine aesthetic, simple expressive cartoon face
--no photorealistic, 3d render, gradient, complex texture, shadow, extra limbs,
deformed hands, blurry, watermark, overdetailed, multiple light sources
```

### Editorial Illustration

```
editorial illustration, risograph print style, [SUBJECT],
limited color palette: [COLOR 1], [COLOR 2], [COLOR 3],
bright daylight lighting,
grain texture overlay, halftone dot texture on surfaces, flat shapes with subtle texture,
[BACKGROUND], [RATIO],
NYT magazine editorial aesthetic
--no photorealistic, 3d render, too many colors, smooth gradient, overdetailed, blurry,
watermark, plastic sheen, clean flat vector
```

### 3D Abstract / Background

```
high-end 3D render, CGI artwork, [SUBJECT],
[COLOR PALETTE],
cinematic studio lighting with bloom and subtle lens flare,
PBR glossy materials, subsurface scattering, bokeh depth of field,
[BACKGROUND], [RATIO],
premium SaaS landing page aesthetic, Octane render quality
--no cartoon, flat 2d, hand-drawn, watermark, text, people, characters,
low quality, plastic cheap look, overexposed, blown highlights
```

### Stylized CGI / Photo

```
stylized photography, high-end commercial CGI, [SUBJECT],
[COLOR PALETTE],
soft directional studio lighting, cinematic color grading,
film grain, subtle chromatic aberration,
[BACKGROUND], [RATIO],
advertising photography aesthetic, shot on Hasselblad
--no cartoon, illustration, 2d, watermark, text, distorted anatomy,
overprocessed, uncanny valley, generic stock photo
```

---

## 시리즈 일관성 유지 전략

### 방법 1 — Style Anchor 고정
`same [STYLE ANCHOR] as previous, now showing [NEW SUBJECT]`
→ Subject만 교체하면 스타일이 유지됨

### 방법 2 — HEX 코드 고정
컬러 팔레트의 HEX 코드를 동일하게 유지.
브랜드 컬러를 직접 주입하면 브랜드 비주얼 시스템과 통일 가능.

### 방법 3 — Seed 고정 (툴 지원 시)
동일 seed + 동일 Style Anchor = 가장 강력한 일관성 보장.
Midjourney `--seed`, DALL-E 3의 재생성 기능 활용.

### 방법 4 — 변형 패턴
| 원본 | 변형 |
|---|---|
| 달리는 캐릭터 | `same character style, now sitting at a desk, working on laptop` |
| 퍼플 3D 배경 | `same composition style, color palette changed to: [NEW COLORS]` |
| 에디토리얼 커버 | `same illustration style, subject changed to: [NEW SUBJECT]` |

---

## 툴별 문법 차이

| 툴 | Negative 방식 | 비율 방식 |
|---|---|---|
| Midjourney | `--no [terms]` | `--ar 16:9` |
| DALL-E 3 | 프롬프트 내 `avoid:` 또는 별도 필드 | 프롬프트 내 기술 |
| Adobe Firefly | Negative prompt 필드 별도 | 설정에서 선택 |
| Flux | `negative_prompt:` 파라미터 | `aspect_ratio:` |
| Stable Diffusion | `negative_prompt:` 파라미터 | `--w` `--h` |