# Changelog & Release Notes 작성 가이드

이 문서는 changelog entry, release notes, 버전 관리, 배포 채널별 포맷을 다룬다.

---

## Entry Anatomy

좋은 changelog entry는 일관된 구조를 따른다.

```
카테고리 라벨 → 사용자 중심 제목 → 지금 할 수 있는 일 → 방법 → 이전 상태 → 시각자료(선택)
```

### 예시

```markdown
### New: Bulk Export for Reports 📊

You can now export up to 10,000 rows at once from any report view.
Select your rows, click Export, and choose CSV or Excel format.

Previously limited to 500 rows per export.

![Bulk export button in the reports toolbar](screenshot.png)
```

### 구조 분해

| 요소 | 역할 | 필수 여부 |
|-----|-----|---------|
| **카테고리 라벨** | New / Improved / Fixed / Removed / Security | 필수 |
| **사용자 중심 제목** | 독자가 얻는 것을 한 줄로 | 필수 |
| **지금 할 수 있는 일** | 기능 설명 (사용자 행동 기준) | 필수 |
| **방법** | 구체적 조작법 또는 접근 경로 | 권장 |
| **이전 상태** | 변경 전과 비교 | 대비 효과가 클 때 |
| **시각자료** | 스크린샷, GIF, 차트 | 새 UI 기능일 때 |

---

## 카테고리

| 카테고리 | 아이콘 | 사용 기준 |
|---------|-------|---------|
| **New** | ✨ 🆕 | 이전에 불가능했던 완전히 새로운 기능 |
| **Improved** | ⚡ 🔧 | 기존 기능이 더 좋아짐 (빠름, 쉬움, 확장) |
| **Fixed** | 🐛 🔨 | 고장 났던 것이 정상 동작으로 복구 |
| **Removed** | 🗑️ ⚠️ | Deprecated 또는 제거된 기능 |
| **Security** | 🔒 | 보안 패치 |

### 카테고리 판단 규칙

- **New** = 사용자가 이전에 전혀 할 수 없었던 것
- **Improved** = 이전에 할 수 있었지만, 이제 더 좋거나/빠르거나/쉬운 것
- **Fixed** = 잘못 동작하던 것이 의도대로 동작하게 된 것
- "Updated"는 사용하지 않는다. 개선인지 수정인지 불분명하기 때문이다

---

## 사용자 중심 언어

### Do / Don't

```
❌ 내부 중심:
"Implemented batch processing queue for the export service"
"Refactored the ReportExporter class to support pagination"
"Fixed bug in CSV serialization (PR #4521)"

✅ 사용자 중심:
"You can now export up to 10,000 rows at once from any report"
"Reports now load 3x faster when filtering large datasets"
"Fixed an issue where exported CSV files had missing columns"
```

### 적용 규칙

- "You can now..." / "[Feature] now..." / "Fixed an issue where..."로 시작한다
- 메커니즘이 아니라 이점(benefit)을 먼저 쓴다
- 현재 시제를 사용한다
- PR 번호, 이슈 번호, 내부 코드명을 노출하지 않는다

---

## 버전 관리

### Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH
  3   .  2  .  1
```

| 구성 요소 | 올리는 시점 | 예시 |
|----------|----------|-----|
| **MAJOR** | Breaking change, 대규모 재설계 | 2.0.0 → 3.0.0 |
| **MINOR** | 새 기능 추가 (하위 호환) | 3.1.0 → 3.2.0 |
| **PATCH** | 버그 수정, 소규모 개선 | 3.2.0 → 3.2.1 |

### 날짜 기반 버전

```
2026-02-08  또는  February 8, 2026
```

SaaS, 지속 배포 환경에 적합하다. SemVer와 날짜 중 프로젝트에 맞는 것을 선택한다.

---

## Breaking Change 구조

Breaking change는 일반 entry와 분리해서, 전용 구조로 작성한다.

### 템플릿

```markdown
### ⚠️ Breaking: API v2 Endpoints Deprecated

**What changed:** API v1 endpoints will stop working on March 15, 2026.

**What you need to do:**
1. Update your API calls to use v2 endpoints ([migration guide →](link))
2. Update authentication to use Bearer tokens instead of API keys
3. Test your integration before March 15

**Timeline:**
- Now: v2 endpoints available, v1 still works
- March 1: v1 returns deprecation warnings
- March 15: v1 stops working

If you need help migrating, contact support@company.com.
```

### 구조: What changed → What to do → Timeline

| 섹션 | 내용 |
|-----|-----|
| **What changed** | 무엇이 바뀌었는지 한 문장으로 |
| **What you need to do** | 독자가 취해야 할 행동, 번호 매긴 순서대로 |
| **Timeline** | 날짜별 단계. 현재 → 경고 → 중단 시점 |

- 마이그레이션 가이드 링크를 반드시 포함한다
- 지원 문의 경로를 안내한다
- breaking change는 changelog 상단에 배치해서 놓치지 않게 한다

---

## Changelog 페이지 구조

### 전체 레이아웃

```markdown
# Changelog

## February 8, 2026

### New
- **Bulk Export for Reports** — Export up to 10,000 rows at once. [Learn more →](link)
- **Dark Mode** — Toggle dark mode from Settings > Appearance.

### Improved
- **Dashboard Loading** — Dashboards now load 3x faster on large datasets.
- **Search** — Search results now include archived items.

### Fixed
- Fixed an issue where exported CSV files had missing column headers.
- Fixed a bug where the date picker showed incorrect timezone.

---

## February 1, 2026

### New
- **API Webhooks** — Get notified when events happen in your account.

### Fixed
- Fixed an issue where email notifications were delayed by up to 2 hours.
```

### 구성 규칙

- 날짜별로 그룹한다 (최신이 위)
- 각 날짜 안에서 카테고리별로 그룹한다 (New → Improved → Fixed → Removed → Security)
- 가장 크거나 가장 많이 요청된 변경이 카테고리 내 첫 번째에 온다
- 관련 문서 링크가 있으면 "Learn more →"로 연결한다
- 날짜 구분선(`---`)으로 릴리스 경계를 표시한다

---

## 시각자료

### 시각자료를 넣어야 할 때

| 변경 유형 | 시각자료 |
|----------|---------|
| 새 UI 기능 | 기능 스크린샷 |
| UI 재설계 | Before / After 비교 |
| 새 워크플로 | 단계별 스크린샷 또는 짧은 영상 |
| 성능 개선 | 개선폭을 보여주는 차트 |
| 복잡한 기능 | 애니메이션 GIF 또는 데모 영상 |

---

## 배포 채널별 포맷

| 채널 | 포맷 | 사용 시점 |
|-----|-----|---------|
| **Changelog 페이지** | 전체 상세 entry | 매 릴리스 |
| **인앱 알림** | 1~2줄 요약 | 새 기능, breaking change |
| **이메일** | 큐레이션된 하이라이트 + 시각자료 | 주요 릴리스 (월간/분기) |
| **블로그** | 맥락과 배경이 포함된 장문 | 큰 런칭 |
| **소셜 미디어** | 단일 기능 하이라이트 | 주목할 기능 |

### 소셜 미디어 snippet 포맷

```
🆕 New in [Product]: [Feature Name]

[1-2 sentence description of what you can now do]

[Screenshot or demo video]

Try it now → [link]
```

---

## Changelog 빈도

| 제품 유형 | 빈도 | 참고 |
|----------|------|-----|
| SaaS (continuous deploy) | 주간 배치 | 일주일 변경 묶기 |
| SaaS (major features) | 기능 런칭별 | 블로그 포스트와 함께 |
| Versioned software | 버전 릴리스별 | SemVer에 맞춤 |
| API | 버전별 + deprecation notice | 마이그레이션 가이드 포함 |
| Mobile app | 앱스토어 릴리스별 | "What's New" 텍스트와 동기화 |

---

## 흔한 실수

| 실수 | 문제 | 해결 |
|-----|-----|-----|
| 개발자 언어 사용 | 사용자가 이해하지 못한다 | 사용자가 할 수 있는 일로 쓴다 |
| "Bug fixes and improvements" | 정보가 제로다 | 구체적 수정 사항을 나열한다 |
| 날짜 누락 | 무엇이 새로운지 파악 불가 | 모든 entry에 날짜를 넣는다 |
| 시각자료 없음 | 사용자가 텍스트를 건너뛴다 | 주요 기능에 스크린샷을 넣는다 |
| Breaking change가 묻힘 | 사용자가 너무 늦게 발견한다 | 눈에 띄는 경고 + 타임라인 |
| 커밋 로그를 그대로 | 시끄럽고 도움이 안 된다 | 독자 관점에서 큐레이션·재작성한다 |

---

## 유형별 셀프 리뷰 체크리스트

- [ ] 모든 entry에 카테고리 라벨(New/Improved/Fixed/Removed/Security)이 있다
- [ ] entry 제목이 사용자 관점 언어로 되어 있다
- [ ] 모든 릴리스에 날짜(또는 버전 번호)가 있다
- [ ] breaking change가 전용 구조(What changed / What to do / Timeline)를 사용한다
- [ ] breaking change에 마이그레이션 가이드 링크가 있다
- [ ] PR 번호, 이슈 번호, 내부 코드명이 노출되지 않는다
- [ ] 카테고리 내 정렬이 영향도 순이다 (가장 큰 변경이 맨 위)
- [ ] "various bug fixes" 같은 정보 없는 요약이 없다
- [ ] 새 UI 기능에 스크린샷이 있다
