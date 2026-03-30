# 작문 원칙 상세 (Composition Principles)

Strunk의 작문 원칙과 명확한 글쓰기 방법론을 상세하게 정리한 레퍼런스다. SKILL.md의 원칙 1–3을 적용할 때 이 문서를 먼저 읽는다.

---

## 1. 능동태와 긍정형

### 능동태 (Active Voice)

능동태는 주어가 행동하는 구조다. 수동태보다 짧고, 명확하고, 힘이 있다.

**원칙**: 수동태를 발견하면 주어를 찾아 문장 앞으로 끌어와서 능동태로 바꾼다. 다만 행위자가 불분명하거나 중요하지 않을 때는 수동태가 적합할 수 있다.

**영문 Before/After**:

| Before (수동태) | After (능동태) |
|----------------|---------------|
| The report was written by the team. | The team wrote the report. |
| Mistakes were made in the process. | We made mistakes in the process. |
| The feature was shipped last week. | We shipped the feature last week. |
| It was decided that the project would be delayed. | The board decided to delay the project. |

**한국어 Before/After**:

| Before (수동태·피동) | After (능동태) |
|-------------------|---------------|
| 보고서가 팀에 의해 작성되었습니다. | 팀이 보고서를 작성했습니다. |
| 이 기능은 지난주에 배포되었습니다. | 지난주에 이 기능을 배포했습니다. |
| 결과가 분석되었고 보고되었습니다. | 결과를 분석하고 보고했습니다. |
| 문제가 발견되어 수정이 진행되었습니다. | 문제를 발견해서 수정했습니다. |

**수동태가 적합한 경우**:
- 행위자가 불분명하거나 중요하지 않을 때: "The server was compromised at 3am." (누구인지 모름)
- 행위자보다 대상이 더 중요할 때: "TypeScript was released in 2012." (Microsoft보다 TypeScript가 초점)

### 긍정형 (Positive Form)

부정으로 우회하지 말고 직접 말한다. 이중 부정은 특히 피한다.

**영문 Before/After**:

| Before (부정형) | After (긍정형) |
|----------------|---------------|
| He was not very often on time. | He usually came late. |
| She did not think that studying was useful. | She thought studying was useless. |
| The API does not allow unauthenticated access. | The API requires authentication. |
| It's not uncommon for deployments to fail. | Deployments sometimes fail. |

**한국어 Before/After**:

| Before (부정형) | After (긍정형) |
|----------------|---------------|
| 이 방법이 효과가 없는 것은 아닙니다. | 이 방법도 효과가 있습니다. |
| 사용하지 않을 수 없는 기능입니다. | 반드시 사용해야 하는 기능입니다. |
| 시간이 부족하지 않은 편입니다. | 시간이 충분한 편입니다. |
| 어렵지 않다고 할 수는 없습니다. | 어렵습니다. |

---

## 2. 간결성 (Omit Needless Words)

모든 단어가 일해야 한다. 삭제해도 의미가 바뀌지 않는 단어는 삭제한다.

### 우회구 → 직접 표현

**영문**:

| Before (우회구) | After (직접) |
|----------------|------------|
| the question as to whether | whether |
| there is no doubt but that | no doubt / doubtless |
| used for fuel purposes | used for fuel |
| he is a man who | he |
| in a hasty manner | hastily |
| this is a subject which | this subject |
| the reason why is that | because |
| owing to the fact that | since / because |
| in spite of the fact that | although |
| call your attention to the fact that | remind you / notify you |
| I was unaware of the fact that | I did not know |
| the fact that he had not succeeded | his failure |
| the fact that I had arrived | my arrival |

**한국어**:

| Before (우회구) | After (직접) |
|----------------|------------|
| ~하는 것이 가능하다 | ~할 수 있다 |
| ~에 대해서 말씀드리자면 | ~는 |
| ~의 경우에는 | ~는 / ~면 |
| ~라는 사실을 감안할 때 | ~이므로 |
| ~하는 방향으로 진행하다 | ~하다 |
| ~에 관련된 부분에서 | ~에서 |
| ~를 실시하다/진행하다/수행하다 | ~하다 |
| ~에 있어서 | ~에서 / ~에 |
| 기본적으로 | (대부분 삭제) |
| ~적인 측면에서 볼 때 | ~으로 보면 |

### 강화어(Intensifier) 점검

실제로 의미를 바꾸지 않는 강화어는 삭제한다.

**삭제 대상 (의미를 바꾸지 않으면)**:
- 영문: very, really, truly, extremely, absolutely, basically, essentially, actually, literally, quite, rather, somewhat, pretty (much)
- 한국어: 매우, 정말, 진정으로, 기본적으로, 사실상, 실질적으로, 상당히, 꽤, 다소

**Before/After**:

| Before | After |
|--------|-------|
| This is a very important update. | This is an important update. |
| The system is extremely reliable. | The system is reliable. |
| 매우 중요한 업데이트입니다. | 중요한 업데이트입니다. |
| 기본적으로 이 기능은 작동합니다. | 이 기능은 작동합니다. |

### 한 문장, 하나의 목적

문장 하나에 두 가지 이상의 목적이 들어가면 나눈다.

**Before**:
> This release includes a new dashboard that improves monitoring capabilities while also addressing performance concerns that were raised in the last quarter when several users reported slow load times.

**After**:
> This release includes a new dashboard for better monitoring. It also fixes the slow load times several users reported last quarter.

**한국어 Before**:
> 이번 릴리스에는 모니터링 역량을 향상시키는 새 대시보드가 포함되어 있으며, 지난 분기에 여러 사용자가 보고한 느린 로딩 시간과 관련된 성능 문제도 함께 해결되었습니다.

**한국어 After**:
> 이번 릴리스에 새 대시보드를 추가했습니다. 모니터링이 더 편해집니다. 지난 분기에 보고된 느린 로딩 문제도 수정했습니다.

---

## 3. 구체적이고 명확한 언어

### 추상 → 구체

**영문**:

| Before (추상적) | After (구체적) |
|----------------|--------------|
| A period of unfavorable weather set in. | It rained every day for a week. |
| Significant improvements were made. | Response time dropped from 800ms to 200ms. |
| Various stakeholders were consulted. | We spoke with the design team, three customers, and the CTO. |
| The tool provides powerful capabilities. | The tool generates PDF reports and exports CSV data. |

**한국어**:

| Before (추상적) | After (구체적) |
|----------------|--------------|
| 다양한 분야에서 활용됩니다. | 금융, 의료, 제조 분야에서 활용됩니다. |
| 상당한 성능 개선이 이루어졌습니다. | 응답 시간이 800ms에서 200ms로 줄었습니다. |
| 많은 사용자가 만족하고 있습니다. | 설문 응답자 중 87%가 만족한다고 답했습니다. |
| 핵심적인 역할을 합니다. | 결제 검증과 사기 탐지를 담당합니다. |

### 판촉 형용사 교체

판촉 형용사(promotional adjectives)는 구체적 근거로 교체한다.

| 판촉 형용사 | 교체 방향 |
|-----------|---------|
| groundbreaking | 무엇이 새로운지 구체적으로 |
| cutting-edge | 어떤 기술을 쓰는지 |
| seamless | 어떤 단계가 줄었는지 |
| robust | 어떤 장애에 견디는지 |
| 혁신적인 | 기존 대비 무엇이 바뀌었는지 |
| 핵심적인 | 어떤 기능을 담당하는지 |
| 효과적인 | 어떤 수치가 나오는지 |

### 관련 단어 근접 배치 (Keep Related Words Together)

수식어와 피수식어 사이에 다른 절이 끼면 의미가 흐려진다.

**Before**:
> He noticed a large stain in the rug that was right in the center.

**After**:
> He noticed a large stain right in the center of the rug.

**한국어 Before**:
> 그는 카펫에서 정중앙에 있는 커다란 얼룩을 발견했습니다.

**한국어 After**:
> 그는 카펫 정중앙에서 커다란 얼룩을 발견했습니다.

### 강조할 단어를 문장 끝에 (Place Emphatic Words at the End)

문장에서 가장 중요한 정보를 끝에 배치하면 기억에 남는다.

**Before**:
> Humanity has hardly advanced in fortitude since that time, though it has advanced in many other ways.

**After**:
> Since that time, humanity has advanced in many ways, but hardly in fortitude.

**한국어 Before**:
> 우리는 많은 면에서 발전했지만 인내심은 거의 변하지 않았습니다, 그때 이후로.

**한국어 After**:
> 그때 이후로 많은 면에서 발전했지만, 인내심만은 거의 그대로입니다.

---

## 4. 단락 구조

### 한 단락에 한 주제

단락은 하나의 주제를 다룬다. 주제가 바뀌면 단락을 나눈다.

### 주제문을 단락 맨 앞에

독자가 단락의 첫 문장만 읽어도 이 단락이 무엇에 대한 것인지 알도록 한다.

**Before**:
> There are various factors to consider. Performance is important, but security matters too. We also need to think about cost, scalability, and developer experience. After careful analysis, we chose PostgreSQL.

**After**:
> We chose PostgreSQL. It balances performance, security, and cost for our scale. Developer experience also played a role — most of the team has PostgreSQL experience.

### 병렬 구조 (Express Coordinate Ideas in Similar Form)

같은 수준의 내용은 같은 형식으로 표현한다.

**Before**:
> The tool can analyze code, it has the capability for generating reports, and optimization of queries is also possible.

**After**:
> The tool analyzes code, generates reports, and optimizes queries.

**한국어 Before**:
> 이 도구는 코드를 분석할 수 있고, 보고서 생성 기능도 있으며, 쿼리 최적화도 가능합니다.

**한국어 After**:
> 이 도구는 코드를 분석하고, 보고서를 생성하고, 쿼리를 최적화합니다.

---

## 5. 금지 패턴 종합

아래 패턴이 보이면 즉시 수정한다.

| 패턴 | 예시 | 교정 방향 |
|-----|-----|---------|
| 이중 부정 | "not uncommon", "어렵지 않다고 할 수는 없다" | 긍정형 직접 서술 |
| 헤지 누적 | "It might possibly perhaps..." | 가장 정확한 정도 하나만 남기기 |
| 빈 수식어 | "very unique", "매우 독특한" | unique/독특한만으로 충분 |
| 동어 반복 | "completely eliminate", "완전히 제거" | eliminate/제거만으로 충분 |
| 우회 동사 | "utilize" → "use", "실시하다" → "하다" | 간단한 동사로 교체 |
| 판촉 수식어 | "groundbreaking", "혁신적인" | 구체적 근거로 교체 |
| filler 문장 | "It goes without saying that..." | 삭제 |
| 모호한 대명사 | "This is important." (무엇이?) | 지시 대상 명시 |
