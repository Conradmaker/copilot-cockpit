# Migrations

Migration은 스키마 diff가 아니라 배포 가능한 데이터 변경 계약이다. 개발용 편의 명령과 운영용 배포 명령을 분리해 다룬다.

## 기본 경로

### 개발

```bash
npx prisma migrate dev --name add_membership_role
npx prisma generate
```

### 운영

```bash
npx prisma migrate deploy
npx prisma generate
```

### 상태 확인

```bash
npx prisma migrate status
npx prisma validate
```

## 명령 선택 기준

- `migrate dev`: 개발 DB에서 migration 생성 및 적용
- `migrate deploy`: 이미 커밋된 migration을 운영 DB에 적용
- `migrate reset`: 개발 DB 리셋 전용
- `db push`: prototype, throwaway DB, migration history가 중요하지 않은 실험, MongoDB 예외 경로에서만 검토

### 빠른 판단 기준

- 운영 플로우에서 `migrate dev`를 쓰면 잘못된 경로다.
- migration history가 필요한 SQL 프로젝트에서 `db push`를 기본값으로 삼지 않는다.

## 파괴적 변경은 expand-migrate-contract로 나눈다

다음 변경은 한 번에 밀어 넣지 않는다.

- nullable → required
- field rename
- type change
- unique constraint 추가

권장 순서:

1. 새 필드나 새 구조를 nullable 또는 additive하게 추가한다.
2. backfill script나 application dual-write로 데이터를 채운다.
3. 코드가 새 필드를 읽도록 전환한다.
4. 마지막 migration에서 old field 제거 또는 required 강화한다.

### 빠른 판단 기준

- 기존 데이터가 있는데 바로 `String?`를 `String`으로 바꾸면 backfill 계획부터 확인한다.
- rename을 drop + add처럼 처리하면 데이터 유실 리스크가 커진다.

## drift와 실패 복구

개발 중 drift가 생기면 먼저 상태를 확인하고, 운영과 개발 복구 전략을 분리한다.

```bash
npx prisma migrate status
```

운영 실패 복구가 필요하면 `migrate resolve`를 검토한다.

```bash
npx prisma migrate resolve --applied "migration_name"
npx prisma migrate resolve --rolled-back "migration_name"
```

### 빠른 판단 기준

- migration SQL을 읽지 않고 그대로 deploy하지 않는다.
- drift를 무시하고 다음 migration만 계속 쌓으면 나중에 더 크게 깨진다.

## MongoDB 예외

MongoDB는 schema-less라 `prisma migrate`를 쓰지 않는다. MongoDB를 유지해야 한다면 [mongodb](mongodb.md) 경로로 분기한다.

## 리뷰 포인트

- migration이 additive인지 destructive인지 구분돼 있는가
- backfill이나 dual-write 단계가 필요한가
- production에서 사용할 명령이 `deploy` 기준으로 정리돼 있는가
- `generate`와 seed가 명시적으로 포함돼 있는가
- rollback 또는 failure handling 경로가 적혀 있는가