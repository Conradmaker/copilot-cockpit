# 배포 전략: npm, Registry, Marketplace

디자인 시스템 컴포넌트는 어떻게 배포하느냐에 따라 코드 소유권, 업데이트 전략, 소비자 경험이 완전히 달라진다. 배포 방식은 구현 후반이 아니라 초기에 같이 결정하는 편이 낫다.

---

## 1. npm package

```bash
npm install @acme/ui-components
```

### 장점

- 버전 관리와 중앙 배포가 쉽다
- peer dependency와 type definition 관리가 명확하다
- 내부 팀에서 버전 고정과 업데이트 추적이 쉽다

### 단점

- 소비자가 내부 구현을 직접 수정하기 어렵다
- Tailwind 기반이면 consuming app에서 source scan 설정이 필요할 수 있다
- 코드 소유권은 패키지 작성자 쪽에 더 무게가 간다

### 이런 경우 적합하다

- 조직 내부에서 안정적 버전 배포가 중요할 때
- 중앙 유지보수와 changelog 관리가 중요할 때

---

## 2. Registry

```bash
npx shadcn@latest add https://your-project.vercel.app/button.json
```

### 장점

- source code를 소비자 저장소로 직접 가져간다
- customization과 ownership이 강하다
- copy-and-paste distribution에 잘 맞는다

### 단점

- 버전 업그레이드가 package보다 느슨하다
- metadata와 public endpoint를 직접 관리해야 한다

### 이런 경우 적합하다

- 소비자가 컴포넌트 코드를 직접 수정해야 할 때
- shared block이나 styled wrapper를 빠르게 배포할 때

---

## 3. Marketplace

### 장점

- discovery와 distribution을 동시에 제공한다
- preview, category, audience를 플랫폼이 제공한다
- 외부 공개 배포에 유리하다

### 단점

- 플랫폼 의존성이 생긴다
- 경쟁이 심하고 품질 기준이 올라간다

### 이런 경우 적합하다

- 외부 사용자에게 컴포넌트를 공개하고 싶을 때
- 자체 distribution 인프라보다 유통 채널이 중요할 때

---

## 빠른 선택 기준

- 코드 소유권과 직접 수정이 중요하면 registry
- 버전 관리와 중앙 배포가 중요하면 npm
- 발견 가능성과 외부 유통이 중요하면 marketplace
- 상황이 다르면 npm + registry를 함께 운영하는 이중 전략도 가능하다