---
name: api-connector-builder
description: "通过精确匹配目标仓库现有的集成模式，构建新的 API 连接器 (Connector) 或提供者 (Provider)。当需要增加一个集成点而不发明第二套架构时使用。"
origin: ECC direct-port adaptation
version: "1.0.0"
---

# API 连接器构建器 (API Connector Builder)

当任务是添加仓库原生的集成界面，而不仅仅是一个通用的 HTTP 客户端时，请使用此技能。

关键点在于匹配宿主仓库的既有模式：

- 连接器布局 (Connector layout)
- 配置模式 (Config schema)
- 认证模型 (Auth model)
- 错误处理 (Error handling)
- 测试风格 (Test style)
- 注册与发现机制 (Registration/discovery wiring)

## 何时使用

- “为此项目构建一个 Jira 连接器”
- “按照现有模式添加一个 Slack 提供者 (Provider)”
- “为此 API 创建一个新的集成点”
- “构建一个匹配该仓库连接器风格的插件”

## 准则

- 当仓库已有集成架构时，不要发明新的集成架构。
- 不要仅依赖厂商提供的文档；首先参考仓库内现有的连接器。
- 如果仓库期望包含注册关联、测试和文档，不要仅仅停留在传输层代码的编写。
- 如果仓库有更新的当前模式，不要生搬硬套旧连接器的做法。

## 工作流

### 1. 学习项目风格

检查至少 2 个现有的连接器/提供者，并理清以下内容：

- 文件布局
- 抽象边界
- 配置模型
- 重试与分页约定
- 注册钩子 (Registry hooks)
- 测试固件 (Test fixtures) 与命名规范

### 2. 明确目标集成范围

仅定义仓库实际需要的界面：

- 认证流 (Auth flow)
- 关键实体
- 核心读/写操作
- 分页与速率限制 (Rate limits)
- Webhook 或轮询模型

### 3. 构建仓库原生的各层级

典型的切片包括：

- 配置/模式 (Config/Schema)
- 客户端/传输层 (Client/Transport)
- 映射层 (Mapping layer)
- 连接器/提供者入口点
- 注册关联
- 测试

### 4. 针对原始模式进行验证

新的连接器在代码库中应该显得顺理成章，而不是看起来像从不同的生态系统中搬运过来的。

## 参考形态

### 提供者 (Provider) 风格

```text
providers/
  existing_provider/
    __init__.py
    provider.py
    config.py
```

### 连接器 (Connector) 风格

```text
integrations/
  existing/
    client.py
    models.py
    connector.py
```

### TypeScript 插件风格

```text
src/integrations/
  existing/
    index.ts
    client.ts
    types.ts
    test.ts
```

## 质量检查清单

- [ ] 匹配仓库内现有的集成模式
- [ ] 存在配置验证逻辑
- [ ] 认证和错误处理是显式的
- [ ] 分页/重试行为遵循仓库规范
- [ ] 注册/发现机制关联完整
- [ ] 测试镜像了宿主仓库的风格
- [ ] 如果仓库有要求，文档/示例已同步更新

## 相关技能

- `backend-patterns`
- `mcp-server-patterns`
- `github-ops`
