---
name: docker-containerization
description: "创建优化的 Docker 容器，使用多阶段构建、安全最佳实践和最小镜像大小。在容器化应用程序、创建 Dockerfile、优化容器镜像或设置 Docker Compose 服务时使用。"
---

# Docker 容器化

## 目录

- [概述](#概述)
- [何时使用](#何时使用)
- [快速启动](#快速启动)
- [参考指南](#参考指南)
- [最佳实践](#最佳实践)

## 概述

遵循安全性、性能和可维护性的最佳实践构建生产就绪的 Docker 容器。

## 何时使用

- 将应用程序容器化以进行部署
- 为新服务创建 Dockerfile
- 优化现有容器镜像
- 设置开发环境
- 构建 CI/CD 容器管道
- 实施微服务

## 快速入门

最小工作示例：

```dockerfile
# Node.js 应用程序的多阶段构建
# 阶段 1：构建
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 阶段 2：生产环境
FROM node:18-alpine
WORKDIR /app
# 仅复制生产依赖和构建文件
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package*.json ./

# 安全：以非 root 用户运行
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## 参考指南

详细实现在 `references/` 目录中：

| 指南 | 内容 |
|---|---|
| [多阶段构建](references/multi-stage-builds.md) | 多阶段构建 |
| [优化技术](references/optimization-techniques.md) | 优化技术 |
| [安全最佳实践](references/security-best-practices.md) | 安全最佳实践、环境配置 |
| [Docker Compose 多容器](references/docker-compose-for-multi-container.md) | Docker Compose 多容器 |
| [.dockerignore 文件](references/dockerignore-file.md) | .dockerignore 文件 |
| [Python](references/python.md) | Python (Django/Flask), Java (Spring Boot), Go |

## 最佳实践

### ✅ 应该做

- 使用官方基础镜像
- 实施多阶段构建
- 以非 root 用户身份运行
- 使用 .dockerignore
- 固定特定版本
- 包含健康检查
- 扫描漏洞
- 最小化层数
- 有效利用构建缓存

### ❌ 不要做

- 在生产中使用 `latest` 标签
- 以 root 用户身份运行
- 在镜像中包含密钥
- 创建不必要的层
- 安装不必要的包
- 忽略安全更新
- 在容器中存储数据
