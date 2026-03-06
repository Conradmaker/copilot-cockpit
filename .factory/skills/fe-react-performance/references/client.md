# 클라이언트 데이터 페칭

**우선순위: 🟡 MEDIUM-HIGH — 자동 중복 제거, 이벤트 최적화**

클라이언트 사이드 데이터 로딩과 이벤트 처리를 최적화하는 4개 규칙이에요.

---

## 1. SWR로 자동 요청 중복 제거

SWR은 컴포넌트 인스턴스 간 요청 중복 제거, 캐싱, 리밸리데이션을 자동으로 처리해요.

**❌ 잘못된 예 (중복 제거 없음, 각 인스턴스가 개별 fetch):**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers)
  }, [])
}
```

**✅ 올바른 예 (여러 인스턴스가 하나의 요청 공유):**

```tsx
import useSWR from 'swr'

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}
```

**불변 데이터:**

```tsx
import { useImmutableSWR } from '@/lib/swr'

function StaticContent() {
  const { data } = useImmutableSWR('/api/config', fetcher)
}
```

**뮤테이션:**

```tsx
import { useSWRMutation } from 'swr/mutation'

function UpdateButton() {
  const { trigger } = useSWRMutation('/api/user', updateUser)
  return <button onClick={() => trigger()}>Update</button>
}
```

---

## 2. 글로벌 이벤트 리스너 중복 등록 방지

`useSWRSubscription()`을 사용하여 여러 컴포넌트 인스턴스에서 글로벌 이벤트 리스너를 공유하세요.

**❌ 잘못된 예 (N개 인스턴스 = N개 리스너):**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) callback()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [key, callback])
}
```

**✅ 올바른 예 (N개 인스턴스 = 1개 리스너):**

```tsx
import useSWRSubscription from 'swr/subscription'

const keyCallbacks = new Map<string, Set<() => void>>()

function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    if (!keyCallbacks.has(key)) keyCallbacks.set(key, new Set())
    keyCallbacks.get(key)!.add(callback)
    return () => {
      const set = keyCallbacks.get(key)
      if (set) {
        set.delete(callback)
        if (set.size === 0) keyCallbacks.delete(key)
      }
    }
  }, [key, callback])

  useSWRSubscription('global-keydown', () => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && keyCallbacks.has(e.key)) {
        keyCallbacks.get(e.key)!.forEach(cb => cb())
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  })
}
```

---

## 3. Passive 이벤트 리스너로 스크롤 성능 최적화

touch, wheel 이벤트 리스너에 `{ passive: true }`를 추가하면 즉각적인 스크롤이 가능해요. 브라우저가 `preventDefault()` 호출 여부를 확인하기 위해 리스너 완료를 기다리는 것을 방지해요.

**❌ 잘못된 예:**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  document.addEventListener('touchstart', handleTouch)
  document.addEventListener('wheel', handleWheel)
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**✅ 올바른 예:**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  document.addEventListener('touchstart', handleTouch, { passive: true })
  document.addEventListener('wheel', handleWheel, { passive: true })
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**passive 사용:** 트래킹/분석, 로깅, `preventDefault()`를 호출하지 않는 모든 리스너
**passive 미사용:** 커스텀 스와이프 제스처, 커스텀 줌 컨트롤

---

## 4. localStorage 스키마 버전 관리 및 최소화

키에 버전 접두사를 추가하고, 필요한 필드만 저장하세요. 스키마 충돌과 민감 데이터 노출을 방지해요.

**❌ 잘못된 예:**

```typescript
localStorage.setItem('userConfig', JSON.stringify(fullUserObject))
```

**✅ 올바른 예:**

```typescript
const VERSION = 'v2'

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config))
  } catch {
    // incognito, 할당량 초과, 비활성화 시 예외 발생
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`)
    return data ? JSON.parse(data) : null
  } catch {
    return null
  }
}
```

**서버 응답에서 최소 필드만 저장:**

```typescript
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem('prefs:v1', JSON.stringify({
      theme: user.preferences.theme,
      notifications: user.preferences.notifications
    }))
  } catch {}
}
```

**항상 try-catch로 감싸세요:** `getItem()`과 `setItem()`은 incognito/프라이빗 브라우징(Safari, Firefox), 할당량 초과, 비활성화 시 예외를 던져요.
