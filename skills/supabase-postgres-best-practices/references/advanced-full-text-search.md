---
title: "使用 tsvector 进行全文搜索"
impact: "中等的"
impactDescription: 100x faster than LIKE, with ranking support
tags: "全文搜索、tsvector、杜松子酒、搜索"
---

## 使用 tsvector 进行全文搜索

带通配符的 LIKE 不能使用索引。使用 tsvector 进行全文搜索的速度要快几个数量级。

**不正确（LIKE 模式匹配）：**

```sql
-- Cannot use index, scans all rows
select * from articles where content like '%postgresql%';

-- Case-insensitive makes it worse
select * from articles where lower(content) like '%postgresql%';
```

**正确（使用 tsvector 进行全文搜索）：**

```sql
-- Add tsvector column and index
alter table articles add column search_vector tsvector
  generated always as (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))) stored;

create index articles_search_idx on articles using gin (search_vector);

-- Fast full-text search
select * from articles
where search_vector @@ to_tsquery('english', 'postgresql & performance');

-- With ranking
select *, ts_rank(search_vector, query) as rank
from articles, to_tsquery('english', 'postgresql') query
where search_vector @@ query
order by rank desc;
```

搜索多个术语：

```sql
-- AND: both terms required
to_tsquery('postgresql & performance')

-- OR: either term
to_tsquery('postgresql | mysql')

-- Prefix matching
to_tsquery('post:*')
```

参考：[全文检索](https://supabase.com/docs/guides/database/full-text-search)
