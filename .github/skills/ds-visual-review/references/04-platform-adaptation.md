# 플랫폼 적응과 반응형 전략

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 다양한 디바이스와 입력 방식에 대응하는 반응형 전략과 플랫폼별 적응 패턴을 다룬다.

---

## 1. Mobile-first 원칙

모바일 레이아웃을 기본값으로 작성하고, 넓은 화면에서 확장한다.

```css
/* 기본: 모바일 */
.container { padding: 1rem; }

/* 확장: 데스크탑 */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}
```

- 브레이크포인트를 기기 모델이 아니라 **콘텐츠가 깨지는 지점**에서 잡는다
- 640 / 768 / 1024 / 1280px은 참고값이지 절대 기준이 아니다 — 콘텐츠로 결정한다

---

## 2. 입력 방식 감지

마우스와 터치를 CSS media query로 구별해 호버/탭 동작을 분기한다.

```css
/* 마우스 사용자 — 정밀한 포인터 */
@media (pointer: fine) and (hover: hover) {
  .card:hover { transform: translateY(-2px); }
}

/* 터치 사용자 — 굵은 포인터 */
@media (pointer: coarse) {
  .button { min-height: 44px; min-width: 44px; }
}
```

- `hover: hover` — 마우스처럼 동작하는 기기에서만 hover 효과를 활성화한다
- `pointer: coarse` — 터치 기기에서 탭 타겟을 최소 44×44px로 보장한다

---

## 3. Safe Area (노치·둥근 모서리 대응)

iPhone 노치, Dynamic Island, 둥근 모서리 기기에서 콘텐츠가 가려지지 않도록 환경 변수를 사용한다.

```css
body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

`<meta name="viewport">`에 `viewport-fit=cover`가 설정되어야 `env()` 값이 활성화된다.

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

---

## 4. 반응형 이미지

### `srcset`과 sizes

```html
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1600.jpg 1600w"
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="Hero image"
  loading="lazy"
  decoding="async"
/>
```

### `<picture>`로 아트 디렉션

화면 크기에 따라 다른 이미지(crop, 비율)를 보여줘야 할 때 사용한다.

```html
<picture>
  <source media="(min-width: 1024px)" srcset="hero-wide.webp" type="image/webp" />
  <source media="(min-width: 768px)" srcset="hero-medium.webp" type="image/webp" />
  <img src="hero-small.jpg" alt="Hero" />
</picture>
```

- `loading="lazy"` — fold 아래 이미지는 lazy loading한다
- `decoding="async"` — 이미지 디코딩을 메인 스레드에서 분리한다
- LCP 이미지는 `loading="eager"` + `fetchpriority="high"`로 우선 로드한다

---

## 5. 레이아웃 적응 패턴

### Desktop → Mobile 전략

| 패턴 | 예시 |
| --- | --- |
| 열 축소 | 3열 → 1열 stack |
| 네비게이션 접기 | 수평 메뉴 → 햄버거 |
| 사이드바 접기 | 영구 사이드바 → 드로어 |
| 테이블 적응 | 가로 스크롤 또는 카드 리스트 |
| 차트 단순화 | 복잡한 차트 → 핵심 수치 카드 |

### Desktop → Tablet 전략

| 패턴 | 예시 |
| --- | --- |
| 사이드바 축소 | 풀 사이드바 → 아이콘 사이드바 |
| 다단 축소 | 4열 → 2열 |
| hover → tap 전환 | hover 미리보기 → explicit button |

---

## 6. 실기기 테스트

에뮬레이터로는 발견하기 어려운 문제가 있다.

### 실기기에서만 확인 가능한 것

- 터치 반응 속도와 스크롤 관성(momentum)
- 소프트 키보드가 열렸을 때의 레이아웃 밀림
- 노치/Dynamic Island 영역 침범
- 네이티브 브라우저 UI(주소창 축소/확장)에 의한 높이 변화
- 실제 네트워크 속도에서의 이미지 로딩 체감

### 최소 테스트 세트

- iOS Safari (iPhone 최신)
- Android Chrome (Galaxy S 또는 Pixel)
- iPad Safari (가로/세로)
- Desktop Chrome + Firefox

---

## 체크리스트

- [ ] 브레이크포인트가 콘텐츠 기반인가 (기기 모델이 아닌)
- [ ] `pointer`와 `hover` media query로 입력 방식을 구별하는가
- [ ] safe area inset이 적용되어 노치/모서리에 콘텐츠가 가려지지 않는가
- [ ] LCP 이미지에 `fetchpriority="high"`가 있고, fold 아래는 `loading="lazy"`인가
- [ ] 실기기에서 소프트 키보드, 주소창, 터치 반응을 테스트했는가
