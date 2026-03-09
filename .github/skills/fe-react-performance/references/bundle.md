# 번들 최적화

**우선순위: 🔴 CRITICAL — TTI, LCP에 직접 영향**

번들 크기는 초기 로딩 속도에 직접적으로 영향을 미친다. barrel import 하나가 200~800ms 비용을 발생시킬 수 있다.

---

## 1. Barrel 파일 Import 회피

barrel 파일(index.js에서 `export * from './module'`)을 통한 import는 수천 개의 미사용 모듈을 로드한다.

**왜 tree-shaking이 도움이 안 되는가:** 라이브러리가 external로 처리되면 번들러가 최적화할 수 없고, 번들에 포함하면 빌드가 크게 느려진다.

**❌ 잘못된 예 (전체 라이브러리 로드):**

```tsx
import {Check, X, Menu} from "lucide-react";
// 1,583개 모듈 로드, 개발 시 ~2.8s 추가
// 런타임 비용: 매 콜드 스타트마다 200-800ms

import {Button, TextField} from "@mui/material";
// 2,225개 모듈 로드, 개발 시 ~4.2s 추가
```

**✅ 올바른 예 (필요한 것만 직접 import):**

```tsx
import Check from "lucide-react/dist/esm/icons/check";
import X from "lucide-react/dist/esm/icons/x";
import Menu from "lucide-react/dist/esm/icons/menu";
// 3개 모듈만 로드 (~2KB vs ~1MB)

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
```

**대안 (Next.js 13.5+):**

```js
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ["lucide-react", "@mui/material"],
  },
};
// barrel import를 빌드 시 자동으로 직접 import로 변환
```

**흔히 영향받는 라이브러리:** `lucide-react`, `@mui/material`, `@mui/icons-material`, `@tabler/icons-react`, `react-icons`, `@headlessui/react`, `@radix-ui/react-*`, `lodash`, `date-fns`, `rxjs`

---

## 2. 무거운 컴포넌트 Dynamic Import

초기 렌더에 필요하지 않은 무거운 컴포넌트는 `next/dynamic`으로 지연 로드한다.

**❌ 잘못된 예 (Monaco가 메인 청크에 포함 ~300KB):**

```tsx
import {MonacoEditor} from "./monaco-editor";

function CodePanel({code}: {code: string}) {
  return <MonacoEditor value={code} />;
}
```

**✅ 올바른 예 (Monaco를 필요 시 로드):**

```tsx
import dynamic from "next/dynamic";

const MonacoEditor = dynamic(
  () => import("./monaco-editor").then((m) => m.MonacoEditor),
  {ssr: false}
);

function CodePanel({code}: {code: string}) {
  return <MonacoEditor value={code} />;
}
```

---

## 3. 비핵심 서드파티 라이브러리 지연 로드

분석, 로깅, 에러 트래킹은 사용자 인터랙션을 차단하지 않는다. 하이드레이션 후에 로드한다.

**❌ 잘못된 예 (초기 번들에 포함):**

```tsx
import {Analytics} from "@vercel/analytics/react";

export default function RootLayout({children}) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

**✅ 올바른 예 (하이드레이션 후 로드):**

```tsx
import dynamic from "next/dynamic";

const Analytics = dynamic(
  () => import("@vercel/analytics/react").then((m) => m.Analytics),
  {ssr: false}
);

export default function RootLayout({children}) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

---

## 4. 사용자 의도 기반 Preload

무거운 번들을 필요하기 전에 미리 로드하여 체감 지연을 줄인다.

**hover/focus 시 preload:**

```tsx
function EditorButton({onClick}: {onClick: () => void}) {
  const preload = () => {
    if (typeof window !== "undefined") {
      void import("./monaco-editor");
    }
  };

  return (
    <button onMouseEnter={preload} onFocus={preload} onClick={onClick}>
      Open Editor
    </button>
  );
}
```

**피처 플래그 활성화 시 preload:**

```tsx
function FlagsProvider({children, flags}: Props) {
  useEffect(() => {
    if (flags.editorEnabled && typeof window !== "undefined") {
      void import("./monaco-editor").then((mod) => mod.init());
    }
  }, [flags.editorEnabled]);

  return <FlagsContext.Provider value={flags}>{children}</FlagsContext.Provider>;
}
```

`typeof window !== 'undefined'` 체크는 SSR에서 preload 모듈의 번들링을 방지한다.

---

## 5. 조건부 모듈 로딩

기능이 활성화될 때만 대용량 데이터나 모듈을 로드한다.

**❌/✅ 애니메이션 프레임 지연 로드:**

```tsx
function AnimationPlayer({enabled, setEnabled}: Props) {
  const [frames, setFrames] = useState<Frame[] | null>(null);

  useEffect(() => {
    if (enabled && !frames && typeof window !== "undefined") {
      import("./animation-frames.js")
        .then((mod) => setFrames(mod.frames))
        .catch(() => setEnabled(false));
    }
  }, [enabled, frames, setEnabled]);

  if (!frames) return <Skeleton />;
  return <Canvas frames={frames} />;
}
```
