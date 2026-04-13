---
title: "索引外键列"
impact: "高的"
impactDescription: 10-100x faster JOINs and CASCADE operations
tags: "外键、索引、连接、模式"
---

## 索引外键列

Postgres 不会自动索引外键列。缺少索引会导致 JOIN 和 CASCADE 操作缓慢。

**不正确（未索引的外键）：**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- No index on customer_id!
-- JOINs and ON DELETE CASCADE both require full table scan
select * from orders where customer_id = 123;  -- Seq Scan
delete from customers where id = 123;          -- Locks table, scans all orders
```

**正确（索引外键）：**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- Always index the FK column
create index orders_customer_id_idx on orders (customer_id);

-- Now JOINs and cascades are fast
select * from orders where customer_id = 123;  -- Index Scan
delete from customers where id = 123;          -- Uses index, fast cascade
```

查找缺失的 FK 索引：

```sql
select
  conrelid::regclass as table_name,
  a.attname as fk_column
from pg_constraint c
join pg_attribute a on a.attrelid = c.conrelid and a.attnum = any(c.conkey)
where c.contype = 'f'
  and not exists (
    select 1 from pg_index i
    where i.indrelid = c.conrelid and a.attnum = any(i.indkey)
  );
```

参考：[外键](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
