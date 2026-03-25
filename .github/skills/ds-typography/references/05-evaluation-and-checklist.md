# 서체 평가와 최종 체크리스트

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 typeface evaluation, multilingual readiness, anti-pattern, shipping checklist를 정리한다.

---

## 1. taste보다 구조를 먼저 본다

specimen이 매력적이어도 실제 product text에서 실패하는 경우가 많다. 먼저 구조와 품질을 본다.

| Check | What to look for |
| --- | --- |
| x-height | small size에서 충분히 읽히는가 |
| counters / apertures | `a`, `e`, `c`가 막히지 않는가 |
| stroke contrast | small size에서 thin stroke가 사라지지 않는가 |
| even color | paragraph block이 uneven gray로 보이지 않는가 |
| distinct characters | `Il1`, `O0`, `rn` vs `m` 구분이 되는가 |
| weights and styles | regular / emphasis / strong hierarchy를 감당할 수 있는가 |
| glyph coverage | target language와 숫자, punctuation이 충분한가 |

---

## 2. real content와 actual size로 테스트한다

### 반드시 확인할 size

- body candidates: 14px, 16px, 18px
- small text: 11px, 12px, 13px
- heading candidates: 24px, 32px, 48px

### lorem ipsum 대신 써야 할 것

- 실제 제품의 한글/영문 문장
- 숫자, 통화, 날짜, 메타데이터
- CTA, caps label, table cell, helper text

dummy text는 character frequency와 paragraph rhythm 문제를 숨긴다.

---

## 3. multilingual checklist

multilingual product에서는 font choice가 미학보다 coverage와 rhythm 문제로 바뀐다.

- 한글/영문 혼합 headline이 어색하지 않은가
- 숫자와 punctuation이 body에서 떠 보이지 않는가
- small text에서 target language glyph가 뭉개지지 않는가
- fallback과 섞였을 때 visual jump가 과하지 않은가

### 문자권별 기억할 것

- Korean과 non-Latin은 tight display leading과 negative tracking에 더 민감하다
- Latin에서 좋은 editorial serif가 CJK 혼합에서는 거칠게 느껴질 수 있다
- UI text는 aesthetics보다 clear differentiation이 먼저다

---

## 4. 흔한 red flags

- 예쁜 specimen인데 14~16px에서 금방 무너진다
- small text에서 `Il1`, `O0` 구분이 약하다
- caps가 많은데 tracking이 없다
- real content block이 uneven gray로 보인다
- 필요한 weight, italic, numeral style이 없다
- license가 불명확하다
- glyph coverage가 target language를 충분히 지원하지 않는다

---

## 5. anti-pattern

- default system font를 아무 이유 없이 쓰고도 intentional choice인 척 설명하기
- 한 화면에 font family를 계속 추가해서 hierarchy를 해결하려 하기
- 800/900 weight를 기본 headline처럼 쓰기
- small text에서 readability 대신 airiness를 우선하기
- visual polish를 이유로 ALL CAPS와 tiny text에 tracking을 빼기
- responsive type 문제를 font change로 해결하려 하기

---

## 6. shipping checklist

- [ ] one-font rule을 깨는 이유가 명확한가
- [ ] scale이 ratio와 token 기준으로 정리됐는가
- [ ] 기본 weight가 3가지 안에서 설명 가능한가
- [ ] body text가 실제 콘텐츠 기준으로 편하게 읽히는가
- [ ] small text와 caps treatment가 거칠지 않은가
- [ ] Korean / non-Latin headline에서 답답함이 없는가
- [ ] glyph coverage와 license를 확인했는가
- [ ] real content와 real device에서 테스트했는가

---

## 7. boundary note

성능과 로딩이 문제라면 typography quality review만으로는 끝나지 않는다. 아래 증상이 중심이면 implementation/performance companion으로 전환한다.

- font payload가 너무 크다
- layout shift가 난다
- preload / `font-display` / subsetting 전략이 필요하다
- fallback metric tuning이 필요하다
