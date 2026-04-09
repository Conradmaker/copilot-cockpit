# 설치 및 트러블슈팅 가이드

## 전제조건

AI Elements를 설치하기 전에 아래 환경을 확인한다.

- [Next.js](https://nextjs.org/) 프로젝트에 [AI SDK](https://ai-sdk.dev/) 설치 완료
- [shadcn/ui](https://ui.shadcn.com/) 설치 완료. 미설치 시 AI Elements CLI가 자동으로 설치한다.
- [AI Gateway](https://vercel.com/docs/ai-gateway) 사용을 권장한다. `env.local`에 `AI_GATEWAY_API_KEY`를 추가하면 별도 provider API 키 없이 실험할 수 있다.

## 설치

### CLI로 컴포넌트 추가

프로젝트의 `packageManager`에 맞는 runner를 사용한다.

```bash
# npx
npx ai-elements@latest add <component>

# pnpm
pnpm dlx ai-elements@latest add <component>

# bun
bunx --bun ai-elements@latest add <component>
```

### 전체 셋업

초기 프로젝트에서 전체 셋업을 실행하면 기본 컴포넌트와 의존성이 함께 설치된다.

```bash
npx ai-elements@latest
```

### 설치 결과

컴포넌트 소스 코드가 `@/components/ai-elements/` 디렉토리에 추가된다. shadcn/ui와 동일한 copy-and-paste 모델이므로 직접 수정이 가능하다.

## 트러블슈팅

### 스타일이 적용되지 않을 때

프로젝트가 shadcn/ui + Tailwind 4 설정을 올바르게 갖추고 있는지 확인한다. `globals.css` 파일이 Tailwind를 import하고 shadcn/ui 기본 스타일을 포함해야 한다.

### CLI 실행 후 파일이 추가되지 않을 때

- 현재 작업 디렉토리가 프로젝트 루트(`package.json`이 있는 곳)인지 확인한다.
- `components.json` 파일이 올바르게 설정되어 있는지 확인한다.
- 최신 버전의 CLI를 사용한다: `npx ai-elements@latest`

### 테마 스위칭이 동작하지 않을 때

shadcn/ui와 AI Elements는 `<html>` 요소의 `data-theme` 속성으로 테마를 전환한다. `tailwind.config.js`가 class 또는 data- selector를 사용하는지 확인한다.

### import가 "module not found"로 실패할 때

파일이 존재하는지 확인하고, `tsconfig.json`에 `@/` path alias가 올바르게 설정되어 있는지 확인한다.

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### AI 코딩 어시스턴트가 AI Elements 컴포넌트에 접근하지 못할 때

1. 설정 파일의 JSON 문법이 유효한지 확인한다.
2. 파일 경로가 올바른지 확인한다.
3. 코딩 어시스턴트를 재시작한다.
4. 안정적인 인터넷 연결을 확인한다.
