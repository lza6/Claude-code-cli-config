---
title: "在 WHERE 和 JOIN 列上添加索引"
impact: "批判的"
impactDescription: 100-1000x faster queries on large tables
tags: "索引、性能、顺序扫描、查询优化"
---

## 在 WHERE 和 JOIN 列上添加索引

对未索引列进行过滤或连接的查询会导致全表扫描，随着表的增长，全表扫描的速度会呈指数级下降。

**不正确（大表上的顺序扫描）：**

```sql
-- No index on customer_id causes full table scan
select * from orders where customer_id = 123;

-- EXPLAIN shows: Seq Scan on orders (cost=0.00..25000.00 rows=100 width=85)
```

**正确（索引扫描）：**

```sql
-- Create index on frequently filtered column
create index orders_customer_id_idx on orders (customer_id);

select * from orders where customer_id = 123;

-- EXPLAIN shows: Index Scan using orders_customer_id_idx (cost=0.42..8.44 rows=100 width=85)
```

对于 JOIN 列，始终索引外键端：

```sql
-- Index the referencing column
create index orders_customer_id_idx on orders (customer_id);

select c.name, o.total
from customers c
join orders o on o.customer_id = c.id;
```

参考：【查询优化】(https://supabase.com/docs/guides/database/query-optimization)
