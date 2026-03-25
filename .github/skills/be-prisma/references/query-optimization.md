# Query Optimization

Prisma query는 작성이 쉬워서 over-fetching과 N+1을 숨기기 쉽다. 기본값은 “필요한 shape만 가져온다”다.

## 1. `select`를 기본값으로 둔다

```ts
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    memberships: {
      select: {
        role: true,
        workspace: {
          select: {
            id: true,
            slug: true,
          },
        },
      },
    },
  },
})
```

### 빠른 판단 기준

- 응답에서 실제로 쓰지 않는 relation을 `include`하고 있으면 줄인다.
- large model을 통째로 반환하는 `findMany()`는 먼저 shape를 좁힌다.

## 2. N+1은 relation query가 루프 안에 들어갈 때 생긴다

```ts
// Bad
const users = await prisma.user.findMany()
for (const user of users) {
  await prisma.membership.findMany({ where: { userId: user.id } })
}

// Better
const users = await prisma.user.findMany({
  include: {
    memberships: true,
  },
})
```

### 빠른 판단 기준

- `findMany()` 뒤 loop 안에서 다시 Prisma query가 나오면 N+1 후보로 본다.
- resolver나 service layer에서 entity별 relation fetch가 반복되면 batching 또는 shape 변경을 먼저 본다.

## 3. list query는 pagination과 stable order를 같이 설계한다

- offset pagination은 admin UI, 작은 목록, 총 건수 중심 화면에 적합하다.
- cursor pagination은 feed, 무한 스크롤, 대형 목록에 적합하다.
- pagination에는 stable `orderBy`를 반드시 붙인다.

```ts
const page = await prisma.post.findMany({
  take: 20,
  cursor: cursor ? { id: cursor } : undefined,
  skip: cursor ? 1 : 0,
  orderBy: { id: 'asc' },
  select: {
    id: true,
    title: true,
    createdAt: true,
  },
})
```

### 빠른 판단 기준

- 무제한 list query는 즉시 수정 대상으로 본다.
- cursor pagination인데 `orderBy`가 cursor field와 안 맞으면 중복/누락을 의심한다.

## 4. query logging으로 실제 비용을 본다

```ts
const prisma = new PrismaClient({ adapter, log: [{ emit: 'event', level: 'query' }] })

prisma.$on('query', (event) => {
  console.log(event.query)
  console.log(event.duration)
})
```

### 빠른 판단 기준

- 느리다고 느끼는 query는 감으로 고치지 말고 실행 시간과 shape를 본다.
- slow query가 index 문제인지 over-fetching인지 먼저 분리한다.

## 5. raw SQL은 escape hatch로만 쓴다

- 복잡한 aggregation, window function, provider-specific SQL이 필요할 때만 검토한다.
- 가능하면 Prisma query로 유지하고, raw는 꼭 필요한 부분만 내린다.
- 문자열 연결 대신 template tag 기반 `$queryRaw`를 쓴다.

```ts
const rows = await prisma.$queryRaw`
  SELECT u.id, COUNT(m.id) AS membership_count
  FROM users u
  LEFT JOIN memberships m ON m.user_id = u.id
  GROUP BY u.id
`
```

### 빠른 판단 기준

- 단순 filter/sort/select인데 raw SQL로 내려가면 과한 선택일 수 있다.
- raw SQL로 내려간 뒤 parameterization이 보이지 않으면 안전성을 다시 본다.

## 리뷰 포인트

- 필요한 field만 가져오고 있는가
- relation fetch가 loop 안에서 반복되지 않는가
- pagination과 stable order가 함께 설계돼 있는가
- index와 query shape가 맞는가
- raw SQL이 정말 필요한가