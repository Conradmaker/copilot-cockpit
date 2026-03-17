# Versioning and API Evolution

## 목적

이 문서는 REST API versioning 전략, deprecation lifecycle, migration policy를 정리한다.

## 1. 기본 원칙

- breaking change는 새 version이 필요하다.
- non-breaking change는 기존 version 안에서 허용된다.
- versioning 전략은 endpoint마다 다르면 안 된다.
- public REST는 기본적으로 URI versioning을 권장한다.

## 2. Breaking vs non-breaking

### breaking change

- field 제거 또는 이름 변경
- field type 변경
- request에 required field 추가
- response shape 변경
- endpoint 제거
- 같은 상황에서 status code 의미 변경
- auth mechanism 변경

### non-breaking change

- 새 endpoint 추가
- optional request field 추가
- response에 optional field 추가
- bug fix
- performance 개선

## 3. 추천 전략

### 기본값: URI versioning

```http
GET /api/v1/users/123
GET /api/v2/users/123
```

#### 장점

- 가장 발견하기 쉽다.
- routing과 caching이 단순하다.
- 문서화와 디버깅이 쉽다.

#### 단점

- URL이 바뀐다.
- 같은 resource라도 version마다 URI가 달라진다.

### 대안: header versioning

```http
GET /api/users/123
Accept: application/vnd.myapi.v2+json
```

- 브라우저 테스트와 디버깅이 어려워지는 대신 URI는 안정적이다.
- strong justification이 없으면 public REST의 기본값으로 두지 않는다.

## 4. Version naming

- major version만 쓴다: `v1`, `v2`, `v3`
- `v1.1`, `v1.2` 같은 URI version은 피한다.
- date-based versioning은 운영 문화가 맞을 때만 쓴다.

## 5. Lifecycle

### introduction

- 새 version release
- migration guide 공개
- breaking change 목록 공개

### deprecation

```http
Deprecation: true
Sunset: Wed, 15 Jan 2027 00:00:00 GMT
Link: </api/v2/users/123>; rel="successor-version"
```

- deprecated version은 여전히 동작하지만 종료 계획을 response header와 docs에 노출한다.

### sunset

```http
HTTP/1.1 410 Gone
Content-Type: application/problem+json
```

```json
{
  "type": "https://api.example.com/errors/version-sunset",
  "title": "API Version Sunset",
  "status": 410,
  "detail": "API v1 was sunset on 2027-01-15. Please migrate to v2.",
  "documentation_url": "https://api.example.com/docs/migration-v1-to-v2"
}
```

## 6. 권장 운영 정책

- 현재 version + 직전 version 정도만 active support
- deprecation notice는 최소 6개월
- migration guide 없이 sunset 금지
- usage telemetry로 version adoption 추적

## 7. Migration guide에 들어갈 것

1. breaking changes 목록
2. old/new request-response diff
3. rename/type-change mapping
4. sample request migration
5. removal timeline

### 예시

```markdown
# Migrating from v1 to v2

## Breaking Changes

- `name` field가 `first_name`, `last_name`으로 분리됨
- `status` enum 값 `disabled`가 `inactive`로 변경됨
```

## 8. OpenAPI versioning

- version마다 독립 spec을 유지하는 편이 가장 명확하다.

```text
openapi-v1.yaml
openapi-v2.yaml
```

- 하나의 spec에서 여러 server를 나열할 수도 있지만, 문서 복잡도가 올라간다.

## 9. Version discovery

필요하면 root endpoint나 version info endpoint를 노출한다.

```json
{
  "versions": {
    "v1": {
      "status": "deprecated",
      "sunset_date": "2027-01-15"
    },
    "v2": {
      "status": "current"
    }
  }
}
```

## 10. 피해야 할 패턴

- version bump 없이 breaking change 배포
- endpoint마다 다른 versioning 전략 사용
- deprecation notice 없이 바로 제거
- active version을 너무 많이 유지
- migration guide 없이 client에게 알아서 옮기라고 요구
