---
name: dev-security
description: "Development security review patterns for application code that handles authentication, user input, secrets, file I/O, network I/O, persistence, or privileged actions. Use this skill when reviewing or implementing app-layer security controls, checking exploitability, or assessing secure coding risks in frontend/backend code. Always consult this skill for developer-facing security review tasks, even if the user only asks for a code review, auth fix, API check, or validation logic. For cloud or infrastructure security use a dedicated infrastructure skill when available. Triggers on: security review, secure coding, auth, authorization, input validation, secrets, XSS, SQL injection, CSRF, path traversal, exploitability, 보안 리뷰, 인증, 인가, 입력 검증, 시크릿, 취약점, 보안."
disable-model-invocation: false
user-invocable: false
---

# 개발 보안 리뷰 (dev-security)

## 목표

애플리케이션 코드 수준의 보안 리스크를 빠르게 식별하고, exploitability와 impact를 evidence와 함께 설명할 수 있게 만든다.

이 문서는 빠른 판단을 위한 요약 가이드다. changed surface와 data flow를 먼저 읽고, 훈련 데이터 기반 추측보다 실제 코드와 관련 reference를 먼저 확인한 뒤 판단한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 검토 순서

### 1. 공격 표면을 먼저 맵핑한다

무슨 입력이 어디로 들어가고, 어떤 권한으로 어떤 상태를 바꾸는지 먼저 정리한다.

#### 빠른 판단 기준

- user input, file input, webhook, external API response가 어디로 흐르는지 설명할 수 없으면 먼저 flow를 정리한다.
- privileged action, persistence write, secret access가 있으면 security review 우선순위를 올린다.

### 2. 인증과 권한 경계를 본다

인증이 있느냐보다, 올바른 주체가 올바른 자원만 다루는지가 중요하다.

#### 빠른 판단 기준

- authN만 있고 authZ나 ownership check가 없으면 위험 신호로 본다.
- tenant boundary, role check, session/token validation이 changed surface 근처에서 빠졌는지 본다.

### 3. 신뢰되지 않은 입력이 dangerous sink로 흐르는지 본다

input validation은 형식 확인만이 아니라 sink까지의 경로를 안전하게 만드는 작업이다.

#### 빠른 판단 기준

- string concatenation query, raw HTML injection, shell/path 조작, unescaped template 사용은 즉시 확인한다.
- validation이 있어도 whitelist인지, sink에 맞는 수준인지까지 본다.

### 4. secret, session, error exposure를 본다

실제 공격은 종종 secret leak, verbose error, insecure token storage에서 시작된다.

#### 빠른 판단 기준

- secret이 코드, 로그, 에러 응답, 클라이언트 번들에 노출되지 않는지 본다.
- token, cookie, session storage 방식이 surface와 위협 모델에 맞는지 본다.
- internal detail이 사용자-facing error에 그대로 드러나지 않는지 본다.

### 5. 파일, 네트워크, 상태 변경 경계를 본다

file I/O, outbound request, persistence write, background job은 abuse surface가 커서 별도 확인이 필요하다.

#### 빠른 판단 기준

- upload/download, webhook, SSRF, path traversal, replay, rate limit 관점을 빠뜨리지 않는다.
- state-changing action이면 abuse cost와 rollback path를 함께 본다.
- concurrency, TOCTOU, duplicate write처럼 integrity risk가 있는지 본다.

### 6. exploitability와 검증 방법을 남긴다

보안 리뷰는 추상적 우려가 아니라 실제 exploit path, impact, fix 방향을 남겨야 한다.

#### 빠른 판단 기준

- finding마다 exploitability, impact, recommended fix를 함께 적는다.
- evidence가 부족하면 severity를 과장하지 말고 evidence gap을 적는다.
- fix 제안은 surface에 맞는 validation, auth, escaping, secret handling 방향으로 구체화한다.

---

## 리뷰 출력 힌트

- 무엇이 취약한지보다 먼저 어떤 경로가 위험한지 적는다.
- severity는 exploitability와 impact를 함께 본다.
- 보안 theater보다 실제 abuse path를 우선한다.

---

## 범위

- cloud, IAM, IaC, CI/CD, infra hardening은 이 스킬의 기본 범위 밖이다.
- clean code, maintainability, boundary condition 전반은 `code-quality` reviewer가 우선 맡는다.
- UI/UX trust signal이나 visual issue는 `design-ex` reviewer가 맡는다.
