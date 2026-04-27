# 계층, leading, tracking

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 weight hierarchy, text color hierarchy, line-height, tracking, line length, vertical rhythm을 정리한다.

---

## 1. hierarchy는 size 하나로 만들지 않는다

계층은 보통 세 가지 레버로 만든다.

1. size
2. weight
3. color / opacity

세 레버를 모두 매 단계마다 크게 흔들 필요는 없다. 인접한 레벨에서는 하나나 둘만 바뀌어도 충분한 경우가 많다.

---

## 2. 기본 weight system

### 기본값

- **400**: body, descriptions
- **500**: labels, subtle emphasis
- **600**: subheadings, buttons, stronger hierarchy

### 원칙

- 기본 조합은 보통 **3가지 이내**로 충분하다
- body text는 400이 기본이다
- small text는 400 또는 500이 안정적이다
- headline은 폰트와 문자권에 따라 400~700 사이에서 고른다
- 800/900은 deliberate display moment가 아니면 기본값으로 쓰지 않는다

---

## 3. text color hierarchy

텍스트 색도 scale의 일부다.

| Level | Opacity / strength | Use |
| --- | --- | --- |
| Primary | 100% 또는 87% | headlines, key data, main body |
| Secondary | 60~70% | descriptions, supporting labels |
| Tertiary | 45% 이하 | metadata, timestamps, helper copy |

### 원칙

- pure black보다 약간 softened neutral이 나을 때가 많다
- body text를 60% 이하로 내리면 airy해 보이기보다 읽기 힘들어진다
- 같은 정보 레벨은 같은 text color level을 반복해서 쓴다

---

## 4. line-height quick reference

| Text type | Line-height | Notes |
| --- | --- | --- |
| Body text | 1.5 – 1.7 | 긴 읽기의 기본값 |
| Short paragraph / compact UI copy | 1.4 – 1.5 | 짧은 폭에서는 약간 타이트 가능 |
| Headline | 1.15 – 1.3 | body보다 조금 더 타이트하지만 script와 line count를 본다 |
| Small text | 1.45 – 1.6 | 읽기 안정성이 더 중요 |

### 기억할 것

- line-height는 글자 크기와 비례해서 작아지는 편이지만, line-height ratio는 text type과 script에 따라 달라진다.

---

## 5. vertical rhythm

AI-slop은 spacing보다 typography spacing에서 먼저 들킨다.

### simple rule

```
Line-height × 0.5 = minimum vertical spacing step
```

예:

```
Body 16px / 1.5 → line-height 24px
Minimum step = 12px
```

이 계산은 text block spacing의 최소 기준점을 잡는 데 유용하다.

> Spacing matters more than font size.

같은 폰트를 써도 spacing rhythm이 달라지면 전혀 다른 제품처럼 보인다.

---

## 6. tracking quick reference

| Text type | Size | Value |
| --- | --- | --- |
| Body text | 12–18px | `0` |
| Small text | 10–14px | `0.01em` – `0.02em` |
| UI labels / buttons | any | `0.01em` – `0.03em` |
| ALL CAPS | any | `0.06em` – `0.1em` |
| Large headings | 24px+ | `0em` to `0.02em` |
| Display text | 32px+ | `0` to `-0.02em` |

### 규칙

- tracking은 **항상 `em`** 단위를 우선한다
- body text는 기본 tracking을 유지하는 편이 낫다
- small text와 caps는 positive tracking이 polishing detail이 아니라 readability rule에 가깝다
- negative tracking은 Latin large heading에서만 보수적으로 쓴다
- Korean과 non-Latin heading은 기본 tracking을 유지하고, 답답함이 명확할 때만 미세 조정한다

---

## 7. line length (measure)

`65ch`는 유용한 기본값이지만 모든 text role에 자동으로 적용하는 규칙이 아니다. measure는 최소한 **문자권(script)** 과 **text role(body / lede / display)** 로 나눠서 본다.

| Text role | Latin | Non-Latin | Notes |
| --- | --- | --- | --- |
| Body prose | 60–75ch | 70–84ch | 긴 읽기의 기본 band |
| Lede / supporting intro | 66–82ch | 76–92ch | 문단 수가 짧고 narrative intro일 때 body보다 조금 넓게 허용 가능 |
| Hero / display headline | 14–18em 또는 `clamp(720px, 52vw, 960px)` | 16–20em 또는 `clamp(760px, 58vw, 1040px)` | `ch`를 기본값으로 두지 말고 intended line count로 판단 |

### 기본 원칙

- Latin body prose의 default target은 여전히 `65ch`다
- Non-Latin에서는 `ch`가 실제 글자 수처럼 1:1로 대응하지 않으므로, body/lede는 더 넓은 band를 허용한다
- hero/display headline에는 body prose measure를 자동 적용하지 않는다
- headline은 **폭 숫자**보다 **의도한 줄 수**가 먼저다. desktop hero headline은 보통 2줄, 길면 3줄을 목표로 한다
- 1280px에서 괜찮아 보여도 1920px에서 headline이 과하게 좁아 보이면 headline measure와 hero column span을 다시 본다

full-width paragraph는 desktop에서 거의 항상 읽기 피로를 만든다. 반대로 hero headline을 body prose와 같은 `65ch` 규칙에 가두면 CJK언어권에서는 3~4줄로 조기 줄바꿈되기 쉽다.

---

## 8. display type는 visual moment다

display font, text swapping, morphing typography는 유효한 visual tool이지만 system default가 아니다.

- display type은 페이지당 1~2회의 deliberate moment로 제한하는 편이 안전하다
- body font처럼 자주 반복되면 novelty보다 noise가 된다
- animated typography는 hierarchy를 보조할 때만 남기고, 읽기 자체를 방해하면 제거한다

---

## shipping checklist

- [ ] size, weight, color가 각각 명확한 역할을 갖는가
- [ ] 기본 weight가 3가지 안에서 정리되는가
- [ ] body leading이 1.5 이상인가
- [ ] small text와 ALL CAPS에 tracking이 있는가
- [ ] large heading tracking이 문자권에 맞게 절제되어 있는가
- [ ] body paragraph가 문자권과 text role에 맞는 measure로 관리되는가 (Latin body ~65ch, Korean body/lede는 더 넓게, hero/display는 별도 기준)
- [ ] Korean 또는 multilingual hero headline이 1280px와 1920px에서 의도한 줄 수(대개 2~3줄)를 유지하는가
- [ ] spacing rhythm이 line-height와 충돌하지 않는가
- [ ] 다크모드에서 body weight를 줄여 시각적 무게를 맞추었는가

### 다크모드 font weight 보정

light text on dark background에서는 글자가 더 굵게 보인다 (irradiation illusion). body text의 weight를 400 → 350으로 줄이면 라이트 모드와 시각적 무게가 비슷해진다.

```css
:root[data-theme="dark"] {
  --body-weight: 350;
}
```
