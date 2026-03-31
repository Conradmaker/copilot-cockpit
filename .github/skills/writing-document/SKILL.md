---
name: writing-document
description: "Product and technical documentation patterns for changelogs, API references, guides, ADRs, SDK docs, config refs, and troubleshooting. Use when writing or reviewing developer documentation. Always consult this skill even if the user only mentions 'release notes', 'API docs', 'changelog', 'migration guide', or 'getting started'. For prose clarity use writing-clearly. For blog/content use writing-content. For README use writing-readme. For UX copy use ds-product-ux. Triggers on: changelog, release notes, API reference, technical guide, migration guide, ADR, troubleshooting, SDK docs, config reference, 체인지로그, 릴리스 노트, API 문서, 기술 문서, 가이드, 마이그레이션, 트러블슈팅."
---

# 제품·기술 문서 작성 가이드 (writing-document)

## 목표

제품과 기술에 관한 문서를 독자와 유형에 맞는 구조로 빠르게 설계하고 작성한다. 이 스킬은 문장을 다듬는 일이 아니라, **어떤 유형의 문서인지 먼저 고르고, 그 유형에 맞는 구조와 언어 규칙을 적용해서 독자가 원하는 정보를 빠르게 찾게 만드는 것**이 핵심이다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 문서를 쓰거나 리뷰할 때는 아래 reference 문서를 직접 읽고 유형별 템플릿, Do/Don't 예시, 셀프 리뷰 체크리스트를 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 6대 핵심 원칙

### 1. 독자와 문서 유형을 먼저 고정한다

같은 기능이라도 changelog와 API reference와 migration guide는 독자의 첫 질문이 다르다. 문서를 쓰기 전에 누가 읽는지, 어떤 유형인지, 읽은 뒤 무엇을 할 수 있어야 하는지를 먼저 정한다.

- 독자가 개발자인지, 운영자인지, 최종 사용자인지에 따라 용어 수준과 전제 지식이 달라진다
- 한 문서에 두 가지 유형을 섞지 않는다. changelog 안에 migration guide를 넣으면 둘 다 흐려진다
- 문서의 성공 기준을 먼저 정한다: 독자가 읽고 나서 할 수 있어야 하는 행동이 분명해야 한다
- 유형이 겹치면 주된 목적을 하나 고르고 보조 reference를 추가로 읽는다

#### 빠른 판단 기준

- 독자를 한 문장으로 설명할 수 없으면 아직 쓰기 전이다
- 아래 `references/ 가이드` 테이블에서 유형에 맞는 reference를 하나 고르지 못하면 범위를 먼저 좁힌다
- 같은 문서 안에서 "이건 changelog이기도 하고 migration guide이기도 하다"면 분리한다

→ 상세: [references/01-documentation-principles.md](references/01-documentation-principles.md)

### 2. 사용자가 할 수 있는 일 중심으로 쓴다

기술문서는 우리가 무엇을 빌드했는지가 아니라 독자가 무엇을 할 수 있는지를 먼저 말해야 한다. 내부 구현 이야기보다 독자의 행동과 결과가 앞에 온다.

- "Implemented batch processing queue"가 아니라 "You can now export up to 10,000 rows at once"
- API reference는 "이 함수는 무엇을 한다"로 시작한다. 설계 배경이나 역사는 뒤에 둔다
- 에러 메시지를 문서화할 때도 원인보다 해결 방법을 먼저 쓴다

#### 빠른 판단 기준

- 첫 문장의 주어가 시스템이나 코드면 독자 중심으로 바꿀 수 있는지 검토한다
- "~를 구현했다", "~를 리팩토링했다"가 보이면 사용자 행동으로 바꾼다
- PR 번호, 내부 코드명, 브랜치 이름이 독자에게 보이면 제거한다

→ 상세: [references/01-documentation-principles.md](references/01-documentation-principles.md)

### 3. 구조를 먼저 세우고 내용을 채운다

기술문서는 위에서 아래로 읽히기보다 필요한 부분을 찾아서 읽힌다. 독자가 원하는 정보를 빠르게 찾을 수 있는 구조가 먼저고, 그 안의 문장은 나중이다.

- 문서 유형별로 정해진 구조 템플릿이 있다. 템플릿을 먼저 채택하고 내용을 넣는다
- 소제목(H2, H3)만 훑어봐도 문서 전체 흐름이 보여야 한다
- 목차가 필요한 긴 문서는 서문 직후에 목차를 넣는다

#### 빠른 판단 기준

- 소제목만 읽어서 문서의 흐름을 파악할 수 없으면 소제목부터 다시 쓴다
- 비슷한 정보가 두 섹션에 나뉘어 있으면 하나로 합친다
- 한 섹션이 화면 3개 이상을 차지하면 분리하거나 하위 섹션으로 나눈다

→ 상세: 현재 문서 유형에 맞는 reference (원칙 1 테이블 참조)

### 4. 코드와 예시를 설명보다 앞에 둔다

개발자는 긴 설명보다 동작하는 코드와 구체적 예시에서 더 빠르게 이해한다. 설명은 예시 뒤에 오는 게 자연스럽다.

- API reference는 정의 직후에 동작하는 최소 코드 예시를 넣는다
- How-to guide는 매 단계마다 코드 또는 명령어를 포함한다
- 설정 문서는 기본값이 포함된 코드 블록을 먼저 보여준다
- "다음과 같이 할 수 있습니다"라고 쓰기보다 코드를 먼저 놓고 설명을 뒤에 붙인다

#### 빠른 판단 기준

- 설명 문단이 코드 없이 3개 이상 이어지면 예시를 끼워 넣을 수 있는지 본다
- 코드 예시가 실제로 동작하지 않는 pseudo-code면 동작하는 코드로 바꾼다
- 코드 블록에 파일 경로(`filename`)와 언어 태그가 빠져 있으면 추가한다

→ 상세: 현재 문서 유형에 맞는 reference (원칙 1 테이블 참조)

### 5. 버전과 변경 이력을 추적 가능하게 만든다

기술문서는 시점에 따라 진실이 달라진다. 어떤 버전에서 이 동작이 바뀌었는지, 어떤 옵션이 언제 deprecated됐는지 독자가 추적할 수 있어야 한다.

- changelog는 날짜와 버전 번호를 빠뜨리지 않는다
- API reference는 Version History 테이블로 변경 이력을 보여준다
- breaking change는 What changed → What to do → Timeline 구조로 명확히 안내한다
- deprecated 기능은 대체 방법과 제거 시점을 함께 적는다

#### 빠른 판단 기준

- changelog entry에 날짜가 없으면 추가한다
- "이 기능은 deprecated됩니다"만 있고 대안과 시점이 없으면 불완전하다
- 버전 간 동작 차이가 있는데 "v2에서 변경" 같은 이력이 없으면 추가한다

→ 상세: [references/02-changelog-release-notes.md](references/02-changelog-release-notes.md), [references/05-migration-adr.md](references/05-migration-adr.md)

### 6. 셀프 리뷰 게이트를 통과한다

문서를 완성하기 전에 아래 체크리스트를 통과한다. 하나라도 실패하면 해당 원칙으로 돌아가서 수정한다.

#### 공통 체크리스트

| # | 점검 항목 | 관련 원칙 |
|---|---------|---------|
| 1 | 독자와 문서 유형이 명확히 정해져 있다 | 원칙 1 |
| 2 | 첫 문장이 독자가 할 수 있는 일 또는 API가 하는 일로 시작한다 | 원칙 2 |
| 3 | 내부 구현 용어(PR 번호, 브랜치명, 내부 코드명)가 독자에게 노출되지 않는다 | 원칙 2 |
| 4 | 소제목만 읽어도 문서 전체 흐름이 파악된다 | 원칙 3 |
| 5 | 주요 설명 앞에 동작하는 코드 예시가 있다 | 원칙 4 |
| 6 | 코드 블록에 언어 태그와 파일 경로가 있다 | 원칙 4 |
| 7 | 버전 정보나 날짜가 필요한 곳에 빠지지 않았다 | 원칙 5 |
| 8 | deprecated 기능에 대안과 제거 시점이 명시되어 있다 | 원칙 5 |
| 9 | "powerful", "easily", "simply", "seamless" 같은 판촉 수식어가 없다 | 전체 |
| 10 | "various bug fixes" 같은 정보 없는 요약이 없다 | 전체 |

#### 유형별 추가 체크리스트

유형별 셀프 리뷰 항목은 해당 reference에 있다. reference를 읽을 때 함께 확인한다.

→ 상세: [references/01-documentation-principles.md](references/01-documentation-principles.md)

---

## 작업 흐름

### 새 문서를 쓸 때

1. **[retrieval]** [references/01-documentation-principles.md](references/01-documentation-principles.md)를 읽는다
2. 원칙 1을 적용하여 독자, 문서 유형, 성공 기준을 고정한다
3. **[retrieval]** 문서 유형에 맞는 reference를 읽는다 (원칙 1 테이블 참조)
4. reference의 구조 템플릿을 선택하고, 원칙 3을 적용하여 소제목부터 잡는다
5. 원칙 2, 4를 적용하며 사용자 중심 언어 + 코드 예시 우선 순서로 내용을 채운다
6. 원칙 5를 적용하여 버전·이력·타임라인 정보를 보강한다
7. 원칙 6 셀프 리뷰 게이트를 통과시킨다

### 기존 문서를 리뷰·갱신할 때

1. **[retrieval]** [references/01-documentation-principles.md](references/01-documentation-principles.md) + 해당 유형 reference를 읽는다
2. 현재 문서와 실제 코드·제품 상태를 대조한다. 불일치가 있으면 표시한다
3. 원칙 6 셀프 리뷰 게이트를 돌려 갭을 식별한다
4. 갭을 수정한다. 구조 문제면 원칙 3부터, 언어 문제면 원칙 2부터 재적용한다

### changelog entry를 쓸 때 (빠른 경로)

1. **[retrieval]** [references/02-changelog-release-notes.md](references/02-changelog-release-notes.md)를 읽는다
2. 카테고리(New/Improved/Fixed/Removed/Security)를 고른다
3. entry anatomy(카테고리 → 제목 → 현재 가능한 일 → 방법 → 변경 전 → 시각자료)를 따른다
4. breaking change면 What changed → What to do → Timeline 구조를 추가한다

---

## references/ 가이드

| 파일 | 내용 | 언제 읽는가 |
|-----|-----|----------|
| [references/01-documentation-principles.md](references/01-documentation-principles.md) | 모든 기술문서에 공통 적용되는 작성 원칙, 금지 패턴, 셀프 리뷰 상세 체크리스트 | 어떤 유형이든 문서를 쓰기 전에 먼저 |
| [references/02-changelog-release-notes.md](references/02-changelog-release-notes.md) | Entry anatomy, 카테고리, 버전 관리, breaking change 구조, 배포 채널 포맷, 템플릿 | Changelog, release notes를 쓸 때 |
| [references/03-api-reference.md](references/03-api-reference.md) | API 카테고리별 템플릿(Function/Component/Config/Directive), 규칙, OpenAPI 연동 | API reference 문서를 쓸 때 |
| [references/04-technical-guides.md](references/04-technical-guides.md) | How-to, Tutorial, Getting Started, Quickstart, Troubleshooting 구조와 템플릿 | 기술 가이드나 트러블슈팅 문서를 쓸 때 |
| [references/05-migration-adr.md](references/05-migration-adr.md) | 마이그레이션 가이드 구조, deprecation 패턴, ADR 포맷과 상태 관리 | 마이그레이션, breaking change, ADR, 기술 명세를 쓸 때 |
| [references/06-config-sdk-reference.md](references/06-config-sdk-reference.md) | Config 옵션 테이블, CLI 레퍼런스, SDK 문서화, 환경변수 패턴 | 설정, CLI, SDK, 환경변수 문서를 쓸 때 |

### 추천 로드 순서

- **Changelog 작성**: `01 → 02`
- **API reference 작성**: `01 → 03`
- **Getting Started / How-to 작성**: `01 → 04`
- **Migration guide 작성**: `01 → 05 → 02` (changelog에 breaking change를 함께 쓸 때)
- **ADR 작성**: `01 → 05`
- **Config / SDK reference 작성**: `01 → 06`
- **Troubleshooting 작성**: `01 → 04`

---

## 응답 패턴

문서를 작성할 때는 결과물만 던지지 않고, 선택한 유형과 구조의 이유를 함께 제시한다.

### 새 문서 작성 요청

1. 독자와 문서 유형 정의
2. 선택한 구조 템플릿과 이유
3. 문서 본문
4. 빠뜨린 정보나 확인이 필요한 항목 표시

### 기존 문서 리뷰 요청

1. 문서 유형과 독자 확인
2. 셀프 리뷰 게이트 결과 (통과/실패 항목)
3. 코드·제품 상태와의 불일치 목록
4. 수정 제안 (구조 → 언어 → 이력 순서)

### Changelog entry 요청

1. 카테고리 선택
2. 사용자 중심 entry
3. breaking change면 마이그레이션 구조 포함

---

## 범위

| 작업 | 사용할 스킬 |
|-----|----------|
| 문장 단위 명료화, AI 패턴 제거, 휴머나이징 | writing-clearly |
| 소셜 포스트, 블로그, 아티클 같은 대외 발행 콘텐츠 | writing-content |
| README 파일 | writing-readme |
| 콘텐츠 소스 리서치·정보 수집 | research-content-source |
| 테크니컬 SEO | seo-technical |
| 콘텐츠 SEO 최적화 | seo-content |
| UX 라이팅, CTA 문구, 에러 문구 | ds-product-ux |

이 스킬은 제품·기술 문서의 구조, 유형별 작성 패턴, 버전 관리, 셀프 리뷰를 담당한다. 문장 교정, 대외 콘텐츠 작성, 리서치, SEO, UX 문구까지 한 스킬에 넣지 않는다.
