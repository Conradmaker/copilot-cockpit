# 비동기 워터폴 제거

**우선순위: 🔴 CRITICAL — 2~10배 성능 개선 가능**

비동기 워터폴은 독립적인 작업이 순차적으로 실행되어 불필요한 대기가 발생하는 패턴이에요.
데이터 페칭 성능 문제의 가장 흔한 원인이며, 가장 먼저 확인해야 해요.

---

## 1. Promise.all()로 독립적 작업 병렬 실행

비동기 작업 간 의존성이 없다면, `Promise.all()`로 동시에 실행하세요.

**❌ 잘못된 예 (순차 실행, 3번의 라운드트립):**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**✅ 올바른 예 (병렬 실행, 1번의 라운드트립):**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

---

## 2. 의존성 기반 병렬화

일부 작업만 의존성이 있는 경우, `better-all` 또는 Promise 체이닝으로 최대한 병렬화하세요.

**❌ 잘못된 예 (profile이 config를 불필요하게 기다림):**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**✅ 올바른 예 (config와 profile이 병렬 실행):**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

**대안: 추가 의존성 없이 Promise 체이닝:**

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

---

## 3. 전략적 Suspense 경계 배치

비동기 컴포넌트에서 데이터를 기다리기 전에 Suspense 경계를 사용하면, 래퍼 UI를 먼저 보여줄 수 있어요.

**❌ 잘못된 예 (전체 페이지가 데이터 로딩에 블로킹):**

```tsx
async function Page() {
  const data = await fetchData() // 전체 페이지 블로킹
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <DataDisplay data={data} />
      <div>Footer</div>
    </div>
  )
}
```

**✅ 올바른 예 (래퍼 즉시 표시, 데이터 스트리밍):**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay />
      </Suspense>
      <div>Footer</div>
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData() // 이 컴포넌트만 블로킹
  return <div>{data.content}</div>
}
```

**대안: 여러 컴포넌트에서 Promise 공유:**

```tsx
function Page() {
  const dataPromise = fetchData() // 즉시 시작, await하지 않음
  return (
    <div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise)
  return <div>{data.content}</div>
}
```

**Suspense를 사용하지 말아야 할 경우:**
- 레이아웃 결정에 필요한 핵심 데이터
- SEO에 중요한 Above-the-fold 콘텐츠
- 작고 빠른 쿼리 (Suspense 오버헤드 > 이득)
- 레이아웃 시프트를 피하고 싶을 때

---

## 4. await를 필요한 분기로 지연

`await`를 실제 사용하는 코드 분기로 이동하여, 불필요한 대기를 방지하세요.

**❌ 잘못된 예 (두 분기 모두 블로킹):**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId)
  if (skipProcessing) {
    return { skipped: true } // 불필요하게 데이터를 기다림
  }
  return processUserData(userData)
}
```

**✅ 올바른 예 (필요할 때만 fetch):**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) {
    return { skipped: true } // 즉시 반환
  }
  const userData = await fetchUserData(userId)
  return processUserData(userData)
}
```

**조기 반환 최적화 예시:**

```typescript
// ✅ 필요한 시점에만 fetch
async function updateResource(resourceId: string, userId: string) {
  const resource = await getResource(resourceId)
  if (!resource) return { error: 'Not found' }

  const permissions = await fetchPermissions(userId)
  if (!permissions.canEdit) return { error: 'Forbidden' }

  return await updateResourceData(resource, permissions)
}
```

---

## 5. API 라우트에서 워터폴 방지

API 라우트와 서버 액션에서, 독립적인 작업은 즉시 시작하고 나중에 await하세요.

**❌ 잘못된 예 (config가 auth를, data가 둘 다 기다림):**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**✅ 올바른 예 (auth와 config 즉시 시작):**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

더 복잡한 의존성 체인의 경우 `better-all`을 사용하여 자동으로 병렬화를 극대화하세요.
