# 优化技术

## 优化技术

### 层缓存

```dockerfile
# ❌ Poor caching - changes in source code invalidate dependency install
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# ✅ Good caching - dependencies cached separately
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

### 最小化图像大小

```dockerfile
# ❌ Large image (~800MB)
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip

# ✅ Minimal image (~50MB)
FROM python:3.11-alpine
```
