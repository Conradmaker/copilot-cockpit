# Typeset — 타이포그래피 개선 워크플로우

Prefer retrieval-led reasoning over pre-training-led reasoning.

타이포그래피가 제너릭하거나, 일관성 없거나, 가독성이 약할 때 의도적이고 정제된 타입 시스템으로 전환한다.

---

## 언제 사용하는가

- 비평에서 "폰트/계층이 약하다"고 나왔을 때
- "글자가 너무 작다", "위계가 안 보인다", "가독성이 떨어진다"
- 시스템 폰트만 사용해서 개성이 없다
- 본문과 제목의 구분이 모호할 때

## 워크플로우

### Step 1: 타이포그래피 진단

현재 타입 시스템의 약점을 분류한다.

| 유형 | 증상 | 예시 |
|------|------|------|
| 폰트 부재 | 시스템 폰트만 사용 | Inter, Roboto, Arial 그대로 |
| 약한 위계 | 크기/무게 차이가 미미 | 14px/15px/16px 처럼 차이가 작음 |
| 임의 사이즈 | 타입 스케일 부재 | 13px, 27px, 43px 같은 임의 값 |
| 가독성 문제 | line-height, 자폭 부적절 | 줄간격 너무 빽빽함 |
| 무게 불일치 | weight 사용 제각각 | Bold/Semibold 혼용 |

### Step 2: 타입 스케일 정의

**5 단계로 대부분 커버:**
1. caption (12px)
2. secondary (14px)
3. body (16px)
4. subheading (20px)
5. heading (24-32px)

**스케일 전략:**
- App UI: 고정 `rem` 스케일 (공간 예측성 중요)
- Marketing/Content: `clamp(min, preferred, max)` 유동 스케일 (헤딩만)

### Step 3: 폰트 선택

**폰트 교체 기준:**
- 브랜드 퍼스널리티와 일치하는가?
- 2-3 개 패밀리 제한 (그 이상은 혼란)
- genuine contrast 있는 페어링 (serif + sans, geometric + humanist)

**웹폰트 로딩:**
- `font-display: swap`으로 레이아웃 시프트 방지
- metric-matched fallback 사용

### Step 4: 가독성 보정

**line-height:**
- 헤딩: 살짝 타이트
- 본문: 살짝 여유있게
- 다크모드: 약간 더 느슨하게

**자폭 (line length):**
- 이상적: 45-75 characters
- `max-width: 65ch`로 제한

**본문 최소 사이즈:**
- 16px / 1rem 이상 (WCAG)

### Step 5: 디테일 정제

**letter-spacing:**
- 대문자/소형 대문자: 약간 넓게
- 디스플레이 텍스트: 기본 또는 타이트

**tabular-nums:**
- 데이터 테이블, 숫자 정렬이 필요할 때

**weight 전략:**
- 3-4 개 무게만 사용 (Regular, Medium, Semibold, Bold)
- 역할 정의 후 일관되게 적용
- 실제로 쓰는 무게만 로드

---

## 체크리스트

- [ ] 타입 스케일이 일관되는가?
- [ ] 헤딩/본문/캡션이 순간 구분되는가?
- [ ] 본문이 16px 이상인가?
- [ ] line-height 가 컨텍스트에 맞는가?
- [ ] weight 가 일관되게 사용되는가?
- [ ] 웹폰트가 효율적으로 로드되는가?
- [ ] WCAG 대비 비율을 만족하는가?

## 참조

- `ds-typography` — 폰트 선택, 페어링, 타입 스케일, 반응형 타이포
- `fe-tailwindcss` — 유틸리티 클래스로 타입 구현
