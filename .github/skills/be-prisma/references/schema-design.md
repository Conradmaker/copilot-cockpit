# Schema Design

Prisma schema는 데이터베이스 구조와 애플리케이션 query surface를 동시에 결정한다. 모델을 추가할 때는 table shape만 보지 말고 relation, uniqueness, query path, migration cost를 함께 본다.

## 1. 식별자와 naming을 먼저 잠근다

- 외부로 노출되는 식별자는 안정적인 값으로 유지한다.
- 물리 테이블 이름과 Prisma model 이름이 다르면 `@@map`이나 `@map`으로 분리한다.
- Prisma model 이름은 도메인 의미를 우선하고, DB naming convention은 map layer에서 맞춘다.

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}
```

### 빠른 판단 기준

- 생성 전략이 불명확한 `Int @id @default(autoincrement())`를 바로 복사하지 않는다.
- API나 다른 서비스가 참조하는 entity라면 ID format 변경 비용을 먼저 본다.

## 2. relation은 explicit하게 설계한다

- relation field만 두지 말고 foreign key scalar field를 함께 둔다.
- 같은 두 모델 사이에 관계가 두 개 이상이면 named relation을 쓴다.
- `onDelete`, `onUpdate`는 DB 기본값에 맡기지 말고 의도를 드러낸다.

```prisma
model User {
  id          String       @id @default(cuid())
  email       String       @unique
  memberships Membership[]
}

model Workspace {
  id          String       @id @default(cuid())
  slug        String       @unique
  memberships Membership[]
}

model Membership {
  id          String        @id @default(cuid())
  userId      String
  workspaceId String
  role        MembershipRole
  user        User          @relation(fields: [userId], references: [id], onDelete: Cascade)
  workspace   Workspace     @relation(fields: [workspaceId], references: [id], onDelete: Cascade)

  @@unique([userId, workspaceId])
  @@index([workspaceId, role])
}

enum MembershipRole {
  OWNER
  MEMBER
}
```

### 빠른 판단 기준

- relation이 있는데 scalar foreign key field가 없으면 model intent를 다시 본다.
- relation이 둘 이상인데 이름이 모두 기본값이면 추후 query 작성과 migration diff가 헷갈리기 쉽다.

## 3. many-to-many는 join table 필요성을 먼저 본다

Implicit many-to-many는 빠르지만 payload, role, audit field, ordering이 붙는 순간 구조가 깨진다.

- membership role, invitedAt, status 같은 메타데이터가 있으면 explicit join table을 쓴다.
- soft delete나 lifecycle이 필요한 relation도 explicit join table을 우선 검토한다.

### 빠른 판단 기준

- relation 테이블에 필드를 하나라도 더 붙이고 싶다면 implicit many-to-many에서 나올 시점이다.
- join entity를 숨긴 채 API나 service layer에서 메타데이터를 우회 저장하고 있으면 schema를 다시 설계한다.

## 4. uniqueness와 index는 query path에 맞춘다

- `@unique`는 business invariant를 표현할 때 쓴다.
- `@@index`는 `where`, `orderBy`, join path에 맞춰 둔다.
- 복합 조회가 잦으면 composite index를 우선 검토한다.

예:

- 로그인이나 lookup에 쓰는 `email`은 `@unique`
- workspace별 멤버 목록 조회가 많으면 `@@index([workspaceId, role])`
- slug와 tenant 조합이 유일해야 하면 `@@unique([tenantId, slug])`

### 빠른 판단 기준

- foreign key field에 index가 빠져 있으면 relation query 비용이 커진다.
- `where`는 복합 조건인데 index가 단일 컬럼에만 있으면 실제 plan을 다시 본다.

## 5. enum, defaults, map을 의도를 표현하는 데 쓴다

- 고정된 상태 집합은 enum을 우선 검토한다.
- 생성 시점 default는 schema에서 보장하고, 서비스 코드에만 맡기지 않는다.
- legacy DB naming과 Prisma naming을 억지로 하나로 맞추지 말고 map layer를 쓴다.

### 빠른 판단 기준

- `status String`에 애플리케이션 전체가 의존하면 enum 후보로 본다.
- createdAt, updatedAt 처리를 서비스 코드에만 두고 있으면 default/`@updatedAt`로 끌어올릴지 먼저 본다.

## 흔한 실패 패턴

- relation은 있는데 FK scalar field가 없어 migration과 query가 불명확한 상태
- join table이 필요한 관계를 implicit many-to-many로 유지하는 상태
- 자주 조회되는 조건에 index가 없는 상태
- DB naming에 끌려가 Prisma model과 field 이름까지 읽기 어렵게 만든 상태
- nullability를 임시로 열어놓고 의미를 설명하지 않는 상태