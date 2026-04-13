---
title: "为您的数据选择正确的索引类型"
impact: "高的"
impactDescription: 10-100x improvement with correct index type
tags: "索引、btree、gin、gist、brin、哈希、索引类型"
---

## 为您的数据选择正确的索引类型

不同的索引类型擅长不同的查询模式。默认 B 树并不总是最佳的。

**不正确（JSONB 包含的 B 树）：**

```sql
-- B-tree cannot optimize containment operators
create index products_attrs_idx on products (attributes);
select * from products where attributes @> '{"color": "red"}';
-- Full table scan - B-tree doesn't support @> operator
```

**正确（JSONB 的 GIN）：**

```sql
-- GIN supports @>, ?, ?&, ?| operators
create index products_attrs_idx on products using gin (attributes);
select * from products where attributes @> '{"color": "red"}';
```

索引类型指南：

```sql
-- B-tree (default): =, <, >, BETWEEN, IN, IS NULL
create index users_created_idx on users (created_at);

-- GIN: arrays, JSONB, full-text search
create index posts_tags_idx on posts using gin (tags);

-- GiST: geometric data, range types, nearest-neighbor (KNN) queries
create index locations_idx on places using gist (location);

-- BRIN: large time-series tables (10-100x smaller)
create index events_time_idx on events using brin (created_at);

-- Hash: equality-only (slightly faster than B-tree for =)
create index sessions_token_idx on sessions using hash (token);
```

参考：[索引类型](https://www.postgresql.org/docs/current/indexes-types.html)
