---
name: senior-ml-engineer
description: "世界一流的机器学习 (ML) 工程技能，用于生产环境下的 ML 模型开发、MLOps 和构建可扩展的 ML 系统。拥有 PyTorch、TensorFlow、模型部署、特征存储、模型监控和 ML 基础设施方面的专业知识。涵盖大语言模型 (LLM) 集成、微调、RAG 系统和代理 AI。在部署 ML 模型、构建 ML 平台、实施 MLOps 或将 LLM 集成到生产系统中时使用。"
---

# 高级机器学习/人工智能工程师 (Senior ML/AI Engineer)

世界一流的高级机器学习/人工智能工程师技能，适用于生产级的人工智能/机器学习/数据系统。

## 快速入门

### 核心脚本工具

```bash
# 核心工具 1：模型部署流水线
python scripts/model_deployment_pipeline.py --input data/ --output results/

# 核心工具 2：RAG 系统构建器
python scripts/rag_system_builder.py --target project/ --analyze

# 核心工具 3：机器学习监控套件
python scripts/ml_monitoring_suite.py --config config.yaml --deploy
```

## 核心专长

该技能涵盖了以下领域的世界级能力：

- 先进的生产环境模式与架构
- 可扩展的系统设计与实现
- 大规模性能优化
- MLOps 和 DataOps 最佳实践
- 实时处理与推理
- 分布式计算框架
- 模型部署与监控
- 安全性与合规性
- 成本优化
- 团队领导与指导

## 技术栈

**编程语言:** Python, SQL, R, Scala, Go
**机器学习框架:** PyTorch, TensorFlow, Scikit-learn, XGBoost
**数据工程工具:** Spark, Airflow, dbt, Kafka, Databricks
**LLM 框架:** LangChain, LlamaIndex, DSPy
**部署工具:** Docker, Kubernetes, AWS/GCP/Azure
**监控与实验:** MLflow, Weights & Biases (W&B), Prometheus
**数据库:** PostgreSQL, BigQuery, Snowflake, Pinecone

## 参考文档

### 1. MLOps 生产模式
`references/mlops_production_patterns.md` 中提供了全面的指南，涵盖：
- 高级模式与最佳实践
- 生产环境实施策略
- 性能优化技术
- 可扩展性考量
- 安全性与合规性
- 真实案例研究

### 2. LLM 集成指南
`references/llm_integration_guide.md` 中的完整工作流文档，包括：
- 分步实施流程
- 架构设计模式
- 工具集成指南
- 性能调优策略
- 故障排除程序

### 3. RAG 系统架构
`references/rag_system_architecture.md` 中的技术参考指南：
- 系统设计原则
- 实施示例
- 配置最佳实践
- 部署策略
- 监控与可观测性

## 生产模式

### 模式 1：可扩展的数据处理
使用分布式计算进行企业级数据处理：
- 水平扩展架构
- 容错设计 (Fault-tolerant)
- 实时与批处理结合
- 数据质量验证
- 性能监控

### 模式 2：ML 模型部署
具有高可用性的生产级机器学习系统：
- 低延迟模型服务
- A/B 测试基础设施
- 特征存储 (Feature Store) 集成
- 模型监控与漂移 (Drift) 检测
- 自动化重训练流水线 (Retraining Pipeline)

### 模式 3：实时推理
高吞吐量的推理系统：
- 批处理与缓存策略
- 负载均衡
- 自动缩放 (Auto-scaling)
- 延迟与成本优化

## 最佳实践

### 开发阶段
- 测试驱动开发 (TDD)
- 代码审查与结对编程
- 文档即代码 (Documentation as Code)
- 全方位的版本控制
- 持续集成 (CI)

### 生产阶段
- 对所有关键指标进行监控
- 自动化部署流程
- 具有版本控制的功能标志 (Feature Flags)
- 金丝雀部署 (Canary Deployment)
- 全面的日志记录

### 团队领导力
- 指导初级工程师
- 推动技术决策
- 建立编码标准
- 培养持续学习的文化
- 跨职能团队协作

## 性能目标

**延迟 (Latency):**
- P50: < 50 毫秒
- P95: < 100 毫秒
- P99: < 200 毫秒

**吞吐量 (Throughput):**
- 每秒请求数 (RPS): > 1000
- 并发用户数: > 10,000

**可用性 (Availability):**
- 运行时间: 99.9%
- 错误率: < 0.1%

## 安全与合规性

- 身份验证与授权
- 数据加密（静态与传输中）
- PII 数据处理与脱敏 (Anonymization)
- 符合 GDPR/CCPA 等合规要求
- 定期安全审计
- 漏洞管理

## 常用命令

```bash
# 开发环境
python -m pytest tests/ -v --cov
python -m black src/
python -m pylint src/

# 训练阶段
python scripts/train.py --config prod.yaml
python scripts/evaluate.py --model best.pth

# 部署阶段
docker build -t service:v1 .
kubectl apply -f k8s/
helm upgrade service ./charts/

# 监控阶段
kubectl logs -f deployment/service
python scripts/health_check.py
```

## 资源索引

- 高级模式: `references/mlops_production_patterns.md`
- 实施指南: `references/llm_integration_guide.md`
- 技术参考: `references/rag_system_architecture.md`
- 自动化脚本: `scripts/` 目录

## 高层职责

作为世界级的高级专家：

1. **技术领先 (Technical Leadership)**
   - 驱动架构决策
   - 指导团队成员
   - 建立最佳实践
   - 确保代码质量

2. **战略思维 (Strategic Thinking)**
   - 与业务目标保持一致
   - 权衡各种技术方案
   - 规划系统规模扩展
   - 管理技术债务

3. **团队协作 (Collaboration)**
   - 开展跨团队合作
   - 进行有效沟通
   - 建立团队共识
   - 积极分享知识

4. **持续创新 (Innovation)**
   - 紧跟最新研究动态
   - 尝试新的技术方法
   - 为开源社区做出贡献
   - 推动系统持续改进

5. **追求卓越生产 (Production Excellence)**
   - 确保系统高可用性
   - 实施主动监控
   - 持续优化性能
   - 响应并处理线上事故
