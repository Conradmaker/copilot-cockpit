# 디자인 시스템 컴포넌트 문서화

문서 없는 공유 컴포넌트는 유지보수 비용이 빠르게 커진다. 문서는 예쁘게 정리된 README가 아니라, 소비자가 설치하고 이해하고 확장할 수 있게 만드는 공개 API의 일부다.

---

## 필수 섹션

### 1. Overview

- 이 컴포넌트가 무엇인지
- 언제 써야 하는지
- 언제 쓰지 말아야 하는지

### 2. Demo와 Preview

- 실제 렌더 결과
- 코드 예시
- 가능하면 source preview까지 제공

### 3. Installation

- npm install
- registry add
- marketplace install 중 실제 지원하는 방식을 명시

### 4. Features

- customizable
- accessible by default
- composable
- type-safe
- theming support

### 5. Examples

- variants
- states
- advanced usage
- composition

### 6. API Reference

- prop 이름
- 타입
- 기본값
- 필수 여부
- 설명

### 7. Accessibility

- keyboard map
- role/ARIA
- focus management
- screen reader behavior

### 8. Changelog

- semver 기준 버전 변경점
- breaking changes
- migration guide

---

## 빠른 체크리스트

- 설치 명령을 한 줄로 보여주는가?
- demo와 source를 함께 보여주는가?
- prop table에 default와 required 정보가 있는가?
- accessibility 섹션이 별도로 존재하는가?
- breaking change가 생기면 migration guide를 남기는가?