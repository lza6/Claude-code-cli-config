---
name: database-query-optimization
description: ">"
  通过索引、查询优化和执行计划分析提升数据库查询性能。减少响应时间和数据库负载。
---

# 数据库查询优化

## 目录

- [概述](#概述)
- [何时使用](#何时使用)
- [快速启动](#快速启动)
- [参考指南](#参考指南)
- [最佳实践](#最佳实践)

## 概述

缓慢的数据库查询是常见的性能瓶颈。通过索引、高效查询和缓存进行优化可显著提高应用程序性能。

## 何时使用

- 响应时间慢
- 数据库 CPU 使用率高
- 性能回归
- 新功能部署前
- 定期维护

## 快速入门

最小工作示例：

```sql
-- 分析查询性能

EXPLAIN ANALYZE
SELECT users.id, users.name, COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE users.created_at > '2024-01-01'
GROUP BY users.id, users.name
ORDER BY order_count DESC;

-- 结果展示：
-- - Seq Scan（慢）vs Index Scan（快）
-- - Rows: actual vs planned（差异大 = 性能差）
-- - Execution time（毫秒）

-- 关键指标：
-- - Sequential Scan：全表扫描（慢）
-- - Index Scan：使用索引（快）
-- - Nested Loop：循环连接
-- - Sort：内存或磁盘排序
```

## 参考指南

详细实现在 `references/` 目录中：

| 指南 | 内容 |
|---|---|
| [查询分析](references/query-analysis.md) | 查询分析 |
| [索引策略](references/indexing-strategy.md) | 索引策略 |
| [查询优化技术](references/query-optimization-techniques.md) | 查询优化技术 |
| [优化清单](references/optimization-checklist.md) | 优化清单 |

## 最佳实践

### ✅ 应该做

- 遵循既定的模式和惯例
- 编写干净、可维护的代码
- 添加适当的文档
- 部署前充分测试

### ❌ 不应该做

- 跳过测试或验证
- 忽略错误处理
- 硬编码配置值
