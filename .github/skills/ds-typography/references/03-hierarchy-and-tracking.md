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
| Headline | 1.15 – 1.3 | body보다 타이트하지만 script와 line count를 본다 |
| Large display | 1.05 – 1.2 | dense only when still readable |
| Small text | 1.45 – 1.6 | 읽기 안정성이 더 중요 |

### 기억할 것

- 긴 line은 leading이 더 필요하다
- 짧은 line은 약간 타이트해도 된다
- Korean과 multiline heading은 Latin single-line heading보다 여유를 더 준다
- Sans serif와 non-Latin scripts는 tight display text보다 약간 더 열린 leading이 필요할 때가 많다

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
| Body text | 14–18px | `0` |
| Small text | 11–13px | `0.01em` – `0.02em` |
| UI labels / buttons | any | `0.01em` – `0.03em` |
| ALL CAPS | any | `0.06em` – `0.1em` |
| Large headings | 32px+ | `0` to `-0.02em` |
| Display text | 48px+ | `-0.02em` to `-0.03em` |

### 규칙

- tracking은 **항상 `em`** 단위를 우선한다
- body text는 기본 tracking을 유지하는 편이 낫다
- small text와 caps는 positive tracking이 polishing detail이 아니라 readability rule에 가깝다
- negative tracking은 Latin large heading에서만 보수적으로 쓴다
- Korean과 non-Latin heading은 기본 tracking을 유지하고, 답답함이 명확할 때만 미세 조정한다

---

## 7. line length (measure)

| Content | Characters |
| --- | --- |
| Optimal | 50–75 |
| Default target | 65ch |
| Too wide warning | 80ch+ |

### 구현 기본값

```css
.prose {
  max-width: 65ch;
}
```

full-width paragraph는 desktop에서 거의 항상 읽기 피로를 만든다.

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
- [ ] body paragraph가 65ch 전후에서 관리되는가
- [ ] spacing rhythm이 line-height와 충돌하지 않는가
