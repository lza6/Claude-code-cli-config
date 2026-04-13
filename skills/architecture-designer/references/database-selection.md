# 数据库选择

## 数据库类型

| 类型 | 示例 | 最适合 |
|------|----------|----------|
| **关系型 (Relational)** | PostgreSQL, MySQL | 事务、复杂查询、关系处理 |
| **文档型 (Document)** | MongoDB, Firestore | 灵活的架构、快速迭代 |
| **键值对 (Key-Value)** | Redis, DynamoDB | 缓存、会话、高吞吐量 |
| **时序型 (Time-Series)** | TimescaleDB, InfluxDB | 指标监控、物联网 (IoT)、分析 |
| **图形 (Graph)** | Neo4j, Neptune | 社交关系、社交网络 |
| **搜索 (Search)** | Elasticsearch, Meilisearch | 全文搜索、日志分析 |

## 关系型 (PostgreSQL, MySQL)

```
最适合：
- 财务交易 (ACID 合规性)
- 带有连接 (Join) 的复杂查询
- 数据完整性要求高
- 结构化、可预测的架构

何时避免：
- 变化极大的架构
- 巨大的水平扩展需求
- 简单的键值访问模式
```

| 特性 | PostgreSQL | MySQL |
|---------|------------|-------|
| JSON 支持 | 极佳 (JSONB) | 良好 (JSON) |
| 全文搜索 | 内置 | 基础 |
| 扩展性 | 丰富的生态系统 | 有限 |
| 复制 | 流复制、逻辑复制 | 基于语句、基于行的复制 |

## 文档型 (MongoDB, Firestore)

```
最适合：
- 灵活、不断演进的架构
- 分层数据 (嵌套文档)
- 快速原型开发
- 内容管理

何时避免：
- 跨文档的复杂事务
- 繁重的关系查询
- 严格的架构要求
```

## 键值对 (Redis, DynamoDB)

```
最适合：
- 会话存储
- 缓存层
- 实时排行榜
- 速率限制计数器

何时避免：
- 复杂查询
- 关系型数据
- 大数据值 (>1MB)
```

## 时序型 (TimescaleDB, InfluxDB)

```
最适合：
- 指标和监控
- 物联网 (IoT) 传感器数据
- 金融行情数据 (Tick data)
- 带有时间戳的事件日志

何时避免：
- 频繁更新现有记录
- 复杂的关系查询
- 非基于时间的访问模式
```

## 决策矩阵

| 需求 | 推荐 |
|-------------|-------------|
| ACID 事务 | PostgreSQL, MySQL |
| 灵活的架构 | MongoDB, Firestore |
| 高速缓存 | Redis |
| 时序数据 | TimescaleDB, InfluxDB |
| 社交关系 | Neo4j |
| 全文搜索 | Elasticsearch |
| 无服务器扩展 | DynamoDB, Firestore |

## 快速参考

| 问题 | 如果是 → |
|----------|----------|
| 需要 ACID 事务？ | 关系型 (PostgreSQL) |
| 架构经常变动？ | 文档型 (MongoDB) |
| 亚毫秒级读取？ | 键值对 (Redis) |
| 基于时间的查询？ | 时序型 |
| 遍历复杂关系？ | 图形数据库 (Neo4j) |
| 以全文搜索为主？ | Elasticsearch |
