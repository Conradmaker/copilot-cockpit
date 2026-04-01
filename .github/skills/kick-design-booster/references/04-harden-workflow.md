# Harden — 견고화 워크플로우

Prefer retrieval-led reasoning over pre-training-led reasoning.

극단적인 입력, 에러 시나리오, 국제화 요구에서도 UI가 깨지지 않도록 강화하는 워크플로우다.

---

## 언제 사용하는가

- 감사에서 엣지 케이스 대응이 약하다고 나왔을 때
- "이름이 길면 어떻게 되지?", "에러나면?"
- 다국어 지원, RTL 레이아웃이 필요할 때

## 워크플로우

### Step 1: 극단 입력 테스트

모든 텍스트 노출 영역에 대해:

| 입력 유형 | 테스트 데이터 | 확인 사항 |
|-----------|--------------|-----------|
| 빈 값 | `""`, `null`, `undefined` | 빈 상태 UI가 나오는가? |
| 초장문 | 200자+ 이름, 1000자 설명 | 잘림/줄바꿈이 적절한가? |
| 특수문자 | `<script>`, `"quotes"`, 이모지 | XSS 방지, 깨짐 없음 |
| 극단 숫자 | 0, -1, 999999999 | 오버플로우 없음 |
| 단일 긴 단어 | `Pneumonoultramicroscopicsilicovolcanoconiosis` | `overflow-wrap: break-word` |

**텍스트 오버플로우 CSS 패턴:**

```css
/* 한 줄 말줄임 */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 여러 줄 말줄임 */
.line-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 긴 단어 줄바꿈 */
.break-word {
  overflow-wrap: break-word;
  word-break: break-word;
  hyphens: auto;
}
```

### Step 2: 에러 시나리오

모든 비동기 작업에 대해:

| 시나리오 | 확인 사항 |
|----------|-----------|
| 네트워크 끊김 | 오프라인 표시, 재시도 유도 |
| 서버 500 | 사용자 친화적 에러 메시지 |
| 타임아웃 | 진행 중단 알림, 재시도 버튼 |
| 권한 없음 (403) | 접근 불가 안내, 권한 요청 경로 |
| 리소스 없음 (404) | 대체 콘텐츠 또는 홈 이동 안내 |
| 중복 제출 | 버튼 비활성화, 낙관적 UI 대기 |
| 부분 실패 | 성공/실패 항목 구분 표시 |

### Step 3: 국제화 (i18n) 견고화

**텍스트 팽창 대응:**

| 영어 길이 | 번역 후 예상 팽창 | 주의 영역 |
|-----------|-------------------|-----------|
| ~10자 | +200~300% | 버튼, 탭, 뱃지 |
| ~20자 | +100~200% | 내비게이션, 폼 라벨 |
| ~70자+ | +30~40% | 본문 |

독일어 기준 +30%가 일반적이다. 핵심 UI 요소에 독일어 길이 텍스트를 넣어 테스트한다.

**날짜/숫자 포맷:**
- `Intl.DateTimeFormat`, `Intl.NumberFormat` 사용
- 하드코딩된 MM/DD/YYYY 제거

**RTL 대응 원칙:**
- 논리적 속성 사용: `margin-inline-start` (not `margin-left`)
- Flexbox `gap`은 자동 대응
- 아이콘 방향 (화살표, 체크마크) 확인
- `dir="rtl"` 테스트

---

## 체크리스트

- [ ] 모든 텍스트 영역에 빈 값, 초장문, 특수문자 테스트 했는가?
- [ ] 모든 비동기 작업에 에러/타임아웃 시나리오가 있는가?
- [ ] 텍스트 팽창 +30%에서 레이아웃이 유지되는가?
- [ ] 하드코딩된 날짜/숫자 포맷이 없는가?
