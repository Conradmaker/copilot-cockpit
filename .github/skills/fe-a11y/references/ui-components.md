# UI 컴포넌트별 접근성 패턴

각 UI 컴포넌트를 접근성 있게 구현하는 방법과 체크리스트를 다룬다.

---

## 모달(Modal / Dialog)

모달은 사용자의 주의를 끌어 중요한 정보나 작업을 처리할 때 사용한다. 모달이 열렸다는 것을 인식하고, **모달 내부에서만 상호작용**할 수 있어야 한다.

### ✅ 권장: `<dialog>` 요소 + `showModal()` 사용

```tsx
const ref = useRef<HTMLDialogElement>(null)

return (
  <>
    <button aria-haspopup="dialog" onClick={() => ref.current?.showModal()}>
      모달 열기
    </button>
    <dialog ref={ref} aria-labelledby="modal-title">
      <h3 id="modal-title">다음에 다시 시도해 주세요</h3>
      <button onClick={() => ref.current?.close()}>확인</button>
    </dialog>
  </>
)
```

`showModal()`을 사용하면 브라우저가 자동으로 제공하는 기능:

- 쌓임맥락과 상관없이 최상위에 위치
- 다이얼로그 내부로 포커스 자동 이동
- 다이얼로그 내부 요소만 포커스 가능 (포커스 트랩)
- ESC 키로 닫기
- 닫으면 원래 포커스로 복원

> ⚠️ `show()` 또는 `<dialog open={true}>`는 "비대화형 다이얼로그"로 판단되어 위 기능을 사용할 수 없다.

### `<dialog>` 없이 구현할 때

`role="dialog"`와 `aria-modal="true"`를 사용하고, 추가로 직접 구현해야 할 것들:

```tsx
{
  isOpen && (
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <h3 id="modal-title">다음에 다시 시도해 주세요</h3>
      <button onClick={closeModal}>확인</button>
    </div>
  )
}
```

#### 1. 포커스 저장과 복원

```tsx
const buttonRef = useRef<HTMLButtonElement>(null)
const closeModal = () => {
  setIsOpen(false)
  requestAnimationFrame(() => {
    buttonRef.current?.focus()
  })
}
```

#### 2. ESC 키로 닫기

```tsx
useEffect(() => {
  if (!isOpen) return
  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === "Escape") onClose()
  }
  document.addEventListener("keydown", handleEscape)
  return () => document.removeEventListener("keydown", handleEscape)
}, [isOpen, onClose])
```

#### 3. 배경 콘텐츠 숨기기 (inert)

```tsx
useEffect(() => {
  const main = document.querySelector("main")
  if (isOpen) {
    main?.setAttribute("inert", "true")
  } else {
    main?.removeAttribute("inert")
  }
  return () => main?.removeAttribute("inert")
}, [isOpen])
```

#### 4. 스크롤 체인 끊기

모달, 드로어, 바텀시트처럼 자체 스크롤 영역이 있는 컴포넌트는 내부 끝에 도달했을 때 배경 페이지가 함께 스크롤되지 않도록 제어한다.

```css
.dialog-body {
  overflow: auto;
  overscroll-behavior: contain;
}
```

`overscroll-behavior: contain`을 주면 터치 스크롤과 트랙패드 스크롤이 배경으로 전파되는 것을 막을 수 있다.

### 모달 체크리스트

- [ ] `<dialog>` + `showModal()` 사용 (또는 `role="dialog"` + `aria-modal="true"`)
- [ ] `aria-labelledby` 또는 `aria-label`로 모달 제목 연결
- [ ] 모달 열릴 때 포커스를 내부로 이동
- [ ] 모달 닫힐 때 원래 포커스로 복원
- [ ] ESC 키로 닫기 가능
- [ ] 모달 열려있는 동안 배경 콘텐츠 상호작용 차단
- [ ] 스크롤 가능한 본문이 있으면 `overscroll-behavior: contain` 적용
- [ ] 트리거 버튼에 `aria-haspopup="dialog"` 추가

---

## 스위치(Switch)

스위치는 두 가지 상태(ON/OFF) 중 하나를 선택할 때 사용한다.

### ✅ input + label 방식

```tsx
<label>
  <input type="checkbox" role="switch" checked={isOn} hidden />
  <img src={`./toggle-icon-${isOn ? "on" : "off"}.png`} alt="" />
  알림 설정
</label>
// 스크린 리더: "알림 설정, 전환 버튼, 켬"
```

### ✅ 커스텀 요소 방식

```tsx
<span role="switch" aria-checked={isOn} tabIndex={0}>
  <img src={`./toggle-icon-${isOn ? "on" : "off"}.png`} alt="" />
  알림 설정
</span>
```

### 레이블 적용 패턴

```tsx
// 1. 내부 텍스트가 있는 경우 → aria-label 불필요
<span role="switch" aria-checked={true} tabIndex={0}>
  알림 설정
</span>

// 2. 외부 텍스트가 있는 경우 → aria-labelledby
<span id="email-switch">이메일 알림</span>
<span role="switch" aria-checked={true} tabIndex={0} aria-labelledby="email-switch" />

// 3. 아이콘만 있는 경우 → aria-label 필수
<span role="switch" aria-checked={true} tabIndex={0} aria-label="다크 모드">
  <img src="./toggle-icon.png" alt="" />
</span>
```

### 스위치 체크리스트

- [ ] `role="switch"` 설정
- [ ] `checked` (input) 또는 `aria-checked` (커스텀)로 현재 상태 명시
- [ ] `tabIndex={0}` (커스텀 요소일 때) 으로 키보드 포커스 가능
- [ ] Space 키로 상태 변경 가능

---

## 탭(Tab)

탭은 관련된 콘텐츠를 그룹화하여 빠르게 접근할 수 있도록 하는 컴포넌트다.

### ✅ 탭 목록 + 탭 패널

```tsx
<div role="tablist" aria-label="메뉴">
  <button role="tab" aria-selected={false} id="home-tab">홈</button>
  <button role="tab" aria-selected={false} id="interest-tab">관심</button>
  <button role="tab" aria-selected={true} id="feed-tab" aria-controls="feed-panel">
    피드
  </button>
</div>
<ul role="tabpanel" id="feed-panel" aria-labelledby="feed-tab">
  <li>
    <h3>탭 콘텐츠</h3>
    <p>피드 탭의 내용이에요.</p>
  </li>
</ul>
```

**스크린 리더:** "메뉴, 탭 목록 / 홈, 탭 / 관심, 탭 / 피드, 선택됨, 탭"

### 역할 설명

| 속성              | 역할                         |
| ----------------- | ---------------------------- |
| `role="tablist"`  | 탭 버튼 그룹 컨테이너        |
| `role="tab"`      | 개별 탭 버튼                 |
| `role="tabpanel"` | 활성화된 탭의 콘텐츠 영역    |
| `aria-selected`   | 현재 선택된 탭 표시          |
| `aria-controls`   | 탭 버튼이 제어하는 패널의 id |
| `aria-labelledby` | 패널과 연결된 탭 버튼의 id   |

> ⚠️ 비활성 탭의 패널은 `hidden` 속성으로 숨겨야 한다. `aria-selected`만으로는 스크린 리더가 구분하지 못한다.

### 탭 체크리스트

- [ ] 탭 목록은 `role="tablist"`로 감싸기
- [ ] 각 탭은 `role="tab"` 설정
- [ ] 활성 탭: `aria-selected="true"`, 비활성 탭: `aria-selected="false"`
- [ ] 탭 패널: `role="tabpanel"` + `aria-labelledby`로 탭 버튼 연결
- [ ] 비활성 탭 패널은 `hidden` 속성으로 숨기기
- [ ] 아이콘만 있거나 텍스트가 모호한 탭에는 `aria-label` 추가

---

## 체크박스(Checkbox)

체크박스는 여러 옵션 중 하나 이상을 선택할 수 있는 컴포넌트다.

### ✅ fieldset/legend + label 연결

```tsx
<fieldset>
  <legend>수신 동의 설정</legend>
  <div>
    <input type="checkbox" id="email" checked />
    <label htmlFor="email">이메일 수신 동의</label>
  </div>
  <div>
    <input type="checkbox" id="sms" />
    <label htmlFor="sms">문자 수신 동의</label>
  </div>
</fieldset>
// 스크린 리더: "수신 동의 설정, 그룹 / 이메일 수신 동의, 체크박스, 선택됨 / ..."
```

### 커스텀 체크박스

```tsx
const [checked, setChecked] = useState(false)

<div
  role="checkbox"
  aria-checked={checked}
  tabIndex={0}
  onClick={() => setChecked(!checked)}
  onKeyDown={(e) => {
    if (e.key === " ") {
      e.preventDefault()
      setChecked(!checked)
    }
  }}
>
  <span>커스텀 체크박스</span>
  {checked && <span>✓</span>}
</div>
```

### 체크박스 체크리스트

- [ ] `fieldset`/`legend`로 그룹 묶기
- [ ] 각 `input`과 `label`을 `id`/`htmlFor`로 연결
- [ ] 커스텀일 때: `role="checkbox"` + `aria-checked` + `tabIndex={0}`
- [ ] Space 키로 체크 상태 토글 가능

---

## 라디오(Radio)

라디오 버튼은 여러 옵션 중 **하나만** 선택할 수 있는 컴포넌트다.

### ✅ fieldset/legend + name 속성

```tsx
<fieldset>
  <legend>안녕하세요! 사용하실 국가를 선택해주세요</legend>
  <label htmlFor="ko">대한민국</label>
  <input type="radio" name="country" id="ko" checked />
  <label htmlFor="au">호주</label>
  <input type="radio" name="country" id="au" />
</fieldset>
// 스크린 리더: "안녕하세요! 사용하실 국가를 선택해주세요, 그룹 / 대한민국, 라디오 버튼, 선택됨"
```

### fieldset 대신 role="radiogroup"

```tsx
<div role="radiogroup" aria-labelledby="payment-title">
  <h3 id="payment-title">결제 방법</h3>
  <input type="radio" name="payment" id="card" />
  <label htmlFor="card">카드 결제</label>
  <input type="radio" name="payment" id="bank" />
  <label htmlFor="bank">계좌 이체</label>
</div>
```

### name 속성의 중요성

- 같은 그룹의 라디오에는 **동일한 `name`** 사용 → 하나만 선택되도록 보장
- 서로 다른 그룹에는 **다른 `name`** 사용 → 독립적으로 동작

### 커스텀 라디오

```tsx
<div
  role="radio"
  aria-checked={checked}
  tabIndex={0}
  onClick={() => setChecked(!checked)}
  onKeyDown={(e) => {
    if (e.key === " ") {
      e.preventDefault()
      setChecked(!checked)
    }
  }}
>
  <span>커스텀 라디오 버튼</span>
  {checked && <span>✓</span>}
</div>
```

### 라디오 체크리스트

- [ ] `fieldset`/`legend`로 그룹 묶기 (또는 `role="radiogroup"` + `aria-labelledby`)
- [ ] 같은 그룹에 동일한 `name` 속성
- [ ] 각 `input`과 `label`을 `id`/`htmlFor`로 연결
- [ ] 커스텀일 때: `role="radio"` + `aria-checked` + `tabIndex={0}`
- [ ] 화살표 키로 라디오 간 이동 가능

---

## 아코디언(Accordion)

아코디언은 정보를 공간을 절약하면서 단계적으로 제공하는 컴포넌트다.

### ✅ 권장: `<details>` + `<summary>` 사용

```tsx
<details open={isOpen} onToggle={handleToggle}>
  <summary>토스뱅크의 한도제한계좌는 어떻게 해제할 수 있나요?</summary>
  <p>금융거래목적을 확인할 수 있는 증빙서류를 제출하여 한도 계좌 해제 신청을 할 수 있어요.</p>
</details>
```

### 커스텀 아코디언

```tsx
<div>
  <button aria-expanded={isOpen} aria-controls="panel-1" onClick={handleClick}>
    토스뱅크의 한도제한계좌는 어떻게 해제할 수 있나요?
  </button>
  <div id="panel-1" role="region" aria-labelledby="button-1" hidden={!isOpen}>
    금융거래목적을 확인할 수 있는 증빙서류를 제출하여 한도 계좌 해제 신청을 할 수 있어요.
  </div>
</div>
```

**스크린 리더:** "토스뱅크의 한도제한계좌는..., 버튼, 펼쳐짐"

### 아코디언 체크리스트

- [ ] `<details>`/`<summary>` 사용 (또는 `aria-expanded` + `aria-controls`)
- [ ] 헤더는 버튼으로 구현 + `aria-expanded`로 열림/닫힘 상태 전달
- [ ] 패널: `role="region"` + `aria-labelledby`로 버튼 id 참조
- [ ] `aria-expanded`와 `hidden` 상태 항상 동기화
- [ ] 아이콘만 있는 헤더에는 `aria-label` 필수
