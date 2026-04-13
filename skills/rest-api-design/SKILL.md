---
name: rest-api-design
description: ">"
  遵循资源建模、HTTP 方法、状态码、版本控制和文档的最佳实践设计 RESTful API。
  在创建新 API、设计端点或改进现有 API 架构时使用。
---

# REST API 设计

## 目录

- [概述](#概述)
- [何时使用](#何时使用)
- [快速启动](#快速启动)
- [参考指南](#参考指南)
- [最佳实践](#最佳实践)

## 概述

设计直观、一致的 REST API，并遵循面向资源的架构的行业最佳实践。

## 何时使用

- 设计新的 RESTful API
- 创建端点结构
- 定义请求/响应格式
- 实施 API 版本控制
- 记录 API 规范
- 重构现有 API

## 快速入门

最小工作示例：

```
✅ 正确的资源命名（名词，复数）
GET    /api/users
GET    /api/users/123
GET    /api/users/123/orders
POST   /api/products
DELETE /api/products/456

❌ 错误的资源命名（动词，不一致）
GET    /api/getUsers
POST   /api/createProduct
GET    /api/user/123  （单复数不一致）
```

## 参考指南

详细实现在 `references/` 目录中：

| 指南 | 内容 |
|---|---|
| [资源命名](references/resource-naming.md) | 资源命名、HTTP 方法和操作 |
| [请求示例](references/request-examples.md) | 请求示例 |
| [查询参数](references/query-parameters.md) | 查询参数 |
| [响应格式](references/response-formats.md) | 响应格式 |
| [HTTP 状态码](references/http-status-codes.md) | HTTP 状态码、API 版本控制、身份验证和安全性、速率限制标头 |
| [OpenAPI 文档](references/openapi-documentation.md) | OpenAPI 文档 |
| [完整示例：Express.js](references/complete-example-expressjs.md) | Express.js 完整示例 |

## 最佳实践

### ✅ 应该做

- 使用名词来表示资源，而不是动词
- 集合使用复数名称
- 与命名约定保持一致
- 返回适当的 HTTP 状态码
- 包括集合的分页
- 提供过滤和排序选项
- 版本化你的 API
- 使用 OpenAPI 进行详细文档
- 使用 HTTPS
- 实施速率限制
- 提供清晰的错误消息
- 使用 ISO 8601 日期格式

### ❌ 不应该做

- 在端点名称中使用动词
- 错误地返回 200
- 不必要地暴露内部 ID
- 过度嵌套资源（最多 2 层）
- 使用不一致的命名
- 忘记身份验证
- 返回敏感数据
- 在不版本化的情况下破坏向后兼容性
