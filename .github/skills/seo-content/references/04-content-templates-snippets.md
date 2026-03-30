# Content Templates and Snippet Formats

## 목표

query type에 맞는 콘텐츠 구조와 snippet-friendly formatting을 고른다.

---

## 1. 형식 선택표

| Query type | 추천 형식 | 핵심 블록 |
| --- | --- | --- |
| What is / definition | definition guide | direct definition, why it matters, FAQ |
| How to | how-to guide | steps, verify, mistakes, FAQ |
| Best / alternatives | roundup / listicle | quick summary table, criteria, verdict |
| A vs B | comparison page | quick answer, table, choose-if blocks |
| broad head term | pillar / complete guide | TOC, major sections, cluster links |

---

## 2. definition block

AI engines와 featured snippet 둘 다 짧은 direct answer를 좋아한다.

### 템플릿

```markdown
**[Term]** is [clear category] that [primary function or purpose].
```

### 길이 기준

- 25-60 words 정도가 무난하다
- 첫 문장에서 용어를 정의하고, 다음 1-2문장에서 맥락을 준다

---

## 3. how-to 구조

```markdown
# How to [Achieve Goal]

## What you'll need

## Step 1: [Action]

## Step 2: [Action]

## Step 3: [Action]

## Common mistakes

## FAQ

## Verify / Next steps
```

### 규칙

- numbered steps를 쓴다
- 각 step는 action verb로 시작한다
- 마지막에 verify를 둔다

---

## 4. comparison 구조

```markdown
# [A] vs [B]: Which Is Better for [Use Case]?

**Quick answer**: ...

## Quick Comparison

| Feature | A | B |
| --- | --- | --- |

## What is A?

## What is B?

## Detailed Comparison

## Which Should You Choose?

## FAQ

## Final Verdict
```

### 규칙

- 표를 앞쪽에 둔다
- "Choose A if / Choose B if" 블록을 넣는다
- comparison query에서 verdict를 피하지 않는다

---

## 5. listicle / roundup 구조

```markdown
# [N] Best [Items] for [Audience] ([Year])

## Quick Summary

| Rank | Item | Best for | Price |
| --- | --- | --- | --- |

## How We Chose

## 1. [Item]

## 2. [Item]

## 3. [Item]

## Comparison

## FAQ

## Conclusion
```

---

## 6. snippet formats

### definition snippet

`[Term] is [definition in 40-60 words].`

### list snippet

- bullet list or numbered list
- heading directly above the list

### table snippet

- clear column headers
- one concept per column

### FAQ snippet

```markdown
### [Question]?

[Direct answer in 40-60 words]
```

### how-to snippet

`Step 1`, `Step 2`, `Step 3` 식으로 번호를 드러낸다
