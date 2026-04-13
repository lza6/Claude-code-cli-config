---
title: "索引 JSONB 列以实现高效查询"
impact: "中等的"
impactDescription: 10-100x faster JSONB queries with proper indexing
tags: "jsonb、杜松子酒、索引、json"
---

## 索引 JSONB 列以实现高效查询

没有索引的 JSONB 查询会扫描整个表。使用 GIN 索引进行包含查询。

**不正确（JSONB 上没有索引）：**

```sql
create table products (
  id bigint primary key,
  attributes jsonb
);

-- Full table scan for every query
select * from products where attributes @> '{"color": "red"}';
select * from products where attributes->>'brand' = 'Nike';
```

**正确（JSONB 的 GIN 索引）：**

```sql
-- GIN index for containment operators (@>, ?, ?&, ?|)
create index products_attrs_gin on products using gin (attributes);

-- Now containment queries use the index
select * from products where attributes @> '{"color": "red"}';

-- For specific key lookups, use expression index
create index products_brand_idx on products ((attributes->>'brand'));
select * from products where attributes->>'brand' = 'Nike';
```

选择正确的运算符类别：

```sql
-- jsonb_ops (default): supports all operators, larger index
create index idx1 on products using gin (attributes);

-- jsonb_path_ops: only @> operator, but 2-3x smaller index
create index idx2 on products using gin (attributes jsonb_path_ops);
```

参考：[JSONB 索引](https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING)
