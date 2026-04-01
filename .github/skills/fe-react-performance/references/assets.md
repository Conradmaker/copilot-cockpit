# 에셋 최적화

**우선순위: 🔴 CRITICAL — LCP, CLS에 직접 영향**

이미지와 폰트는 웹 페이지 전체 바이트의 상당 부분을 차지한다. 올바른 포맷, 로딩 전략, 힌트만으로 LCP를 크게 개선할 수 있다.

---

## 1. 이미지 포맷 선택

| 포맷 | 용도 | 참고 |
| --- | --- | --- |
| WebP | 사진, 복잡한 그래픽의 기본 포맷 | JPEG 대비 25–35% 더 작다 |
| AVIF | 최고 압축률이 필요할 때 | WebP 대비 20% 더 작지만 인코딩이 느리다 |
| SVG | 아이콘, 로고, 단순 일러스트 | 해상도 무관, 최소 크기 |
| PNG | 투명도가 필요한 UI 에셋 | WebP/AVIF 투명도 지원으로 점차 대체 |

### `<picture>` 폴백 패턴

```html
<picture>
  <source srcset="hero.avif" type="image/avif" />
  <source srcset="hero.webp" type="image/webp" />
  <img src="hero.jpg" alt="Hero" width="1200" height="600" />
</picture>
```

---

## 2. 반응형 이미지

```html
<img
  src="photo-800.webp"
  srcset="photo-400.webp 400w, photo-800.webp 800w, photo-1600.webp 1600w"
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="Product photo"
  loading="lazy"
  decoding="async"
/>
```

- `width`와 `height` 속성을 항상 명시해 CLS를 방지한다
- `loading="lazy"` — fold 아래 이미지에 적용한다
- `decoding="async"` — 이미지 디코딩을 메인 스레드에서 분리한다

---

## 3. LCP 이미지 우선 로딩

페이지의 가장 큰 콘텐츠 요소(hero image 등)는 가능한 빨리 로드해야 한다.

```html
<!-- LCP 이미지에는 lazy 대신 eager + fetchpriority -->
<img
  src="hero.webp"
  alt="Hero"
  loading="eager"
  fetchpriority="high"
  width="1200"
  height="600"
/>
```

```html
<!-- preload로 발견을 더 앞당긴다 -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high" />
```

- LCP 이미지에는 `loading="lazy"`를 **쓰지 않는다**
- Next.js `<Image>`는 `priority` prop으로 동일하게 동작한다

---

## 4. 웹 폰트 최적화

### font-display 전략

| 값 | 동작 | 용도 |
| --- | --- | --- |
| `swap` | FOUT 발생, 텍스트 즉시 표시 | body text 기본값 |
| `optional` | 네트워크 빠르면 사용, 느리면 포기 | 보조 폰트, 장식 폰트 |
| `block` | 최대 3초 대기 | 아이콘 폰트 (로딩 중 깨진 문자 방지) |

### Preload

```html
<link
  rel="preload"
  href="/fonts/inter-var.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

`crossorigin` 속성은 같은 도메인이라도 필수다 — 없으면 이중 다운로드가 발생한다.

### 서브셋팅

사용하는 글리프만 포함해 파일 크기를 줄인다.

```css
@font-face {
  font-family: 'Pretendard';
  src: url('/fonts/pretendard-subset.woff2') format('woff2');
  unicode-range: U+AC00-D7A3; /* 한글 음절 */
}

@font-face {
  font-family: 'Pretendard';
  src: url('/fonts/pretendard-latin.woff2') format('woff2');
  unicode-range: U+0020-007E; /* 기본 라틴 */
}
```

`unicode-range`를 지정하면 해당 글리프가 페이지에 없을 때 폰트를 아예 다운로드하지 않는다.

### Fallback Font Metrics

폰트 로딩 중 CLS를 줄이려면 시스템 폰트의 metrics를 커스텀 폰트에 맞춘다.

```css
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial');
  size-adjust: 107%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

Next.js의 `next/font`는 이를 자동으로 처리한다.

---

## 체크리스트

- [ ] 사진에 WebP 또는 AVIF를 사용하고 `<picture>` 폴백이 있는가
- [ ] LCP 이미지에 `fetchpriority="high"` + `loading="eager"`가 있는가
- [ ] fold 아래 이미지에 `loading="lazy"`가 있는가
- [ ] 모든 `<img>`에 `width`/`height`가 명시되어 CLS가 방지되는가
- [ ] 웹 폰트에 `preload` + `font-display: swap`이 설정되어 있는가
- [ ] 한글 폰트에 `unicode-range` 서브셋팅이 적용되어 있는가
