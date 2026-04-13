# 技能全景文档

> 最后更新：2026年4月8日
> 技能总数：99 个（已从 290+ 精简清理）
> 插件数量：8 个（已清理重复）

---

## 一、技能分类总览

### 📂 分类索引

| 分类 | 技能数量 | 说明 |
|------|---------|------|
| 🔧 **开发核心** | 18 | 编码、调试、测试、代码审查等核心开发技能 |
| 🏗️ **架构与设计** | 6 | 系统设计、API 设计、前端设计等 |
| 🗄️ **数据库与数据工程** | 5 | SQL 查询、数据库优化、数据管道等 |
| 🐳 **DevOps 与基础设施** | 5 | Docker、K8s、Terraform、CI/CD 等 |
| 🧠 **AI 代理系统** | 12 | 代理自主、自我改进、记忆系统等 |
| 🔍 **搜索与研究** | 5 | 深度调研、文件搜索、超级搜索等 |
| 🌐 **浏览器与桌面控制** | 4 | 浏览器自动化、桌面控制等 |
| 🔐 **安全** | 5 | 安全审计、技能审查等 |
| 📝 **文档与工具** | 8 | 文档生成、Markdown、翻译等 |
| 🎨 **AI 生成** | 2 | AI 图像生成等 |
| 💼 **技能管理** | 5 | 技能发现、安装、推荐等 |
| ⚙️ **系统配置** | 6 | OpenClaw 配置、定时任务等 |
| 🔌 **区块链** | 2 | Web3 开发 |
| 🧪 **机器学习** | 2 | 深度学习、ML 工程 |
| 📊 **其他工具** | 14 | 各种实用工具 |

---

## 二、各分类详细说明

---

### 🔧 一、开发核心（18 个）

核心编程相关技能，覆盖编码全流程。

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **code** | 1.0.4 | 编码工作流：规划、实施、验证、测试 | 标准化编码流程，覆盖完整开发周期 | 较为通用，缺少特定框架深度指导 | 日常编码任务 |
| **senior-frontend** | - | React/Next.js/TypeScript/Tailwind 前端开发 | 覆盖现代前端技术栈，生产级标准 | 仅限前端，不包含后端 | React/Next.js 项目 |
| **debug-pro** | 1.0.0 | 系统调试方法和特定语言调试命令 | 跨语言调试，系统化调试方法论 | 需要手动执行调试命令 | 排查 bug、定位问题 |
| **test-runner** | 1.0.0 | 跨语言和框架编写和运行测试 | 支持 Vitest/Jest/pytest/Playwright | 测试框架配置需要手动处理 | 编写和运行单元测试 |
| **code-review-quality** | - | 上下文导向的代码审查 | 关注质量/可测试性/可维护性 | 不如专业工具（如 CodeRabbit）自动化 | 代码审查、PR 评审 |
| **git-essentials** | 1.0.0 | 基本 Git 命令和工作流 | 版本控制、分支管理 | 基础功能，不包含高级 Git 技巧 | 日常 Git 操作 |
| **github** | 1.0.0 | 通过 gh CLI 与 GitHub 交互 | Issues/PRs/CI 管理一体化 | 需要安装 gh CLI | GitHub 项目管理 |
| **shell-script** | 1.0.0 | Shell 脚本编写与执行 | 自动化运维任务 | 仅限 Shell，不包含 Python 等 | 系统管理、自动化脚本 |
| **workflow-automation** | - | 自动执行重复开发任务 | npm 脚本/Makefile/GitHub Actions | 需要手动配置工作流 | 开发效率提升 |
| **opencode-controller** | 1.0.0 | 通过斜杠命令控制 Opencode | 会话/模型管理 | 仅限 Opencode 工具 | Opencode 用户 |
| **encore-frontend** | - | React/Next.js 连接 Encore.ts 后端 | 全栈连接方案 | 仅限 Encore.ts 框架 | Encore.ts 全栈项目 |
| **tmux** | 1.0.0 | 远程控制 tmux 会话 | 发送击键/抓取输出 | 仅限 Linux/WSL 环境 | 远程服务器管理 |
| **checklist** | 1.0.0 | 任务清单管理器 | 确保复杂任务不遗漏步骤 | 需要手动维护清单 | 复杂多步骤任务 |
| **executing-plans** | 0.1.0 | 执行书面实施计划 | 带审查检查点 | 较简单 | 按计划执行任务 |
| **planning-with-files** | 1.2.0 | Manus 风格基于文件规划 | 创建 task_plan/findings/progress | 文件较多可能混乱 | 复杂项目规划 |
| **writing-plans** | 0.1.0 | 编写多步骤任务规范/计划 | 结构化任务描述 | 较简单 | 任务规划 |
| **session-logs** | 1.0.0 | 搜索和分析会话日志 | 回顾历史对话 | 日志文件格式依赖 | 查找历史信息 |
| **clawdbot-filesystem** | 1.0.2 | 高级文件系统操作 | 列表/搜索/批处理/目录分析 | 较底层 | 文件系统操作 |

**总结：** 开发核心是最高频使用的技能集合，覆盖编码→调试→测试→审查→版本控制全流程。

---

### 🏗️ 二、架构与设计（6 个）

系统架构和界面设计相关技能。

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **architecture-designer** | 0.1.0 | 系统设计、架构审查、设计模式、ADR | 覆盖完整架构设计流程 | 需要丰富的架构经验配合 | 新项目架构设计 |
| **api-design** | - | 设计 RESTful 和 GraphQL API | OpenAPI 规范支持 | 仅限 API 层 | 新 API 设计 |
| **rest-api-design** | - | REST API 设计规范 | 标准化 API 设计 | 与 api-design 有重叠 | RESTful API |
| **frontend-design-3** | 0.1.0 | 创建高设计质量前端界面 | 设计导向，美观现代 | 仅限前端 UI | 前端页面设计 |
| **superdesign** | 1.0.0 | 创建美观现代 UI 的前端设计指南 | 避免 AI 通用美学 | 指导性而非自动化 | UI 设计优化 |
| **data-visualization** | - | 数据可视化专家 | 图表选择/色彩理论/数据叙事 | 需要数据准备 | 数据展示、仪表板 |

**总结：** 架构类技能适合项目初期使用，设计类技能适合前端开发配合使用。

---

### 🗄️ 三、数据库与数据工程（5 个）

数据库查询、优化和数据管道。

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **sql-queries** | - | 跨所有主流数据仓库编写高性能 SQL | Snowflake/BigQuery/PostgreSQL 等 | 需要数据库访问权限 | 数据查询分析 |
| **database-query-optimization** | - | 数据库查询性能优化 | 慢查询优化、索引建议 | 需要 EXPLAIN 分析能力 | 慢 SQL 优化 |
| **supabase-postgres-best-practices** | 1.1.0 | Supabase Postgres 最佳实践 | 性能优化和最佳实践 | 仅限 Supabase/Postgres | Supabase 项目 |
| **data-engineering-data-pipeline** | - | 数据管道架构 | 批处理和流数据处理 | 需要大数据经验 | ETL 管道设计 |
| **analysis-data** | 1.0.0 | 数据分析 | 通用数据分析 | 较通用 | 数据分析任务 |

**总结：** 数据库技能适合数据驱动项目，SQL 和查询优化最常用。

---

### 🐳 四、DevOps 与基础设施（5 个）

容器化、编排和基础设施即代码。

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **docker-containerization** | - | 创建优化的 Docker 容器 | 多阶段构建、最佳实践 | 需要 Docker 基础 | 容器化应用 |
| **kubernetes-deployment** | - | K8s 部署和管理 | 生产级 K8s 配置 | 学习曲线陡峭 | K8s 集群部署 |
| **terraform-infrastructure** | - | Terraform 基础设施即代码 | 多云支持、版本控制 | 需要云账号配置 | 云基础设施 |
| **cicd-pipeline-setup** | - | CI/CD 流水线设置 | GitHub Actions/自动化部署 | 需要仓库配置 | 自动化构建部署 |
| **automation-workflows** | 0.1.0 | 设计自动化工作流 | 跨工具构建 | 较通用 | 工作流自动化 |

**总结：** DevOps 技能适合有运维需求的团队，Docker 最常用，K8s/Terraform 适合大型项目。

---

### 🧠 五、AI 代理系统（12 个）⭐

**最重要的技能类别** —— 让 Agent 自主进化和改进。

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **proactive-agent** | 3.0.0 | AI 代理从任务执行者变为主动合作伙伴 | 心跳期间主动工作，无需等待指令 | 配置较复杂 | 核心代理系统 |
| **proactive-tasks** | - | 主动目标/任务管理 | 心跳期间主动推进任务 | 与 proactive-agent 有重叠 | 任务自主管理 |
| **agent-autonomy-kit** | 1.0.0 | Agent 自主运行工具包 | 心跳期间自动工作，无需等待提示 | 较底层 | 代理自主性 |
| **self-driven** | 0.1.0 | AI 自我驱动闭环 | 不用人催自己找事做 | 实验性质 | 自主工作 |
| **capability-evolver** | 1.27.3 | AI 代理自我进化引擎 | 分析运行时历史识别改进 | 需要 EvoMap 注册 | 代理能力进化 |
| **evolver** | 1.27.3 | AI 代理自我进化引擎 | 与 capability-evolver 类似 | 功能重叠 | 代理进化 |
| **self-improving** | 1.2.12 | 自我反思+批评+学习+组织记忆 | 持续改进机制 | 需要记忆系统配合 | 自我改进 |
| **self-reflection** | 1.1.1 | 通过结构化反思不断自我完善 | 心跳期间定期反思 | 较简单 | 自我反思 |
| **agent-self-reflection** | 1.0.0 | 定期自我反思 | 分析进展与问题，写入工作区文件 | 与 self-reflection 重叠 | 定期反思 |
| **claw-self-improving-plus** | 1.0.2 | 将错误转化为结构化学习 | 保守自我改进工作流 | 审批制进化 | 经验积累 |
| **agent-guardian** | 1.0.0 | Agent 体验守护系统 | 解决无响应/卡死/中英文混用 | 监控性质 | 代理体验保障 |
| **context-compression** | - | 压缩上下文、减少令牌使用 | 结构化摘要、节省 60-80% 令牌 | 需要手动触发 | 长对话压缩 |

**总结：** 这是让 Agent"活起来"的核心技能群。proactive-agent + self-improving + capability-evolver 是黄金组合。

---

### 🧠 六、记忆系统（4 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **agent-memory** | 1.0.0 | 持久内存系统 | 记住事实、跨会话跟踪 | 基础功能 | 通用记忆 |
| **elite-longterm-memory** | 1.2.3 | 终极记忆系统 | WAL 协议+向量搜索+git-notes+云端备份 | 配置复杂 | 长期记忆 |
| **memory** | 1.0.2 | 无限组织内存 | 补充代理内置内存 | 较简单 | 补充记忆 |
| **memory-merger** | - | 合并成熟经验到指令文件 | 知识沉淀自动化 | 需要手动触发 | 经验固化 |

---

### 🔍 七、搜索与研究（5 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **deep-research-pro** | 1.0.2 | 多源深度调研 | 无需 API 密钥，生成引用报告 | 需要 DuckDuckGo 访问 | 深度调研 |
| **cellcog** | 1.0.21 | Any-to-Any AI 深度推理 | 多模态、多 Agent 编排 | 较重 | 复杂研究 |
| **file-search** | 1.0.0 | 快速文件名和内容搜索 | fd + ripgrep，极速 | 仅限本地文件 | 查找文件 |
| **qmd** | 1.0.0 | 本地语义搜索 | BM25+向量+rerank | 需要索引构建 | 语义搜索代码 |
| **super-search** | - | 搜索编码记忆 | 回忆以前会话信息 | 依赖记忆系统 | 查找历史工作 |

---

### 🌐 八、浏览器与桌面控制（4 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **browser-use** | 1.0.2 | 浏览器自动化 | 浏览网页/填表/截图/抓取 | 需要 Chrome/Chromium | 网页自动化 |
| **fast-browser-use** | - | 快速浏览器自动化 | 更快的执行速度 | 功能较少 | 快速网页操作 |
| **agent-browser** | 0.2.0 | 基于 Rust 的快速无头浏览器 | 结构化命令输出 | 较新，可能不稳定 | 无头浏览器场景 |
| **desktop-control** | 1.0.0 | 完整 Windows 桌面控制 | 鼠标/键盘/截图 | 仅限 Windows | 桌面应用自动化 |
| **windows-control** | 1.0.0 | Windows 桌面控制 | 与 desktop-control 类似 | 功能重叠 | Windows 自动化 |

---

### 🔐 九、安全（5 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **aliyun-clawscan** | 1.0.0 | OpenClaw 安全态势分析 | 扫描环境和技能安全 | 仅限 OpenClaw | 安全审计 |
| **clawdefender** | 1 | 安全扫描器 | 检测提示注入/命令注入/SSRF | 被动检测 | 安全防护 |
| **openclaw-security-suite** | 0.2.3 | AST 静态扫描+语义行为审查 | 深度安全分析 | 较重 | 全面安全检查 |
| **skill-vetter** | 1.0.0 | Skill 安全第一审查 | 检查危险信号/权限 | 安装前使用 | 技能安全审查 |
| **skill-vetting** | 1.1.0 | ClawHub 技能审核 | 安全性和实用性评估 | 与 skill-vetter 重叠 | 技能安装前审核 |
| **skillshieldskill** | 1.0.0 | AI Agent 技能安全扫描 | 检测恶意技能 | 额外开销 | 技能生态安全 |
| **security-auditor** | 1.0.0 | OWASP Top 10/SQL 注入防护 | 标准安全审计 | 仅限代码层面 | 代码安全检查 |

---

### 📝 十、文档与工具（8 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **docs-generator** | 1.0.0 | 自动文档生成 | API docs/README/CHANGELOG | 需要代码变更触发 | 项目文档 |
| **docx** | - | 创建/读取/编辑 Word 文档 | .docx 格式支持 | 仅限 Word | Word 文档处理 |
| **pptx** | - | 创建/编辑 PowerPoint | 演示文稿生成 | 格式可能不精确 | PPT 制作 |
| **markdown-linter-cli** | 1.0.0 | Markdown 格式检查 | 断链/样式一致性 | 仅检查不修复 | Markdown 维护 |
| **quick-translation** | 1.0.0 | 快速翻译工具 | 支持 100+ 语言 | 翻译质量依赖模型 | 跨语言任务 |
| **summarize** | 1.0.0 | 汇总 URL 或文件 | Web/PDF/音频/YouTube | 长内容可能丢失细节 | 内容摘要 |
| **model-usage** | 1.0.0 | 模型使用统计 | 成本/token 消耗统计 | 仅统计 | 成本监控 |
| **auto-updater** | 1.0.0 | 每日自动更新 | Clawdbot 和技能自动更新 | 可能引入不兼容更新 | 自动维护 |

---

### 🎨 十一、AI 生成（2 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **ai-image-generation** | - | 50+ 模型 AI 图像生成 | FLUX/Gemini/Grok 等，文生图/图生图/LoRA | 需要 API 密钥 | AI 艺术创作 |

---

### 💼 十二、技能管理（5 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **clawdhub** | 1.0.0 | ClawHub 技能市场 CLI | 搜索/安装/发布技能 | 需要网络 | 技能管理 |
| **skills-finder** | 1.6.0 | 智能技能匹配 | 搜索多个市场 | 与 clawdhub 有重叠 | 技能发现 |
| **find-skills** | - | 发现并安装代理技能 | 基础技能发现 | 功能较简单 | 技能搜索 |
| **find-skills-v2** | 1.0.0 | 智能技能匹配 V2 | 多市场搜索 | 与 skills-finder 重叠 | 技能发现 |
| **clawhub-recommender** | 1.0.0 | ClawHub 推荐器 | 推荐热门高评分技能 | 被动推荐 | 技能推荐 |
| **skill-creator-pro** | 1.0.0 | 创建/改进技能 | 评估驱动迭代 | 需要技能开发知识 | 自定义技能 |

---

### ⚙️ 十三、系统配置（6 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **openclaw-config** | - | OpenClaw 配置管理 | 通道/代理/安全配置 | 配置复杂 | OpenClaw 设置 |
| **easy-openclaw** | 1.0.0 | OpenClaw 配置优化向导 | 快速初始化/优化 | 向导性质 | 快速配置 |
| **openclaw-soul** | 1.1.0 | 自我进化框架 | 宪法/SOUL/心跳/PARA 记忆 | 框架性质 | Agent 性格定义 |
| **cron** | - | 定时任务调度 | 提醒和重复任务 | 基础 cron | 定时任务 |
| **cron-mastery** | 1.0.3 | Cron 定时精通 | Cron vs Heartbeat 理解 | 与 cron 重叠 | 高级定时任务 |
| **ping-me** | 1.0.2 | 自然语言提醒 | 自动检测渠道/时区 | 仅提醒 | 一次性提醒 |

---

### 🔌 十四、区块链（2 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **blockchain-developer** | - | Web3 应用/智能合约 | DeFi/NFT/DAO | 需要区块链知识 | Web3 开发 |
| **software-crypto-web3** | - | EVM/Solana/Cosmos/TON | 多链支持 | 学习曲线陡 | 区块链智能合约 |

---

### 🧪 十五、机器学习（2 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **deep-learning-pytorch** | - | PyTorch/Transformers/Diffusers | 深度学习/LLM 集成/RAG | 需要 GPU | AI 模型开发 |
| **senior-ml-engineer** | - | ML 工程/MLOps | 生产 ML/LLM 微调 | 需要 ML 基础 | ML 系统部署 |

---

### 📊 十六、其他工具（14 个）

| 技能名 | 版本 | 说明 | 优点 | 缺点 | 适用场景 |
|--------|------|------|------|------|---------|
| **1password** | 1.0.1 | 1Password 密码管理器集成 | 安全读取/注入密钥 | 需要 1Password 账号 | 密码管理 |
| **aethercore** | 3.3.4 | 高性能 JSON 优化 | 通用智能索引 | 性能优化性质 | JSON 处理 |
| **para-memory** | 1.0.0 | 3 层 PARA 内存系统 | 每日笔记/知识图 | 需要 PARA 方法论 | 知识管理 |
| **prompt-engineering-expert** | 1.0.0 | 提示工程专家 | 自定义指令设计 | 指导性 | 提示词优化 |
| **project-assistant** | 1.0.0 | 项目初始化与智能分析 | 项目结构分析 | 初始化性质 | 新项目启动 |
| **clawddocs** | 1.2.2 | Clawdbot 文档专家 | 决策树导航 | 仅限 Clawdbot | Clawdbot 使用 |
| **workspace-context-linter** | 1.0.0 | 诊断工作区上下文文件 | 减少膨胀/检测重复 | 诊断性质 | 上下文优化 |
| **openclaw-skills-web-search-plus** | 2.7.2 | 统一搜索技能 | 智能自动路由多搜索引擎 | 网络依赖 | 网络搜索 |
| **OpenClaw** | 2026.3.8 | OpenClaw 核心 | 核心框架 | 框架性质 | OpenClaw 使用 |
| **memory** | 1.0.2 | 无限组织内存 | 补充代理内置内存 | 与 agent-memory 重叠 | 记忆补充 |
| **checklist** | 1.0.0 | 任务清单管理 | 复杂任务不遗漏 | 需要手动维护 | 任务跟踪 |
| **focus-mind** | 1.0.0 | 专注力管理 | 提高工作效率 | 指导性 | 工作效率 |
| **imgcraft** | 1.1.0 | 获取公网 IP 信息 | 网络诊断 | 功能单一 | 网络诊断 |

---

## 三、插件清单

### 已安装插件（8 个）

| 插件名 | 来源 | 说明 | 状态 | 建议 |
|--------|------|------|------|------|
| **superpowers** | claude-plugins-official | TDD/调试/并行 Agent 分发等 14 个技能 | ✅ 保留 | 核心开发工作流 |
| **agent-skills** | addy-agent-skills | Addy Osmani 的 20 个 SDLC 技能 | ✅ 保留 | 高质量开发技能 |
| **code-review** | claude-plugins-official | PR 自动化代码审查（4 个并行 Agent） | ⚠️ 按需 | 需 GitHub CLI |
| **code-simplifier** | claude-plugins-official | 代码简化和重构 | ⚠️ 按需 | 与 agent-skills 重叠 |
| **coderabbit** | claude-plugins-official | CodeRabbit AI 代码审查 | ❌ 可移除 | 需 CodeRabbit 账号 |
| **plugin-dev** | claude-plugins-official | 插件开发工具包 | ⚠️ 按需 | 开发插件时需要 |
| **postman** | claude-plugins-official | Postman API 管理 | ❌ 可移除 | 需 Postman API Key |
| **ralph-loop** | claude-plugins-official | 持续自引用迭代开发循环 | ❌ 可移除 | 实验性质 |

### 已删除插件（2 个）

| 插件名 | 删除原因 | 替代者 |
|--------|---------|--------|
| skill-creator | 功能被替代 | skill-creator-pro（更强版本） |
| frontend-design | 功能重复 | skills 目录中的 frontend-design-3 |

---

## 四、清理记录

### 本次清理删除的技能（约 190 个）

#### 1. 重复版本删除（17 个）
- clawdhub（无版本）→ 保留 clawdhub-1.0.0
- find-skills-0.1.0 → 保留 find-skills / find-skills-v2
- frontend-design → 保留 frontend-design-3
- elite-memory-skill → 保留 elite-longterm-memory
- cron-mastery（旧版）→ 保留 cron-mastery-1.0.3
- github-1 → 保留 github-1.0.0
- openai-whisper（旧版）→ 保留 openai-whisper-1.0.0
- self-improving-1.1.3 → 保留 self-improving-1.2.12
- self-improving-agent → 保留 self-improving-agent-3.0.1
- ui-ux-pro-max-0.1.0 → 保留 ui-ux-pro-max
- pdf → 与 nano-pdf 重叠
- xlsx → 与 excel-xlsx 重叠
- videotranscript → 与 video-transcript 重叠
- skill-creator-0.1.0 → 保留 skill-creator-pro
- proactive-agent-3.1.0 → 保留 proactive-agent
- proactive-agent-lite → 与 proactive-agent 重叠
- proactive-agent-v2 → 与 proactive-agent 重叠

#### 2. GSD 系列（70+ 个细分项目管理技能）
全部删除，功能过度细分且重叠。

#### 3. 个人定制技能（16 个）
- kimi-claw-sanqian-*（4 个）
- xixi-fengche-*（6 个）
- investment-advisor-zhang-*（2 个）
- harry-skill-evolver
- autoglm-*（9 个）
- xcrawl-*（4 个）

#### 4. 编程不相关技能（37 个）
- 天气、股票分析、淘宝客、社交媒体、营销、日历、日记、闪卡、阅读清单、面试设计、心理、YouTube、TTS、语音、笔记、 discord-bot、Google Sheets 等

#### 5. 其他不常用（40+ 个）
- 新闻聚合、Reddit、广告、学术深度研究、飞书部分技能、视频帧提取、本地语音、Pinokio、Pollinations AI、Vercel 部署、Cursor Agent、Gemini 等

---

## 五、推荐使用策略

### 🏆 核心技能群（建议始终加载）
```
code, senior-frontend, debug-pro, test-runner, git-essentials, github,
proactive-agent, self-improving, agent-memory, browser-use, file-search
```

### 📦 按项目类型加载

**Web 全栈项目：**
```
code, senior-frontend, senior-ml-engineer, sql-queries, docker-containerization,
api-design, architecture-designer, cicd-pipeline-setup
```

**AI/研究项目：**
```
deep-research-pro, cellcog, deep-learning-pytorch, prompt-engineering-expert,
summarize, super-search
```

**DevOps/基础设施：**
```
docker-containerization, kubernetes-deployment, terraform-infrastructure,
cicd-pipeline-setup, automation-workflows, shell-script
```

**自主 Agent 配置：**
```
proactive-agent, capability-evolver, self-improving, agent-memory,
elite-longterm-memory, agent-guardian, context-compression
```

---

## 六、技能依赖关系图

```
proactive-agent
    ├── agent-autonomy-kit
    ├── agent-guardian
    └── self-improving
            ├── agent-memory
            │       └── elite-longterm-memory
            │               └── memory-merger
            └── self-reflection
                    └── agent-self-reflection

code
    ├── debug-pro
    ├── test-runner
    ├── code-review-quality
    └── git-essentials
            └── github

deep-research-pro
    ├── cellcog
    ├── super-search
    └── file-search

docker-containerization
    ├── kubernetes-deployment
    └── cicd-pipeline-setup
            └── terraform-infrastructure
```

---

## 七、维护建议

1. **定期检查更新**：使用 `auto-updater` 技能每天自动检查更新
2. **安全审查**：安装新技能前使用 `skill-vetting` 或 `skill-vetter` 审查
3. **记忆管理**：定期使用 `memory-merger` 合并成熟经验到指令文件
4. **上下文优化**：对话过长时使用 `context-compression` 压缩历史
5. **不要过度安装**：技能越多，上下文开销越大，保持精简

---

> 💡 **提示**：本文档由 AI 自动生成和维护，如有变更请同步更新。
