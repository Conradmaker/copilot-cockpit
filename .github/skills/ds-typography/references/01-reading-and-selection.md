# 읽기 모델과 컨텍스트 선택

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 폰트를 고르기 전에 먼저 고정해야 하는 reading context와 selection 질문을 정리한다.

---

## 1. 타이포그래피의 두 가지 job

모든 텍스트는 대체로 두 역할 중 하나에 가깝다.

| Context | 목적 | 우선순위 |
| --- | --- | --- |
| **Type for a moment** | 시선을 잠깐 잡고 행동을 유도한다 | personality, impact, distinction |
| **Type to live with** | 오래 읽히고 반복적으로 사용된다 | readability, comfort, endurance |

예시:

- headline, CTA, badge, tab label, navigation = type for a moment
- body copy, docs, descriptions, table text, form helper text = type to live with

둘을 같은 기준으로 보면 과장되거나 밋밋해진다.

---

## 2. 어떻게 읽히는지 이해한다

읽기 편한 typography는 "예쁜 폰트"보다 "어떻게 읽히는지"에 더 가깝다.

- **Saccades**: 눈은 부드럽게 흐르지 않고 7~9자 정도씩 점프한다
- **Fixations**: 점프 사이사이 멈추며 정보를 흡수한다
- **Word shape (bouma)**: 숙련된 독자는 글자를 하나씩 세기보다 단어의 형태와 리듬을 본다
- **Legibility vs readability**: legibility는 글자 구분의 문제이고, readability는 긴 읽기에서 편한지의 문제다

### 왜 중요한가

- measure가 너무 길면 return sweep에서 다음 줄을 놓치기 쉽다
- leading이 부족하면 fixation 간 리듬이 무너진다
- tracking이 잘못되면 작은 텍스트와 caps가 특히 거칠게 보인다

---

## 3. selection 전에 답할 질문

폰트를 보기 전에 아래 질문을 먼저 고정한다.

| 질문 | 왜 중요한가 |
| --- | --- |
| **Work tool or marketing?** | neutrality와 personality 허용 범위를 나눈다 |
| **Long reading or scanning?** | leading, measure, density 기본값이 달라진다 |
| **B2B, B2C, or dev tool?** | font character와 weight 감도를 바꾼다 |
| **Single-language or multilingual?** | glyph coverage, tracking, line-height 예외를 결정한다 |
| **App UI or editorial surface?** | one-font default와 pairing 허용 범위가 달라진다 |

---

## 4. 기본 default

불확실할 때는 아래 기본값이 안전하다.

- **When in doubt**: denser, simpler, more neutral
- product app: one font family, restrained weight range, conservative scale
- landing or brand surface: anchor font + neutral body 조합 허용
- long reading: 16~18px body, 1.5~1.7 leading, 50~75 characters
- scanning UI: smaller scale, stronger hierarchy, tighter but still readable leading

---

## 5. 문자권과 language scope

Latin typography 규칙을 그대로 한글과 비라틴 문자권에 복사하면 거칠어지기 쉽다.

- Korean과 non-Latin headline은 Latin display text보다 leading을 조금 더 여유 있게 본다
- Latin large heading에서는 negative tracking이 유효할 수 있지만, Korean heading은 기본 tracking을 유지하고 미세 조정만 한다
- multilingual product는 target language 문자열, 숫자, 특수문자, 날짜 포맷까지 실제 UI 문장으로 테스트한다
- glyph coverage는 body text보다도 small text와 mixed-language UI에서 먼저 문제를 드러낸다

---

## 빠른 체크리스트

- [ ] 이 텍스트가 type for a moment인지 type to live with인지 나눴는가
- [ ] work tool인지 marketing surface인지 먼저 정했는가
- [ ] reading context가 scanning인지 long reading인지 정했는가
- [ ] 한글/영문/숫자/특수문자를 실제 문자열로 볼 계획이 있는가
- [ ] 불확실한데도 personality-heavy choice로 먼저 달려가고 있지 않은가
