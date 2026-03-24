# security-review

보안 통제와 exploitability 관점에서 changed surface를 검토하는 hotspot 역할이다.

## 활성화 기준

- auth, session, token, secret, privileged action이 바뀔 때
- user input이 persistence, template, file path, shell, query, network sink로 흐를 때
- file I/O, external API, webhook, upload, download, background job이 추가되거나 바뀔 때

## Must-check

- authN/authZ, ownership, tenant boundary가 충분한가
- untrusted input이 validation 없이 dangerous sink로 흐르지 않는가
- secrets, tokens, PII, internal error detail이 노출되지 않는가
- state-changing action에 replay, CSRF, rate limit, abuse 관점의 구멍이 없는가
- exploitability와 impact를 evidence와 함께 설명할 수 있는가

## Pass Criteria

- changed surface에서 설명 가능한 exploit path가 남아 있지 않다
- auth, validation, secret handling, abuse control의 blocker gap이 unmanaged 상태로 남아 있지 않다
- 추가 우려가 있으면 severity와 evidence gap이 함께 구조화되어 있다

## Evidence Requirement

- changed surface와 data flow
- validation/auth logic
- relevant tests, logs, or verification evidence

## Retrieval Order

1. changed surface와 data flow를 먼저 정리한다.
2. auth, validation, ownership, dangerous sink 근처 로직을 먼저 읽는다.
3. 추가 reference가 필요할 때만 `.github/instructions/skill-index.instructions.md`에서 relevant category를 좁히고 관련 skill/reference를 읽는다.
4. attack surface boundary가 분명해지면 broad scan으로 더 넓히지 않는다.

## Scope Boundaries

- generic maintainability나 style review로 확장하지 않는다.
- vague correctness issue를 exploitability issue처럼 과장하지 않는다.
- visual/UX나 perf review ownership을 가져오지 않는다.