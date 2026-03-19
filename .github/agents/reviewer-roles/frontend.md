# frontend-review

프론트엔드 구현 품질과 shared UI surface의 개발적 건전성을 검토하는 역할이다.

## 활성화 기준

- React/UI implementation, state/render flow, client/server boundary가 바뀔 때
- reusable component, shared UI primitive, component API가 바뀔 때
- form, modal, interaction-heavy surface, accessibility-sensitive UI가 바뀔 때

## Must-check

- state placement, render flow, side effect, composition pattern이 일관적인가
- shared UI surface면 component API, composition, accessibility contract가 깨지지 않는가
- framework-level anti-pattern이나 avoidable rerender/waterfall이 없는가
- UI 구현이 design intent를 망치지 않으면서 maintainable한가

## Retrieval Order

1. `.github/instructions/skill-index.instructions.md`의 `Frontend engineering` category를 먼저 좁힌다.
2. current UI surface에 대응하는 `design.md`가 있으면 먼저 읽어 intended interaction과 visual constraint를 맞춘다.
3. changed surface가 shared UI면 component API 관련 skill/reference를 추가로 읽는다.
4. UX나 visual ambiguity가 남을 때만 `.github/instructions/skill-index.instructions.md`의 `Design & UX` category를 보조적으로 읽는다.

## Quality Lift 관점

- shared UI API의 일관성 개선
- component split/merge, state ownership, reuse boundary 개선