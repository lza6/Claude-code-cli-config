---
title: "启用 pg_stat_statements 进行查询分析"
impact: "低-中"
impactDescription: "识别最消耗资源的查询"
tags: "pg-stat-语句，监控，统计，性能"
---

## 启用pg_stat_statements进行查询分析

pg_stat_statements 跟踪所有查询的执行统计信息，帮助识别缓慢和频繁的查询。

**不正确（无法查看查询模式）：**

```sql
-- Database is slow, but which queries are the problem?
-- No way to know without pg_stat_statements
```

**正确（启用并查询 pg_stat_statements）：**

```sql
-- Enable the extension
create extension if not exists pg_stat_statements;

-- Find slowest queries by total time
select
  calls,
  round(total_exec_time::numeric, 2) as total_time_ms,
  round(mean_exec_time::numeric, 2) as mean_time_ms,
  query
from pg_stat_statements
order by total_exec_time desc
limit 10;

-- Find most frequent queries
select calls, query
from pg_stat_statements
order by calls desc
limit 10;

-- Reset statistics after optimization
select pg_stat_statements_reset();
```

要监控的关键指标：

```sql
-- Queries with high mean time (candidates for optimization)
select query, mean_exec_time, calls
from pg_stat_statements
where mean_exec_time > 100  -- > 100ms average
order by mean_exec_time desc;
```

参考：[pg_stat_statements](https://supabase.com/docs/guides/database/extensions/pg_stat_statements)
