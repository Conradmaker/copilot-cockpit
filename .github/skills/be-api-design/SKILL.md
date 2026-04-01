---
name: be-api-design
description: "REST API 설계와 계약 중심 명세 작성을 위한 스킬이다. Use this skill when designing or reviewing REST endpoints, resource models, OpenAPI 3.1 specifications, response envelopes, status codes, pagination, filtering, versioning, error contracts, or rate limiting policies. Always consult this skill for backend API contract work, even if the user only asks to add an endpoint, choose a status code, or shape request and response payloads. For framework-specific server implementation use the relevant backend skill. Triggers on: REST API, OpenAPI, endpoint design, resource modeling, status code, pagination, versioning, error handling, API contract, API review, 백엔드 API, 엔드포인트 설계, 명세 작성, 상태 코드, 페이지네이션, 버저닝, 에러 응답."
disable-model-invocation: false
user-invocable: false
---

# Backend API Design

## 목표

이 스킬은 REST API를 설계하거나 리뷰할 때 계약 표면을 빠르게 고정하도록 돕는다.

이 문서는 빠른 판단용 요약 가이드다. 실제 설계를 시작하기 전에는 관련 reference를 먼저 읽고, 훈련 데이터 기반 추측보다 로컬 reference를 우선 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 단계

### 1. 도메인과 resource boundary를 먼저 고정한다

- actor, resource, relationship, lifecycle, permission을 먼저 정리한다.
- 엔드포인트를 쓰기 전에 컬렉션, 단건, 하위 리소스, action endpoint가 왜 필요한지 구분한다.
- CRUD에 맞지 않는 동작은 action endpoint로 허용하되, resource-oriented 구조를 깨지 않는지 확인한다.

#### 빠른 판단 기준

- URL이 명사가 아니라 동사로 시작하면 다시 설계한다.
- 하위 리소스가 3단계를 넘어가면 aggregate boundary나 query 모델을 다시 본다.
- 동일한 개념이 여러 엔드포인트에서 다른 이름으로 불리면 naming부터 정리한다.

상세 레퍼런스: [REST resource/contract 기준](references/rest-patterns.md)

### 2. URI 규칙과 field naming contract를 분리해서 잠근다

- URI path segment는 소문자, 복수형, kebab-case를 기본값으로 사용한다.
- path parameter는 `{id}` 같은 resource identifier 이름을 쓴다.
- query parameter와 JSON field는 같은 API version 안에서 하나의 casing 규칙만 사용한다.
- 기본값은 public REST에서 `snake_case`다. 기존 API가 `camelCase`라면 version 전체에서 그대로 유지한다.
- URI kebab-case와 payload/query snake_case는 서로 다른 surface이므로 섞어도 되지만, payload/query 내부에서 `snake_case`와 `camelCase`를 동시에 쓰면 안 된다.

#### 빠른 판단 기준

- `/getUsers`, `/user`, `/team_members` 같은 경로가 보이면 수정한다.
- `created_at`와 `createdAt`가 같은 version에 같이 나오면 contract drift로 본다.
- filter operator 표기법이 `price[gte]`와 `min_price`로 혼재하면 하나로 통일한다.

상세 레퍼런스: [REST naming/filter 규칙](references/rest-patterns.md)

### 3. 성공 응답과 오류 응답의 envelope를 먼저 고정한다

- 성공 응답은 `data`를 기본 envelope로 두고, 필요할 때만 `meta`와 `links`를 추가한다.
- collection endpoint는 pagination metadata를 명시한다.
- 오류 응답은 기본적으로 RFC 7807 `application/problem+json`을 사용한다.
- field-level validation이 필요하면 `errors[]` 같은 extension field를 문제 상세 객체에 확장한다.
- 내부 구현 세부사항, stack trace, raw DB error는 절대 노출하지 않는다.

#### 빠른 판단 기준

- 200 OK 안에 `success: false`를 넣는 구조면 잘못 설계된 것이다.
- validation error와 auth error가 다른 JSON shape를 쓰면 통일한다.
- retry 가능한 오류면 `Retry-After`, `request_id`, retry guidance를 함께 검토한다.

상세 레퍼런스: [RFC 7807 오류 계약](references/error-handling.md)

### 4. collection behavior는 pagination, filtering, sorting까지 한 번에 설계한다

- collection endpoint에는 pagination을 기본 적용한다.
- cursor는 large dataset, feed, real-time 목록의 기본값이다.
- offset/page는 admin UI, 검색 결과, 총 건수 노출이 필요한 화면에서만 선택한다.
- filtering, sorting, search, sparse fieldset, include semantics를 함께 설계해 query surface를 예측 가능하게 만든다.
- default limit과 max limit을 문서화하고, 429 정책과 함께 traffic control을 본다.

#### 빠른 판단 기준

- `GET /items`가 무제한 목록을 반환하면 바로 수정한다.
- cursor pagination인데 total count와 page number를 같이 강제하면 어색한 설계일 가능성이 높다.
- sort field가 cursor에 반영되지 않으면 중복/누락 위험이 있다.

상세 레퍼런스: [pagination 전략](references/pagination.md), [filter/sort 계약](references/rest-patterns.md)

### 5. OpenAPI 3.1을 계약의 source of truth로 만든다

- resource model, endpoint table, request/response schema, auth, error catalog, rate limit headers를 OpenAPI 3.1에 반영한다.
- request/response example을 반드시 넣는다.
- operationId, tags, reusable components, problem schema를 정리한다.
- lint와 mock 검증을 설계 단계에 포함한다.

#### 빠른 판단 기준

- spec이 없고 대화 설명만 있으면 계약이 고정되지 않은 것이다.
- response example이 없으면 consumer 입장에서 해석 차이가 남는다.
- error response가 components로 재사용되지 않으면 drift 가능성이 높다.

상세 레퍼런스: [OpenAPI 3.1 계약 작성](references/openapi.md)

### 6. versioning, deprecation, migration path를 설계 초기에 포함한다

- public REST는 기본적으로 URI versioning을 권장한다.
- breaking change와 non-breaking change를 구분한다.
- deprecated version에는 `Deprecation`, `Sunset`, `successor-version` link를 고려한다.
- active version 수를 제한하고 migration guide를 남긴다.

#### 빠른 판단 기준

- field rename, type change, auth mechanism change는 breaking change로 본다.
- 구버전 제거 계획 없이 새 버전만 추가하면 운영 리스크가 커진다.
- version strategy가 endpoint마다 다르면 API 전체가 불안정해진다.

상세 레퍼런스: [API versioning/evolution](references/versioning.md)

---

## 상세 레퍼런스 가이드

| 상세 레퍼런스 | 용도 |
| --- | --- |
| [references/rest-patterns.md](references/rest-patterns.md) | resource, URI, method/status, filter/sort, auth/rate limiting 기준 |
| [references/pagination.md](references/pagination.md) | pagination 전략과 response contract |
| [references/error-handling.md](references/error-handling.md) | RFC 7807 기반 오류 계약 |
| [references/versioning.md](references/versioning.md) | versioning, deprecation, migration policy |
| [references/openapi.md](references/openapi.md) | OpenAPI 3.1 구조와 검증 흐름 |

---

## 범위

- In scope: REST resource modeling, endpoint design, status codes, response envelope, error contract, pagination, filtering, rate limiting, OpenAPI 3.1, versioning, API contract review
- Out of scope: GraphQL schema design, backend framework implementation detail, ORM/query tuning, database physical schema optimization
- GraphQL이 필요하면 별도 전용 스킬이나 별도 설계 문서로 분리한다.
