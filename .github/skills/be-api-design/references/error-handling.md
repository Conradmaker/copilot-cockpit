# Error Handling and Problem Details

## 목적

이 문서는 REST API 오류 계약을 RFC 7807 기준으로 일관되게 설계하도록 돕는다.

## 1. 기본 원칙

- 오류는 HTTP status code와 body shape가 함께 의미를 만든다.
- error response는 endpoint마다 shape가 달라지면 안 된다.
- 기본값은 `application/problem+json`이다.
- machine-readable field와 human-readable field를 모두 제공한다.
- 내부 예외 메시지, stack trace, raw SQL error는 절대 노출하지 않는다.

## 2. 기본 Problem Details shape

```http
HTTP/1.1 404 Not Found
Content-Type: application/problem+json
```

```json
{
  "type": "https://api.example.com/errors/resource-not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "User with ID user_123 does not exist.",
  "instance": "/api/v1/users/user_123"
}
```

### 핵심 필드

| Field | 의미 |
| --- | --- |
| `type` | stable error type URI |
| `title` | 짧고 반복 가능한 에러 제목 |
| `status` | HTTP status code |
| `detail` | 현재 발생 건에 대한 구체적 설명 |
| `instance` | 요청 또는 리소스 instance 식별자 |

## 3. Extension field

field-level validation, debugging, docs 연결이 필요하면 아래 같은 확장을 허용한다.

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "One or more fields are invalid.",
  "instance": "/api/v1/users/req_abc123",
  "request_id": "req_abc123",
  "documentation_url": "https://api.example.com/docs/errors#validation-error",
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Must be a valid email address."
    }
  ]
}
```

### 권장 extension

- `request_id`
- `documentation_url`
- `errors[]`
- `retry_after` 또는 retry metadata

## 4. 상태 코드별 기본 정책

| Status | 언제 쓰는가 | 주의점 |
| --- | --- | --- |
| 400 | malformed JSON, invalid query syntax | semantic validation과 구분 |
| 401 | missing/invalid credential | `WWW-Authenticate` 고려 |
| 403 | authenticated but forbidden | 401과 혼동 금지 |
| 404 | resource not found | security policy상 404 masking 여부 검토 |
| 409 | state conflict, duplicate | retry 가능성 또는 conflict resolution 설명 |
| 422 | semantically invalid request | field-level validation에 적합 |
| 429 | rate limit exceeded | `Retry-After` 권장 |
| 500 | unexpected internal error | detail은 안전하게 제한 |
| 503 | temporary unavailable | maintenance, overload, upstream degraded |

## 5. Validation error

### syntax vs semantic 구분

- malformed JSON, invalid query serialization: 400
- valid JSON but invalid domain data: 422

### field-level validation 예시

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "Request validation failed.",
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Must be a valid email address."
    },
    {
      "field": "age",
      "code": "out_of_range",
      "message": "Must be between 18 and 120."
    }
  ]
}
```

### cross-field validation 예시

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "Date range is invalid.",
  "errors": [
    {
      "fields": ["start_date", "end_date"],
      "code": "invalid_range",
      "message": "end_date must be after start_date."
    }
  ]
}
```

## 6. Auth and permission errors

### 401 Unauthorized

```http
WWW-Authenticate: Bearer realm="api", error="invalid_token"
```

```json
{
  "type": "https://api.example.com/errors/invalid-token",
  "title": "Authentication Failed",
  "status": 401,
  "detail": "The access token is invalid or expired."
}
```

### 403 Forbidden

```json
{
  "type": "https://api.example.com/errors/insufficient-permissions",
  "title": "Forbidden",
  "status": 403,
  "detail": "You do not have permission to delete this user."
}
```

## 7. Conflict, rate limiting, server error

### 409 Conflict

```json
{
  "type": "https://api.example.com/errors/resource-already-exists",
  "title": "Conflict",
  "status": 409,
  "detail": "A user with this email already exists."
}
```

### 429 Too Many Requests

```http
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
```

```json
{
  "type": "https://api.example.com/errors/rate-limit-exceeded",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "Try again in 60 seconds.",
  "retry_after": 60
}
```

### 500 / 503

```json
{
  "type": "https://api.example.com/errors/internal-server-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred. Please try again later.",
  "request_id": "req_abc123"
}
```

```json
{
  "type": "https://api.example.com/errors/service-unavailable",
  "title": "Service Unavailable",
  "status": 503,
  "detail": "Service is temporarily unavailable due to maintenance.",
  "retry_after": 300
}
```

## 8. Error catalog 설계

에러는 `type` URI와 내부 code catalog를 같이 관리하는 편이 좋다.

| Type URI | Internal code | Status | 의미 |
| --- | --- | --- | --- |
| `/errors/validation-error` | `validation_error` | 422 | field/domain validation 실패 |
| `/errors/invalid-token` | `invalid_token` | 401 | invalid or expired token |
| `/errors/insufficient-permissions` | `insufficient_permissions` | 403 | permission 부족 |
| `/errors/resource-not-found` | `resource_not_found` | 404 | resource 없음 |
| `/errors/resource-already-exists` | `resource_already_exists` | 409 | duplicate/conflict |
| `/errors/rate-limit-exceeded` | `rate_limit_exceeded` | 429 | traffic 제한 초과 |

## 9. Request tracking and observability

- 모든 오류 응답에는 추적 가능한 `request_id`를 권장한다.
- server log와 client-visible request_id를 연결한다.
- client support와 incident 대응에서 request_id가 핵심이 된다.

## 10. 피해야 할 패턴

- 200 + error body
- endpoint마다 다른 error JSON shape
- machine-readable code 없음
- internal stack trace 노출
- retryable error인데 retry guidance 없음
- documented status code와 실제 runtime status 불일치
