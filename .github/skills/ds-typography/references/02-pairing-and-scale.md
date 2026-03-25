# 폰트 조합과 타입 스케일

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 anchor font, one-font rule, pairing, type scale의 기본 판단 기준을 정리한다.

---

## 1. 기본값은 one-font rule이다

대부분의 product UI는 한 패밀리로 충분하다.

```
One font + multiple weights = default
Two fonts = needs justification
Three fonts = almost never
```

### 두 번째 폰트가 필요한 경우

- marketing / landing page처럼 personality를 명확히 줘야 할 때
- editorial, documentation처럼 body reading comfort와 headline character를 분리할 때
- brand-led surface라서 anchor font가 실제로 art direction 역할을 할 때

이유를 설명할 수 없으면 한 패밀리로 되돌리는 편이 낫다.

---

## 2. anchor font는 언제 쓰는가

personality가 중요한 surface에서는 body보다 headline font가 먼저다.

- anchor font는 화면의 tone을 결정한다
- body font는 anchor font를 돋보이게 하되 긴 읽기에서 버텨야 한다
- brand surface가 아니면 body/UI font를 먼저 고르고 headline도 같은 family 안에서 해결하는 편이 안전하다

### 실전 분기

| Surface | 시작점 |
| --- | --- |
| SaaS / work tool | body/UI font first |
| marketing landing | anchor font first |
| editorial / docs | body reading font first, then display choice |
| dashboard | dense UI font first |

---

## 3. pairing은 대비가 보여야 한다

좋은 pairing은 "다른데 같이 맞는다"이고, 나쁜 pairing은 "비슷해서 실수처럼 보인다"다.

### 좋은 pairing 기준

- serif + sans-serif처럼 구조적 대비가 있다
- one face has personality, the other stays neutral
- x-height와 visual size가 너무 따로 놀지 않는다
- 두 폰트의 역할이 headline/body처럼 명확하다

### 피할 pairing

- 너무 비슷한 두 sans
- 너무 비슷한 두 serif
- 둘 다 개성이 강해 서로 경쟁하는 조합
- body font가 headline보다 더 강하게 보이는 조합

---

## 4. safe defaults by product type

| Product type | 기본 방향 |
| --- | --- |
| SaaS / tech | one sans family, 400/500/600, neutral body |
| finance / enterprise | neutral sans 또는 restrained serif, 신뢰 우선 |
| startup marketing | anchor + neutral body 허용 |
| developer tool | neutral sans + mono accent 정도로 제한 |
| editorial / docs | reading comfort 우선, pairing justified |

---

## 5. type scale은 ratio로 만든다

눈대중으로 크기를 찍지 말고 ratio를 먼저 고른다.

| Ratio | Multiplier | Best for |
| --- | --- | --- |
| Minor Second | 1.067 | dense UI, dashboards |
| Major Second | 1.125 | compact interfaces |
| **Minor Third** | **1.2** | general purpose default |
| Major Third | 1.25 | marketing, editorial |
| Perfect Fourth | 1.333 | bold expressive layouts |
| Golden Ratio | 1.618 | hero-only, general UI에는 과함 |

### 실전 기본값

- dense UI / dashboard: 1.067~1.125
- general product UI: 1.125~1.2
- marketing / editorial: 1.2~1.25
- bold hero moments: 1.333 이상은 예외적으로만

---

## 6. practical scale boundaries

### size count

- production에서는 보통 **6~8개 text size**면 충분하다
- landing page는 **5~6개**로도 충분한 경우가 많다
- dashboard는 24px 이하 영역에서 촘촘하게 구성하는 편이 안정적이다

### sample scale (16px base, minor third)

| Role | Size |
| --- | --- |
| Caption | 11px |
| Small / metadata | 13px |
| Body | 16px |
| Large body | 19px |
| H4 | 23px |
| H3 | 28px |
| H2 | 33px |
| H1 | 40px |
| Display | 48px |

이 표는 출발점이지, 모든 surface에 그대로 복붙하는 preset이 아니다.

---

## 7. scale과 weight는 같이 본다

- 큰 텍스트는 더 가벼운 weight도 충분히 버틴다
- 작은 텍스트는 400보다 가벼워지면 무너지기 쉽다
- 800/900은 default hierarchy가 아니라 visual moment다

---

## 빠른 체크리스트

- [ ] 두 번째 폰트를 쓰는 이유를 설명할 수 있는가
- [ ] anchor font가 필요한 surface인지 먼저 판단했는가
- [ ] pairing이 실제 대비를 만들고 있는가
- [ ] scale ratio를 먼저 골랐는가
- [ ] text size 수가 불필요하게 많지 않은가
- [ ] 700 이상 weight가 기본 hierarchy로 남용되고 있지 않은가
