# Query Patterns Reference Guide

Comprehensive reference for querying with Drizzle ORM.

These examples assume a standard Node.js PostgreSQL setup with `drizzle-orm/node-postgres`. Where a capability depends on the selected driver, the note calls that out explicitly.

## Table of Contents

- [Core Query Patterns](#core-query-patterns)
  - [Basic CRUD Operations](#basic-crud-operations)
  - [Advanced Filtering](#advanced-filtering)
  - [Joins and Relations](#joins-and-relations)
  - [Aggregations](#aggregations)
  - [Subqueries](#subqueries)
  - [Transactions](#transactions)
  - [Batch Operations](#batch-operations)
  - [Raw SQL](#raw-sql)
  - [Performance Optimization](#performance-optimization)
  - [Type Safety](#type-safety)
  - [Common Patterns](#common-patterns)
- [Advanced Query Patterns](#advanced-query-patterns)
  - [Common Table Expressions (CTEs)](#common-table-expressions-ctes)
  - [Window Functions](#window-functions)
  - [Prepared Statements](#prepared-statements)
  - [LATERAL Joins](#lateral-joins)
  - [UNION Queries](#union-queries)
  - [Distinct Queries](#distinct-queries)
  - [Locking Strategies](#locking-strategies)
  - [Query Builder Patterns](#query-builder-patterns)
  - [Related Resources](#related-resources)

---

## Core Query Patterns

## Basic CRUD Operations

### Create (Insert)

**Single record:**

```typescript
import { db } from './db';
import { users } from './db/schema';

const newUser = await db.insert(users)
  .values({
    email: 'user@example.com',
    name: 'John Doe',
  })
  .returning();

console.log(newUser[0]); // { id: 1, email: '...', name: '...' }
```

**Multiple records:**

```typescript
const newUsers = await db.insert(users)
  .values([
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
    { email: 'user3@example.com', name: 'User 3' },
  ])
  .returning();
```

**With onConflictDoNothing:**

```typescript
await db.insert(users)
  .values({ email: 'user@example.com', name: 'John' })
  .onConflictDoNothing();
```

**With onConflictDoUpdate (upsert):**

```typescript
await db.insert(users)
  .values({ email: 'user@example.com', name: 'John' })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'John Updated' },
  });
```

### Read (Select)

**All records:**

```typescript
const allUsers = await db.select().from(users);
```

**Specific columns:**

```typescript
const userEmails = await db.select({
  id: users.id,
  email: users.email,
}).from(users);
```

**With WHERE clause:**

```typescript
import { and, eq, gt, like, lt, or } from 'drizzle-orm';

const user = await db.select()
  .from(users)
  .where(eq(users.email, 'user@example.com'));

const activeUsers = await db.select()
  .from(users)
  .where(eq(users.isActive, true));
```

**Multiple conditions:**

```typescript
const filteredUsers = await db.select()
  .from(users)
  .where(
    and(
      eq(users.isActive, true),
      gt(users.createdAt, new Date('2024-01-01'))
    )
  );
```

**With LIMIT and OFFSET:**

```typescript
const paginatedUsers = await db.select()
  .from(users)
  .limit(10)
  .offset(20); // Page 3
```

**With ORDER BY:**

```typescript
const sortedUsers = await db.select()
  .from(users)
  .orderBy(users.createdAt); // ASC by default

import { desc } from 'drizzle-orm';

const recentUsers = await db.select()
  .from(users)
  .orderBy(desc(users.createdAt));
```

### Update

**Single record:**

```typescript
await db.update(users)
  .set({ name: 'Jane Doe' })
  .where(eq(users.id, 1));
```

**Multiple records:**

```typescript
await db.update(users)
  .set({ isActive: false })
  .where(eq(users.deletedAt, null));
```

**With returning:**

```typescript
const updated = await db.update(users)
  .set({ name: 'Updated Name' })
  .where(eq(users.id, 1))
  .returning();
```

**Partial updates:**

```typescript
const updates: Partial<typeof users.$inferSelect> = {
  name: 'New Name',
};

await db.update(users)
  .set(updates)
  .where(eq(users.id, 1));
```

### Delete

**Single record:**

```typescript
await db.delete(users)
  .where(eq(users.id, 1));
```

**Multiple records:**

```typescript
await db.delete(users)
  .where(eq(users.isActive, false));
```

**With returning:**

```typescript
const deleted = await db.delete(users)
  .where(eq(users.id, 1))
  .returning();
```

**Soft delete (recommended):**

```typescript
await db.update(users)
  .set({ deletedAt: new Date() })
  .where(eq(users.id, 1));
```

## Advanced Filtering

### Comparison Operators

```typescript
import { eq, gt, gte, lt, lte, ne } from 'drizzle-orm';

const adults = await db.select()
  .from(users)
  .where(gte(users.age, 18));

const recentPosts = await db.select()
  .from(posts)
  .where(gt(posts.createdAt, new Date('2024-01-01')));

const excludeAdmin = await db.select()
  .from(users)
  .where(ne(users.role, 'admin'));
```

### Pattern Matching

```typescript
import { ilike, like } from 'drizzle-orm';

const gmailUsers = await db.select()
  .from(users)
  .where(like(users.email, '%@gmail.com'));

const searchByName = await db.select()
  .from(users)
  .where(ilike(users.name, '%john%')); // Case-insensitive
```

### NULL Checks

```typescript
import { isNotNull, isNull } from 'drizzle-orm';

const usersWithPhone = await db.select()
  .from(users)
  .where(isNotNull(users.phoneNumber));

const unverifiedUsers = await db.select()
  .from(users)
  .where(isNull(users.emailVerifiedAt));
```

### IN Operator

```typescript
import { inArray } from 'drizzle-orm';

const specificUsers = await db.select()
  .from(users)
  .where(inArray(users.id, [1, 2, 3, 4, 5]));
```

### BETWEEN

```typescript
import { between } from 'drizzle-orm';

const postsThisMonth = await db.select()
  .from(posts)
  .where(
    between(
      posts.createdAt,
      new Date('2024-01-01'),
      new Date('2024-01-31')
    )
  );
```

### Complex Conditions

```typescript
import { and, eq, gte, not, or } from 'drizzle-orm';

const complexQuery = await db.select()
  .from(users)
  .where(
    or(
      and(
        eq(users.isActive, true),
        gte(users.age, 18)
      ),
      eq(users.role, 'admin')
    )
  );
```

## Joins and Relations

### Manual Joins

**Inner join:**

```typescript
const postsWithAuthors = await db.select({
  postId: posts.id,
  postTitle: posts.title,
  authorName: users.name,
  authorEmail: users.email,
})
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id));
```

**Left join:**

```typescript
const allPostsWithOptionalAuthors = await db.select()
  .from(posts)
  .leftJoin(users, eq(posts.authorId, users.id));
```

### Relational Queries (Recommended)

**Define relations first:**

```typescript
import { relations } from 'drizzle-orm';

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

**Query with relations:**

```typescript
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
});

console.log(usersWithPosts[0].posts); // Array of posts
```

**Nested relations:**

```typescript
const postsWithAuthorsAndComments = await db.query.posts.findMany({
  with: {
    author: true,
    comments: {
      with: {
        author: true,
      },
    },
  },
});
```

**Filtered relations:**

```typescript
const usersWithRecentPosts = await db.query.users.findMany({
  with: {
    posts: {
      where: gt(posts.createdAt, new Date('2024-01-01')),
      orderBy: desc(posts.createdAt),
      limit: 5,
    },
  },
});
```

**Partial selection:**

```typescript
const usersWithPostTitles = await db.query.users.findMany({
  columns: {
    id: true,
    name: true,
  },
  with: {
    posts: {
      columns: {
        id: true,
        title: true,
      },
    },
  },
});
```

## Aggregations

### Count

```typescript
import { avg, count, max, min, sql, sum } from 'drizzle-orm';

const userCount = await db.select({
  count: count(),
}).from(users);

console.log(userCount[0].count); // Total users
```

### Count with grouping

```typescript
const postsByAuthor = await db.select({
  authorId: posts.authorId,
  postCount: count(),
})
  .from(posts)
  .groupBy(posts.authorId);
```

### Sum, Avg, Min, Max

```typescript
const stats = await db.select({
  totalViews: sum(posts.views),
  avgViews: avg(posts.views),
  minViews: min(posts.views),
  maxViews: max(posts.views),
}).from(posts);
```

### Multiple aggregates

```typescript
const orderStats = await db
  .select({
    count: count(),
    total: sum(orders.amount),
    avg: avg(orders.amount),
    min: min(orders.amount),
    max: max(orders.amount),
  })
  .from(orders);
```

### HAVING

```typescript
const activeAuthors = await db.select({
  authorId: posts.authorId,
  postCount: count(),
})
  .from(posts)
  .groupBy(posts.authorId)
  .having(gt(count(), 5)); // Authors with > 5 posts
```

### GROUP BY with HAVING

```typescript
const prolificAuthors = await db
  .select({
    author: authors.name,
    postCount: count(posts.id),
  })
  .from(authors)
  .leftJoin(posts, eq(authors.id, posts.authorId))
  .groupBy(authors.id)
  .having(sql`COUNT(${posts.id}) > 5`);
```

## Subqueries

### In WHERE clause

```typescript
const activeUserIds = db.select({ id: users.id })
  .from(users)
  .where(eq(users.isActive, true));

const postsFromActiveUsers = await db.select()
  .from(posts)
  .where(inArray(posts.authorId, activeUserIds));
```

### As derived table

```typescript
const recentPosts = db.select()
  .from(posts)
  .where(gt(posts.createdAt, new Date('2024-01-01')))
  .as('recentPosts');

const authorsOfRecentPosts = await db.select()
  .from(users)
  .innerJoin(recentPosts, eq(users.id, recentPosts.authorId));
```

### SELECT subqueries

```typescript
import { avg, eq, gt, sql } from 'drizzle-orm';

// Scalar subquery
const avgPrice = db.select({ value: avg(products.price) }).from(products);

const expensiveProducts = await db
  .select()
  .from(products)
  .where(gt(products.price, avgPrice));

// Correlated subquery
const authorsWithPostCount = await db
  .select({
    author: authors,
    postCount: sql<number>`(
      SELECT COUNT(*)
      FROM ${posts}
      WHERE ${posts.authorId} = ${authors.id}
    )`,
  })
  .from(authors);
```

### EXISTS subqueries

```typescript
const authorsWithPosts = await db
  .select()
  .from(authors)
  .where(
    sql`EXISTS (
      SELECT 1
      FROM ${posts}
      WHERE ${posts.authorId} = ${authors.id}
    )`
  );

const authorsWithoutPosts = await db
  .select()
  .from(authors)
  .where(
    sql`NOT EXISTS (
      SELECT 1
      FROM ${posts}
      WHERE ${posts.authorId} = ${authors.id}
    )`
  );
```

### IN subqueries

```typescript
const usersWhoCommented = await db
  .select()
  .from(users)
  .where(
    sql`${users.id} IN (
      SELECT DISTINCT ${comments.userId}
      FROM ${comments}
    )`
  );
```

## Transactions

Transactions depend on driver capabilities. Use a driver or adapter that supports persistent connections for transactional work. If the selected driver does not support transactions, use non-atomic batching only when rollback is not required.

```typescript
await db.transaction(async (tx) => {
  const user = await tx.insert(users)
    .values({ email: 'user@example.com', name: 'John' })
    .returning();

  await tx.insert(posts)
    .values({
      authorId: user[0].id,
      title: 'First post',
      content: 'Hello world',
    });
});
```

**With error handling:**

```typescript
try {
  await db.transaction(async (tx) => {
    await tx.insert(users).values({ email: 'user@example.com' });
    await tx.insert(posts).values({ title: 'Post' });

    throw new Error('Rollback!'); // Transaction rolls back
  });
} catch (err) {
  console.error('Transaction failed:', err);
}
```

**Nested transactions:**

```typescript
await db.transaction(async (tx) => {
  await tx.insert(users).values({ email: 'user1@example.com' });

  await tx.transaction(async (tx2) => {
    await tx2.insert(posts).values({ title: 'Post 1' });
  });
});
```

## Batch Operations

### Batch insert

```typescript
const newUsers = await db.insert(users).values([
  { email: 'user1@example.com', name: 'User 1' },
  { email: 'user2@example.com', name: 'User 2' },
  { email: 'user3@example.com', name: 'User 3' },
]).returning();
```

### Batch insert with conflict handling

```typescript
await db.insert(users).values(bulkUsers).onConflictDoNothing();

await db.insert(users)
  .values(bulkUsers)
  .onConflictDoUpdate({
    target: users.email,
    set: { name: sql`EXCLUDED.name` },
  });
```

### Batch update

```typescript
await db.transaction(async (tx) => {
  for (const update of updates) {
    await tx.update(users)
      .set({ name: update.name })
      .where(eq(users.id, update.id));
  }
});
```

```typescript
await db.execute(sql`
  UPDATE ${users}
  SET ${users.role} = CASE ${users.id}
    ${sql.join(
      updates.map((u) => sql`WHEN ${u.id} THEN ${u.role}`),
      sql.raw(' ')
    )}
  END
  WHERE ${users.id} IN (${sql.join(updates.map((u) => u.id), sql.raw(', '))})
`);
```

### Batch delete

```typescript
await db.delete(users).where(inArray(users.id, [1, 2, 3, 4, 5]));

await db.delete(posts).where(
  and(
    lt(posts.createdAt, new Date('2023-01-01')),
    eq(posts.isDraft, true)
  )
);
```

### Driver batch API (when supported)

```typescript
await db.batch([
  db.insert(users).values({ email: 'user1@example.com' }),
  db.insert(users).values({ email: 'user2@example.com' }),
  db.insert(posts).values({ title: 'Post 1' }),
]);
```

**Note:** This reduces round trips when the selected driver supports batch execution, but it is not atomic. Use transactions when you need rollback capability.

## Raw SQL

### Safe raw queries

```typescript
import { SQL, and, like, sql } from 'drizzle-orm';

const userId = 123;
const user = await db.execute(
  sql`SELECT * FROM ${users} WHERE ${users.id} = ${userId}`
);

const result = await db.execute<{ count: number }>(
  sql`SELECT COUNT(*) as count FROM ${users}`
);
```

### Execute raw query

```typescript
const gmailUsers = await db.execute(sql`
  SELECT * FROM users
  WHERE email LIKE ${'%@gmail.com'}
`);
```

### SQL in WHERE clause

```typescript
const gmailMatches = await db.select()
  .from(users)
  .where(sql`${users.email} LIKE '%@gmail.com'`);
```

### SQL expressions

```typescript
const postSummaries = await db.select({
  id: posts.id,
  title: posts.title,
  excerpt: sql<string>`LEFT(${posts.content}, 100)`,
}).from(posts);
```

### SQL template composition

```typescript
function whereActive() {
  return sql`${users.isActive} = true`;
}

function whereRole(role: string) {
  return sql`${users.role} = ${role}`;
}

const admins = await db
  .select()
  .from(users)
  .where(sql`${whereActive()} AND ${whereRole('admin')}`);
```

### Dynamic WHERE clauses

```typescript
interface Filters {
  name?: string;
  role?: string;
  isActive?: boolean;
}

function buildFilters(filters: Filters): SQL | undefined {
  const conditions: SQL[] = [];

  if (filters.name) {
    conditions.push(like(users.name, `%${filters.name}%`));
  }

  if (filters.role) {
    conditions.push(eq(users.role, filters.role));
  }

  if (filters.isActive !== undefined) {
    conditions.push(eq(users.isActive, filters.isActive));
  }

  return conditions.length > 0 ? and(...conditions) : undefined;
}

const filters: Filters = { name: 'John', isActive: true };
const filteredUsers = await db
  .select()
  .from(users)
  .where(buildFilters(filters));
```

### Custom functions

```typescript
const searchResults = await db.select()
  .from(posts)
  .where(
    sql`to_tsvector('english', ${posts.content}) @@ to_tsquery('english', ${'search query'})`
  );
```

## Performance Optimization

### Select only needed columns

❌ **Bad:**

```typescript
const users = await db.select().from(users); // All columns
```

✅ **Good:**

```typescript
const userSummaries = await db.select({
  id: users.id,
  email: users.email,
}).from(users);
```

### Use indexes

```typescript
const user = await db.select()
  .from(users)
  .where(eq(users.email, 'user@example.com')); // Fast if users.email is indexed
```

### Avoid N+1 queries

❌ **Bad:**

```typescript
const allPosts = await db.select().from(posts);

for (const post of allPosts) {
  const author = await db.select()
    .from(users)
    .where(eq(users.id, post.authorId)); // N queries!
}
```

✅ **Good:**

```typescript
const postsWithAuthors = await db.query.posts.findMany({
  with: {
    author: true,
  },
});
```

✅ **Good: Dataloader pattern**

```typescript
import DataLoader from 'dataloader';

const postLoader = new DataLoader(async (authorIds: number[]) => {
  const authorPosts = await db.select()
    .from(posts)
    .where(inArray(posts.authorId, authorIds));

  const grouped = authorIds.map((id) =>
    authorPosts.filter((post) => post.authorId === id)
  );

  return grouped;
});
```

### Use pagination

```typescript
async function getPaginatedUsers(page: number, pageSize: number = 10) {
  return db.select()
    .from(users)
    .limit(pageSize)
    .offset((page - 1) * pageSize);
}
```

### Batch inserts

❌ **Bad:**

```typescript
for (const user of users) {
  await db.insert(users).values(user); // N queries
}
```

✅ **Good:**

```typescript
await db.insert(users).values(users); // Single query
```

### Query timeouts

```typescript
await db.execute(sql`SET statement_timeout = '5s'`);

const withTimeout = async <T>(promise: Promise<T>, ms: number): Promise<T> => {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error('Query timeout')), ms)
  );

  return Promise.race([promise, timeout]);
};

const timelyUsers = await withTimeout(
  db.select().from(users),
  5000
);
```

## Type Safety

### Infer types from schema

```typescript
type User = typeof users.$inferSelect;
type NewUser = typeof users.$inferInsert;

const user: User = {
  id: 1,
  email: 'user@example.com',
  name: 'John',
  createdAt: new Date(),
};

const newUser: NewUser = {
  email: 'user@example.com',
  name: 'John',
};
```

### Type-safe WHERE conditions

```typescript
function getUsersByStatus(status: User['status']) {
  return db.select()
    .from(users)
    .where(eq(users.status, status));
}
```

### Type-safe updates

```typescript
function updateUser(id: number, data: Partial<NewUser>) {
  return db.update(users)
    .set(data)
    .where(eq(users.id, id))
    .returning();
}
```

## Common Patterns

### Soft deletes

**Schema:**

```typescript
export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  deletedAt: timestamp('deleted_at'),
});
```

**Queries:**

```typescript
const activePosts = await db.select()
  .from(posts)
  .where(isNull(posts.deletedAt));

const deletedPosts = await db.select()
  .from(posts)
  .where(isNotNull(posts.deletedAt));
```

### Timestamps

**Auto-update:**

```typescript
async function updatePost(id: number, data: Partial<NewPost>) {
  return db.update(posts)
    .set({
      ...data,
      updatedAt: new Date(),
    })
    .where(eq(posts.id, id))
    .returning();
}
```

### Search

**Simple search:**

```typescript
const searchUsers = await db.select()
  .from(users)
  .where(
    or(
      ilike(users.name, `%${query}%`),
      ilike(users.email, `%${query}%`)
    )
  );
```

**Full-text search:**

```typescript
const searchPosts = await db.select()
  .from(posts)
  .where(
    sql`to_tsvector('english', ${posts.title} || ' ' || ${posts.content}) @@ plainto_tsquery('english', ${query})`
  );
```

### Unique constraints

**Handle duplicates:**

```typescript
try {
  await db.insert(users).values({ email: 'user@example.com' });
} catch (err) {
  if (err.code === '23505') { // Unique violation
    console.error('Email already exists');
  }
}
```

**Or use upsert:**

```typescript
await db.insert(users)
  .values({ email: 'user@example.com', name: 'John' })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'John Updated' },
  });
```

---

## Advanced Query Patterns

## Common Table Expressions (CTEs)

### Basic CTE

```typescript
import { sql } from 'drizzle-orm';

const topAuthors = db.$with('top_authors').as(
  db.select({
    id: authors.id,
    name: authors.name,
    postCount: sql<number>`COUNT(${posts.id})`.as('post_count'),
  })
    .from(authors)
    .leftJoin(posts, eq(authors.id, posts.authorId))
    .groupBy(authors.id)
    .having(sql`COUNT(${posts.id}) > 10`)
);

const result = await db
  .with(topAuthors)
  .select()
  .from(topAuthors);
```

### Recursive CTE

```typescript
export const employees = pgTable('employees', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  managerId: integer('manager_id').references((): AnyPgColumn => employees.id),
});

const employeeHierarchy = db.$with('employee_hierarchy').as(
  db.select({
    id: employees.id,
    name: employees.name,
    managerId: employees.managerId,
    level: sql<number>`1`.as('level'),
  })
    .from(employees)
    .where(isNull(employees.managerId))
    .unionAll(
      db.select({
        id: employees.id,
        name: employees.name,
        managerId: employees.managerId,
        level: sql<number>`employee_hierarchy.level + 1`,
      })
        .from(employees)
        .innerJoin(
          sql`employee_hierarchy`,
          sql`${employees.managerId} = employee_hierarchy.id`
        )
    )
);

const hierarchy = await db
  .with(employeeHierarchy)
  .select()
  .from(employeeHierarchy);
```

### Multiple CTEs

```typescript
const activeUsers = db.$with('active_users').as(
  db.select().from(users).where(eq(users.isActive, true))
);

const recentPosts = db.$with('recent_posts').as(
  db.select().from(posts).where(gt(posts.createdAt, sql`NOW() - INTERVAL '30 days'`))
);

const combinedResult = await db
  .with(activeUsers, recentPosts)
  .select({
    user: activeUsers,
    post: recentPosts,
  })
  .from(activeUsers)
  .leftJoin(recentPosts, eq(activeUsers.id, recentPosts.authorId));
```

## Window Functions

```typescript
const rankedProducts = await db
  .select({
    product: products,
    priceRank: sql<number>`RANK() OVER (PARTITION BY ${products.categoryId} ORDER BY ${products.price} DESC)`,
  })
  .from(products);

const ordersWithRunningTotal = await db
  .select({
    order: orders,
    runningTotal: sql<number>`SUM(${orders.amount}) OVER (ORDER BY ${orders.createdAt})`,
  })
  .from(orders);

const numberedUsers = await db
  .select({
    user: users,
    rowNum: sql<number>`ROW_NUMBER() OVER (ORDER BY ${users.createdAt})`,
  })
  .from(users);
```

## Prepared Statements

### Reusable queries

```typescript
const getUserById = db
  .select()
  .from(users)
  .where(eq(users.id, sql.placeholder('id')))
  .prepare('get_user_by_id');

const user1 = await getUserById.execute({ id: 1 });
const user2 = await getUserById.execute({ id: 2 });

const searchUsers = db
  .select()
  .from(users)
  .where(
    and(
      like(users.name, sql.placeholder('name')),
      eq(users.role, sql.placeholder('role'))
    )
  )
  .prepare('search_users');

const admins = await searchUsers.execute({ name: '%John%', role: 'admin' });
```

## LATERAL Joins

```typescript
const authorsWithTopPosts = await db
  .select({
    author: authors,
    post: posts,
  })
  .from(authors)
  .leftJoin(
    sql`LATERAL (
      SELECT * FROM ${posts}
      WHERE ${posts.authorId} = ${authors.id}
      ORDER BY ${posts.views} DESC
      LIMIT 3
    ) AS ${posts}`,
    sql`true`
  );
```

## UNION Queries

```typescript
const allContent = await db
  .select({ id: posts.id, title: posts.title, type: sql<string>`'post'` })
  .from(posts)
  .union(
    db.select({ id: articles.id, title: articles.title, type: sql<string>`'article'` })
      .from(articles)
  );

const allItems = await db
  .select({ id: products.id, name: products.name })
  .from(products)
  .unionAll(
    db.select({ id: services.id, name: services.name }).from(services)
  );
```

## Distinct Queries

```typescript
const uniqueRoles = await db.selectDistinct({ role: users.role }).from(users);

const latestPostPerAuthor = await db
  .selectDistinctOn([posts.authorId], {
    post: posts,
  })
  .from(posts)
  .orderBy(posts.authorId, desc(posts.createdAt));
```

## Locking Strategies

```typescript
await db.transaction(async (tx) => {
  const [user] = await tx
    .select()
    .from(users)
    .where(eq(users.id, userId))
    .for('update');

  await tx.update(users)
    .set({ balance: user.balance - amount })
    .where(eq(users.id, userId));
});

const sharedUser = await db
  .select()
  .from(users)
  .where(eq(users.id, userId))
  .for('share');

const availableTask = await db
  .select()
  .from(tasks)
  .where(eq(tasks.status, 'pending'))
  .limit(1)
  .for('update', { skipLocked: true });
```

## Query Builder Patterns

### Type-safe query builder

```typescript
class UserQueryBuilder {
  private query = db.select().from(users);

  whereRole(role: string) {
    this.query = this.query.where(eq(users.role, role));
    return this;
  }

  whereActive() {
    this.query = this.query.where(eq(users.isActive, true));
    return this;
  }

  orderByCreated() {
    this.query = this.query.orderBy(desc(users.createdAt));
    return this;
  }

  async execute() {
    return await this.query;
  }
}

const admins = await new UserQueryBuilder()
  .whereRole('admin')
  .whereActive()
  .orderByCreated()
  .execute();
```

## Related Resources

- `advanced-schemas.md` - Advanced table, key, and generated-column patterns
- `vs-prisma.md` - Compare Drizzle and Prisma patterns
- `guides/schema-only.md` - Schema design patterns
- `references/adapters.md` - Transaction availability by driver or adapter
- `guides/troubleshooting.md` - Query error solutions
- `templates/schema-example.ts` - Complete schema with relations