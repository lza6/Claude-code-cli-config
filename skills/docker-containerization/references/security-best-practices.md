# 安全最佳实践

## 安全最佳实践

```dockerfile
FROM node:18-alpine

# 更新软件包以获取安全补丁
RUN apk update && apk upgrade

# 不要以 root 身份运行
RUN addgroup -g 1001 appgroup && adduser -S -u 1001 -G appgroup appuser
USER appuser

# 使用特定版本，不要使用 'latest'
WORKDIR /app

# 扫描漏洞
# 运行：docker scan your-image:tag
```


## 环境配置

```dockerfile
# 使用构建参数以提高灵活性
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD node healthcheck.js || exit 1

# 元数据标签
LABEL maintainer="team@example.com" \
      version="1.0.0" \
      description="生产环境 API 服务"
```
