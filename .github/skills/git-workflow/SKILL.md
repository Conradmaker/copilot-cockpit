---
name: git-workflow
description: "Unified Git workflow guide based on GitHub Flow. Covers branch strategy, commit conventions, and PR creation with gh CLI integration. Always consult this skill for any git-related workflow task. Triggers on: commit message, commit convention, branch creation, create branch, pull request, PR, git workflow, gh pr, gh issue, 커밋 메시지, 커밋 컨벤션, 브랜치 만들어줘, 새 브랜치, PR 만들어줘, PR 생성, 풀 리퀘스트, 깃 워크플로우, 브랜치 전략, 커밋 규칙."
---

# Git 워크플로우 가이드

## 목표

GitHub Flow 브랜치 전략과 Conventional Commits를 결합하여, 브랜치 생성 → 커밋 → PR 생성까지 일관된 Git 워크플로우를 제공한다. 이 문서는 빠른 판단을 위한 요약 가이드이며, 각 단계의 상세 규칙은 references/ 문서를 직접 읽고 적용한다.

Git CLI 작업은 `gh` (GitHub CLI)를 적극 활용한다. 상세 명령어 레퍼런스는 `gh-cli` 스킬을 참조한다.

---

## 브랜치 전략 요약

| 브랜치       | 용도                    | 분기 | 병합 |
| ------------ | ----------------------- | ---- | ---- |
| `main`       | 배포 가능한 기준 브랜치 | -    | PR   |
| `feature/*`  | 새 기능 개발            | main | main |
| `fix/*`      | 버그 수정               | main | main |
| `docs/*`     | 문서 작업               | main | main |
| `refactor/*` | 리팩토링                | main | main |

#### 빠른 판단 기준

- 변경사항이 새 기능을 추가하는가? → `feature/*`
- 버그나 오류를 수정하는가? → `fix/*`
- 문서/주석만 변경하는가? → `docs/*`
- 위 세 가지에 해당하지 않으면 → `refactor/*`

브랜치 네이밍 규칙, 변경사항 분석 기준, 결정 트리, 예외 처리는 [references/branch-strategy.md](references/branch-strategy.md)를 직접 읽고 적용한다.

---

## 커밋 컨벤션 요약

```
<type>(<scope?>): <subject> (<ticket?>)
```

| 타입       | 용도        | 타입      | 용도          |
| ---------- | ----------- | --------- | ------------- |
| `feat`     | 새로운 기능 | `test`    | 테스트        |
| `fix`      | 버그 수정   | `chore`   | 빌드/도구     |
| `docs`     | 문서/주석   | `build`   | 빌드 시스템   |
| `style`    | 코드 포맷팅 | `ci`      | CI 설정       |
| `refactor` | 리팩토링    | `release` | 버전 릴리즈   |
| `perf`     | 성능 개선   | `revert`  | 커밋 되돌리기 |

#### 핵심 규칙

1. **한국어로 작성** (팀 합의 시 영어 가능)
2. **50자 이내**, 마침표 금지, **명사로 끝내기**
3. **한 커밋 = 한 목적** — 여러 기능을 한 커밋에 섞지 않음

작성 규칙, 상세 예시, 안티패턴은 [references/commit-convention.md](references/commit-convention.md)를 직접 읽고 적용한다.

---

## PR 워크플로우 요약

```bash
# 1. 기존 PR 확인
gh pr list --head $(git branch --show-current)

# 2. Draft PR 생성
gh pr create --draft --base main --title "feat(auth): 소셜 로그인 기능 추가"

# 3. Ready for review
gh pr ready

# 4. 리뷰어/담당자 할당
gh pr edit --add-reviewer user1 --add-assignee @me

# 5. 병합
gh pr merge --squash --delete-branch
```

#### 핵심 규칙

- **PR 제목 = 대표 커밋 제목** — changelog 품질 유지
- 생성 전에 기존 PR 중복 여부를 확인한다
- 하나의 PR은 하나의 작업 단위를 포함한다

PR 생성 절차, 템플릿, 병합 후 정리는 [references/pr-workflow.md](references/pr-workflow.md)를 직접 읽고 적용한다. PR 템플릿은 [references/pull_request_template.md](references/pull_request_template.md)에 있다.

---

## 전체 워크플로우

```
1. main에서 브랜치 분기  →  git checkout -b feature/PROJ-123-기능설명 main
2. 작업 & 커밋           →  feat(auth): 소셜 로그인 기능 추가
3. 푸시                  →  git push origin feature/PROJ-123-기능설명
4. PR 생성               →  gh pr create --draft --base main
5. 리뷰 & CI 통과        →  gh pr checks / gh pr ready
6. main에 병합           →  gh pr merge --squash --delete-branch
```

---

## references/ 가이드

아래 문서는 "더 자세한 참고자료"가 아니라, 실제 적용 전 반드시 확인해야 하는 구현 가이드다. 본문에서 방향을 잡고, 변경을 시작하기 전에 해당 문서를 직접 읽는다.

| 파일 | 내용 |
| --- | --- |
| `references/branch-strategy.md` | GitHub Flow 브랜치 전략, 브랜치 자동 생성 워크플로우, 결정 트리, 예외 처리 |
| `references/commit-convention.md` | 커밋 메시지 형식, 타입별 규칙, 작성 예시, 안티패턴 |
| `references/pr-workflow.md` | gh CLI 기반 PR 생성 절차, PR 규칙, 병합 후 정리, gh CLI 명령어 요약 |
| `references/pull_request_template.md` | PR 본문 템플릿 (프로젝트에 `.github/pull_request_template.md`가 있으면 프로젝트 우선) |

---

## 범위

- GitHub CLI 명령어 상세 레퍼런스 → `gh-cli`
- 코드 리뷰 체크리스트 → `fe-code-review`
