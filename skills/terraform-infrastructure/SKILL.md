---
name: terraform-infrastructure
description: "Terraform基础设施 - 使用Terraform进行基础设施即代码，包含模块化组件、状态管理和多云部署。适用于配置和管理云资源。"
---

# Terraform 基础设施

＃＃ 目录

- [概述](#概述)
- [何时使用](#when-to-use)
- [快速启动](#quick-start)
- [参考指南](#reference-guides)
- [最佳实践](#best-practices)

＃＃ 概述

使用 Terraform 构建可扩展的基础设施即代码，通过声明性配置、远程状态和自动配置来管理 AWS、Azure、GCP 和本地资源。

## 何时使用

- 云基础设施配置
- 多环境管理（开发、登台、生产）
- 基础设施版本控制和代码审查
- 成本跟踪和资源优化
- 灾难恢复和环境复制
- 自动化基础设施测试
- 跨区域部署

## 快速入门

最小工作示例：

```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state configuration
  backend "s3" {
    bucket         = "terraform-state-prod"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
// ... (see reference guides for full implementation)
```

## 参考指南

详细实现在`references/`目录中：

|指南|内容 |
|---|---|
| [AWS 基础设施模块](references/aws-infrastruct-module.md) | AWS 基础设施模块 |
| [变量和输出](references/variables-and-outputs.md) |变量和输出 |
| [Terraform 部署脚本](references/terraform-deployment-script.md) | Terraform 部署脚本 |

## 最佳实践

### ✅ 做

- 使用远程状态（S3、Terraform Cloud）
- 实施状态锁定（DynamoDB）
- 将代码组织成模块
- 使用工作空间作为环境
- 一致地应用标签
- 使用变量来提高灵活性
- 申请前实施代码审查
- 将敏感数据保存在单独的变量文件中

### ❌不要

- 将状态文件存储在本地 git 中
- 使用硬编码值
- 单一状态下的混合环境
- 跳过地形计划审查
- 一切都使用根模块
- 将秘密存储在代码中
- 禁用状态锁定
