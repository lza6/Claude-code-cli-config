---
title: "使用 SKIP LOCKED 进行非阻塞队列处理"
impact: "中高"
impactDescription: 10x throughput for worker queues
tags: "跳过锁定、队列、工人、并发"
---

## 使用 SKIP LOCKED 进行非阻塞队列处理

当多个工作进程处理一个队列时，SKIP LOCKED 允许工作进程无需等待即可处理不同的行。

**不正确（工人互相阻塞）：**

```sql
-- Worker 1 and Worker 2 both try to get next job
begin;
select * from jobs where status = 'pending' order by created_at limit 1 for update;
-- Worker 2 waits for Worker 1's lock to release!
```

**正确（并行处理时跳过锁定）：**

```sql
-- Each worker skips locked rows and gets the next available
begin;
select * from jobs
where status = 'pending'
order by created_at
limit 1
for update skip locked;

-- Worker 1 gets job 1, Worker 2 gets job 2 (no waiting)

update jobs set status = 'processing' where id = $1;
commit;
```

完整的队列模式：

```sql
-- Atomic claim-and-update in one statement
update jobs
set status = 'processing', worker_id = $1, started_at = now()
where id = (
  select id from jobs
  where status = 'pending'
  order by created_at
  limit 1
  for update skip locked
)
returning *;
```

参考：[SELECT FOR UPDATE SKIP LOCKED](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE)
