---
name: workflow-automation
description: "自动执行重复的开发任务和工作流程。在创建构建脚本、自动化部署或设置开发工作流程时使用。处理 npm 脚本、Makefile、GitHub Actions 工作流和任务自动化。"
metadata:
  tags: automation, scripts, workflow, npm-scripts, Makefile, task-runner
  platforms: Claude, ChatGPT, Gemini
---


# 工作流自动化


## 何时使用此技能

- **重复任务**：每次都运行相同的命令
- **复杂构建**：多步骤构建流程
- **团队入职**：一致的开发环境

## 说明

### 步骤 1：npm 脚本

**package.json**：
```json
{
  "scripts": {
    "dev": "nodemon src/index.ts",
    "build": "tsc && vite build",
    "test": "jest --coverage",
    "test:watch": "jest --watch",
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,json}\"",
    "type-check": "tsc --noEmit",
    "pre-commit": "lint-staged",
    "prepare": "husky install",
    "clean": "rm -rf dist node_modules",
    "reset": "npm run clean && npm install",
    "docker:build": "docker build -t myapp .",
    "docker:run": "docker run -p 3000:3000 myapp"
  }
}
```

### 步骤 2：Makefile

**Makefile**：
```makefile
.PHONY: help install dev build test clean docker

.DEFAULT_GOAL := help

help: ## 显示此帮助信息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装依赖
	npm install

dev: ## 启动开发服务器
	npm run dev

build: ## 构建生产版本
	npm run build

test: ## 运行所有测试
	npm test

lint: ## 运行代码检查
	npm run lint

lint-fix: ## 修复代码检查问题
	npm run lint:fix

clean: ## 清理构建产物
	rm -rf dist coverage

docker-build: ## 构建 Docker 镜像
	docker build -t myapp:latest .

docker-run: ## 运行 Docker 容器
	docker run -d -p 3000:3000 --name myapp myapp:latest

deploy: build ## 部署到生产环境
	@echo "正在部署到生产环境..."
	./scripts/deploy.sh production

ci: lint test build ## 本地运行 CI 流水线
	@echo "✅ CI 流水线通过！"
```

**用法**：
```bash
make help        # 显示所有命令
make dev         # 启动开发环境
make ci          # 本地运行完整 CI
```

### 步骤 3：Husky + lint-staged（Git 钩子）

**package.json**：
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

**.husky/pre-commit**：
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "正在运行提交前检查..."

# 检查暂存文件
npx lint-staged

# 类型检查
npm run type-check

# 运行与已更改文件相关的测试
npm test -- --onlyChanged

echo "✅ 提交前检查通过！"
```

### 步骤 4：任务运行器脚本

**scripts/dev-setup.sh**：
```bash
#!/bin/bash
set -e

echo "🚀 正在设置开发环境..."

# 检查前置条件
if ! command -v node &> /dev/null; then
    echo "❌ 未安装 Node.js"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ 未安装 Docker"
    exit 1
fi

# 安装依赖
echo "📦 正在安装依赖..."
npm install

# 复制环境文件
if [ ! -f .env ]; then
    echo "📄 正在创建 .env 文件..."
    cp .env.example .env
    echo "⚠️ 请用你的配置更新 .env"
fi

# 启动 Docker 服务
echo "🐳 正在启动 Docker 服务..."
docker-compose up -d

# 等待数据库
echo "⏳ 等待数据库就绪..."
./scripts/wait-for-it.sh localhost:5432 --timeout=30

# 运行迁移
echo "🗄️ 正在运行数据库迁移..."
npm run migrate

# 种子数据（可选）
read -p "是否用示例数据填充数据库？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    npm run seed
fi

echo "✅ 开发环境准备就绪！"
echo "运行 'make dev' 启动开发服务器"
```

**scripts/deploy.sh**：
```bash
#!/bin/bash
set -e

ENV=$1

if [ -z "$ENV" ]; then
    echo "用法: ./deploy.sh [staging|production]"
    exit 1
fi

echo "🚀 正在部署到 $ENV..."

# 构建
echo "📦 正在构建应用..."
npm run build

# 运行测试
echo "🧪 正在运行测试..."
npm test

# 根据环境部署
if [ "$ENV" == "production" ]; then
    echo "🌍 正在部署到生产环境..."
    # 生产环境部署逻辑
    ssh production "cd /app && git pull && npm install && npm run build && pm2 restart all"
elif [ "$ENV" == "staging" ]; then
    echo "🧪 正在部署到预发布环境..."
    # 预发布环境部署逻辑
    ssh staging "cd /app && git pull && npm install && npm run build && pm2 restart all"
fi

echo "✅ 部署到 $ENV 完成！"
```

### 步骤 5：GitHub Actions 工作流自动化

**.github/workflows/ci.yml**：
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: 设置 Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: 安装依赖
        run: npm ci

      - name: 运行代码检查
        run: npm run lint

      - name: 类型检查
        run: npm run type-check

      - name: 运行测试
        run: npm test -- --coverage

      - name: 上传覆盖率
        uses: codecov/codecov-action@v3
```

## 输出格式

```
project/
├── scripts/
│   ├── dev-setup.sh
│   ├── deploy.sh
│   ├── test.sh
│   └── cleanup.sh
├── Makefile
├── package.json
└── .husky/
    ├── pre-commit
    └── pre-push
```

## 约束条件

### 必需规则（必须遵守）

1. **幂等性**：脚本可以安全地多次运行
2. **错误处理**：清晰的失败消息
3. **文档**：关于如何使用脚本的注释

### 禁止事项（不得执行）

1. **硬编码密钥**：不要在脚本中包含密码或 API 密钥
2. **破坏性命令**：未经确认请勿运行 rm -rf

## 最佳实践

1. **使用 Make**：与平台无关的接口
2. **Git 钩子**：自动化质量检查
3. **CI/CD**：使用 GitHub Actions 实现自动化

## 参考资料

- [npm 脚本](https://docs.npmjs.com/cli/v9/using-npm/scripts)
- [Make 教程](https://makefiletutorial.com/)
- [Husky](https://typicode.github.io/husky/)

## 元数据

### 版本
- **当前版本**：1.0.0
- **最后更新**：2025-01-01
- **兼容平台**：Claude、ChatGPT、Gemini

### 标签
`#automation` `#scripts` `#workflow` `#npm-scripts` `#Makefile` `#utilities`

## 示例

### 示例 1：基本用法
<!-- 在此添加示例内容 -->

### 示例 2：高级用法
<!-- 在此添加高级示例内容 -->
