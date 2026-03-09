# Pull Request 생성 워크플로우

## 실행 절차

PR 생성은 `gh` CLI를 활용하여 자동화한다. 상세 CLI 명령어는 `gh-cli` 스킬을 참조한다.

### 1. PR 템플릿 확인

[references/pull_request_template.md](pull_request_template.md) 에서 PR 템플릿을 확인한다. 프로젝트에 `.github/pull_request_template.md`가 있으면 프로젝트 템플릿을 우선한다.

### 2. 기존 PR 확인

```bash
# 현재 브랜치의 기존 PR 확인
gh pr status
gh pr list --head $(git branch --show-current)
```

### 3. Draft PR 생성

```bash
# main 대상으로 draft PR 생성
gh pr create --draft --base main \
  --title "feat(auth): 소셜 로그인 기능 추가" \
  --body-file .github/PULL_REQUEST_TEMPLATE.md

# 또는 인터랙티브 모드
gh pr create --draft
```

### 4. 변경사항 분석 & PR 업데이트

```bash
# PR diff 확인
gh pr diff

# PR 본문/제목 업데이트
gh pr edit --title "feat(auth): 소셜 로그인 기능 추가" \
  --body "## 변경 사항\n- Google, Kakao 소셜 로그인 지원"
```

### 5. Ready for Review

```bash
# draft → ready for review
gh pr ready
```

### 6. 리뷰어 & 담당자 할당

```bash
# 리뷰어 추가
gh pr edit --add-reviewer user1,user2

# 담당자 할당
gh pr edit --add-assignee @me

# 라벨 추가
gh pr edit --add-label enhancement
```

### 7. PR URL 제공

```bash
# PR을 브라우저에서 열기
gh pr view --web
```

---

## PR 규칙

- **PR 제목 = 대표 커밋 제목** — changelog 품질을 유지한다.
- PR 템플릿의 모든 항목을 충실히 채운다.
- 생성 전에 기존 PR 중복 여부를 확인한다.
- 하나의 PR은 하나의 작업 단위를 포함한다.

---

## PR 병합 후

```bash
# PR 병합 (squash merge 권장)
gh pr merge --squash --delete-branch

# 또는 merge commit
gh pr merge --merge --delete-branch

# 로컬 정리
git checkout main
git pull origin main
git branch -d feature/PROJ-123-기능설명
```

---

## PR 관련 gh CLI 요약

| 작업                 | 명령어                                    |
| -------------------- | ----------------------------------------- |
| PR 생성              | `gh pr create --draft --base main`        |
| PR 목록              | `gh pr list`                              |
| PR 상세              | `gh pr view 123`                          |
| PR diff              | `gh pr diff 123`                          |
| PR 수정              | `gh pr edit 123 --title "..." --body "..."` |
| Ready for review     | `gh pr ready 123`                         |
| PR 체크 상태         | `gh pr checks 123`                        |
| PR 리뷰              | `gh pr review 123 --approve`              |
| PR 병합              | `gh pr merge 123 --squash --delete-branch` |
| PR 브라우저 열기     | `gh pr view 123 --web`                    |

상세 옵션은 `gh-cli` 스킬의 [references/collaboration.md](../../gh-cli/references/collaboration.md) Pull Requests 섹션을 참조한다.
