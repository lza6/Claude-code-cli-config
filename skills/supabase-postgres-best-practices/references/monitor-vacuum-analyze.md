---
title: "使用 VACUUM 和 ANALYZE 维护表统计信息"
impact: "中等的"
impactDescription: 2-10x better query plans with accurate statistics
tags: "真空、分析、统计、维护、自动真空"
---

## 使用 VACUUM 和 ANALYZE 维护表统计信息

过时的统计信息会导致查询规划器做出错误的决策。 VACUUM 回收空间，ANALYZE 更新统计信息。

**不正确（过时的统计数据）：**

```sql
-- Table has 1M rows but stats say 1000
-- Query planner chooses wrong strategy
explain select * from orders where status = 'pending';
-- Shows: Seq Scan (because stats show small table)
-- Actually: Index Scan would be much faster
```

**正确（保持最新统计数据）：**

```sql
-- Manually analyze after large data changes
analyze orders;

-- Analyze specific columns used in WHERE clauses
analyze orders (status, created_at);

-- Check when tables were last analyzed
select
  relname,
  last_vacuum,
  last_autovacuum,
  last_analyze,
  last_autoanalyze
from pg_stat_user_tables
order by last_analyze nulls first;
```

针对繁忙表的 Autovacuum 调优：

```sql
-- Increase frequency for high-churn tables
alter table orders set (
  autovacuum_vacuum_scale_factor = 0.05,     -- Vacuum at 5% dead tuples (default 20%)
  autovacuum_analyze_scale_factor = 0.02     -- Analyze at 2% changes (default 10%)
);

-- Check autovacuum status
select * from pg_stat_progress_vacuum;
```

参考：[VACUUM](https://supabase.com/docs/guides/database/database-size#vacuum-operations)
