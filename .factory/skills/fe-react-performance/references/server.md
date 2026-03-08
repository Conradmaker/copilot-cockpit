# 서버사이드 성능

**우선순위: 🟠 HIGH — 서버 응답 시간 단축, 보안 강화**

서버 컴포넌트, 서버 액션, API 라우트의 성능과 보안을 최적화하는 8개 규칙이다.

---

## 1. React.cache()로 요청 내 중복 제거

`React.cache()`는 단일 요청 내에서 동일한 함수 호출을 자동으로 중복 제거한다. 인증, DB 쿼리에 가장 유용하다.

```typescript
import {cache} from "react";

export const getCurrentUser = cache(async () => {
  const session = await auth();
  if (!session?.user?.id) return null;
  return await db.user.findUnique({where: {id: session.user.id}});
});
// 하나의 요청 내에서 여러 번 호출해도 쿼리는 1회만 실행
```

**⚠️ 인라인 객체 인자 주의:** `React.cache()`는 얕은 동등성(`Object.is`)을 사용한다. 인라인 객체는 매번 새 참조를 생성하여 캐시 미스가 발생한다.

**❌ 항상 캐시 미스:**

```typescript
const getUser = cache(async (params: {uid: number}) => {
  return await db.user.findUnique({where: {id: params.uid}});
});
getUser({uid: 1});
getUser({uid: 1}); // 캐시 미스, 쿼리 재실행
```

**✅ 원시 타입 인자로 캐시 히트:**

```typescript
const getUser = cache(async (uid: number) => {
  return await db.user.findUnique({where: {id: uid}});
});
getUser(1);
getUser(1); // 캐시 히트
```

**Next.js 참고:** `fetch` API는 자동으로 요청 메모이제이션이 적용된다. `React.cache()`는 fetch 이외의 비동기 작업(DB 쿼리, 인증 체크, 파일 시스템 등)에 사용한다.

---

## 2. LRU 캐시로 요청 간 데이터 캐싱

`React.cache()`는 단일 요청 내에서만 동작한다. 여러 요청에 걸쳐 데이터를 캐싱하려면 LRU 캐시를 사용한다.

```typescript
import {LRUCache} from "lru-cache";

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000, // 5분
});

export async function getUser(id: string) {
  const cached = cache.get(id);
  if (cached) return cached;

  const user = await db.user.findUnique({where: {id}});
  cache.set(id, user);
  return user;
}
// 요청 1: DB 쿼리, 결과 캐시
// 요청 2: 캐시 히트, DB 쿼리 없음
```

**Vercel Fluid Compute:** 여러 동시 요청이 같은 함수 인스턴스와 캐시를 공유할 수 있어 LRU 캐싱이 특히 효과적이다.

**전통적 서버리스:** 각 호출이 격리되므로 Redis 같은 외부 캐시를 고려한다.

---

## 3. 서버 액션 인증/권한 검증

서버 액션(`"use server"`)은 공개 엔드포인트로 노출된다. **반드시 각 서버 액션 내부에서** 인증/권한을 검증한다. 미들웨어나 레이아웃 가드에만 의존하면 안 된다.

**❌ 잘못된 예 (인증 없음):**

```typescript
"use server";
export async function deleteUser(userId: string) {
  await db.user.delete({where: {id: userId}}); // 누구나 호출 가능!
}
```

**✅ 올바른 예 (인증 + 권한 + 입력 검증):**

```typescript
"use server";
import {verifySession} from "@/lib/auth";
import {z} from "zod";

const schema = z.object({
  userId: z.string().uuid(),
  name: z.string().min(1).max(100),
});

export async function updateProfile(data: unknown) {
  const validated = schema.parse(data); // 입력 검증
  const session = await verifySession(); // 인증
  if (!session) throw new Error("Unauthorized");
  if (session.user.id !== validated.userId)
    // 권한
    throw new Error("Can only update own profile");

  await db.user.update({
    where: {id: validated.userId},
    data: {name: validated.name},
  });
}
```

---

## 4. RSC 경계에서 직렬화 최소화

React Server/Client 경계는 모든 객체 프로퍼티를 문자열로 직렬화한다. 클라이언트가 실제 사용하는 필드만 전달한다.

**❌ 잘못된 예 (50개 필드 모두 직렬화):**

```tsx
async function Page() {
  const user = await fetchUser(); // 50개 필드
  return <Profile user={user} />;
}
("use client");
function Profile({user}: {user: User}) {
  return <div>{user.name}</div>; // 1개 필드만 사용
}
```

**✅ 올바른 예 (1개 필드만 직렬화):**

```tsx
async function Page() {
  const user = await fetchUser();
  return <Profile name={user.name} />;
}
("use client");
function Profile({name}: {name: string}) {
  return <div>{name}</div>;
}
```

---

## 5. 컴포넌트 합성으로 서버 페칭 병렬화

React Server Components는 트리 내에서 순차적으로 실행된다. 합성 패턴으로 데이터 페칭을 병렬화한다.

**❌ 잘못된 예 (Sidebar가 Page의 fetch 완료를 기다림):**

```tsx
export default async function Page() {
  const header = await fetchHeader();
  return (
    <div>
      <div>{header}</div>
      <Sidebar />
    </div>
  );
}
```

**✅ 올바른 예 (동시 fetch):**

```tsx
async function Header() {
  const data = await fetchHeader();
  return <div>{data}</div>;
}

async function Sidebar() {
  const items = await fetchSidebarItems();
  return <nav>{items.map(renderItem)}</nav>;
}

export default function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  );
}
```

---

## 6. RSC Props 중복 직렬화 방지

RSC→client 직렬화는 참조 기반으로 중복 제거한다. `.toSorted()`, `.filter()`, `.map()` 등의 변환은 새 참조를 생성하므로, 클라이언트에서 수행한다.

**❌ 잘못된 예 (배열 중복 직렬화):**

```tsx
<ClientList usernames={usernames} usernamesOrdered={usernames.toSorted()} />
```

**✅ 올바른 예 (한 번만 전송, 클라이언트에서 변환):**

```tsx
<ClientList usernames={usernames} />;

// 클라이언트
("use client");
const sorted = useMemo(() => [...usernames].sort(), [usernames]);
```

---

## 7. after()로 비차단 작업 처리

Next.js의 `after()`로 응답 전송 후 실행할 작업을 예약한다. 로깅, 분석 등이 응답을 블로킹하지 않는다.

**❌ 잘못된 예 (로깅이 응답 블로킹):**

```tsx
export async function POST(request: Request) {
  await updateDatabase(request);
  await logUserAction({userAgent: request.headers.get("user-agent")}); // 블로킹
  return Response.json({status: "success"});
}
```

**✅ 올바른 예 (응답 후 비차단 로깅):**

```tsx
import {after} from "next/server";

export async function POST(request: Request) {
  await updateDatabase(request);
  after(async () => {
    const userAgent = (await headers()).get("user-agent") || "unknown";
    logUserAction({userAgent});
  });
  return Response.json({status: "success"});
}
```

**활용 사례:** 분석 추적, 감사 로깅, 알림 전송, 캐시 무효화, 정리 작업

---

## 8. 정적 I/O를 모듈 레벨로 호이스팅

정적 에셋(폰트, 로고, 설정 파일)은 모듈 레벨에서 로드한다. 모듈 레벨 코드는 모듈 최초 import 시 한 번만 실행된다.

**❌ 잘못된 예 (매 요청마다 폰트 파일 읽기):**

```typescript
export async function GET(request: Request) {
  const fontData = await fetch(new URL("./fonts/Inter.ttf", import.meta.url)).then(
    (res) => res.arrayBuffer()
  ); // 매 요청마다 실행!
  // ...
}
```

**✅ 올바른 예 (모듈 초기화 시 한 번만 로드):**

```typescript
// 모듈 레벨: 최초 import 시 한 번만 실행
const fontData = fetch(new URL("./fonts/Inter.ttf", import.meta.url)).then((res) =>
  res.arrayBuffer()
);

export async function GET(request: Request) {
  const font = await fontData; // 이미 시작된 Promise await
  // ...
}
```

**사용하면 좋은 경우:** OG 이미지용 폰트, 정적 로고/아이콘, 설정 파일, 이메일 템플릿

**사용하면 안 되는 경우:** 요청/사용자별로 달라지는 에셋, 런타임에 변경되는 파일, 메모리에 상주시키기 너무 큰 파일
