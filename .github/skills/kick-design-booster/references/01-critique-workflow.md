# 디자인 품질 비평 워크플로우

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 UI의 디자인 품질을 체계적으로 평가하는 절차와 결과 포맷을 다룬다.

---

## 1. AI Slop 탐지 (가장 먼저)

"AI가 만들었다고 하면 바로 믿겠는가?" — 이 질문에 "예"라면 문제가 있다.

**확인 항목:**
- AI 색상 팔레트 (indigo/violet gradient, cyan/teal 조합)
- 다크 모드 + 네온 악센트 + 글래스모피즘
- gradient text on metrics
- 모든 heading 위에 둥근 큰 아이콘
- 동일한 카드 그리드 반복
- generic 시스템 폰트 (의도 없이 Inter/Roboto)

→ 상세 기준: `ds-visual-design/references/anti-ai-slop.md`

## 2. 시각적 위계

- 눈이 가장 중요한 요소로 먼저 가는가?
- 명확한 primary action이 있는가? 2초 안에 찾을 수 있는가?
- 크기, 색, 위치가 중요도를 올바르게 전달하는가?
- 서로 다른 무게여야 할 요소들이 시각적으로 경쟁하지 않는가?

## 3. 정보 구조와 인지부하

- 구조가 직관적인가? 새 사용자가 조직을 이해하겠는가?
- 관련 콘텐츠가 논리적으로 그룹화되어 있는가?
- 한 결정 지점에서 보이는 선택지가 4개를 넘는가?
- 내비게이션이 명확하고 예측 가능한가?
- 복잡성이 필요할 때만 드러나는가? (진행적 노출)
- **인지부하 8항목 체크리스트**를 실행한다 → `references/10-cognitive-load.md`

## 4. 감정 여정

- 이 인터페이스가 불러일으키는 감정은 무엇인가? 의도적인가?
- 브랜드 성격과 일치하는가?
- 대상 사용자가 "이건 나를 위한 것"이라고 느끼겠는가?
- **Peak-end rule**: 가장 강렬한 순간이 긍정적인가? 경험이 좋게 끝나는가?
- **감정 골짜기**: 온보딩 좌절, 결제/삭제/커밋의 불안이 있는가?
- 부정적 순간에 설계된 개입(진행 표시, 안심 카피, undo, 사회적 증거)이 있는가?

## 5. 발견성과 어포던스

- 인터랙티브 요소가 명확히 인터랙티브해 보이는가?
- 설명 없이 무엇을 해야 하는지 알겠는가?
- hover/focus 상태가 유용한 피드백을 주는가?
- 더 보여줘야 할 숨겨진 기능이 있는가?

## 6. 구성과 균형

- 레이아웃이 균형 잡혔는가, 불편하게 치우쳐 있는가?
- 여백이 의도적인가, 남은 공간인가?
- spacing과 반복에서 시각적 리듬이 있는가?
- 비대칭이 설계된 것인가, 우연한 것인가?

## 7. 커뮤니케이션으로서의 타이포그래피

- 타입 위계가 읽기 순서를 안내하는가?
- 본문 텍스트가 읽기 편한가? (줄 길이, 간격, 크기)
- 폰트 선택이 브랜드/톤을 강화하는가?
- 제목 레벨 간 충분한 대비가 있는가?

## 8. 목적 있는 색상

- 색이 장식이 아니라 의미를 전달하는가?
- 팔레트가 응집력 있는가?
- 악센트 색이 올바른 곳으로 주의를 끄는가?
- 색각 이상 사용자에게도 의미가 전달되는가?

## 9. 상태와 엣지 케이스

- 빈 상태가 행동을 안내하는가?
- 로딩 상태가 체감 대기 시간을 줄이는가?
- 에러 상태가 도움이 되고 비난하지 않는가?
- 성공 상태가 확인하고 다음 단계를 안내하는가?

## 10. 마이크로카피와 보이스

- 글이 명확하고 간결한가?
- 사람처럼 들리는가? (이 브랜드에 맞는 사람)
- 라벨과 버튼이 모호하지 않은가?
- 에러 카피가 문제 해결을 돕는가?

---

## 결과 포맷

### Design Health Score

Nielsen 10 Heuristic 각각 0–4로 채점한다. → `references/09-heuristics-scoring.md`

```markdown
| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | ? | |
| 2 | Match System / Real World | ? | |
| 3 | User Control and Freedom | ? | |
| 4 | Consistency and Standards | ? | |
| 5 | Error Prevention | ? | |
| 6 | Recognition Rather Than Recall | ? | |
| 7 | Flexibility and Efficiency | ? | |
| 8 | Aesthetic and Minimalist Design | ? | |
| 9 | Error Recovery | ? | |
| 10 | Help and Documentation | ? | |
| **Total** | | **??/40** | |
```

정직하게 채점한다. 4점은 진짜 뛰어남을 의미한다. 대부분의 인터페이스는 20–32점이다.

### Anti-Patterns Verdict

Pass/Fail: AI가 만든 것처럼 보이는가? 구체적 징후를 나열한다.

### Persona Test (선택)

2~3개 페르소나로 핵심 동선을 테스트한다. → `references/11-personas.md`

### 전체 인상

잘 되는 것 2~3가지, 가장 큰 개선 기회 1가지를 명시한다.
