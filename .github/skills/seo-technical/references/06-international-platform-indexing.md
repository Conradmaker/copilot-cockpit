# International and Cross-Engine Indexing

## 목표

locale, hreflang, region targeting이 기술 SEO와 플랫폼 visibility에 미치는 영향을 정리한다.

---

## 1. hreflang 기본 체크

- hreflang이 실제로 존재하는가
- self-referencing hreflang이 있는가
- return tags가 맞는가
- language/region code가 유효한가
- x-default가 필요한 구조인가

### 흔한 실수

| 실수 | 영향 |
| --- | --- |
| self-reference 없음 | locale 신호 약화 |
| return tag 없음 | 매핑 무효화 가능 |
| 잘못된 코드 | 검색 엔진 해석 실패 |
| canonical과 hreflang conflict | 잘못된 대표 URL 선택 |

---

## 2. locale-specific indexing 관점

- Google은 hreflang, canonical, content language, host/ccTLD, internal linking을 함께 본다
- Bing도 locale targeting을 보지만, implementation tolerance가 다를 수 있다
- AI engines는 명시적 hreflang보다도 index source와 clear locale signals에 더 의존할 수 있다

---

## 3. 점검 표

```markdown
| Check | Status | Notes |
| --- | --- | --- |
| hreflang tags present | ✅/⚠️/❌ | |
| self-referencing | ✅/⚠️/❌ | |
| return tags | ✅/⚠️/❌ | |
| valid locale codes | ✅/⚠️/❌ | |
| canonical aligns with locale | ✅/⚠️/❌ | |
| x-default strategy | ✅/⚠️/❌ | |
```

---

## 4. 언제 이 reference를 읽는가

- 국가별 서브디렉터리 또는 서브도메인이 있을 때
- 특정 지역 결과에서만 누락될 때
- migration으로 locale URL 구조가 바뀌었을 때