---
title: "使用基于光标的分页而不是 OFFSET"
impact: "中高"
impactDescription: "无论页面深度如何，始终保持 O(1) 性能"
tags: "分页、光标、键集、偏移、性能"
---

## 使用基于光标的分页而不是 OFFSET

基于 OFFSET 的分页会扫描所有跳过的行，在更深的页面上速度会变慢。游标分页时间复杂度为 O(1)。

**不正确（偏移分页）：**

```sql
-- Page 1: scans 20 rows
select * from products order by id limit 20 offset 0;

-- Page 100: scans 2000 rows to skip 1980
select * from products order by id limit 20 offset 1980;

-- Page 10000: scans 200,000 rows!
select * from products order by id limit 20 offset 199980;
```

**正确（光标/键集分页）：**

```sql
-- Page 1: get first 20
select * from products order by id limit 20;
-- Application stores last_id = 20

-- Page 2: start after last ID
select * from products where id > 20 order by id limit 20;
-- Uses index, always fast regardless of page depth

-- Page 10000: same speed as page 1
select * from products where id > 199980 order by id limit 20;
```

对于多列排序：

```sql
-- Cursor must include all sort columns
select * from products
where (created_at, id) > ('2024-01-15 10:00:00', 12345)
order by created_at, id
limit 20;
```

参考：[分页](https://supabase.com/docs/guides/database/pagination)
