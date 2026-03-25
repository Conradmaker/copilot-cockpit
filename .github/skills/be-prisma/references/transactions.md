# Transactions

Transaction은 atomicity를 위한 도구지만, 모든 write path에 무조건 interactive transaction을 붙이는 방식은 오히려 비용이 크다. 독립 작업인지, 중간 검증이 필요한지, 충돌이 잦은지부터 본다.

## 1. 독립 쿼리 묶음이면 array transaction을 쓴다

```ts
const [user, profile] = await prisma.$transaction([
  prisma.user.create({ data: userData }),
  prisma.profile.create({ data: profileData }),
])
```

### 빠른 판단 기준

- 쿼리 사이에 애플리케이션 로직이 없으면 array transaction을 먼저 검토한다.
- 순서상 의존성이나 validation이 있으면 interactive transaction으로 넘긴다.

## 2. 중간 검증이 필요하면 interactive transaction을 쓴다

```ts
const result = await prisma.$transaction(
  async (tx) => {
    const membership = await tx.membership.create({ data: membershipData })

    if (membership.role === 'OWNER' && !(await canAssignOwner(tx, membership.workspaceId))) {
      throw new Error('Owner assignment is not allowed')
    }

    await tx.auditLog.create({
      data: {
        actorId,
        action: 'membership.created',
        workspaceId: membership.workspaceId,
      },
    })

    return membership
  },
  {
    maxWait: 5_000,
    timeout: 10_000,
    isolationLevel: 'Serializable',
  },
)
```

### 빠른 판단 기준

- transaction 안에서 외부 API 호출이나 long-running job enqueue를 기다리지 않는다.
- isolation level은 기본값을 맹신하지 말고 충돌 위험과 비용을 같이 본다.

## 3. 낙관적 동시성 제어를 같이 본다

충돌이 잦은 레코드는 version field나 timestamp 기반 guard를 붙이는 편이 단순한 retry보다 예측 가능하다.

```ts
await prisma.post.update({
  where: {
    id_version: {
      id: postId,
      version: currentVersion,
    },
  },
  data: {
    content: nextContent,
    version: { increment: 1 },
  },
})
```

### 빠른 판단 기준

- 마지막 write wins가 위험한 레코드는 OCC 후보로 본다.
- 충돌이 잦은데 retry만 늘리고 있으면 data model과 isolation 전략을 다시 본다.

## 4. transaction conflict는 retry 전략까지 포함해 설계한다

```ts
try {
  await prisma.$transaction(async (tx) => {
    // work
  })
} catch (error) {
  if ((error as { code?: string }).code === 'P2034') {
    // retry or surface conflict explicitly
  }
  throw error
}
```

### 빠른 판단 기준

- transaction conflict 코드를 무시하고 generic 500으로 덮지 않는다.
- retry가 필요한 작업인지, 사용자가 다시 시도해야 하는 작업인지 구분한다.

## 리뷰 포인트

- array transaction과 interactive transaction을 구분해서 쓰는가
- transaction 안에서 외부 I/O를 하지 않는가
- timeout과 maxWait이 환경에 맞는가
- OCC나 conflict handling이 필요한 write path를 놓치지 않았는가