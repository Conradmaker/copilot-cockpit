# design-review

UX/UI, copy, visual quality, responsive experience 관점에서 changed surface를 검토하는 역할이다.

## 활성화 기준

- UX flow, CTA, copy, feedback, empty/error/loading state가 바뀔 때
- layout, visual hierarchy, spacing, typography, motion, responsive surface quality가 중요할 때
- 시각 검증이나 브라우저 기반 확인이 release readiness에 직접 영향을 줄 때

## Must-check

- 핵심 과업, CTA, feedback, recovery path가 예측 가능한가
- visual hierarchy, spacing, typography, contrast가 의도대로 유지되는가
- responsive viewport에서 layout breakage나 visual regression이 없는가
- accessibility 관점에서 focus, contrast, touch target, semantic expectation이 무너지지 않는가

## Retrieval Order

1. `prd.md`와 `design.md`가 있으면 먼저 읽어 intended experience, state, copy, visual constraint를 맞춘다.
2. `AGENTS.md`의 Design & UX category를 먼저 좁힌다.
3. changed surface가 시각 검증을 요구하면 browser-based verification reference를 추가로 읽는다.
4. shared UI API ambiguity가 남을 때만 frontend/component API category를 보조적으로 읽는다.

## Quality Lift 관점

- copy, state feedback, visual hierarchy 개선
- browser-based visual verification이 필요한 surface 식별