---
name: fe-ai-elements
description: "AI Elements 컴포넌트로 AI 채팅 인터페이스를 구축하는 스킬이다. Use when building, composing, or customizing AI chat UIs with ai-elements, wiring Vercel AI SDK useChat/useCompletion, handling streaming responses, tool invocation displays, multi-modal input (attachments, audio, speech), or any AI-native application UI. Always consult this skill for AI chat and assistant UI work, even if the user only asks to 'add a chat', 'make a chatbot', 'show tool results', 'add voice input', or 'build an AI assistant page'. For shadcn/ui basics use fe-shadcn-ui; for React patterns use fe-react-patterns; for a11y use fe-a11y; for Tailwind use fe-tailwindcss. Triggers on: ai-elements, AI chat, chatbot, AI SDK, useChat, Conversation, Message, PromptInput, Tool display, AI streaming, chain-of-thought, reasoning UI, tool invocation, multi-modal input, voice input, AI 채팅, AI 챗봇, AI 어시스턴트, AI 컴포넌트, 채팅 인터페이스, 도구 표시, 음성 입력, 스트리밍 UI."
---

# AI Elements 컴포넌트

## 목표

[AI Elements](https://www.npmjs.com/package/ai-elements)를 사용하여 AI 채팅 인터페이스를 빠르고 일관되게 구축한다. shadcn/ui 위에 구축된 AI 전용 컴포넌트 레지스트리이므로, 기존 shadcn/ui 워크플로우와 자연스럽게 통합되면서 Conversation, Message, Tool, PromptInput 같은 AI 특화 컴포넌트를 제공한다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 컴포넌트를 추가하거나 조합할 때는 아래 references/ 문서를 직접 읽고 API와 예시를 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 패턴

### 1. 프로젝트 환경을 먼저 확인한다

AI Elements는 Next.js + AI SDK + shadcn/ui 위에서 동작한다. 컴포넌트를 추가하기 전에 전제조건을 확인해야 한다.

- Node.js 18 이상
- Next.js 프로젝트에 [AI SDK](https://ai-sdk.dev/) 설치 완료
- [shadcn/ui](https://ui.shadcn.com/) 설치 완료 (미설치 시 CLI가 자동 설치)
- `tsconfig.json`에 `@/*` path alias 설정 완료

#### 빠른 판단 기준

- `package.json`에 `ai`(AI SDK)가 있는가 → 없으면 먼저 설치
- `components.json`이 있는가 → shadcn/ui 설정 확인
- `@/components/ai-elements/` 디렉토리가 이미 있는가 → 기존 컴포넌트 확인

설치와 트러블슈팅 상세는 [references/setup-guide.md](references/setup-guide.md)를 읽는다.

### 2. CLI로 컴포넌트를 추가한다

프로젝트의 패키지 매니저에 맞는 runner를 사용한다. 예시는 `npx`를 기준으로 하되 프로젝트에 따라 `pnpm dlx` 또는 `bunx --bun`으로 대체한다.

```bash
# 컴포넌트 추가
npx ai-elements@latest add conversation
npx ai-elements@latest add message
npx ai-elements@latest add prompt-input

# 전체 셋업 (초기 프로젝트)
npx ai-elements@latest
```

컴포넌트는 `@/components/ai-elements/` 디렉토리에 소스 코드로 추가된다. shadcn/ui와 동일한 copy-and-paste 모델이므로 직접 수정이 가능하다.

#### 빠른 판단 기준

- 커스텀 AI 채팅 마크업을 직접 작성하려는가 → 기존 컴포넌트가 있는지 먼저 확인
- 컴포넌트 import가 실패하는가 → `@/` alias와 파일 존재 여부 확인
- 추가 후 스타일이 안 보이는가 → Tailwind + shadcn/ui 글로벌 CSS 확인

### 3. Conversation + Message 기본 조합을 이해한다

AI 채팅 UI의 핵심 뼈대는 Conversation과 Message의 조합이다. AI SDK의 `useChat`과 직접 연결하여 스트리밍을 처리한다.

```tsx
"use client";

import {
  Conversation,
  ConversationContent,
  ConversationMessages,
} from "@/components/ai-elements/conversation";
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";
import { useChat } from "@ai-sdk/react";

const ChatPage = () => {
  const { messages } = useChat();

  return (
    <Conversation>
      <ConversationContent>
        <ConversationMessages>
          {messages.map(({ role, parts }, index) => (
            <Message from={role} key={index}>
              <MessageContent>
                {parts.map((part, i) => {
                  switch (part.type) {
                    case "text":
                      return (
                        <MessageResponse key={`${role}-${i}`}>
                          {part.text}
                        </MessageResponse>
                      );
                  }
                })}
              </MessageContent>
            </Message>
          ))}
        </ConversationMessages>
      </ConversationContent>
    </Conversation>
  );
};
```

#### 빠른 판단 기준

- `Message`의 `from` prop으로 `"user"` / `"assistant"` 스타일이 자동 분기된다
- `parts` 배열을 순회하며 `text`, `tool-invocation`, `reasoning` 등 타입별로 렌더링한다
- 스크롤 자동 이동이 필요하면 `ConversationScrollButton`을 확인한다

상세 API와 sub-component 구성은 [references/conversation.md](references/conversation.md), [references/message.md](references/message.md)를 읽는다.

### 4. AI SDK 통합 패턴을 따른다

AI Elements는 Vercel AI SDK의 `useChat` hook과 긴밀하게 연동된다. tool invocation, streaming, reasoning 등의 AI 기능을 UI로 표현하는 전용 컴포넌트를 제공한다.

- **Tool 표시**: `Tool`, `ToolHeader`, `ToolBody`, `ToolContent`로 tool invocation 결과를 접이식/펼치기로 표시
- **Reasoning/Chain-of-thought**: `Reasoning`, `ChainOfThought` 컴포넌트로 AI의 사고 과정을 시각화
- **Plan/Task**: `Plan`, `Task`로 AI가 생성한 실행 계획을 단계별로 표시
- **Code Block**: `CodeBlock`으로 코드 결과를 syntax highlighting과 함께 표시

#### 빠른 판단 기준

- `parts`에 `tool-invocation` 타입이 있는가 → `Tool` 컴포넌트 사용
- AI의 사고 과정을 보여줘야 하는가 → `Reasoning` 또는 `ChainOfThought`
- 실행 계획 UI가 필요한가 → `Plan` + `Task`
- 코드 결과를 보여줘야 하는가 → `CodeBlock`

상세는 [references/tool.md](references/tool.md), [references/reasoning.md](references/reasoning.md), [references/plan.md](references/plan.md), [references/code-block.md](references/code-block.md)를 읽는다.

### 5. 컴포넌트를 커스터마이징한다

모든 AI Elements 컴포넌트는 HTML 속성을 확장하므로 `className`, `style`, 이벤트 핸들러를 자유롭게 전달할 수 있다. 커스터마이징은 단계적으로 한다.

1. **className으로 Tailwind 클래스 추가** — 가장 간단한 방법
2. **소스 코드 직접 수정** — `@/components/ai-elements/` 내 파일 수정
3. **Compound component 조합 변경** — sub-component를 교체하거나 생략

```tsx
// className으로 커스터마이징
<MessageContent className="rounded-none">
  {children}
</MessageContent>

// 소스 코드에서 직접 수정 (예: rounded-lg 제거)
// components/ai-elements/message.tsx 파일을 열어 수정
```

#### 빠른 판단 기준

- 레이아웃 변경이면 → className으로 충분한지 먼저 확인
- 구조 변경이면 → compound component 조합을 바꾸는 것을 검토
- 동작 변경이면 → 소스 코드 직접 수정

### 6. 멀티모달 입력을 지원한다

AI Elements는 텍스트 외에 파일 첨부, 음성 입력, 이미지 등 멀티모달 입력을 위한 컴포넌트를 제공한다.

- **PromptInput**: 텍스트 입력의 기본 컴포넌트. 자동 높이 조절, 제출 버튼, 툴팁 지원
- **Attachments**: 파일 첨부 UI (드래그 앤 드롭, 미리보기)
- **SpeechInput / MicSelector**: 음성 인식 입력
- **AudioPlayer / VoiceSelector**: 음성 재생 및 목소리 선택
- **ModelSelector**: AI 모델 선택 드롭다운

#### 빠른 판단 기준

- 파일 업로드가 필요한가 → `Attachments`
- 음성 입력이 필요한가 → `SpeechInput` + `MicSelector`
- 모델 선택이 필요한가 → `ModelSelector`
- 텍스트 입력만 필요한가 → `PromptInput`

상세는 [references/prompt-input.md](references/prompt-input.md), [references/attachments.md](references/attachments.md), [references/speech-input.md](references/speech-input.md)를 읽는다.

---

## references/ 가이드

48개의 컴포넌트 reference 문서를 카테고리별로 정리한다. 각 reference 파일은 컴포넌트의 설치 명령, API, props, 사용 예시를 포함한다. 대응하는 `scripts/` 디렉토리의 `.tsx` 파일에서 working example을 확인할 수 있다.

### Core — 대화/메시지 기본

| 파일 | 언제 읽는가 |
|------|------------|
| [references/conversation.md](references/conversation.md) | 채팅 컨테이너, 메시지 목록, 스크롤 구성 |
| [references/message.md](references/message.md) | 메시지 버블, 역할별 스타일, 액션 버튼 |
| [references/prompt-input.md](references/prompt-input.md) | 텍스트 입력, 자동 높이, 제출 버튼, 커서, 툴팁 |
| [references/suggestion.md](references/suggestion.md) | 프롬프트 제안 칩 |
| [references/queue.md](references/queue.md) | 메시지 큐 관리 |

### AI Intelligence — 추론/도구/계획

| 파일 | 언제 읽는가 |
|------|------------|
| [references/agent.md](references/agent.md) | AI 에이전트 상태 표시 |
| [references/tool.md](references/tool.md) | tool invocation 결과 표시, 접이식 UI |
| [references/reasoning.md](references/reasoning.md) | 추론 과정 시각화 |
| [references/chain-of-thought.md](references/chain-of-thought.md) | 사고 과정 단계별 표시 |
| [references/plan.md](references/plan.md) | 실행 계획 표시 |
| [references/task.md](references/task.md) | 개별 작업 진행률 표시 |
| [references/checkpoint.md](references/checkpoint.md) | 체크포인트 상태 |

### Code & Output — 코드/출력 표시

| 파일 | 언제 읽는가 |
|------|------------|
| [references/code-block.md](references/code-block.md) | 코드 블록, syntax highlighting, 복사 |
| [references/terminal.md](references/terminal.md) | 터미널 출력 표시 |
| [references/stack-trace.md](references/stack-trace.md) | 에러 스택 트레이스 |
| [references/test-results.md](references/test-results.md) | 테스트 결과 표시 |
| [references/snippet.md](references/snippet.md) | 코드 스니펫 |
| [references/schema-display.md](references/schema-display.md) | JSON 스키마, API 파라미터 표시 |
| [references/sandbox.md](references/sandbox.md) | 코드 샌드박스 실행 |
| [references/jsx-preview.md](references/jsx-preview.md) | JSX 라이브 프리뷰 |
| [references/web-preview.md](references/web-preview.md) | 웹 페이지 미리보기 |

### Media & Input — 미디어/입력

| 파일 | 언제 읽는가 |
|------|------------|
| [references/attachments.md](references/attachments.md) | 파일 첨부, 드래그 앤 드롭, 미리보기 |
| [references/audio-player.md](references/audio-player.md) | 오디오 재생 컨트롤 |
| [references/image.md](references/image.md) | 이미지 표시 |
| [references/speech-input.md](references/speech-input.md) | 음성 인식 입력 |
| [references/mic-selector.md](references/mic-selector.md) | 마이크 장치 선택 |
| [references/voice-selector.md](references/voice-selector.md) | TTS 목소리 선택 |
| [references/transcription.md](references/transcription.md) | 음성 전사 표시 |

### UI Controls — 컨트롤/네비게이션

| 파일 | 언제 읽는가 |
|------|------------|
| [references/controls.md](references/controls.md) | 재생/정지 등 범용 컨트롤 |
| [references/toolbar.md](references/toolbar.md) | 도구 모음 |
| [references/panel.md](references/panel.md) | 사이드 패널 |
| [references/model-selector.md](references/model-selector.md) | AI 모델 선택 드롭다운 |
| [references/persona.md](references/persona.md) | AI 페르소나/아바타 |
| [references/shimmer.md](references/shimmer.md) | 로딩 시머 애니메이션 |
| [references/confirmation.md](references/confirmation.md) | 확인/거절 다이얼로그 |
| [references/open-in-chat.md](references/open-in-chat.md) | 외부에서 채팅으로 열기 |

### Data & Context — 데이터/컨텍스트 표시

| 파일 | 언제 읽는가 |
|------|------------|
| [references/artifact.md](references/artifact.md) | AI가 생성한 artifact 표시 |
| [references/canvas.md](references/canvas.md) | 편집 가능한 캔버스 |
| [references/context.md](references/context.md) | 컨텍스트 정보 블록 |
| [references/environment-variables.md](references/environment-variables.md) | 환경변수 표시 |
| [references/file-tree.md](references/file-tree.md) | 파일 트리 탐색기 |
| [references/package-info.md](references/package-info.md) | 패키지 정보 카드 |
| [references/sources.md](references/sources.md) | 출처/소스 목록 |
| [references/inline-citation.md](references/inline-citation.md) | 인라인 인용 마커 |
| [references/connection.md](references/connection.md) | 연결 상태 표시 |
| [references/commit.md](references/commit.md) | Git 커밋 정보 표시 |

### Graph & Flow — 그래프/플로우

| 파일 | 언제 읽는가 |
|------|------------|
| [references/node.md](references/node.md) | 그래프 노드 |
| [references/edge.md](references/edge.md) | 그래프 엣지 |

---

## 범위

이 스킬은 AI Elements 컴포넌트의 선택, 추가, 조합, 커스터마이징, AI SDK 연동을 다룬다.

| 시나리오 | 이 스킬에서 처리 | 다른 스킬로 위임 |
|---------|----------------|----------------|
| ai-elements CLI로 컴포넌트 추가 | ✅ | shadcn/ui 설정 문제 → `fe-shadcn-ui` |
| Conversation/Message 조합 | ✅ | 일반 컴포넌트 아키텍처 → `fe-react-patterns` |
| AI 컴포넌트 className 커스터마이징 | ✅ | theme token, CSS variable 설계 → `fe-tailwindcss` |
| AI 채팅 키보드/ARIA 기본 | ✅ | 상세 접근성 패턴 → `fe-a11y` |
| useChat/streaming 연동 | ✅ | TanStack Query 통합 → `fe-tanstack-query` |
| AI 채팅 페이지 레이아웃 | 컴포넌트 조합 | 전체 페이지 레이아웃 → `ds-ui-patterns` |
| AI 컴포넌트를 디자인 시스템으로 배포 | — | `fe-ui-element-components` |
