# Example Workflow: SaaS Churn Reduction

이 예시는 디자인 리서치를 어떻게 discovery → research → analyze → handoff까지 연결하는지 보여준다. 여기서는 설계와 구현을 직접 마무리하지 않고, owner skill로 넘길 수 있는 evidence packet을 만드는 데서 멈춘다.

---

## 0. Discovery Brief

**Context:** TaskFlow — project management SaaS for small teams. Monthly churn rate at 8%, goal is to reduce to 4%. Scope: cancellation flow redesign + retention intervention research.

**Brief**

> "나는 team admin을 위한 cancellation flow를 조사하고 있다. 이 flow의 핵심 과업은 사용자가 불필요한 마찰 없이 취소하거나, 저장 가능한 경우 적절한 대안을 찾게 하는 것이다. 가장 큰 objection은 '이 과정을 어렵게 만들 것 같다', '데이터를 잃을 것 같다', '과하게 설득당할 것 같다'이다. platform은 web이고, billing/legal constraint가 있다."

---

## 1. Research Plan

### Challenge lens

- trust-sensitive exit flow
- churn reduction and retention
- graceful cancellation without dark patterns

### Query loop

1. broad: `cancellation flow subscription`
2. specific: `cancel subscription retention`
3. leader: `Spotify cancel`, `Clay cancellation`, `ElevenLabs cancel`
4. component: `pause subscription`, `retention offer discount modal`
5. adjacent: `win back reactivate comeback`

### Tool choice

- flow 이해: `search_flows` → `get_flow`
- 특정 retention modal이나 consequence screen deep dive: `search_screens` → `get_screen`

---

## 2. Deep Dive Findings

### Clay

- 7-step cancellation flow
- reason selection 이후 `25% OFF FOR LIFE` retention offer 등장
- final cancellation 이전에 loss consequence를 구체적으로 나열

### ElevenLabs

- 6-step flow
- feature loss를 텍스트가 아니라 thumbnail로 보여줌
- reason collection이 radio가 아니라 multi-select checkbox임

### Train Fitness

- post-cancel 상태에서도 `Renew: [exact price]`를 버튼에 직접 표기

---

## 3. Research Summary

```
📊 RESEARCH SUMMARY
────────────────────────────────────────
Queries: 8 | Screens/Flows reviewed: 200+ | Deep dives: 8

WHAT I FOUND:
- modal-based cancellation flows가 dominant하다
- consequence screen은 final confirm 이전에 배치되는 경우가 많다
- retention offer는 permanence, exact savings, visual tangibility를 함께 쓸 때 강해진다
- multi-select reason collection은 single-select보다 더 풍부한 signal을 준다
- exact pricing on reactivation reduces friction after cancel

GAPS:
- win-back email timing evidence는 부족하다
────────────────────────────────────────
```

---

## 4. Pattern Table

| Aspect | Clay | ElevenLabs | Train Fitness | Pattern |
| --- | --- | --- | --- | --- |
| Flow length | 7-step | 6-step | shorter native path | 5~8 steps common |
| Reason collection | radio | checkbox | n/a | multi-select worth considering |
| Offer framing | `OFF FOR LIFE` | one-time offer | n/a | permanence or urgency used |
| Loss presentation | text list | thumbnails | n/a | concrete loss beats abstract loss |
| Reactivation | not prominent | visible | exact price in button | recovery path should stay visible |

---

## 5. Steal List

| Source | Exact detail | Why it works | Candidate use |
| --- | --- | --- | --- |
| Clay | `25% OFF FOR LIFE` ticket-style offer | permanence reduces temp-fix objection | permanence framing test |
| ElevenLabs | feature thumbnails in loss screen | concrete loss increases salience | visual loss treatment research |
| ElevenLabs | multi-select checkbox reasons | captures more accurate intent | replace single-select reasons |
| Train Fitness | exact renew price on CTA | lowers reactivation friction | explicit reactivation pricing |

---

## 6. Candidate Decisions

여기서 중요한 점은 final design system을 확정하지 않는 것이다. evidence를 다음 owner가 바로 쓸 수 있는 decision packet으로 번역한다.

### Candidate decision A

- Decision: cancellation reason은 single-select보다 multi-select를 우선 검토한다
- Evidence: ElevenLabs flow
- Why this matters: user intent를 더 정확히 수집하고 retention branch quality를 높일 수 있다
- Owner handoff: ds-product-ux

### Candidate decision B

- Decision: consequence screen은 final confirm 이전에 둔다
- Evidence: Clay, Spotify, ElevenLabs
- Why this matters: 사용자가 무엇을 잃는지 confirm 전 인지하게 한다
- Owner handoff: ds-product-ux + ds-ui-patterns

### Candidate decision C

- Decision: feature loss는 텍스트만이 아니라 concrete visual treatment를 검토한다
- Evidence: ElevenLabs thumbnails
- Why this matters: loss aversion이 stronger signal로 작동한다
- Owner handoff: ds-ui-patterns + ds-visual-design

### Candidate decision D

- Decision: post-cancel에도 immediate recovery CTA를 남긴다
- Evidence: Train Fitness exact renew price
- Why this matters: cancellation 후 return path friction을 낮춘다
- Owner handoff: ds-product-ux

---

## 7. Handoff Packet

### ds-product-ux로 넘길 것

- reason collection 방식
- trust-sensitive cancellation copy
- objection handling and recovery path
- retention offer를 dark pattern 없이 다루는 방식

### ds-ui-patterns로 넘길 것

- modal vs page structure
- consequence screen section order
- feature loss representation pattern

### ds-visual-design로 넘길 것

- loss thumbnail이나 offer treatment의 visual distinctiveness
- cancellation/renew state의 visual hierarchy

이 시점에서 멈추고, final UX rule과 visual rule은 각 owner skill에서 확정한다.