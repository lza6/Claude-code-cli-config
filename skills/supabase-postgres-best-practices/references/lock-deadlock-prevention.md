---
title: "通过一致的锁顺序防止死锁"
impact: "中高"
impactDescription: "消除死锁错误，提高可靠性"
tags: "死锁、锁定、事务、排序"
---

## 通过一致的锁顺序防止死锁

当事务以不同的顺序锁定资源时，就会发生死锁。总是
以一致的顺序获取锁。

**不正确（锁顺序不一致）：**

```sql
-- Transaction A                    -- Transaction B
begin;                              begin;
update accounts                     update accounts
set balance = balance - 100         set balance = balance - 50
where id = 1;                       where id = 2;  -- B locks row 2

update accounts                     update accounts
set balance = balance + 100         set balance = balance + 50
where id = 2;  -- A waits for B     where id = 1;  -- B waits for A

-- DEADLOCK! Both waiting for each other
```

**正确（首先以一致的顺序锁定行）：**

```sql
-- Explicitly acquire locks in ID order before updating
begin;
select * from accounts where id in (1, 2) order by id for update;

-- Now perform updates in any order - locks already held
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id = 2;
commit;
```

替代方案：使用单个语句进行原子更新：

```sql
-- Single statement acquires all locks atomically
begin;
update accounts
set balance = balance + case id
  when 1 then -100
  when 2 then 100
end
where id in (1, 2);
commit;
```

检测日志中的死锁：

```sql
-- Check for recent deadlocks
select * from pg_stat_database where deadlocks > 0;

-- Enable deadlock logging
set log_lock_waits = on;
set deadlock_timeout = '1s';
```

参考：
[死锁](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS)
