# 반응형 디자인

모바일 퍼스트 breakpoint와 capability 기반 스타일링으로 모든 디바이스를 대응한다.

---

## 1. Breakpoints

Tailwind는 **모바일 퍼스트**다. 기본 스타일이 모바일이고, prefix로 더 큰 화면을 추가한다.

| Prefix | Min Width | 대표 디바이스        |
| ------ | --------- | -------------------- |
| (none) | 0         | 모바일 기본          |
| `sm:`  | 640px     | 대형 폰 / 소형 태블릿 |
| `md:`  | 768px     | 태블릿 (iPad 세로)   |
| `lg:`  | 1024px    | 소형 랩탑 (iPad 가로) |
| `xl:`  | 1280px    | 데스크톱             |
| `2xl:` | 1536px    | 대화면               |

---

## 2. Show/Hide 패턴

```tsx
// 데스크톱 네비게이션 (모바일 숨김)
<nav className="hidden lg:flex h-stack gap-4">

// 모바일 메뉴 버튼 (데스크톱 숨김)
<button className="lg:hidden">
  <MenuIcon />
</button>

// 텍스트 전환
<span className="md:hidden">짧은 텍스트</span>
<span className="hidden md:inline">긴 텍스트</span>
```

---

## 3. 반응형 레이아웃

### 스택 전환

```tsx
<div className={cn(
  "v-stack gap-4",        // 모바일: 세로
  "md:h-stack md:gap-6",  // 태블릿+: 가로
  "lg:gap-8",             // 랩탑+: 간격 확대
)}>
```

### 그리드 컬럼

```tsx
// 모바일 1열  →  태블릿 2열  →  데스크톱 3열
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

### 반응형 너비

```tsx
<aside className="w-full md:w-64 lg:w-80">
<div className="w-full px-4 md:px-8 lg:max-w-6xl lg:mx-auto">
```

---

## 4. 반응형 타이포그래피

### 텍스트 스케일

| 클래스      | 크기 | 용도                      |
| ----------- | ---- | ------------------------- |
| `text-xs`   | 12px | 캡션, 뱃지 라벨           |
| `text-sm`   | 14px | 보조 텍스트, 모바일 본문  |
| `text-base` | 16px | 본문                      |
| `text-lg`   | 18px | 큰 본문, 부제목           |
| `text-xl`   | 20px | 소제목                    |
| `text-2xl`  | 24px | 섹션 제목                 |
| `text-3xl`  | 30px | 페이지 제목               |
| `text-4xl`  | 36px | 히어로 제목               |

### 패턴

```tsx
// 페이지 제목
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">

// 본문
<p className="text-sm md:text-base leading-relaxed">

// 캡션
<span className="text-xs md:text-sm text-muted-foreground">
```

breakpoint 변경은 2~3단계로 충분하다. 5단계 이상은 지양한다.

### 줄임

```tsx
// 한 줄 truncate
<p className="truncate">

// 다중 줄 clamp
<p className="line-clamp-2 md:line-clamp-3">
```

---

## 5. 반응형 간격

```tsx
// 패딩
<div className="p-4 md:p-6 lg:p-8 xl:p-12">

// 갭
<div className="v-stack gap-4 md:gap-6 lg:gap-8">

// 마진
<section className="mt-8 md:mt-12 lg:mt-16">
```

---

## 6. Capability 기반 디자인

디바이스 이름("모바일", "데스크톱")이 아닌 **입력 방식**에 따라 스타일한다.

### pointer-coarse / pointer-fine

터치 디바이스에서 터치 타겟을 키운다:

```tsx
<button className="h-10 w-10 pointer-coarse:h-12 pointer-coarse:w-12">
  <Icon />
</button>
```

### hover 가능 여부

hover 효과는 hover를 지원하는 디바이스에서만 적용한다:

```tsx
<button className="bg-gray-900 text-white hover:bg-gray-800">
  Primary
</button>
```

### 규칙

1. "모바일 vs 데스크톱" 가정을 UI 동작에 적용하지 않는다
2. 터치 타겟 크기는 `pointer-coarse:` / `pointer-fine:`으로 조정한다
3. hover 전용 affordance는 hover 가능한 디바이스에서만 노출한다
4. breakpoint는 레이아웃 전환에 사용하고, 디바이스 특정 너비를 타겟하지 않는다

---

## 빠른 체크리스트

- 기본 스타일이 모바일이고, prefix로 더 큰 화면을 추가하는가? (모바일 퍼스트)
- breakpoint 변경이 2~3단계를 넘지 않는가?
- `hidden`/`block` 패턴으로 불필요한 콘텐츠를 적절히 숨기는가?
- 터치 디바이스에서 터치 타겟이 충분히 큰가? (`pointer-coarse:` 활용)
- hover 효과가 hover를 지원하지 않는 디바이스에서도 접근 가능한가?
