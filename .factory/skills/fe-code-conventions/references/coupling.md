# 결합도 (Coupling)

> 코드를 수정했을 때의 영향 범위를 말해요. 수정 시 영향 범위가 적어서, 변경에 따른 범위를 예측할 수 있는 코드가 수정하기 쉬운 코드예요.

결합도가 낮은 코드는 하나의 변경이 다른 코드에 미치는 영향이 최소화되어 있어요.

## 핵심 전략

1. **책임을 하나씩 관리하기** — 하나의 Hook/함수에 하나의 책임
2. **중복 코드 허용하기** — 불필요한 공통화보다 독립성 확보
3. **Props Drilling 제거하기** — 조합 패턴 또는 Context API 활용

---

## 예제 1: 책임을 하나씩 관리하기 (단일 책임 Hook)

쿼리 파라미터, 상태, API 호출과 같은 로직의 종류에 따라서 함수/Hook을 나누지 마세요. 광범위한 책임을 가진 Hook은 유지 관리가 어렵고, 수정 시 영향 범위가 급격히 확장될 수 있어요.

### ❌ Before

```typescript
export function usePageState() {
  const [query, setQuery] = useQueryParams({
    cardId: NumberParam,
    statementId: NumberParam,
    dateFrom: DateParam,
    dateTo: DateParam,
    statusList: ArrayParam
  });

  return useMemo(
    () => ({
      values: {
        cardId: query.cardId ?? undefined,
        statementId: query.statementId ?? undefined,
        dateFrom: query.dateFrom == null ? defaultDateFrom : moment(query.dateFrom),
        dateTo: query.dateTo == null ? defaultDateTo : moment(query.dateTo),
        statusList: query.statusList as StatementStatusType[] | undefined
      },
      controls: {
        setCardId: (cardId: number) => setQuery({ cardId }, "replaceIn"),
        setStatementId: (statementId: number) => setQuery({ statementId }, "replaceIn"),
        setDateFrom: (date?: Moment) => setQuery({ dateFrom: date?.toDate() }, "replaceIn"),
        setDateTo: (date?: Moment) => setQuery({ dateTo: date?.toDate() }, "replaceIn"),
        setStatusList: (statusList?: StatementStatusType[]) => setQuery({ statusList }, "replaceIn")
      }
    }),
    [query, setQuery]
  );
}
```

**문제점:**
- "이 페이지에 필요한 모든 쿼리 매개변수를 관리하는 것"이라는 광범위한 책임
- 페이지 내 컴포넌트나 다른 Hook들이 이 Hook에 의존하게 되어 수정 시 영향 범위가 급격히 확장
- 시간이 지나며 유지 관리가 점점 어려워짐

### ✅ After

```typescript
export function useCardIdQueryParam() {
  const [cardId, _setCardId] = useQueryParam("cardId", NumberParam);

  const setCardId = useCallback((cardId: number) => {
    _setCardId({ cardId }, "replaceIn");
  }, []);

  return [cardId ?? undefined, setCardId] as const;
}
```

각 쿼리 파라미터별로 별도의 Hook을 작성하여:
- 수정에 따른 영향 범위를 좁힘
- 예상하지 못한 영향이 생기는 것을 방지
- 명확한 이름과 책임을 부여

---

## 예제 2: 중복 코드 허용하기

여러 페이지에 걸친 중복 코드를 하나의 Hook으로 공통화하면 응집도는 높아지지만, 불필요한 결합도가 생겨서 오히려 수정이 어려워질 수 있어요.

### ❌ Before — 성급한 공통화

```typescript
export const useOpenMaintenanceBottomSheet = () => {
  const maintenanceBottomSheet = useMaintenanceBottomSheet();
  const logger = useLogger();

  return async (maintainingInfo: TelecomMaintenanceInfo) => {
    logger.log("점검 바텀시트 열림");
    const result = await maintenanceBottomSheet.open(maintainingInfo);
    if (result) {
      logger.log("점검 바텀시트 알림받기 클릭");
    }
    closeView();
  };
};
```

여러 페이지에서 반복적으로 보이는 로직이기에 공통화했지만, 다양한 변경 가능성이 존재해요:
- 페이지마다 로깅하는 값이 달라진다면?
- 어떤 페이지에서는 바텀시트를 닫더라도 화면을 닫을 필요가 없다면?
- 바텀시트에서 보여지는 텍스트나 이미지를 다르게 해야 한다면?

이 Hook의 구현을 수정할 때마다, 이 Hook을 쓰는 **모든 페이지**가 잘 작동하는지 테스트해야 해요.

### ✅ After — 중복 허용

다소 반복되어 보이는 코드일지 몰라도, 중복 코드를 허용하는 것이 좋은 방향일 수 있어요.

### 공통화 vs 중복 허용 판단 기준

**공통화가 좋은 경우 (응집도 우선):**
- 페이지에서 로깅하는 값이 동일하고
- 동작이 동일하고
- UI가 동일하고
- **앞으로도 그럴 예정**일 때

**중복 허용이 좋은 경우 (결합도 우선):**
- 페이지마다 동작이 달라질 여지가 있을 때
- 각 사용처가 독립적으로 변경될 가능성이 있을 때

---

## 예제 3: Props Drilling 제거하기

Props Drilling은 부모 컴포넌트와 자식 컴포넌트 사이에 결합도가 생겼다는 명확한 표시예요. prop이 변경되면 해당 prop을 참조하는 모든 컴포넌트를 수정해야 해요.

### 결합도 관점에서의 핵심 원칙

- Props Drilling이 발생하면 수정 범위가 필요 이상으로 넓어져요
- `children` prop을 이용한 조합(Composition) 패턴으로 depth를 먼저 줄이세요
- 조합 패턴으로도 해결되지 않을 때 Context API를 사용하세요
- props가 컴포넌트의 역할과 의도를 담고 있다면 Props Drilling이 문제가 아닐 수 있어요

> Context API를 사용하기 전, 먼저 조합 패턴을 고려하세요. 불필요한 중간 추상화를 제거하여 컴포넌트의 역할과 의도를 명확히 이해할 수 있도록 도와줘요.

자세한 Composition 패턴 코드 예제는 `fe-react-patterns`의 references/composition.md를 참고하세요.

---

## 핵심 규칙 체크리스트

- [ ] 하나의 Hook/함수가 하나의 명확한 책임만 가지고 있는가?
- [ ] 광범위한 책임을 가진 "페이지 레벨" Hook이 없는가?
- [ ] 공통화할 때, 앞으로도 동일하게 동작할 것인지 충분히 검토했는가?
- [ ] 불필요한 Props Drilling이 없는가?
- [ ] 조합(Composition) 패턴을 먼저 시도한 후 Context API를 사용했는가?
- [ ] 코드 수정 시 영향 범위를 예측할 수 있는가?
