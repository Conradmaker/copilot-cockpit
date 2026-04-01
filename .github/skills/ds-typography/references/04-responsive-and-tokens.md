# 반응형 타이포그래피와 토큰 브리지

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 responsive type, variable font decision, Tailwind v4 token bridge를 다룬다. 구현 mechanics 전체가 아니라 decision을 token으로 옮기는 얇은 연결 문서다.

---

## 1. responsive type는 bounded scaling이 기본이다

고정 px와 무제한 viewport scaling 모두 극단에서 무너지기 쉽다. 기본값은 `clamp()` 같은 bounded scaling이다.

### body text example

```css
body {
  font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
}
```

### heading example

```css
h1 {
  font-size: clamp(2rem, 1.5rem + 2vw, 3.5rem);
}
```

### 원칙

- minimum은 모바일 readability 기준으로 잡는다
- maximum은 wide desktop에서 과장되지 않는 선으로 잡는다
- body와 heading은 같은 slope를 공유하지 않아도 된다

---

## 2. breakpoint보다 reading result를 먼저 본다

- mobile: body size를 무조건 줄이기보다 reading distance를 고려한다
- tablet: line length control과 hierarchy 유지가 중요하다
- desktop: headline 확대보다 paragraph width 제어가 더 중요할 수 있다

responsive type는 device naming보다 reading outcome을 기준으로 조정한다.

### fluid type vs fixed rem 판단

| 영역 | 권장 | 이유 |
| --- | --- | --- |
| marketing headings | `clamp()` fluid | viewport에 따라 임팩트 조절이 필요하다 |
| product UI headings | fixed rem | 예측 가능해야 하고 density control이 중요하다 |
| body text | 항상 fixed rem | fluid body는 읽기 리듬을 깨뜨린다 |

fluid와 fixed를 혼합하는 것도 유효하다. marketing surface 안에서도 hero headline만 fluid, 본문은 fixed rem이 안전하다.

---

## 3. variable font는 의미 있는 control이 있을 때만 쓴다

### 좋은 경우

- 여러 static weight를 하나로 줄일 수 있다
- hover, emphasis, editorial display 등에서 axis control이 실제 가치를 준다
- width, weight, slant를 viewport나 interaction에 맞게 미세 조정한다

### 굳이 안 써도 되는 경우

- 실제로는 400, 500, 600 세 weight만 쓰는 product UI
- font file 이점보다 implementation complexity가 더 큰 경우
- axis를 거의 만지지 않는데 variable font라는 이유만으로 채택한 경우

---

## 4. Tailwind v4 token bridge

Tailwind v4에서 typography decision은 utility class가 아니라 token에서 먼저 굳히는 편이 안전하다.

### decision → token mapping

| Decision | Example token |
| --- | --- |
| Primary family | `--font-sans` |
| Optional display family | `--font-display` |
| Type scale | `--text-sm`, `--text-base`, `--text-xl` |
| Leading | `--leading-tight`, `--leading-normal`, `--leading-relaxed` |
| Tracking | `--tracking-tight`, `--tracking-wide`, `--tracking-widest` |

### Tailwind v4 pattern

```css
@import "tailwindcss";

:root {
  --type-base: 1rem;
  --type-lg: 1.1875rem;
  --type-2xl: 1.75rem;
  --leading-tight: 1.2;
  --leading-normal: 1.55;
  --tracking-wide: 0.015em;
  --tracking-widest: 0.08em;
}

@theme inline {
  --font-sans: var(--font-inter), system-ui;
  --font-display: var(--font-newsreader), serif;
}
```

여기서 핵심은 값 자체를 Tailwind 안에서 즉흥적으로 만들지 않고, ds-typography decision을 token으로 옮기는 것이다.

---

## 5. out of scope boundary

이 문서는 아래 주제를 자세히 다루지 않는다.

- `@font-face` authoring
- `font-display` strategy
- preload / preconnect
- subsetting과 font budget
- fallback metric tuning

이 영역은 implementation/performance companion에서 다룬다.

---

## 체크리스트

- [ ] fixed px 대신 bounded scaling을 검토했는가
- [ ] mobile과 desktop에서 hierarchy가 같은 규칙으로 읽히는가
- [ ] variable font 채택 이유가 실제 axis usage로 이어지는가
- [ ] typography decision이 utility가 아니라 token으로 먼저 고정되는가
- [ ] font-loading/performance deep dive를 이 문서 범위에 억지로 넣고 있지 않은가
