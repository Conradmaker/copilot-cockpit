# 시맨틱 HTML & 구조

HTML 요소를 올바르게 배치하고, 의미에 맞는 태그를 사용하는 것은 접근성의 시작이다.

---

## 인터랙티브 요소 중첩 금지

HTML과 접근성 기준에서 인터랙티브 요소(버튼, 링크 등) 안에 또 다른 인터랙티브 요소를 넣는 것은 **금지**다.

### 왜 문제인가?

1. **키보드 탐색이 혼란스럽다** - 어떤 버튼이 눌릴지 불분명
2. **스크린 리더가 잘못 읽을 수 있다** - "버튼 안에 또 다른 버튼"으로 인식
3. **포커스 순서가 꼬인다** - 모바일에서 의도치 않은 버튼이 눌릴 수 있음

### 인터랙티브 요소 목록

| 요소                                                                                                   | 조건                        |
| ------------------------------------------------------------------------------------------------------ | --------------------------- |
| `<a>`, `<button>`, `<details>`, `<embed>`, `<iframe>`, `<keygen>`, `<label>`, `<select>`, `<textarea>` | 항상                        |
| `<audio>`, `<video>`                                                                                   | `controls` 속성이 있는 경우 |
| `<img>`, `<object>`                                                                                    | `usemap` 속성이 있는 경우   |
| `<input>`                                                                                              | `type="hidden"`이 아닌 경우 |
| `<menu>`                                                                                               | `type="toolbar"`인 경우     |

### 패턴 1: 링크 안에 버튼

```tsx
// ❌ <a> 안에 <button> 중첩
<a href="/go-to">
  <Button>확인했어요.</Button>
</a>

// ✅ Button 컴포넌트가 <a>를 렌더링하도록 설정
<Button as="a" href="/go-to">
  확인했어요.
</Button>
```

### 패턴 2: 버튼 안에 버튼 (카드 UI)

카드 전체가 클릭 가능하면서 내부에 별도 버튼이 필요한 경우:

```tsx
// ❌ 버튼 중첩 + stopPropagation
<button>
  서비스 검토 관리
  <button aria-label="삭제" onClick={(e) => e.stopPropagation()}>x</button>
</button>

// ✅ 레이어링으로 분리
<div
  style={{ position: "relative", isolation: "isolate" }}
  className="wrapper"
  role="listitem"
  aria-label="서비스 검토 관리"
>
  <button
    className="detail-button"
    style={{ position: "absolute", inset: 0, opacity: 0 }}
  >
    상세보기
  </button>
  서비스 검토 관리
  <div style={{ position: "relative", zIndex: 2 }}>
    <button aria-label="삭제">x</button>
  </div>
</div>
```

> **포커스 스타일 팁:** 투명 버튼에 포커스 표시가 안 보일 수 있으니 `:focus-within`을 활용한다.
>
> ```css
> .wrapper:focus-within {
>   outline: 2px solid blue;
> }
> ```

### 포커스 표시를 지우지 않기

포커스 링은 키보드 사용자가 현재 위치를 파악하는 핵심 단서다. `outline: none` 또는 `outline-none`으로 기본 포커스를 제거했다면, 반드시 같은 수준 이상의 대체 표시를 제공해야 한다.

```css
/* ❌ 키보드 포커스가 사라짐 */
.button {
  outline: none;
}

/* ✅ 클릭에는 포커스 링을 숨기고, 키보드 포커스에는 명확히 표시 */
.button:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}
```

- 포커스 표시는 `:focus`보다 `:focus-visible`을 우선 사용한다. 마우스 클릭 때까지 항상 링이 보이면 시각적 노이즈가 커진다.
- 입력 + 버튼처럼 묶인 복합 컨트롤은 개별 요소보다 컨테이너에 `:focus-within` 스타일을 주는 편이 현재 활성 영역을 더 명확하게 보여준다.
- 커스텀 버튼, 링크, 카드형 인터랙션을 만들 때는 hover/active 상태와 별도로 focus-visible 상태를 반드시 확인한다.

---

## 테이블 행 링크

테이블 행 전체를 클릭 가능하게 만들 때, `<tr>`에 직접 `onClick`을 붙이면 안 된다.

### 문제점

```tsx
// ❌ tr에 직접 클릭 이벤트
<tr onclick="location.assign('/detail/김토스')">
  <td>
    김토스 <Icon />
  </td>
  <td>22</td>
  <td>공부</td>
</tr>
```

- 키보드로 포커스할 수 없다
- 스크린 리더에서 클릭 가능하다는 정보가 전달되지 않는다
- 브라우저의 링크 기능(새 창 열기, 링크 복사)을 사용할 수 없다

### ✅ 개선: CSS 가상 요소로 링크 영역 확장

```tsx
<style>
  .link::after {
    position: absolute;
    display: block;
    content: '';
    inset: 0;
  }
</style>

<tr style={{ position: "relative" }}>
  <td>
    김토스
    <IconLink
      label="자세히 보기"
      href="/detail/김토스"
      className="link"
    />
  </td>
  <td>22</td>
  <td>공부</td>
</tr>
```

**이점:**

- Tab 키로 링크에 포커스하고 Enter로 활성화 가능
- 스크린 리더에서 "링크"로 인식되어 클릭 가능함을 알려줌
- 브라우저 링크 기능(새 창 열기, 링크 복사) 사용 가능
- 행 전체가 클릭 가능하여 마우스 사용자의 편의성 유지

---

## 중복 이름 인터랙티브 요소 구분

같은 이름의 버튼이 여러 번 등장하면 스크린 리더 사용자가 각각을 구분할 수 없다.

### 문제점

```html
<!-- ❌ 두 버튼 모두 "선택, 버튼"으로 들림 -->
<div>
  <div>종이를 사용할 경우</div>
  <button>선택</button>
</div>
<div>
  <div>연필을 사용할 경우</div>
  <button>선택</button>
</div>
```

### ✅ 방법 1: aria-label로 설명 추가

```html
<button aria-label="종이를 사용할 경우에 선택">선택</button>
<button aria-label="연필을 사용할 경우에 선택">선택</button>
```

> ⚠️ `aria-label`을 사용하면 기존 시각적 텍스트가 스크린 리더에 노출되지 않는다. 가능하면 시각적 텍스트를 포함한 문장으로 작성한다.

### ✅ 방법 2: 리스트 마크업 + aria-labelledby

```html
<ul>
  <li aria-labelledby="paper-title">
    <div id="paper-title">종이를 사용할 경우</div>
    <button>선택</button>
  </li>
  <li aria-labelledby="pencil-title">
    <div id="pencil-title">연필을 사용할 경우</div>
    <button>선택</button>
  </li>
</ul>
```

### ✅ 방법 3: 버튼에도 aria-labelledby 직접 연결 (가장 확실)

```html
<ul>
  <li aria-labelledby="paper-title">
    <div id="paper-title">종이를 사용할 경우</div>
    <button id="paper-btn" aria-labelledby="paper-title paper-btn">선택</button>
  </li>
  <li aria-labelledby="pencil-title">
    <div id="pencil-title">연필을 사용할 경우</div>
    <button id="pencil-btn" aria-labelledby="pencil-title pencil-btn">선택</button>
  </li>
</ul>
<!-- 스크린 리더: "종이를 사용할 경우 선택, 버튼" -->
```

---

## 필수 레이블 (인터랙티브 요소에 이름 붙이기)

모든 인터랙티브 요소에는 반드시 접근 가능한 이름이 필요하다.

### 이름 부여 방법과 우선순위

| 순위 | 방법              | 예시                                                |
| ---- | ----------------- | --------------------------------------------------- |
| 1    | `<label>` 요소    | `<label for="name">이름</label><input id="name" />` |
| 2    | `aria-label`      | `<input aria-label="이름" />`                       |
| 3    | `aria-labelledby` | `<input aria-labelledby="heading" />`               |

### label 요소 사용 (권장)

```html
<!-- ✅ 가장 좋은 방법 -->
<label for="user-name">이름</label>
<input id="user-name" type="text" />
```

**장점:**

- 스크린 리더에게 입력 필드의 목적을 명확히 전달
- 레이블 클릭 시 연결된 입력 필드에 포커스 (터치 인터페이스에서 유용)
- 입력 중에도 항상 표시됨

### aria-label (디자인 제약 시 차선책)

```html
<input type="text" aria-label="이름" placeholder="이름을 입력하세요" />
```

### aria-labelledby (화면의 기존 텍스트 활용)

```html
<h2 id="address-heading">배송 주소</h2>
<input type="text" aria-labelledby="address-heading" />
```

### placeholder는 레이블의 대체재가 아니다

```html
<!-- ❌ placeholder만 사용 -->
<input type="email" placeholder="이메일" />

<!-- ✅ 레이블 + placeholder 보조 힌트 -->
<label for="email">이메일</label>
<input id="email" type="email" placeholder="example@email.com" />
```

### 그 외 인터랙티브 요소

```html
<!-- 버튼: 아이콘만 있을 때 -->
<button aria-label="닫기">
  <svg aria-hidden="true">...</svg>
</button>

<!-- 선택 요소 -->
<label for="country">국가 선택</label>
<select id="country">
  <option value="kr">대한민국</option>
  <option value="us">미국</option>
</select>
```
