---
title: "选择最优主键策略"
impact: "高的"
impactDescription: "更好的索引局部性，减少碎片"
tags: "主键、身份、uuid、序列、模式"
---

## 选择最优主键策略

主键选择会影响插入性能、索引大小和复制
效率。

**不正确（有问题的 PK 选择）：**

```sql
-- identity is the SQL-standard approach
create table users (
  id serial primary key  -- Works, but IDENTITY is recommended
);

-- Random UUIDs (v4) cause index fragmentation
create table orders (
  id uuid default gen_random_uuid() primary key  -- UUIDv4 = random = scattered inserts
);
```

**正确（最佳PK策略）：**

```sql
-- Use IDENTITY for sequential IDs (SQL-standard, best for most cases)
create table users (
  id bigint generated always as identity primary key
);

-- For distributed systems needing UUIDs, use UUIDv7 (time-ordered)
-- Requires pg_uuidv7 extension: create extension pg_uuidv7;
create table orders (
  id uuid default uuid_generate_v7() primary key  -- Time-ordered, no fragmentation
);

-- Alternative: time-prefixed IDs for sortable, distributed IDs (no extension needed)
create table events (
  id text default concat(
    to_char(now() at time zone 'utc', 'YYYYMMDDHH24MISSMS'),
    gen_random_uuid()::text
  ) primary key
);
```

指南：

- 单一数据库：`bigint Identity`（顺序，8字节，SQL标准）
- 分布式/公开 ID：UUIDv7（需要 pg_uuidv7）或 ULID（按时间顺序，无
  碎片）
- `serial` 有效，但 `identity` 是 SQL 标准，并且是新的首选
  应用
- 避免将随机 UUID (v4) 作为大型表的主键（导致索引
  碎片）

参考：
[标识列](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY)
