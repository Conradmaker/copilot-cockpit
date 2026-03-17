# REST Resource and Contract Patterns

## 목적

이 문서는 REST resource 설계, URI 규칙, 응답 envelope, filtering/sorting, auth/rate limiting 같은 계약 표면을 구체적으로 정리한다.

## 1. Resource-first 설계

- resource는 명사다. method가 동사를 담당한다.
- collection, single resource, nested resource, action endpoint를 구분한다.
- nested resource는 ownership이나 containment가 분명할 때만 쓴다.
- action endpoint는 CRUD로 표현하기 어색한 경우에만 허용한다.

### 좋은 예시

```http
GET    /api/v1/users
GET    /api/v1/users/{id}
POST   /api/v1/users
PATCH  /api/v1/users/{id}
DELETE /api/v1/users/{id}

GET    /api/v1/users/{id}/orders
POST   /api/v1/users/{id}/orders

POST   /api/v1/orders/{id}/cancel
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
```

### 피해야 할 예시

```http
POST /api/v1/getUsers
GET  /api/v1/user
GET  /api/v1/users/{id}/getOrders
POST /api/v1/createOrder
```

## 2. Naming contract

### URI 규칙

- path segment: lowercase, plural noun, kebab-case
- path param: `{id}`, `{user_id}`처럼 resource identifier 의미가 드러나는 이름
- sub-resource: `/users/{id}/orders`

### Query와 JSON 규칙

- query parameter와 JSON field는 같은 version 안에서 하나의 casing 규칙만 쓴다.
- 기본값은 public REST에서 `snake_case`다.
- 기존 API가 이미 `camelCase`라면 version 전체에서 유지한다.
- URI kebab-case와 payload/query snake_case는 surface가 다르므로 허용된다.

### 좋은 예시

```text
/api/v1/team-members
/api/v1/orders?status=active&customer_id=user_123

{
  "user_id": "user_123",
  "created_at": "2026-03-18T10:00:00Z"
}
```

### 나쁜 예시

```text
/api/v1/team_members
/api/v1/getUsers

{
  "user_id": "user_123",
  "createdAt": "2026-03-18T10:00:00Z"
}
```

## 3. HTTP method semantics

| Method | Safe | Idempotent | 일반 용도 |
| --- | --- | --- | --- |
| GET | Yes | Yes | 조회 |
| POST | No | No | 생성, non-idempotent action |
| PUT | No | Yes | 전체 교체 |
| PATCH | No | Depends | 부분 수정 |
| DELETE | No | Yes | 삭제 |
| HEAD | Yes | Yes | metadata 확인 |
| OPTIONS | Yes | Yes | allowed methods 확인 |

### 상태 코드 기본 매핑

| Status | 의미 | 대표 상황 |
| --- | --- | --- |
| 200 | 성공 | GET, PUT, PATCH |
| 201 | 생성 성공 | POST + Location header |
| 202 | 비동기 접수 | background job |
| 204 | 본문 없는 성공 | DELETE, idempotent action |
| 400 | syntax/request 형식 오류 | malformed JSON, invalid query |
| 401 | 인증 실패 | missing or invalid credential |
| 403 | 인가 실패 | authenticated but not allowed |
| 404 | 리소스 없음 | identifier not found |
| 409 | 상태 충돌 | duplicate, concurrent modification |
| 422 | semantic validation 실패 | valid JSON, invalid domain data |
| 429 | rate limit 초과 | retry-after 필요 |
| 500 | 예상치 못한 서버 오류 | internal failure |
| 503 | 일시적 불가 | maintenance, overload |

## 4. 성공 응답 envelope

public 또는 partner-facing REST는 아래 구조를 기본값으로 둔다.

```json
{
  "data": {
    "id": "user_123",
    "email": "alice@example.com",
    "created_at": "2026-03-18T10:00:00Z"
  }
}
```

collection response는 `meta` 또는 `pagination`, 그리고 필요 시 `links`를 사용한다.

```json
{
  "data": [
    { "id": "user_123", "name": "Alice" },
    { "id": "user_456", "name": "Bob" }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 142,
    "total_pages": 8
  },
  "links": {
    "self": "/api/v1/users?page=1&per_page=20",
    "next": "/api/v1/users?page=2&per_page=20"
  }
}
```

### 피해야 할 패턴

```json
{
  "status": 200,
  "success": false,
  "error": "Not found"
}
```

HTTP status와 body semantics를 이중화하면 client logic이 복잡해진다.

## 5. Filtering, sorting, search

### Filtering

```http
GET /api/v1/orders?status=active&customer_id=user_123
GET /api/v1/products?price[gte]=10&price[lte]=100
GET /api/v1/orders?created_at[after]=2026-01-01
GET /api/v1/products?category=electronics,clothing
GET /api/v1/orders?customer.country=KR
```

- operator 표기법은 bracket notation 또는 suffix notation 중 하나만 고른다.
- multi-value filter는 comma-separated 또는 repeated param 중 하나만 고른다.
- nested field filter를 허용하면 문서화가 필수다.

### Sorting

```http
GET /api/v1/products?sort=-created_at
GET /api/v1/products?sort=-featured,price,-created_at
```

- descending prefix는 `-field` 패턴이 가장 읽기 쉽다.
- multi-field sort를 허용할 때는 stable secondary sort를 같이 정의한다.

### Search

```http
GET /api/v1/products?q=wireless+headphones
GET /api/v1/users?email=alice@example.com
```

- full-text search와 exact-match filter는 구분해서 설명한다.
- search 결과는 offset/page pagination이 더 자연스러운 경우가 많다.

### Sparse fieldsets

```http
GET /api/v1/users?fields=id,name,email
GET /api/v1/orders?fields=id,total,status&include=customer.name
```

- partial response는 payload 비용이 큰 public API에서 유용하다.
- `fields`와 `include` semantics가 복잡해지면 JSON:API 수준 계약이 필요한지 다시 판단한다.

## 6. Auth, authorization, rate limiting

### 인증 전달 기본값

```http
Authorization: Bearer <token>
X-API-Key: <key>
```

- bearer token과 API key를 섞을 수는 있지만, endpoint별 허용 전략은 명확히 문서화한다.
- 401과 403을 혼동하지 않는다.

### Rate limit header 예시

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1760000000

HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/problem+json
```

### 권장 tier 예시

| Tier | Limit | Window | 대표 용도 |
| --- | --- | --- | --- |
| Anonymous | 30/min | per IP | public endpoint |
| Authenticated | 100/min | per user | standard access |
| Premium | 1000/min | per API key | paid plan |
| Internal | 10000/min | per service | service-to-service |

## 7. Idempotency and concurrency

### POST의 idempotency 필요 시

```http
POST /api/v1/payments
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

- payment, order submission, webhook replay-safe endpoint는 idempotency key를 우선 고려한다.

### optimistic concurrency 예시

```http
If-Match: "etag-value"
```

- concurrent update 가능성이 크면 ETag/If-Match 또는 revision field를 노출한다.

## 8. 캐시와 conditional request

```http
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 15 Jan 2026 10:30:00 GMT
```

- read-heavy resource는 cacheability를 설계 단계에서 같이 검토한다.
- mutable resource update에는 If-Match를 검토한다.

## 9. 최종 점검

- URI가 resource-oriented한가
- URI와 payload/query naming이 각각 일관적인가
- success/error envelope가 endpoint마다 흔들리지 않는가
- filtering, sorting, search 규칙이 문서화됐는가
- auth, rate limit, idempotency가 누락되지 않았는가
