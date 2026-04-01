# 오버레이와 드롭다운 구현 패턴

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 모달, 팝오버, 드롭다운 같은 오버레이 요소를 올바른 웹 API와 패턴으로 구현하는 가이드다.

---

## 1. Dialog와 inert

### `<dialog>` 기본 패턴

모달은 `<dialog>` 요소의 `.showModal()` 메서드로 열어야 한다.

- 자동으로 top layer에 올라간다 (z-index 전쟁 불필요)
- 자동으로 `::backdrop`을 제공한다
- Esc 키로 닫기가 기본 동작이다
- `.showModal()`로 열면 뒤의 콘텐츠에 자동으로 `inert`이 적용되어 접근성과 포커스 트랩을 동시에 해결한다

### inert 속성

모달이 열렸을 때 뒤의 콘텐츠를 비활성화하는 속성이다.

```html
<main inert>...</main>
<dialog open>...</dialog>
```

`aria-hidden`과 달리 포커스 이동, 클릭, 키보드 입력도 함께 차단한다. `<dialog>.showModal()`을 사용하면 브라우저가 자동으로 처리한다.

---

## 2. Popover API

### 기본 사용

가벼운 팝업(tooltip, dropdown, context menu)에 사용한다. top layer에 올라가므로 z-index가 불필요하다.

```html
<button popovertarget="menu">열기</button>
<div id="menu" popover>
  <!-- 메뉴 내용 -->
</div>
```

### 핵심 특성

- **Light-dismiss**: popover 바깥을 클릭하면 자동으로 닫힌다
- **Top layer**: z-index 없이 항상 최상단에 표시된다
- **`popover="auto"` (기본값)**: 열린 popover가 있으면 다른 auto popover가 열릴 때 자동으로 닫힌다
- **`popover="manual"`**: 수동 제어가 필요할 때 — light-dismiss가 적용되지 않는다

### Dialog vs Popover 선택 기준

| 기준 | `<dialog>` | Popover |
| --- | --- | --- |
| 용도 | 확인, 폼, 중요 결정 | tooltip, dropdown, 메뉴 |
| 모달 차단 | O (showModal) | X |
| 포커스 트랩 | 자동 | 없음 |
| Light-dismiss | 수동 구현 | 자동 |
| backdrop | 자동 | 없음 |

---

## 3. CSS Anchor Positioning

드롭다운이나 tooltip을 트리거 요소에 정확히 붙이는 CSS-only 패턴이다.

```css
.trigger {
  anchor-name: --trigger;
}

.dropdown {
  position: absolute;
  position-anchor: --trigger;
  top: anchor(bottom);
  left: anchor(left);
}
```

### `@position-try` 폴백

뷰포트 가장자리에서 잘릴 때 대체 위치를 지정한다.

```css
.dropdown {
  position-try-fallbacks: --above;
}

@position-try --above {
  top: auto;
  bottom: anchor(top);
}
```

> CSS Anchor Positioning은 2024 기준 Chromium에서 지원한다. 미지원 브라우저에서는 Floating UI 같은 JS 라이브러리로 폴백한다.

---

## 4. Portal / Teleport 패턴

### 문제

오버레이를 트리거 컴포넌트와 같은 DOM 위치에 렌더하면, 부모의 `overflow: hidden`, `z-index` 컨텍스트, `transform`에 갇혀 잘리거나 가려진다.

### 해결

오버레이를 DOM tree의 최상단(`<body>` 직하)으로 텔레포트한다.

- **React**: `createPortal(children, document.body)`
- **Vue**: `<Teleport to="body">...</Teleport>`

### 주의

- Portal로 옮겨도 React 이벤트 버블링은 원래 컴포넌트 트리를 따른다
- 접근성 관계(`aria-controls`, `aria-describedby`)는 명시적으로 연결해야 한다

---

## 5. 드롭다운 안티패턴

| 안티패턴 | 문제 | 해결 |
| --- | --- | --- |
| `overflow: hidden` 안에 `position: absolute` | 부모에 잘림 | Portal 또는 Popover API |
| 임의 z-index 값 (z-index: 9999) | z-index 전쟁, 관리 불가 | top layer (dialog/popover) 또는 semantic z-index scale |
| 인라인 마크업 (트리거 옆에 직접 배치) | DOM 구조에 종속, 스크롤 시 어긋남 | Portal + Floating UI 또는 CSS Anchor |
| JS로 좌표 직접 계산 | 리사이즈/스크롤 시 깨짐, 유지보수 어려움 | CSS Anchor Positioning 또는 Floating UI |

---

## 체크리스트

- [ ] 모달은 `<dialog>.showModal()`을 사용하는가
- [ ] 가벼운 팝업은 Popover API를 먼저 검토했는가
- [ ] 드롭다운이 `overflow: hidden` 부모에 갇히지 않는가
- [ ] z-index를 임의 숫자로 붙이지 않고 semantic scale 또는 top layer를 사용하는가
- [ ] 포커스 관리와 Esc 닫기가 동작하는가
