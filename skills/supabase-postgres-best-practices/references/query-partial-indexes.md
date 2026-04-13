---
title: "使用部分索引进行过滤查询"
impact: "高的"
impactDescription: 5-20x smaller indexes, faster writes and queries
tags: "索引、部分索引、查询优化、存储"
---

## 使用部分索引进行过滤查询

部分索引仅包含与 WHERE 条件匹配的行，当查询一致过滤相同条件时，它们会更小且更快。

**不正确（完整索引包括不相关的行）：**

```sql
-- Index includes all rows, even soft-deleted ones
create index users_email_idx on users (email);

-- Query always filters active users
select * from users where email = 'user@example.com' and deleted_at is null;
```

**正确（部分索引与查询过滤器匹配）：**

```sql
-- Index only includes active users
create index users_active_email_idx on users (email)
where deleted_at is null;

-- Query uses the smaller, faster index
select * from users where email = 'user@example.com' and deleted_at is null;
```

部分索引的常见用例：

```sql
-- Only pending orders (status rarely changes once completed)
create index orders_pending_idx on orders (created_at)
where status = 'pending';

-- Only non-null values
create index products_sku_idx on products (sku)
where sku is not null;
```

参考：[部分索引](https://www.postgresql.org/docs/current/indexes-partial.html)
