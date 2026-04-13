---
title: "使用建议锁进行应用程序级锁定"
impact: "中等的"
impactDescription: "高效协调，无需行级锁开销"
tags: "咨询锁、协调、应用程序锁"
---

## 使用建议锁进行应用程序级锁定

咨询锁提供应用程序级协调，而不需要锁定数据库行。

**不正确（创建行只是为了锁定）：**

```sql
-- Creating dummy rows to lock on
create table resource_locks (
  resource_name text primary key
);

insert into resource_locks values ('report_generator');

-- Lock by selecting the row
select * from resource_locks where resource_name = 'report_generator' for update;
```

**正确（咨询锁）：**

```sql
-- Session-level advisory lock (released on disconnect or unlock)
select pg_advisory_lock(hashtext('report_generator'));
-- ... do exclusive work ...
select pg_advisory_unlock(hashtext('report_generator'));

-- Transaction-level lock (released on commit/rollback)
begin;
select pg_advisory_xact_lock(hashtext('daily_report'));
-- ... do work ...
commit;  -- Lock automatically released
```

非阻塞操作的尝试锁定：

```sql
-- Returns immediately with true/false instead of waiting
select pg_try_advisory_lock(hashtext('resource_name'));

-- Use in application
if (acquired) {
  -- Do work
  select pg_advisory_unlock(hashtext('resource_name'));
} else {
  -- Skip or retry later
}
```

参考：[咨询锁](https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS)
