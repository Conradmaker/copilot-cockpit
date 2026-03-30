# Configuration & SDK Reference 작성 가이드

이 문서는 configuration reference, CLI reference, SDK documentation, 환경변수 문서화 패턴을 다룬다.

---

## Configuration Reference

### 목표

독자가 설정 옵션을 빠르게 찾아서, 무엇을 제어하는지 알고, 올바른 값을 설정하는 것이 목표다.

### Config 옵션 테이블 포맷

설정 문서의 핵심은 옵션 테이블이다. 아래 포맷을 표준으로 사용한다.

```markdown
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `port` | `number` | `3000` | Server listening port. |
| `host` | `string` | `'localhost'` | Server hostname. |
| `debug` | `boolean` | `false` | Enables verbose logging. |
| `timeout` | `number` | `30000` | Request timeout in milliseconds. |
```

### 필수 컬럼

| 컬럼 | 역할 | 생략 가능 |
|------|-----|---------|
| **Option** | 옵션 이름 (코드와 동일하게) | 불가 |
| **Type** | 값의 타입 | 불가 |
| **Default** | 기본값. 기본값이 없으면 `required`로 표시 | 불가 |
| **Description** | 한 줄 설명. 이 옵션이 무엇을 제어하는지 | 불가 |

### 복잡한 옵션

한 줄로 설명할 수 없는 옵션은 테이블 아래에 서브섹션으로 확장한다.

```markdown
### `database`

Database connection configuration.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `database.host` | `string` | `'localhost'` | Database hostname. |
| `database.port` | `number` | `5432` | Database port. |
| `database.name` | `string` | — | Database name. Required. |
| `database.ssl` | `boolean \| object` | `false` | SSL configuration. |

#### `database.ssl`

When set to `true`, uses default SSL settings. Pass an object for custom configuration:

\`\`\`ts
{
  ssl: {
    rejectUnauthorized: true,
    ca: '/path/to/ca.pem',
  }
}
\`\`\`
```

### 전체 템플릿

```markdown
# Configuration Reference

{한 문장: 이 문서에서 다루는 설정 범위.}

## Quick Start

\`\`\`ts filename="config.ts"
// 최소 동작 설정. 기본값만으로 동작하는 예시.
export default {
  port: 3000,
}
\`\`\`

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `port` | `number` | `3000` | Server listening port. |
| ... | ... | ... | ... |

### `{complexOption}`

{상세 설명 + 코드 예시.}

## Examples

### {사용 시나리오 이름}

{맥락 한 문장.}

\`\`\`ts filename="config.ts"
// 해당 시나리오의 완전한 설정
\`\`\`

## Environment Variables

| Variable | Maps to | Default |
|----------|---------|---------|
| `PORT` | `port` | `3000` |
| `DATABASE_URL` | `database.url` | — |
```

### 작성 규칙

- **기본값이 포함된 코드를 먼저 보여준다.** 독자는 옵션 목록을 읽기 전에 "기본으로 어떻게 생겼는지"를 본다
- Option 이름은 코드에서 사용하는 이름과 정확히 같아야 한다
- Type은 코드의 타입과 일치한다. `string | number` 같은 유니온 타입도 표시한다
- Default가 없으면 `required`로 표시한다. 빈 칸으로 두면 독자가 혼동한다
- nested 옵션은 dot notation(`database.host`)이나 서브섹션으로 표현한다

---

## CLI Reference

### 목표

독자가 CLI 명령어를 빠르게 찾아서 올바른 옵션과 함께 사용하는 것이 목표다.

### 명령어 구조

````markdown
## `{command} {subcommand}`

{한 문장: 이 명령어가 무엇을 하는가.}

### Usage

```bash
{command} {subcommand} [options] <arguments>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<name>` | Yes | The name of the resource to create. |

### Options

| Option | Alias | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output` | `-o` | `string` | `'json'` | Output format. |
| `--verbose` | `-v` | `boolean` | `false` | Enable verbose output. |
| `--force` | `-f` | `boolean` | `false` | Skip confirmation. |

### Examples

```bash
# 기본 사용
{command} {subcommand} my-resource

# 옵션과 함께
{command} {subcommand} my-resource --output table --verbose
```
````

### 작성 규칙

- Usage 라인에서 필수 인자는 `<angle brackets>`, 선택 인자는 `[square brackets]`로 표기한다
- Alias(단축 옵션)가 있으면 별도 컬럼으로 표시한다
- 실행 가능한 예시를 최소 2개 포함한다 (기본 사용 + 옵션 포함)
- 위험한 옵션(`--force`, `--delete`)에는 설명에 주의 문구를 넣는다

---

## SDK Documentation

### 목표

독자가 SDK를 설치하고, 초기화하고, 첫 번째 API 호출을 완료하는 것이 목표다.

### 구조: Install → Initialize → Use → Handle errors

```markdown
# {SDK Name}

{한 문장: 이 SDK가 무엇을 제공하는가.}

## Installation

\`\`\`bash
npm install {package-name}
\`\`\`

## Quick Start

\`\`\`ts filename="app.ts"
import { Client } from '{package-name}'

const client = new Client({
  apiKey: process.env.API_KEY,
})

const result = await client.resources.list()
console.log(result)
\`\`\`

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiKey` | `string` | — | API key. Required. |
| `baseUrl` | `string` | `'https://api.example.com'` | Base URL. |
| `timeout` | `number` | `30000` | Request timeout (ms). |

## Usage

### {Resource/Method}

{정의 + 코드 예시.}

\`\`\`ts
const user = await client.users.get('user-id')
\`\`\`

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `string` | Yes | User ID. |

#### Returns

{반환 타입 + 예시.}

### Error Handling

\`\`\`ts
import { ApiError } from '{package-name}'

try {
  const result = await client.resources.create({ name: 'test' })
} catch (error) {
  if (error instanceof ApiError) {
    console.error(error.status, error.code, error.message)
  }
}
\`\`\`

| Error Code | Status | Description |
|------------|--------|-------------|
| `invalid_request` | 400 | Missing or invalid parameters. |
| `unauthorized` | 401 | Invalid or expired API key. |
| `rate_limited` | 429 | Too many requests. |
```

### 작성 규칙

- **Quick Start는 5줄 이내 코드로 첫 번째 동작을 보여준다**
- 인증 설정은 환경변수를 사용하는 예시를 기본으로 한다 (하드코딩 금지)
- Error Handling 섹션을 반드시 포함한다. 에러 타입, 코드, 대응 방법을 보여준다
- 여러 언어를 지원하면 언어별로 코드 블록을 병렬 배치한다

---

## 환경변수 문서화

### 테이블 포맷

```markdown
## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string. |
| `API_KEY` | Yes | — | API authentication key. |
| `PORT` | No | `3000` | Server port. |
| `NODE_ENV` | No | `'development'` | Runtime environment. |
| `LOG_LEVEL` | No | `'info'` | Logging level: `debug`, `info`, `warn`, `error`. |
```

### `.env.example` 패턴

```markdown
### Setup

Copy the example file and fill in your values:

\`\`\`bash
cp .env.example .env
\`\`\`

\`\`\`bash filename=".env.example"
# Required
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
API_KEY=your-api-key-here

# Optional
PORT=3000
NODE_ENV=development
LOG_LEVEL=info
\`\`\`
```

### 작성 규칙

- Required 여부를 반드시 표시한다
- 기본값이 있으면 명시한다. 없으면 Required=Yes로 표시한다
- `.env.example` 파일을 항상 함께 문서화한다
- 시크릿 값(API key, password)은 예시에 `your-xxx-here` 형태로 표기한다. 실제 값을 넣지 않는다
- 허용 값이 제한적이면(`debug | info | warn | error`) Description에 나열한다

---

## 유형별 셀프 리뷰 체크리스트

### Configuration Reference

- [ ] 기본값이 포함된 코드가 Options 테이블보다 앞에 있다
- [ ] 모든 옵션에 Option, Type, Default, Description이 있다
- [ ] Default가 없는 필수 옵션은 `required`로 표시되어 있다
- [ ] 복잡한 옵션은 서브섹션으로 확장되어 있다
- [ ] 환경변수 매핑 테이블이 있다 (해당하는 경우)

### CLI Reference

- [ ] Usage 라인에 `<필수>` / `[선택]` 표기가 올바르다
- [ ] Options에 Alias가 표시되어 있다 (있는 경우)
- [ ] 실행 가능한 예시가 최소 2개 있다
- [ ] 위험한 옵션에 주의 문구가 있다

### SDK Documentation

- [ ] Quick Start가 5줄 이내 코드로 첫 동작을 보여준다
- [ ] 인증 예시가 환경변수를 사용한다 (하드코딩 아님)
- [ ] Error Handling 섹션이 있다
- [ ] Configuration 테이블에 모든 옵션이 있다

### 환경변수

- [ ] Required 여부가 모든 변수에 표시되어 있다
- [ ] 기본값이 명시되어 있다
- [ ] `.env.example` 파일이 함께 문서화되어 있다
- [ ] 시크릿 값에 실제 값이 노출되지 않는다
