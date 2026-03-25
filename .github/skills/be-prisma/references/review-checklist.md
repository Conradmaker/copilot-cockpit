# Review Checklist

## Runtime baseline

- [ ] Prisma version과 target runtime이 명확한가
- [ ] `prisma-client` generator와 explicit `output`이 맞는가
- [ ] `prisma.config.ts`에서 datasource URL을 관리하는가
- [ ] adapter 또는 `accelerateUrl` 경로가 현재 provider와 맞는가
- [ ] env loading 방식이 v7 기준에 맞는가

## Schema quality

- [ ] 모든 model에 명확한 `@id` 전략이 있는가
- [ ] relation에 foreign key scalar field와 `references`가 명시돼 있는가
- [ ] named relation이 필요한 곳에 이름이 붙어 있는가
- [ ] 자주 조회되는 field와 복합 조건에 index가 있는가
- [ ] business invariant가 `@unique` 또는 `@@unique`로 표현돼 있는가
- [ ] legacy DB naming이 필요하면 `@map`/`@@map`이 적절한가

## Query patterns

- [ ] 필요한 field만 `select`로 가져오는가
- [ ] loop 안의 relation query로 N+1이 생기지 않는가
- [ ] list query에 pagination과 stable `orderBy`가 있는가
- [ ] raw SQL은 정말 필요한 부분에만 쓰는가
- [ ] query logging이나 slow query 확인 경로가 있는가

## Transactions and connections

- [ ] Prisma client singleton이 유지되는가
- [ ] adapter pool 설정이 환경과 DB limit에 맞는가
- [ ] transaction 안에서 외부 I/O를 하지 않는가
- [ ] conflict handling 또는 OCC가 필요한 path를 다루는가
- [ ] serverless, edge, Accelerate 같은 runtime nuance를 반영했는가

## Migration safety

- [ ] 개발과 운영 명령이 분리돼 있는가
- [ ] destructive change에 expand-migrate-contract 계획이 있는가
- [ ] drift를 확인하는 절차가 있는가
- [ ] generate와 seed가 명시적 흐름으로 정리돼 있는가
- [ ] rollback 또는 failure handling 경로가 적혀 있는가

## Legacy exceptions

- [ ] MongoDB가 필요한데 v7 mainline 경로로 잘못 안내하지 않았는가
- [ ] `prisma://` 또는 `prisma+postgres://` URL을 direct adapter에 잘못 넣지 않았는가
- [ ] removed middleware와 auto behaviors를 v6처럼 가정하지 않았는가