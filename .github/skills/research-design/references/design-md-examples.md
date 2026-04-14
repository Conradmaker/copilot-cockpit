# DESIGN.md 예시 가이드

`assets/` 폴더에 18개의 실서비스 DESIGN.md 예시가 있다. 이 파일들은 project-wide style guide의 실제 작성 수준, tone, 구조를 참고할 때 사용한다.

## Refero MCP와의 역할 구분

이 assets는 Refero MCP의 screen/flow research를 대체하지 않는다. 역할이 다르다.

- **Refero MCP**: 실서비스의 layout, section rhythm, flow sequence, interaction pattern 조사
- **assets/ DESIGN.md**: 프로젝트 전체 visual system을 문서화하는 style guide의 tone, 구조, 상세도 참고

## 사용 시점

- research에서 수집한 visual evidence를 DESIGN.md로 정리해야 할 때
- 특정 industry나 aesthetic과 비슷한 tone의 DESIGN.md 작성 수준을 확인할 때
- design decisions에서 "이 visual system은 어떤 구조로 문서화하면 되는가"가 나올 때

DESIGN.md 작성 규칙과 section-by-section 가이드는 [writing-design-prompt/references/design-md.md](../../writing-design-prompt/references/design-md.md)가 owner다.

## 예시 목록

| 파일 | 특징 | 주목할 점 |
| --- | --- | --- |
| [cal.md](../assets/cal.md) | Scheduling, monochrome confidence, Cal Sans display | multi-layered shadow compositing (ring + soft + contact), grayscale-only aesthetic |
| [claude.md](../assets/claude.md) | AI product, warm parchment, serif headings | 철저한 warm neutral palette (cool gray 없음), Anthropic Serif/Sans/Mono 3-font system, gradient-free depth |
| [composio.md](../assets/composio.md) | Developer tools, clean dark mode | concise component documentation, dark/light surface interplay |
| [cursor.md](../assets/cursor.md) | Code editor, warm off-white, 3-font system | oklab color space border, CursorGothic + jjannon serif + berkeleyMono, OpenType cswh swash |
| [elevenlabs.md](../assets/elevenlabs.md) | Voice AI, near-black canvas, studio aesthetic | monospace-forward typography, amber accent on dark, editorial precision |
| [ibm.md](../assets/ibm.md) | Enterprise, structured grid, Plex font system | systematic color tokens, 8-point grid, accessibility-first hierarchy |
| [intercom.md](../assets/intercom.md) | Customer messaging, warm brand personality | conversational tone reflected in design language, distinctive brand green |
| [mintlify.md](../assets/mintlify.md) | Documentation, minimal 5-section structure | compact format 예시 — 1-5 section만으로도 유효한 DESIGN.md |
| [ollama.md](../assets/ollama.md) | Developer CLI, pure grayscale, radical minimalism | 완전한 무채색 palette, SF Pro Rounded + pill geometry, zero shadows |
| [revolut.md](../assets/revolut.md) | Fintech, clean authority, data-dense | utilitarian precision, strong neutral hierarchy, financial-grade trust signals |
| [runwayml.md](../assets/runwayml.md) | Creative AI, editorial black-and-white | cinematic photography, art-direction typography, creative tool aesthetic |
| [spacex.md](../assets/spacex.md) | Aerospace, dramatic dark mode, cinematic scale | large-format imagery, futuristic geometry, extreme contrast |
| [stripe.md](../assets/stripe.md) | Fintech, premium purple accent, custom sohne-var font | multi-layer blue-tinted shadow 시스템, OpenType ss01 활용, 극단적으로 가벼운 weight 300 전략 |
| [supabase.md](../assets/supabase.md) | Developer platform, dark-mode-native, emerald accent | HSL-based color token system, translucent layering, Circular font with compressed display |
| [together-ai.md](../assets/together-ai.md) | AI infrastructure, clean modern | developer-friendly dark surface, gradient accent strategy |
| [vercel.md](../assets/vercel.md) | Developer infrastructure, monochrome, Geist font family | shadow-as-border 기법 (`0px 0px 0px 1px`), extreme negative letter-spacing, workflow-specific accent colors |
| [voltagent.md](../assets/voltagent.md) | AI agents framework, developer-focused | technical documentation style, gradient accents on dark surface |
| [warp.md](../assets/warp.md) | Terminal, warm dark editorial, Matter font | warm parchment text on dark, cinematic photography, uppercase editorial labels |

## Industry별 빠른 선택

| 프로젝트 성격 | 참고할 예시 |
| --- | --- |
| AI product / chatbot | claude, cursor, elevenlabs, together-ai |
| Developer tool / infrastructure | vercel, ollama, supabase, composio, voltagent |
| Fintech / trust-critical | stripe, revolut |
| Enterprise / structured | ibm, intercom |
| Creative / editorial | runwayml, warp, spacex |
| Documentation / minimal | mintlify |
| Scheduling / utility | cal |

예시를 참조할 때는 자신의 프로젝트와 가장 성격이 비슷한 1-3개를 골라 섹션별 작성 수준과 어투를 모델링한다.
