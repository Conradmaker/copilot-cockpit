# OpenAPI 3.1 Contract Guide

## 목적

이 문서는 REST API 계약을 OpenAPI 3.1로 고정할 때 필요한 최소 구조, 재사용 패턴, 검증 방법을 정리한다.

## 1. 왜 OpenAPI를 쓰는가

- interactive docs
- client/server code generation
- lint/contract validation
- mock server
- human review와 consumer alignment

설계 대화만으로 계약을 고정하지 말고, OpenAPI를 source of truth로 만든다.

## 2. 최소 구조

```yaml
openapi: 3.1.0
info:
  title: Example API
  version: 1.0.0
  description: REST API contract
servers:
  - url: https://api.example.com/api/v1
paths: {}
components:
  schemas: {}
  responses: {}
  securitySchemes: {}
```

## 3. Resource starter example

```yaml
openapi: 3.1.0
info:
  title: Example API
  version: 1.0.0
servers:
  - url: https://api.example.com/api/v1
paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags: [Users]
      parameters:
        - name: cursor
          in: query
          schema:
            type: string
          description: Opaque pagination cursor
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        "200":
          description: Paginated list of users
          content:
            application/json:
              schema:
                type: object
                required: [data, pagination]
                properties:
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/User"
                  pagination:
                    $ref: "#/components/schemas/CursorPage"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "429":
          $ref: "#/components/responses/TooManyRequests"
  /users/{id}:
    get:
      summary: Get a user
      operationId: getUser
      tags: [Users]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: User found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          $ref: "#/components/responses/NotFound"
components:
  schemas:
    User:
      type: object
      required: [id, email, created_at]
      properties:
        id:
          type: string
          readOnly: true
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
          readOnly: true
    CursorPage:
      type: object
      required: [next_cursor, has_more]
      properties:
        next_cursor:
          type: string
          nullable: true
        has_more:
          type: boolean
    Problem:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
        title:
          type: string
        status:
          type: integer
        detail:
          type: string
        instance:
          type: string
          format: uri
  responses:
    Unauthorized:
      description: Missing or invalid authentication
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/Problem"
    NotFound:
      description: Resource not found
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/Problem"
    TooManyRequests:
      description: Rate limit exceeded
      headers:
        Retry-After:
          schema:
            type: integer
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/Problem"
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
security:
  - BearerAuth: []
```

## 4. components 설계 원칙

- 공통 schema는 components로 올린다.
- error response, pagination schema, auth scheme는 재사용한다.
- request/response example도 components/examples로 재사용한다.
- `operationId`는 code generation을 고려해 unique하고 명확하게 쓴다.

## 5. 꼭 문서화할 것

- auth mechanism
- rate limit header
- pagination parameter와 response shape
- filtering/sorting/search parameter
- error catalog와 representative examples
- deprecation/sunset policy가 있으면 관련 header

## 6. Example 정책

- requestBody마다 realistic example 제공
- 200, 4xx, 429 정도는 최소 example 제공
- example은 schema를 설명하는 수준을 넘어, consumer가 바로 구현할 수 있을 만큼 구체적이어야 한다.

## 7. Lint and mock verification

```bash
npx @redocly/cli lint openapi.yaml
npx @stoplight/prism-cli mock openapi.yaml
```

- lint를 통과하지 못하면 계약이 미완성된 것이다.
- mock server는 consumer-facing contract smoke test에 유용하다.

## 8. Review checklist

- paths와 methods가 resource model과 일치하는가
- query/path/request/response schema가 모두 타입과 example을 가지는가
- error response가 `application/problem+json`으로 문서화됐는가
- securitySchemes와 실제 auth contract가 일치하는가
- rate limit과 pagination이 문서화됐는가
- operationId와 tags가 일관적인가

## 9. 피해야 할 패턴

- path만 있고 example 없음
- error response schema 미정의
- auth를 prose로만 설명하고 spec에는 누락
- pagination 파라미터는 있는데 response metadata가 없음
- spec version과 deployed API version 불일치
