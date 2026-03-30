# 기술문서 공통 작성 원칙

이 문서는 모든 유형의 기술문서에 공통 적용되는 작성 원칙, 금지 패턴, 셀프 리뷰 체크리스트를 담는다. 문서 유형에 관계없이, 기술문서를 쓰기 전에 이 문서를 먼저 읽는다.

---

## 1. 독자 정의

문서를 쓰기 전에 아래 세 가지를 먼저 고정한다.

| 항목 | 질문 | 예시 |
|-----|-----|-----|
| **누가 읽는가** | 이 문서의 1차 독자는 누구인가? | 프론트엔드 개발자, 인프라 운영자, 제품 사용자 |
| **어떤 상태에서 읽는가** | 독자가 이 문서를 찾는 시점의 상황은? | 새 기능을 처음 연동할 때, 에러가 발생해서 해결법을 찾을 때 |
| **읽은 뒤 무엇을 할 수 있어야 하는가** | 문서의 성공 기준은? | API 호출을 완료한다, 마이그레이션을 마친다, 에러를 해결한다 |

이 세 가지가 모호하면 문서를 쓰지 않는다. 먼저 좁힌다.

### 독자 수준별 전제 지식

- **초급 독자**: 용어를 정의하고 모든 단계를 보여준다. "이건 알 것이다"라고 가정하지 않는다.
- **중급 독자**: 기본 개념은 생략할 수 있지만, 컨텍스트가 달라지는 부분은 명시한다.
- **고급 독자**: 배경 설명을 최소화하고 참조 정보와 edge case에 집중한다.

하나의 문서에서 여러 수준을 동시에 만족시키려 하지 않는다. 독자를 하나로 정한다.

---

## 2. 사용자 중심 언어

기술문서는 우리가 무엇을 만들었는지가 아니라 독자가 무엇을 할 수 있는지를 먼저 말한다.

### Do / Don't

| Don't (내부 중심) | Do (사용자 중심) |
|------------------|---------------|
| Implemented batch processing queue for the export service | You can now export up to 10,000 rows at once from any report |
| Refactored the ReportExporter class to support pagination | Reports now load 3x faster when filtering large datasets |
| Fixed bug in CSV serialization (PR #4521) | Fixed an issue where exported CSV files had missing columns |
| Updated the auth module | You can now sign in with Google or GitHub |

### 적용 규칙

- 첫 문장의 주어가 시스템이나 코드이면 독자 중심으로 바꿀 수 있는지 검토한다
- "~를 구현했다", "~를 리팩토링했다"는 독자에게 의미 없다. 독자의 행동이나 결과로 바꾼다
- PR 번호, 내부 코드명, 브랜치 이름은 독자에게 보이지 않게 한다
- 이점(benefit)을 메커니즘(mechanism)보다 앞에 둔다

---

## 3. 기계적·관찰 가능한 언어

기술문서는 느낌이나 가치 판단이 아니라, 무슨 일이 일어나는지를 서술한다.

### Do / Don't

| Don't (주관적·판촉적) | Do (기계적·관찰 가능) |
|---------------------|------------------|
| This powerful function lets you easily manage cookies | `cookies` is an async function that reads HTTP request cookies in Server Components |
| You can conveniently access... | Returns an object containing... |
| The best way to handle navigation | `<Link>` extends the HTML `<a>` element to provide prefetching and client-side navigation |
| Seamlessly integrates with your workflow | Accepts a config object and returns a client instance |

### 금지 수식어

아래 단어는 기술문서에서 정보를 추가하지 않는다. 제거한다.

> powerful, easily, simply, seamlessly, effortlessly, conveniently, intuitively, beautifully, elegantly, robust, comprehensive, state-of-the-art, cutting-edge, game-changing, revolutionary, best-in-class, world-class

### 금지 패턴

| 패턴 | 문제 | 대안 |
|------|-----|-----|
| "various bug fixes" | 정보가 없다 | 구체적인 수정 사항을 나열한다 |
| "Updated [feature]" | 어떻게 바뀌었는지 알 수 없다 | 개선인지 수정인지 명시한다 |
| "다양한 성능 개선" | 독자가 확인할 수 없다 | 어디가 어떻게 빨라졌는지 수치를 넣는다 |
| "기타 수정" | 게으르다 | 나열하거나, 정말 중요하지 않으면 생략한다 |
| "자세한 내용은 문서를 참조하세요" (링크 없음) | 독자가 찾을 수 없다 | 구체적 링크를 건다 |

---

## 4. 구조 우선 원칙

기술문서는 위에서 아래로 읽히기보다, 독자가 필요한 부분을 찾아서 읽는다. 구조가 먼저다.

### 소제목 규칙

- 소제목(H2, H3)만 훑어봐도 문서 전체 흐름이 보여야 한다
- 소제목에 동사를 넣는다: "Authentication" 대신 "Authenticate requests"
- 비슷한 정보가 두 곳에 있으면 하나로 합친다
- 한 섹션이 화면 3개 이상이면 분리하거나 하위 섹션으로 나눈다

### 목차

- 섹션이 5개 이상이거나, 문서가 화면 10개 이상이면 서문 직후에 목차를 넣는다
- 목차는 H2 수준까지만 노출한다. H3까지 넣으면 목차가 본문만큼 길어진다

### Answer-first 구조

- 각 섹션은 결론→설명→예시 순서로 배치한다
- 독자가 첫 문장만 읽어도 이 섹션이 뭘 다루는지 알 수 있어야 한다
- "배경 설명 3문단 뒤에 결론"은 기술문서에서 통하지 않는다

---

## 5. 코드와 예시 우선

개발자는 설명보다 동작하는 코드에서 더 빠르게 이해한다.

### 적용 규칙

- API reference는 정의 직후에 동작하는 최소 코드 예시를 넣는다
- How-to guide는 매 단계마다 코드 또는 명령어를 포함한다
- 설정 문서는 기본값이 포함된 코드 블록을 먼저 보여준다
- "다음과 같이 할 수 있습니다"보다 코드를 먼저 놓고 설명을 뒤에 붙인다

### 코드 블록 규칙

- 언어 태그를 반드시 붙인다: ````typescript`, ````bash` 등
- 파일 경로가 있으면 파일명을 함께 표기한다: ````tsx filename="app/page.tsx"`
- 하이라이트할 핵심 줄이 있으면 `highlight` 속성을 쓴다
- pseudo-code 대신 실제 동작하는 코드를 넣는다
- 코드 예시가 3개 이상 이어지면 목적별로 소제목을 나눈다

### 설명 문단 3개 규칙

설명 문단이 코드 없이 3개 이상 이어지면, 예시를 끼워 넣을 수 있는지 확인한다.

---

## 6. 버전과 변경 이력

기술문서는 시점에 따라 진실이 달라진다.

- changelog과 release notes는 날짜와 버전 번호를 빠뜨리지 않는다
- API reference는 Version History 테이블로 변경 이력을 보여준다
- breaking change는 타임라인과 마이그레이션 경로를 함께 안내한다
- deprecated 기능은 대안 + 제거 시점을 명시한다. "곧 제거됩니다"는 부족하다

---

## 7. 내부 정보 제거

독자에게 보이면 안 되는 것들:

- PR 번호, 이슈 번호 (독자가 접근할 수 없는 내부 트래커)
- 브랜치 이름, 커밋 해시
- 내부 코드명, 프로젝트 코드명
- 팀 이름, 담당자 이름 (external doc인 경우)
- 내부 Slack 채널이나 노션 링크

예외: 오픈소스 프로젝트처럼 GitHub issue가 public인 경우는 참조를 허용한다.

---

## 셀프 리뷰 체크리스트 (상세)

문서를 완성하기 전에 아래를 통과시킨다.

### 독자와 범위

- [ ] 1차 독자를 한 문장으로 정의할 수 있다
- [ ] 독자가 읽은 뒤 할 수 있어야 하는 행동이 명확하다
- [ ] 문서 유형이 하나로 고정되어 있다 (changelog + migration guide가 섞이지 않았다)
- [ ] 독자 수준에 맞지 않는 전제 지식을 가정하지 않았다

### 언어와 표현

- [ ] 첫 문장이 독자가 할 수 있는 일 또는 API가 하는 일로 시작한다
- [ ] 내부 구현 용어(PR 번호, 브랜치명)가 독자에게 노출되지 않는다
- [ ] 금지 수식어(powerful, easily, simply, seamless 등)가 없다
- [ ] "various bug fixes", "기타 수정" 같은 정보 없는 요약이 없다
- [ ] "자세한 내용은 문서를 참조하세요" 뒤에 구체적 링크가 있다

### 구조와 탐색

- [ ] 소제목만 읽어도 문서 전체 흐름이 파악된다
- [ ] 각 섹션의 첫 문장이 그 섹션의 내용을 요약한다
- [ ] 비슷한 정보가 두 곳에 나뉘어 있지 않다
- [ ] 문서가 길면 목차가 있다

### 코드와 예시

- [ ] 주요 설명 앞에 동작하는 코드 예시가 있다
- [ ] 코드 블록에 언어 태그와 파일 경로가 있다
- [ ] 설명 문단이 3개 이상 코드 없이 이어지지 않는다
- [ ] pseudo-code 대신 실제 동작하는 코드를 사용했다

### 버전과 이력

- [ ] 버전 정보나 날짜가 필요한 곳에 빠지지 않았다
- [ ] deprecated 기능에 대안과 제거 시점이 있다
- [ ] breaking change에 마이그레이션 경로가 있다
- [ ] Version History 테이블이 필요한 API reference에 있다

### 최종 점검

- [ ] 맞춤법과 용어 일관성을 확인했다
- [ ] 모든 링크가 동작한다
- [ ] 코드 예시를 실행했거나 실행 가능함을 확인했다
- [ ] 문서 제목이 독자가 검색할 키워드를 포함한다
