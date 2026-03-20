# 접근성 기본 - 역할, 레이블, 상태

스크린 리더가 화면 요소를 올바르게 전달하기 위해 알아야 할 3가지 핵심 요소를 다룬다.

## 역할(Role)

UI 컴포넌트가 어떤 의미를 지니는지 스크린 리더가 이해하게 하려면 `role` 속성을 명확히 지정해야 한다.

### HTML 요소별 기본 역할 매핑

| 컴포넌트 | HTML 요소 | role 속성 | 설명 |
| --- | --- | --- | --- |
| 텍스트 | `<span>`, `<div>` | 없음 | 정보 전달 시 적절한 역할 지정 필요 |
| 입력창 | `<input>` | `role="textbox"` | 텍스트를 입력하는 요소 |
| 체크박스 | `<input type="checkbox">` | `role="checkbox"` | 여러 옵션 중 원하는 항목을 모두 선택 |
| 라디오 | `<input type="radio">` | `role="radiogroup"`, `role="radio"` | 여러 옵션 중 하나 선택 |
| 링크 | `<a>` | `role="link"` | 페이지 이동 요소 |
| 버튼 | `<button>` | `role="button"` | 동작을 수행하는 요소 |
| 다이얼로그 | `<dialog>` | `role="dialog"` | 다이얼로그 |
| 아코디언 | `<details>` `<summary>` | `role="group"` | 아코디언 |

### 언제 role을 명시해야 하나?

- HTML 기본 요소(`<button>`, `<input>`, `<a>` 등)는 이미 역할이 내장되어 있다
- `<div>`로 커스텀 요소를 만들거나, 탭(tab), 스위치(switch)처럼 기본 요소가 없을 때 명시적으로 `role`을 선언해야 한다

```tsx
// ❌ div에 role 없이 클릭 이벤트만 부여
<div onClick={handleClick}>클릭</div>

// ✅ role을 명시하여 버튼임을 알려줌
<div role="button" tabIndex={0} onClick={handleClick}>클릭</div>

// ✅✅ 가장 좋은 방법: 시맨틱 요소 사용
<button onClick={handleClick}>클릭</button>
```

---

## 레이블(Label)

레이블은 화면에 보이지 않는 텍스트를 스크린 리더에 전달한다. 특히 인터랙티브 요소(입력창, 버튼 등)에 텍스트가 없으면 중요한 상호작용을 놓칠 수 있다.

### 레이블 우선순위

스크린 리더는 다음 순서대로 이름을 읽는다:

| 순위 | 방법              | 설명                                           |
| ---- | ----------------- | ---------------------------------------------- |
| 1    | `aria-labelledby` | 가장 먼저 읽는 속성, 다른 요소의 텍스트를 참조 |
| 2    | `aria-label`      | `aria-labelledby`가 없을 경우 읽는 속성        |
| 3    | `<label>`         | ARIA 속성이 없을 경우 읽는 HTML 레이블         |
| 4    | `placeholder`     | 레이블 대용으로는 권장하지 않음                |
| 5    | 요소의 내용       | 위 속성들이 모두 없을 경우 내부 텍스트를 읽음  |

### 입력창 레이블

```tsx
// ❌ 레이블 없는 입력창 - "입력창"으로만 들림
<input type="text" />

// ✅ label 요소로 연결
<label htmlFor="address">주소</label>
<input type="text" id="address" />

// ✅ aria-label 사용 (시각적 레이블을 표시할 수 없을 때)
<input type="text" aria-label="상세주소" />
```

### 여러 입력창 그룹화

```tsx
// ✅ fieldset/legend로 그룹화 + 개별 aria-label
<fieldset>
  <legend>카드번호</legend>
  <input type="text" maxLength={4} aria-label="카드번호 첫번째 4자리" />
  <input type="text" maxLength={4} aria-label="카드번호 두번째 4자리" />
  <input type="text" maxLength={4} aria-label="카드번호 세번째 4자리" />
  <input type="text" maxLength={4} aria-label="카드번호 네번째 4자리" />
</fieldset>
// 스크린 리더: "카드번호, 그룹 / 카드번호 첫번째 4자리, 입력창 / ..."
```

### 아이콘 버튼 레이블

```tsx
// ❌ 아이콘만 있는 버튼 - "버튼"으로만 들림
<button><SearchIcon /></button>

// ✅ aria-label로 기능 설명
<button aria-label="검색"><SearchIcon /></button>

// ✅ 텍스트가 함께 있으면 aria-label 불필요
<button><SearchIcon /> 검색</button>
```

### 방향 버튼 레이블

```tsx
// ❌ "버튼, 8월, 버튼"으로 들림
<button><LeftArrowIcon /></button>
<span>8월</span>
<button><RightArrowIcon /></button>

// ✅ "지난 달, 버튼 / 8월 / 다음 달, 버튼"으로 들림
<button aria-label="지난 달"><LeftArrowIcon /></button>
<span>8월</span>
<button aria-label="다음 달"><RightArrowIcon /></button>
```

### aria-labelledby로 여러 텍스트 조합

```tsx
// 여러 ID를 공백으로 연결하면 순서대로 이어 붙여서 읽는다
<button id="paper-button" aria-labelledby="paper-title paper-button">
  선택
</button>
// 스크린 리더: "종이를 사용할 경우 선택, 버튼"
```

### 선택형 컴포넌트 레이블

```tsx
// ❌ "선택됨, 체크박스" - 무엇을 선택하는지 알 수 없음
<input type="checkbox" />

// ✅ "이메일 수신 동의, 선택됨, 체크박스"
<label>
  <input type="checkbox" checked />
  이메일 수신 동의
</label>
```

---

## 상태(State)

컴포넌트의 동작 변화(켜짐/꺼짐, 펼침/접힘 등)를 스크린 리더에 알려주려면 상태 속성을 설정해야 한다.

### 주요 aria 상태 속성

| 속성            | 의미                 | 적용 예시          |
| --------------- | -------------------- | ------------------ |
| `aria-checked`  | 체크 여부            | 체크박스, 스위치   |
| `aria-selected` | 선택 여부            | 탭, 리스트         |
| `aria-expanded` | 펼침 여부            | 아코디언, 드롭다운 |
| `aria-disabled` | 비활성화 여부        | 버튼 등            |
| `aria-current`  | 현재 위치 여부       | 네비게이션, 달력   |
| `aria-busy`     | 로딩 중 여부         | 데이터 로드 시     |
| `aria-live`     | 실시간 업데이트 알림 | 에러/알림 메시지   |

### aria-checked (체크 여부)

```tsx
// input 요소는 checked 사용
<input type="checkbox" checked={true} />

// input이 아닌 요소는 aria-checked 사용
<span role="checkbox" aria-checked={true} tabIndex={0}>
  체크박스
</span>
```

### aria-selected (선택 여부)

```tsx
// option 요소는 selected 사용
<select>
  <option value="1" selected>사과</option>
</select>

// option이 아닌 요소는 aria-selected 사용
<div role="listbox">
  <button role="option" aria-selected={true}>사과</button>
  <button role="option" aria-selected={false}>딸기</button>
</div>
```

### aria-expanded (펼침 여부)

```tsx
// details 요소는 open 사용
<details open={true}>
  <summary>펼침</summary>
  <p>내용</p>
</details>

// 그 외 요소는 aria-expanded 사용
<button aria-expanded={true}>펼침</button>
<p hidden={false}>내용</p>
```

### aria-disabled (비활성화 여부)

```tsx
// button/input은 disabled 사용
<button disabled={true}>비활성화</button>

// 그 외 요소는 aria-disabled 사용
<div role="switch" aria-checked={false} aria-disabled={true} tabIndex={0}>
  스위치
</div>
```

### aria-current (현재 위치)

```tsx
// 네비게이션에서 현재 페이지 표시
<nav aria-label="메뉴">
  <a href="/" aria-current="page">홈</a>
  <a href="/about">소개</a>
</nav>

// 달력에서 오늘 날짜 표시
<button role="option" aria-current="date">2025-11-13</button>
```

### aria-busy (로딩 중)

```tsx
<div aria-busy={true}>로딩 중</div>
```

### aria-live (실시간 알림)

| 값          | 동작                          | 사용 시점                  |
| ----------- | ----------------------------- | -------------------------- |
| `polite`    | 현재 읽던 내용을 마친 후 알림 | 검증 메시지, 업데이트 알림 |
| `assertive` | 즉시 읽기 중단 후 알림        | 오류/실패 메시지           |
| `off`       | 알리지 않음                   | -                          |

```tsx
// 입력 중 에러 메시지 (polite)
<input type="email" aria-describedby="error-msg" />
<p id="error-msg" aria-live="polite">이메일 형식이 올바르지 않습니다.</p>

// 긴급 오류 메시지 (assertive)
<p aria-live="assertive">인터넷 연결이 끊어졌습니다.</p>
```

> **참고:** `role="alert"` = `aria-live="assertive"`, `role="status"` = `aria-live="polite"`와 동일하게 동작한다.
