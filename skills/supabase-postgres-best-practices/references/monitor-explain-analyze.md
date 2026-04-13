---
title: "使用 EXPLAIN ANALYZE 诊断慢速查询"
impact: "低-中"
impactDescription: "确定查询执行中的确切瓶颈"
tags: "解释、分析、诊断、查询计划"
---

## 使用 EXPLAIN ANALYZE 诊断慢查询

EXPLAIN ANALYZE 执行查询并显示实际时间，揭示真正的性能瓶颈。

**不正确（猜测性能问题）：**

```sql
-- Query is slow, but why?
select * from orders where customer_id = 123 and status = 'pending';
-- "It must be missing an index" - but which one?
```

**正确（使用解释分析）：**

```sql
explain (analyze, buffers, format text)
select * from orders where customer_id = 123 and status = 'pending';

-- Output reveals the issue:
-- Seq Scan on orders (cost=0.00..25000.00 rows=50 width=100) (actual time=0.015..450.123 rows=50 loops=1)
--   Filter: ((customer_id = 123) AND (status = 'pending'::text))
--   Rows Removed by Filter: 999950
--   Buffers: shared hit=5000 read=15000
-- Planning Time: 0.150 ms
-- Execution Time: 450.500 ms
```

需要寻找的关键事项：

```sql
-- Seq Scan on large tables = missing index
-- Rows Removed by Filter = poor selectivity or missing index
-- Buffers: read >> hit = data not cached, needs more memory
-- Nested Loop with high loops = consider different join strategy
-- Sort Method: external merge = work_mem too low
```

参考：[解释](https://supabase.com/docs/guides/database/inspect)
