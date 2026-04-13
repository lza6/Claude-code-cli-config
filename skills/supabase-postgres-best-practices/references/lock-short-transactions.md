---
title: "保持事务简短以减少锁争用"
impact: "中高"
impactDescription: 3-5x throughput improvement, fewer deadlocks
tags: "事务、锁定、争用、性能"
---

## 保持事务简短以减少锁争用

长时间运行的事务持有会阻塞其他查询的锁。保持事务尽可能短。

**不正确（带有外部调用的长事务）：**

```sql
begin;
select * from orders where id = 1 for update;  -- Lock acquired

-- Application makes HTTP call to payment API (2-5 seconds)
-- Other queries on this row are blocked!

update orders set status = 'paid' where id = 1;
commit;  -- Lock held for entire duration
```

**正确（最小交易范围）：**

```sql
-- Validate data and call APIs outside transaction
-- Application: response = await paymentAPI.charge(...)

-- Only hold lock for the actual update
begin;
update orders
set status = 'paid', payment_id = $1
where id = $2 and status = 'pending'
returning *;
commit;  -- Lock held for milliseconds
```

使用“statement_timeout”来防止事务失控：

```sql
-- Abort queries running longer than 30 seconds
set statement_timeout = '30s';

-- Or per-session
set local statement_timeout = '5s';
```

参考：【事务管理】(https://www.postgresql.org/docs/current/tutorial-transactions.html)
