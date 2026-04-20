# Artifacts Template

이 문서는 `/memories/session/artifacts.md`를 위한 짧은 인덱스 템플릿이다.
Mate는 planning phase에서 이 문서를 반드시 만들고, 이후 phase owner는 실제로 새 session 문서를 만든 경우에만 기존 인덱스를 갱신한다.

## Rules

- `artifacts.md`는 session-wide generated document index다. evidence ledger가 아니다.
- 실제로 존재하는 session 문서만 적는다.
- `prd.md`가 있으면 첫 번째 entry로 둔다.
- 각 entry에는 path, owner, status, summary, open when만 남긴다.
- 문서 본문, 외부 링크 dump, rationale appendix는 복제하지 않는다.
- stale 또는 conflict는 숨기지 말고 status나 note에 적는다.

## Template

```markdown
## Artifacts: {Session or feature title}

- Primary source of truth: {/memories/session/prd.md or N/A}
- Current phase: {Planning / Downstream Definition / Execution / Review}
- Last updated by: {Mate / Designer / Architector / Commander / Reviewer}

### Documents

- `/memories/session/prd.md` — owner: Mate — status: {draft / approved / stale} — summary: {what this PRD locks} — open when: first
- `{existing path}` — owner: {owner} — status: {draft / approved / current / stale} — summary: {what it is for} — open when: {when to read it}
- `{existing path}` — owner: {owner} — status: {draft / approved / current / stale} — summary: {what it is for} — open when: {when to read it}

### Notes

- {optional stale artifact, conflict, or intentional absence}
```

## Checklist

- `prd.md`가 있으면 첫 번째 entry인가
- 존재하는 문서만 적었는가
- 각 entry에 path, owner, status, summary, open when이 있는가
- 본문 복제나 source dump가 없는가