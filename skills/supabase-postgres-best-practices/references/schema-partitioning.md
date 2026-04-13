---
title: "对大表进行分区以获得更好的性能"
impact: "中高"
impactDescription: 5-20x faster queries and maintenance on large tables
tags: "分区、大表、时间序列、性能"
---

## 对大表进行分区以获得更好的性能

分区将大表分割成更小的部分，从而提高查询性能和维护操作。

**不正确（单个大表）：**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz,
  data jsonb
);

-- 500M rows, queries scan everything
select * from events where created_at > '2024-01-01';  -- Slow
vacuum events;  -- Takes hours, locks table
```

**正确（按时间范围划分）：**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz not null,
  data jsonb
) partition by range (created_at);

-- Create partitions for each month
create table events_2024_01 partition of events
  for values from ('2024-01-01') to ('2024-02-01');

create table events_2024_02 partition of events
  for values from ('2024-02-01') to ('2024-03-01');

-- Queries only scan relevant partitions
select * from events where created_at > '2024-01-15';  -- Only scans events_2024_01+

-- Drop old data instantly
drop table events_2023_01;  -- Instant vs DELETE taking hours
```

何时分区：

- 表 > 100M 行
- 具有基于日期的查询的时间序列数据
- 需要有效删除旧数据

参考：[表分区](https://www.postgresql.org/docs/current/ddl-partitioning.html)
