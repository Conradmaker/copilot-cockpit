# API Reference 작성 가이드

이 문서는 API reference 문서의 카테고리별 템플릿, 공통 규칙, OpenAPI 연동 패턴을 다룬다.

---

## API 카테고리

API reference를 쓰기 전에, 문서화할 API가 어떤 카테고리에 속하는지 먼저 고른다.

| 카테고리 | 대상 | 핵심 구조 |
|---------|-----|---------|
| **Function** | 함수, 메서드, 유틸리티 | Signature → Params/Returns → Methods table → Examples |
| **Component** | React/Vue 등 UI 컴포넌트 | Props summary table → Per-prop docs → Examples |
| **File convention** | 파일 기반 라우팅 규칙 | Definition → Code convention → Props → Behavior → Examples |
| **Directive** | 컴파일러/런타임 지시어 | Definition → Usage → Constraints → Reference |
| **Config option** | 설정 옵션, 환경 변수 | Definition → Config code → Behavioral sections |
| **REST endpoint** | HTTP API endpoint | Method/Path → Request → Response → Errors → Examples |

---

## 공통 규칙

카테고리에 관계없이 모든 API reference에 적용되는 규칙이다.

### 1. 첫 문장은 정의다

API가 무엇을 하는지 한 문장으로 정의한다. 배경이나 감상은 쓰지 않는다.

```
✅ "`cookies` is an async function that reads HTTP request cookies in Server Components."
✅ "POST /api/users creates a new user account and returns the created user object."
❌ "This powerful function lets you easily manage cookies."
❌ "The Users API provides a comprehensive set of endpoints."
```

### 2. 정의 직후에 코드를 보여준다

첫 문장 다음에 바로 최소 동작 코드를 넣는다. Reference 섹션보다 앞이다.

```tsx filename="app/page.tsx"
import { cookies } from 'next/headers'

export default async function Page() {
  const cookieStore = await cookies()
  const theme = cookieStore.get('theme')
  return <p>Theme: {theme?.value}</p>
}
```

### 3. 테이블 vs 서브섹션

- prop/param이 한 줄 설명이면 **테이블**을 쓴다
- 코드 예시나 상세 설명이 필요하면 **`#### propName` 서브섹션**을 쓴다
- 같은 페이지 안에서 두 방식을 혼용할 수 있다

### 4. 기계적·관찰 가능한 언어

- "Returns an object" (O) vs "gives you an object" (X)
- "Accepts a string" (O) vs "you can conveniently pass" (X)
- 금지 수식어: powerful, easily, simply, seamlessly, best way

### 5. Version History 테이블

변경 이력이 있는 API는 문서 맨 아래에 Version History를 넣는다.

```markdown
## Version History

| Version   | Changes                                    |
| --------- | ------------------------------------------ |
| `v15.0.0` | `cookies` is now async. Returns a Promise. |
| `v13.0.0` | `cookies` introduced.                      |
```

새로 도입된 API는 첫 릴리스 전까지 이 섹션을 생략한다.

### 6. 링크와 참조

- 관련 API는 상대 경로로 링크한다
- "자세한 내용은 문서를 참조하세요" 대신 구체적 링크를 건다
- 같은 페이지 안에서 중복 설명하지 않고 해당 섹션으로 링크한다

### 7. em dash 금지

em dash(—) 대신 마침표, 쉼표, 괄호를 사용한다.

---

## 카테고리별 템플릿

### Function

````markdown
---
title: {functionName}
description: API Reference for the {functionName} function.
---

{한 문장 정의: 무엇을 하고, 어디서 쓰는가.}

```tsx filename="path/to/file.tsx"
// 최소 동작 코드
```

## Reference

### Parameters

| Parameter | Type     | Required | Description              |
| --------- | -------- | -------- | ------------------------ |
| `name`    | `string` | Yes      | The name of the cookie.  |
| `options` | `object` | No       | Configuration options.   |

### Returns

{반환 타입과 설명. 반환값에 메서드가 있으면 Methods 테이블로 정리한다.}

| Method   | Return Type     | Description                     |
| -------- | --------------- | ------------------------------- |
| `get()`  | `object`        | Gets a cookie by name.          |
| `set()`  | `void`          | Sets a cookie with options.     |

### Options

| Option    | Type      | Default | Description                |
| --------- | --------- | ------- | -------------------------- |
| `path`    | `string`  | `'/'`   | Cookie path.               |
| `secure`  | `boolean` | `false` | HTTPS only.                |

## Good to know

- {기본 동작이나 암묵적 효과}
- {주의사항, 버전별 차이}
- {edge case}

## Examples

### {예시 이름}

{1~2문장 맥락.}

```tsx filename="path/to/file.tsx"
// 완전한 동작 코드
```

## Version History

| Version   | Changes                    |
| --------- | -------------------------- |
| `vX.Y.Z`  | {What changed.}            |
````

### Component

````markdown
---
title: {ComponentName}
description: API Reference for the {ComponentName} component.
---

{한 문장 정의.}

```tsx filename="path/to/file.tsx"
// 최소 동작 코드
```

## Reference

### Props

| Prop       | Example             | Type      | Required |
| ---------- | ------------------- | --------- | -------- |
| `href`     | `href="/dashboard"` | `string`  | Yes      |
| `replace`  | `replace`           | `boolean` | No       |

#### href

{설명 + 코드 + 값 테이블 (필요시).}

#### replace

{설명 + 코드.}

## Good to know

- {기본 동작}
- {주의사항}

## Examples

### {예시 이름}

{맥락 + 코드.}

## Version History

| Version   | Changes              |
| --------- | -------------------- |
| `vX.Y.Z`  | {What changed.}      |
````

### REST Endpoint

````markdown
---
title: {Method} {Path}
description: {한 문장 설명}
---

{한 문장 정의: 무엇을 하는 endpoint인가.}

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

## Request

### Path Parameters

| Parameter | Type     | Required | Description        |
| --------- | -------- | -------- | ------------------ |
| `id`      | `string` | Yes      | The user ID.       |

### Query Parameters

| Parameter | Type     | Default | Description          |
| --------- | -------- | ------- | -------------------- |
| `limit`   | `number` | `20`    | Items per page.      |

### Request Body

```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

| Field   | Type     | Required | Description          |
| ------- | -------- | -------- | -------------------- |
| `name`  | `string` | Yes      | User's display name. |
| `email` | `string` | Yes      | Email address.       |

## Response

### 201 Created

```json
{
  "id": "usr_abc123",
  "name": "Alice",
  "email": "alice@example.com",
  "created_at": "2026-02-08T10:00:00Z"
}
```

### Error Responses

| Status | Code              | Description                   |
| ------ | ----------------- | ----------------------------- |
| `400`  | `invalid_request` | Missing or invalid parameters |
| `409`  | `already_exists`  | Email already registered      |

## Examples

### {예시 이름}

{맥락 + 코드.}

## Version History

| Version | Changes             |
| ------- | ------------------- |
| `v2.0`  | {What changed.}     |
````

### Config Option

````markdown
---
title: {optionName}
description: Configuration reference for {optionName}.
---

{한 문장 정의.}

```ts filename="next.config.ts"
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  optionName: 'value',
}

export default nextConfig
```

## Reference

{옵션별 상세. 단순하면 테이블, 복잡하면 서브섹션.}

| Option       | Type      | Default   | Description              |
| ------------ | --------- | --------- | ------------------------ |
| `optionName` | `string`  | `''`      | What it controls.        |

## Good to know

- {기본 동작}
- {주의사항}

## Examples

### {예시 이름}

{맥락 + 코드.}
````

---

## OpenAPI 3.1 연동

OpenAPI spec이 있는 프로젝트에서 API reference를 쓸 때 적용하는 패턴이다.

### Spec을 source of truth로 사용

- OpenAPI spec의 path, parameter, schema 정의를 reference 문서의 근거로 사용한다
- spec과 문서가 불일치하면 spec을 기준으로 문서를 수정한다
- spec에 `description`, `example` 필드가 있으면 문서에 그대로 반영한다

### 인증·보안 섹션

- OpenAPI의 `securitySchemes`를 기반으로 인증 방식을 문서화한다
- 인증 섹션은 개별 endpoint보다 앞에 두거나, 별도 페이지로 분리한다
- OAuth 2.0 flow를 쓸 때는 flow 다이어그램 또는 단계별 설명을 포함한다

### Error envelope

- error response는 일관된 포맷(error envelope)을 먼저 설명하고, endpoint별 에러 코드를 나열한다
- HTTP status code + application error code를 함께 문서화한다

---

## 유형별 셀프 리뷰 체크리스트

- [ ] 첫 문장이 API 정의로 시작한다 (배경이나 감상이 아니다)
- [ ] 정의 직후에 최소 동작 코드가 있다
- [ ] 코드 블록에 언어 태그와 파일 경로가 있다
- [ ] Parameters/Props 테이블이 Type, Required, Default, Description을 포함한다
- [ ] 복잡한 param/prop에는 `####` 서브섹션 + 코드 예시가 있다
- [ ] "Good to know" 섹션에 기본 동작, 주의사항, edge case가 있다
- [ ] 금지 수식어(powerful, easily, simply)가 없다
- [ ] em dash가 없다
- [ ] 변경 이력이 있는 API에 Version History 테이블이 있다
- [ ] 관련 API 링크가 상대 경로로 잘 연결되어 있다
