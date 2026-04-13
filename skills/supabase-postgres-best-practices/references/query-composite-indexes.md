---
title: "为多列查询创建复合索引"
impact: "高的"
impactDescription: 5-10x faster multi-column queries
tags: "索引、复合索引、多列、查询优化"
---

## 为多列查询创建复合索引

当查询对多个列进行筛选时，复合索引比单独的单列索引更有效。

**不正确（单独的索引需要位图扫描）：**

```sql
-- Two separate indexes
create index orders_status_idx on orders (status);
create index orders_created_idx on orders (created_at);

-- Query must combine both indexes (slower)
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**正确（综合指数）：**

```sql
-- Single composite index (leftmost column first for equality checks)
create index orders_status_created_idx on orders (status, created_at);

-- Query uses one efficient index scan
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**列顺序很重要** - 将相等列放在前面，将范围列放在最后：

```sql
-- Good: status (=) before created_at (>)
create index idx on orders (status, created_at);

-- Works for: WHERE status = 'pending'
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
-- Does NOT work for: WHERE created_at > '2024-01-01' (leftmost prefix rule)
```

参考：[多列索引](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
