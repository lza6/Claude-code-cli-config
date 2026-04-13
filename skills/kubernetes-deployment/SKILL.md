---
name: kubernetes-deployment
description: ">"
  在 Kubernetes 集群上部署、管理和扩展容器化应用，
  遵循生产工作负载、资源管理和滚动更新的最佳实践。
---

# Kubernetes 部署

## 目录

- [概述](#概述)
- [何时使用](#何时使用)
- [快速启动](#快速启动)
- [参考指南](#参考指南)
- [最佳实践](#最佳实践)

## 概述

掌握 Kubernetes 部署以大规模管理容器化应用，包括多容器服务、资源分配、健康检查和滚动部署策略。

## 何时使用

- 容器编排和管理
- 多环境部署（开发、预发布、生产）
- 自动扩缩微服务
- 滚动更新和蓝绿部署
- 服务发现和负载均衡
- 资源配额和限制管理
- Pod 网络和安全策略

## 快速入门

最小工作示例：

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  namespace: production
  labels:
    app: api-service
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
        version: v1
      annotations:
// ...（完整实现请参考指南）
```

## 参考指南

详细实现在 `references/` 目录中：

| 指南 | 内容 |
|---|---|
| [资源管理的完整部署](references/complete-deployment-with-resource-management.md) | 包含资源管理的完整部署 |
| [部署脚本](references/deployment-script.md) | 部署脚本 |
| [服务帐户和 RBAC](references/service-account-and-rbac.md) | 服务帐户和 RBAC |

## 最佳实践

### ✅ 应该做

- 使用资源请求和限制
- 实施健康检查（存活探针、就绪探针）
- 使用 ConfigMaps 进行配置
- 应用安全上下文限制
- 使用服务帐户和 RBAC
- 实现 Pod 反亲和性
- 使用命名空间进行隔离
- 启用 Pod 安全策略

### ❌ 不应该做

- 在生产中使用 latest 镜像标签
- 以 root 身份运行容器
- 设置无限制的资源使用
- 跳过错落探针
- 部署无资源限制的应用
- 在容器镜像中混合配置
- 使用默认服务帐户
