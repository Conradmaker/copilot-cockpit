# Hard Rules (Must Follow)

이 규칙은 mandatory다. 위반하면 스킬이 올바르게 작동하지 않음을 의미한다.

---

## No Solution-First Thinking

솔루션을 먼저 정의하지 않음. 항상 문제와 outcome을 먼저 명시한다.

```markdown
❌ FORBIDDEN:
"We should build a search bar for the product page"
"Let's add AI recommendations"
"Users need a mobile app"

✅ REQUIRED:
"Problem: Users can't find products (40% exit rate on catalog)
Outcome: Reduce exit rate to 20%
Possible solutions:
1. Search bar with filters
2. AI-powered recommendations
3. Better category navigation
4. Visual product browsing"
```

---

## Evidence-Based Decisions

실제 사용자 리서치의 근거 없이 사용자 needs를 assume하지 않음.

```markdown
❌ FORBIDDEN:
- "Users probably want X" (assumption without data)
- "Our competitor has X, so we need it too" (copycat without validation)
- "The CEO thinks we should build X" (HiPPO without evidence)
- "It's obvious users need X" (intuition without validation)

✅ REQUIRED:
- "5 out of 8 interviewed users mentioned X as a pain point"
- "Analytics show 60% of users abandon at step 3"
- "Prototype test: 7/10 users completed task successfully"
- "Survey (n=500): 45% rated feature as 'must have'"
```

---

## Minimum Interview Threshold

segment당 최소 5개의 사용자 인터뷰 없이 문제를 validate하지 않음.

```markdown
❌ FORBIDDEN:
- "We talked to 2 users and they loved the idea"
- "One customer requested this feature"
- "Based on a quick chat with sales..."

✅ REQUIRED:
| Segment | Interviews | Key Finding |
|---------|------------|-------------|
| Power Users | 6 | 5/6 struggle with X |
| New Users | 5 | 4/5 drop off at onboarding |
| Churned | 5 | 3/5 cited missing feature Y |

Minimum per segment: 5 interviews
Confidence increases with more interviews
```

---

## Falsifiable Assumptions

모든 assumption은 testable + falsifiable + clear success criteria여야 함.

```markdown
❌ FORBIDDEN:
- "Users will like the new design" (not falsifiable)
- "This will improve engagement" (no success criteria)
- "The feature will be useful" (vague)

✅ REQUIRED:
| Assumption | Test | Success Criteria | Result |
|------------|------|------------------|--------|
| Users will complete onboarding in new flow | Prototype test with 10 users | >70% completion | TBD |
| Users prefer visual search | A/B test | >10% lift in conversions | TBD |
| Price point is acceptable | Landing page test | >3% conversion | TBD |
```

---

## Core Principles

### Continuous Discovery
일회성 리서치가 아닌 매주 사용자 대화

### Outcome-Driven
만들 솔루션이 아닌 달성할 outcome에서 시작

### Assumption Testing
리소스를 투입하기 전에 위험한 가정을 검증

### Co-Creation
고객을 위해 만드는 게 아니라 고객과 함께 만듦

### Data-Driven
직관과 이해관계자 의견보다 근거를 사용

### Problem-First
솔루션을 구상하기 전에 문제 영역을 깊이 이해