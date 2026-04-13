---
name: cicd-pipeline-setup
description: "使用 GitHub Actions、GitLab CI、Jenkins 或 CircleCI 设计和实现 CI/CD 管道。用于自动化测试、构建和部署工作流。"
---

# CI/CD 管道设置

## 目录

- [概述](#概述)
- [何时使用](#何时使用)
- [快速启动](#快速启动)
- [参考指南](#参考指南)
- [最佳实践](#最佳实践)

## 概述

构建自动化的持续集成和部署管道，以最少的手动干预来测试代码、构建工件、运行安全检查并部署到多个环境。

## 何时使用

- 自动化代码测试和质量检查
- 容器化应用程序构建
- 多环境部署
- 发布管理和版本控制
- 自动安全扫描
- 性能测试集成
- 工件管理和注册

## 快速入门

最小工作示例：

```yaml
# .github/workflows/deploy.yml
name: 构建和部署

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
// ... (完整实现请参阅参考指南)
```

## 参考指南

详细实现在 `references/` 目录中：

| 指南 | 内容 |
|---|---|
| [GitHub Actions 工作流](references/github-actions-workflow.md) | GitHub Actions 工作流 |
| [GitLab CI 管道](references/gitlab-ci-pipeline.md) | GitLab CI 管道 |
| [Jenkins 管道](references/jenkins-pipeline.md) | Jenkins 管道 |
| [CI/CD 脚本](references/cicd-script.md) | CI/CD 脚本 |

## 最佳实践

### ✅ 应该做

- 通过早期验证快速失败
- 尽可能并行运行测试
- 对依赖项使用缓存
- 实施适当的秘密管理
- 经批准后进行生产部署
- 监控管道故障并发出警报
- 使用一致的环境配置
- 实施基础设施即代码

### ❌ 不要做

- 在管道配置中存储凭据
- 无需自动化测试即可部署
- 跳过安全扫描
- 允许长时间运行的管道
- 混合暂存和生产管道
- 忽略测试失败
- 直接部署到主分支
- 部署后跳过健康检查
