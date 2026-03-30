# Competitive Analysis

## 경쟁자 유형

| 유형 | 정의 | 예시 |
|------|------|------|
| **Direct** | 같은 솔루션, 같은 시장, 같은 고객 | Slack vs Microsoft Teams vs Discord (업무용) |
| **Indirect** | 다른 솔루션, 같은 문제 | 이메일 vs 프로젝트 관리 도구 (둘 다 팀 커뮤니케이션) |
| **Substitute** | 근본적으로 다른 방식으로 문제 해결 | Uber vs 대중교통 vs 자전거 공유 |
| **Potential Entrants** | 지금은 경쟁하지 않지만 진입 가능 | 검색 시장 진입하는 Apple (Google에 잠재적 위협) |

---

## Porter's Five Forces

경쟁 강도와 산업 수익성 분석 프레임워크.

```
           THREAT OF NEW ENTRANTS
                    ↓
SUPPLIER POWER ← INDUSTRY → BUYER POWER
                 RIVALRY
                    ↑
           THREAT OF SUBSTITUTES
```

### 1. Competitive Rivalry

**질문**:
- 경쟁자가 얼마나 많은가?
- 제품이 얼마나 유사한가?
- 산업 성장률은 어떤가?
- 퇴출 장벽은 무엇인가?

**High Rivalry 지표**:
- 비슷한 규모의 경쟁자 다수
- 느린 산업 성장
- 높은 고정 비용
- 낮은 차별화 (commoditized)
- 높은 퇴출 장벽

### 2. Threat of New Entrants

**질문**:
- 진입 장벽은 무엇인가?
- 경쟁을 시작하기 얼마나 쉬운가?

**진입 장벽**:
- 자본 요구사항
- 브랜드 충성도
- 전환 비용
- 규제 장벽
- 특허/IP
- 유통 접근성

### 3. Threat of Substitutes

**질문**:
- 문제를 해결할 대안이 있는가?
- 대안으로의 전환 비용은 어떤가?

**High Threat 지표**:
- 많은 대안 존재
- 낮은 전환 비용
- 대안이 개선되고 있음
- 대안의 가격-성능이 매력적

### 4. Supplier Power

**질문**:
- 공급자가 얼마나 많은가?
- 그들의 투입물이 얼마나 독특한가?
- 공급자를 쉽게 바꿀 수 있는가?

**High Supplier Power**:
- 소수의 공급자
- 독특한 투입물
- 높은 전환 비용
- 공급자가 forward integration 가능

### 5. Buyer Power

**질문**:
- 구매자가 얼마나 많은가?
- 가격에 얼마나 민감한가?
- 쉽게 바꿀 수 있는가?

**High Buyer Power**:
- 많은 구매자
- 표준화된 제품
- 낮은 전환 비용
- 구매자가 backward integration 가능
- 구매자의 가격 민감도

---

## Competitive Positioning Matrix

### 2x2 Matrix 프레임워크

**목적**: 두 가지 핵심 차원에서 경쟁 환경 시각화

**일반적인 차원 쌍**:
- 가격 (낮음 ← → 높음) × 기능 (적음 ← → 많음)
- 사용 편의성 (단순 ← → 복잡) × 파워 (기본 ← → 고급)
- 시장 초점 (SMB ← → Enterprise) × 전문화 (일반 ← → Niche)

**예시: 프로젝트 관리 도구**

```
                많은 기능
                   ↑
              [Jira]
                   |
단순 ← [Trello] [Asana] [Monday.com] → 복잡
                   |
              [ClickUp]
                   ↓
                적은 기능
```

**인사이트**:
- 경쟁자가 어디에 모여 있는가? (혼잡한 공간)
- White space는 어디인가? (기회)
- 우리는 어떻게 차별화되는가?

---

## Feature Comparison Matrix

| 기능 | 우리 | 경쟁사 A | 경쟁사 B | 경쟁사 C |
|------|-----|----------|----------|----------|
| **가격** |
| 무료 티어 | ✓ | ✓ | ✗ | ✓ |
| 유료 티어 | $10, $20 | $15, $30 | $25 | $12 |
| **핵심 기능** |
| 실시간 협업 | ✓ | ✓ | ✓ | ✗ |
| 모바일 앱 | ✓ | ✓ | ✗ | ✗ |
| 연동 | 50+ | 100+ | 20 | 10 |
| API 접근 | ✓ | ✓ (Enterprise) | ✓ | ✗ |
| **고급** |
| AI 기능 | ✓ | ✗ | ✓ | ✗ |
| 커스텀 워크플로우 | ✓ | ✓ | ✗ | ✗ |
| **지원** |
| 이메일 지원 | ✓ | ✓ | ✓ | ✓ |
| 채팅 지원 | ✓ | ✗ | ✓ | ✗ |
| 전담 CSM | ✓ (Enterprise) | ✓ (Enterprise) | ✗ | ✗ |

**색상 코딩**:
- ✓ = 우리 승리
- ✗ = 우리 패배
- ≈ = 동등

---

## 정보 수집 소스

### 제품 분석
- 경쟁사 제품 가입 (무료 체험)
- 고객처럼 사용해보기
- UX, 기능, 성능 문서화
- 스크린샷과 노트 작성

### 고객 리뷰
- G2, Capterra, TrustRadius
- App Store 리뷰 (iOS, Android)
- Reddit, Product Hunt 댓글
- 트위터/소셜 미디어 감성

찾을 것:
- 고객이 좋아하는 것 (따라해야 할 강점)
- 고객이 싫어하는 것 (공략할 약점)

### 공개 소스
- 연례 보고서 (상장사)
- 보도자료 및 공지
- 블로그 포스트와 콘텐츠
- 채용 공고 (무엇을 만들고 있는지)
- 컨퍼런스 발표
- Changelog와 릴리스 노트