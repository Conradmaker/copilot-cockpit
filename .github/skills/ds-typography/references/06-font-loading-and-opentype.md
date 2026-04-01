# 웹 폰트 로딩과 OpenType

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 web font 로딩 전략과 OpenType feature 활용을 정리한다. typography decision이 아니라 구현 mechanics를 다룬다.

---

## 1. font-display 전략

`font-display`는 web font이 로드되기 전에 텍스트를 어떻게 보여줄지 결정한다.

| 값 | 동작 | 권장 용도 |
| --- | --- | --- |
| `swap` | fallback을 바로 보여주고, 로드되면 교체 | body text, UI text (대부분의 기본값) |
| `optional` | 빠르면 교체, 아니면 fallback 유지 | 성능 중시 product UI |
| `block` | 짧은 시간(~3s) 숨긴 뒤 교체 | icon font 외에는 비추 |

```css
@font-face {
  font-family: 'Brand Sans';
  src: url('/fonts/brand-sans.woff2') format('woff2');
  font-display: swap;
}
```

### preload

critical path에 있는 font file은 preload한다.

```html
<link rel="preload" href="/fonts/brand-sans.woff2" as="font" type="font/woff2" crossorigin>
```

- woff2만 preload한다 (woff는 fallback)
- `crossorigin` attribute가 반드시 필요하다 (same-origin이어도)
- 2~3개 이상 preload하면 역효과가 날 수 있다

---

## 2. fallback metric 매칭

web font과 system fallback의 metric이 다르면 swap 시 layout shift(CLS)가 발생한다. `size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`로 fallback의 metric을 web font에 가깝게 맞춘다.

```css
@font-face {
  font-family: 'Brand Sans Fallback';
  src: local('Arial');
  size-adjust: 100.5%;
  ascent-override: 96%;
  descent-override: 24%;
  line-gap-override: 0%;
}

body {
  font-family: 'Brand Sans', 'Brand Sans Fallback', system-ui;
}
```

### Fontaine

[Fontaine](https://github.com/unjs/fontaine)은 web font의 metric을 분석해 fallback `@font-face`를 자동 생성한다. Next.js(`next/font`), Nuxt, Vite에서 사용 가능하다.

---

## 3. subsetting

font file에서 사용하지 않는 glyph를 제거해 payload를 줄인다.

- Google Fonts는 Unicode range subsetting을 자동 적용한다
- self-hosting이면 `pyftsubset`이나 `subfont`으로 필요한 range만 추출한다
- Latin + Korean 혼합 product에서는 Latin과 Korean을 별도 `@font-face`로 나누고 `unicode-range`를 지정한다

```css
/* Latin subset */
@font-face {
  font-family: 'Brand Sans';
  src: url('/fonts/brand-sans-latin.woff2') format('woff2');
  unicode-range: U+0020-007F, U+00A0-00FF;
}

/* Korean subset */
@font-face {
  font-family: 'Brand Sans';
  src: url('/fonts/brand-sans-kr.woff2') format('woff2');
  unicode-range: U+AC00-D7AF, U+1100-11FF;
}
```

---

## 4. OpenType feature 활용

OpenType feature는 font에 내장된 고급 타이포그래피 옵션이다. 모든 font가 지원하는 것은 아니므로 사용 전에 feature availability를 확인한다.

### 자주 쓰는 feature

| Feature | CSS | 용도 |
| --- | --- | --- |
| tabular figures | `font-variant-numeric: tabular-nums` | 표, 숫자 정렬이 필요한 곳 |
| proportional figures | `font-variant-numeric: proportional-nums` | 본문의 숫자 (기본값) |
| diagonal fractions | `font-variant-numeric: diagonal-fractions` | 분수 표현 (1/2, 3/4) |
| small caps | `font-variant-caps: all-small-caps` | 약어, label, 세련된 강조 |
| kerning | `font-kerning: auto` | 대부분의 브라우저 기본값 |
| ligatures off | `font-variant-ligatures: none` | code block에서 `fi`, `fl` 합자 방지 |

### 간결한 설정

```css
/* 표와 데이터 */
.data-table {
  font-variant-numeric: tabular-nums;
}

/* 코드 블록 */
code, pre {
  font-variant-ligatures: none;
}

/* 약어, 배지 */
.badge {
  font-variant-caps: all-small-caps;
  letter-spacing: 0.05em;
}
```

---

## 5. 접근성 기본값

- `font-size`는 `rem` 또는 `em`으로 지정한다 — `px`은 사용자의 브라우저 글꼴 크기 설정을 무시한다
- body text 최소 `1rem`(16px)을 유지한다
- `user-scalable=no`를 쓰지 않는다 — 줌을 막으면 접근성 위반이다
- 텍스트 링크의 tap target은 최소 44px을 확보한다
