# Pagination Patterns

## 목적

이 문서는 collection endpoint에서 어떤 pagination 전략을 선택해야 하는지와, 각 전략이 요구하는 response contract를 정리한다.

## 1. 기본 원칙

- collection endpoint는 기본적으로 pagination을 가진다.
- unbounded list를 그대로 반환하지 않는다.
- pagination은 filtering, sorting, total count 정책과 분리해서 생각하지 않는다.

## 2. 전략 선택 표

| 전략 | 강점 | 약점 | 추천 상황 |
| --- | --- | --- | --- |
| Offset | 구현 단순, 임의 페이지 접근 가능 | 큰 offset에서 느림, 실시간 데이터에 취약 | admin UI, 작은 데이터셋 |
| Page | 사용자에게 직관적 | 내부적으로 offset 문제를 그대로 가짐 | 검색 결과, 문서형 목록 |
| Cursor | 큰 데이터셋에 안정적, 일관성 좋음 | page jump 불가, total count 어려움 | feed, activity, public large collection |
| Keyset | 인덱스 친화적, 빠름 | 정렬 제약이 큼 | monotonic ID/time 기반 목록 |

기본값은 아래처럼 둔다.

- public REST collection: cursor 우선
- admin/search UI: offset 또는 page 허용
- append-only / time-series: keyset 또는 cursor

## 3. Offset/page pagination

### Request 예시

```http
GET /api/v1/users?page=3&per_page=10
GET /api/v1/users?offset=20&limit=10
```

### Response 예시

```json
{
  "data": [
    { "id": "user_21", "name": "User 21" },
    { "id": "user_22", "name": "User 22" }
  ],
  "pagination": {
    "page": 3,
    "per_page": 10,
    "total_count": 150,
    "total_pages": 15,
    "has_more": true
  },
  "links": {
    "first": "/api/v1/users?page=1&per_page=10",
    "prev": "/api/v1/users?page=2&per_page=10",
    "next": "/api/v1/users?page=4&per_page=10",
    "last": "/api/v1/users?page=15&per_page=10"
  }
}
```

### 사용 기준

- user가 page number를 기대하는 UX인가
- total count가 반드시 필요한가
- 데이터가 자주 변하지 않는가

### 주의점

- large offset는 느리다.
- insertion/deletion이 잦으면 중복/누락이 생길 수 있다.
- `page`와 `offset`를 같은 endpoint에 동시에 노출하지 않는 편이 낫다.

## 4. Cursor pagination

### Request 예시

```http
GET /api/v1/users?limit=20
GET /api/v1/users?cursor=eyJpZCI6MTIzLCJzb3J0IjoiY3JlYXRlZF9hdCJ9&limit=20
```

### Response 예시

```json
{
  "data": [
    { "id": "user_21", "name": "User 21" },
    { "id": "user_22", "name": "User 22" }
  ],
  "pagination": {
    "next_cursor": "eyJpZCI6MzAsInNvcnQiOiJjcmVhdGVkX2F0In0",
    "prev_cursor": null,
    "has_more": true,
    "limit": 20
  },
  "links": {
    "next": "/api/v1/users?cursor=eyJpZCI6MzAsInNvcnQiOiJjcmVhdGVkX2F0In0&limit=20"
  }
}
```

### 설계 규칙

- cursor는 opaque string으로 다룬다.
- cursor는 정렬 기준 필드를 포함해야 한다.
- multi-field sort면 cursor에도 secondary sort field를 반영한다.
- page number와 total page를 억지로 같이 넣지 않는다.

### 추천 상황

- feed, timeline, activity log
- large dataset
- concurrent insert/delete가 흔한 목록

## 5. Keyset pagination

### Request 예시

```http
GET /api/v1/events?after_id=20&limit=10
GET /api/v1/events?after_created_at=2026-03-18T10:30:00Z&limit=10
```

### Response 예시

```json
{
  "data": [
    { "id": 21, "created_at": "2026-03-18T11:00:00Z" },
    { "id": 22, "created_at": "2026-03-18T11:30:00Z" }
  ],
  "pagination": {
    "after_id": 30,
    "limit": 10,
    "has_more": true
  }
}
```

- indexed monotonic field가 있을 때 매우 효율적이다.
- ordering이 단순할수록 적합하다.

## 6. Limits policy

기본 limit과 max limit을 반드시 문서화한다.

```json
{
  "default_limit": 20,
  "max_limit": 100,
  "min_limit": 1
}
```

### invalid limit 예시

```http
GET /api/v1/users?limit=1000

HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
```

## 7. Sorting과 pagination의 결합

```http
GET /api/v1/users?sort=-created_at&limit=10
GET /api/v1/users?sort=last_name,first_name&limit=10
```

- cursor pagination에서는 sort field를 cursor에 포함한다.
- stable sort가 없으면 결과가 흔들린다.
- primary sort에 tie가 많으면 secondary sort를 추가한다.

## 8. Filtering과 pagination의 결합

적용 순서는 아래가 기본이다.

1. filter
2. sort
3. paginate
4. response metadata 계산

filter 후 total count를 계산할지 여부는 비용에 따라 결정한다.

## 9. Total count 정책

### count 포함이 좋은 경우

- admin grid
- search result
- page navigation UI

### count 생략이 좋은 경우

- very large dataset
- real-time feed
- cursor pagination
- infinite scroll

필요하다면 `include_total=true` 같은 opt-in contract를 둘 수 있다.

## 10. Edge cases

### empty result

```json
{
  "data": [],
  "pagination": {
    "limit": 20,
    "has_more": false
  }
}
```

### out-of-range page

- empty result를 200으로 반환할지
- page not found를 404로 반환할지

둘 중 하나를 고르고 API 전체에서 일관되게 유지한다.

## 11. 피해야 할 패턴

- 무제한 collection 반환
- cursor endpoint에 page number 섞기
- limit max를 문서화하지 않기
- count 비용이 큰 목록에 total count를 강제하기
- sort 규칙 없이 cursor만 노출하기
