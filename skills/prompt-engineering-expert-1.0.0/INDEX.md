# 快速工程专家技能 - 完整索引

## 📋 快速导航

### 入门
- **[README.md](README.md)** - 从这里开始！概述、使用方法和快速入门指南
- **[SUMMARY.md](SUMMARY.md)** - 创建了什么以及如何使用它

### 核心技能文件
- **[SKILL.md](SKILL.md)** - 技能元数据和功能概述
- **[CLAUDE.md](CLAUDE.md)** - 主要技能说明和专业领域

### 文档
- **[docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md)** - 综合最佳实践指南
- **[docs/TECHNIQUES.md](docs/TECHNIQUES.md)** - 高级提示工程技术
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - 常见问题和解决方案

### 示例和模板
- **[examples/EXAMPLES.md](examples/EXAMPLES.md)** - 10 个真实示例和模板

---

## 📚 包含什么

### 专业领域（7大领域）
1. 即时写作最佳实践
2. 先进的快速工程技术
3. 自定义指令及系统提示
4. 及时优化完善
5. 反模式和常见错误
6. 评估与测试
7. 多模式和高级提示

### 关键功能（8 项功能）
1. 及时分析
2. 提示生成
3. 及时完善
4. 定制指令设计
5. 最佳实践指南
6. 反模式识别
7. 测试策略
8. 文档

### 用例（9 个用例）
1. 细化模糊或无效的提示
2. 创建专门的系统提示
3. 为代理设计定制指令
4. 优化一致性和可靠性
5. 教授提示工程最佳实践
6.调试提示性能问题
7. 为工作流程创建提示模板
8. 提高效率和代币使用
9. 制定评估框架

---

## 🎯 如何使用此技能

### 用于即时分析
```
"Review this prompt and suggest improvements:
[YOUR PROMPT]

Focus on: clarity, specificity, format, and consistency."
```

### 用于提示生成
```
"Create a prompt that:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

The prompt should handle [use cases]."
```

### 自定义说明
```
"Design custom instructions for an agent that:
- [Role/expertise]
- [Key responsibilities]
- [Behavioral guidelines]"
```

### 用于故障排除
```
"This prompt isn't working well:
[PROMPT]

Issues: [DESCRIBE ISSUES]

How can I fix it?"
```

---

## 📖 文档结构

### BEST_PRACTICES.md（综合指南）
- 核心原则（清晰、简洁、自由度）
- 先进技术（CoT、few-shot、XML、基于角色、预填充、链接）
- 定制说明设计
- 技能结构最佳实践
- 评估和测试框架
- 要避免的反模式
- 工作流程和反馈循环
- 内容指南
- 多模式提示
- 开发工作流程
- 完整的清单

### TECHNIQUES.md（高级方法）
- 通过示例进行思路提示
- Few-Shot 学习（1-shot、2-shot、multi-shot）
- 带有 XML 标签的结构化输出
- 基于角色的提示
- 预填回复
- 提示链接
- 上下文管理
- 多模式提示
- 组合技术
- 反模式

### TROUBLESHOOTING.md（问题解决）
- 8 个常见问题及其解决方案
- 调试工作流程
- 快速参考表
- 测试清单

### Examples.md（真实案例）
- 10个实际例子
- 之前/之后的比较
- 模板和框架
- 优化清单

---

## ✅ 最佳实践总结

### 要做的 ✅
- 清晰具体
- 提供例子
- 指定格式
- 定义约束
- 彻底测试
- 记录假设
- 使用渐进式披露
- 处理边缘情况

### 不该做的事❌
- Be vague or ambiguous
- 假设理解
- 跳过格式规范
- 忽略边缘情况
- 过度指定约束
- 使用行话而不解释
- 硬编码值
- 忽略错误处理

---

## 🚀 开始使用

### 第 1 步：阅读概述
从 **README.md** 开始了解此技能提供的内容。

### Step 2: Learn Best Practices
查看 **docs/BEST_PRACTICES.md** 了解基础知识。

### 第 3 步：探索示例
检查 **examples/EXAMPLES.md** 了解实际用例。

### 第 4 步：尝试一下
分享您的提示或描述您的开始需求。

### 第 5 步：排除故障
如果遇到问题，请使用 **docs/TROUBLESHOOTING.md**。

---

## 🔧 高级主题

### 思路提示
鼓励对复杂任务进行逐步推理。
→ 请参阅：TECHNIQUES.md，第 1 节

### 少样本学习
在没有明确指示的情况下，使用示例来指导行为。
→ 请参阅：TECHNIQUES.md，第 2 节

### 结构化输出
为了清晰和解析使用 XML 标签。
→ 请参阅：TECHNIQUES.md，第 3 节

### 基于角色的提示
分配专业知识来指导行为。
→ 请参阅：TECHNIQUES.md，第 4 节

### 提示链接
将复杂的任务分解为连续的提示。
→ 请参阅：TECHNIQUES.md，第 6 节

### 上下文管理
优化令牌使用和清晰度。
→ 请参阅：TECHNIQUES.md，第 7 节

### 多模式整合
处理图像、文件和嵌入。
→ 请参阅：TECHNIQUES.md，第 8 节

---

## 📊 文件结构

```
prompt-engineering-expert/
├── INDEX.md                    # This file
├── SUMMARY.md                  # What was created
├── README.md                   # User guide & getting started
├── SKILL.md                    # Skill metadata
├── CLAUDE.md                   # Main instructions
├── docs/
│   ├── BEST_PRACTICES.md       # Best practices guide
│   ├── TECHNIQUES.md           # Advanced techniques
│   └── TROUBLESHOOTING.md      # Common issues & solutions
└── examples/
    └── EXAMPLES.md             # Real-world examples
```

---

## 🎓 学习路径

### 初学者
1.阅读：README.md
2. 阅读：BEST_PRACTICES.md（核心原则部分）
3. 回顾：EXAMPLES.md（示例 1-3）
4. 尝试：创建一个简单的提示

### 中级
1. 阅读：TECHNIQUES.md（第 1-4 节）
2. 复习：EXAMPLES.md（示例 4-7）
3. 阅读：故障排除.md
4. 尝试：优化现有提示

### 高级
1. 阅读：TECHNIQUES.md（第 5-8 节）
2. 复习：EXAMPLES.md（示例 8-10）
3. 阅读：BEST_PRACTICES.md（高级部分）
4.尝试：结合多种技术

---

## 🔗 整合点

该技能适用于：
- **Claude Code** - 用于测试和迭代提示
- **代理 SDK** - 用于实施自定义指令
- **文件 API** - 用于分析提示文档
- **愿景** - 用于多模式提示设计
- **扩展思维** - 用于复杂的提示推理

---

## 📝 关键概念

### 清晰度
- 明确的目标
- 精确的语言
- 具体例子
- 逻辑结构

### 简洁
- 重点内容
- 无冗余
- 渐进式披露
- 代币效率

### 一致性
- 定义的约束
- 指定格式
- 明确的指导方针
- 可重复的结果

### 完整性
- 足够的背景
- 边缘情况处理
- 成功标准
- 错误处理

---

## ⚠️ 限制

- **仅分析**：不执行代码或运行实际提示
- **无实时数据**：无法访问外部 API 或当前数据
- **基于最佳实践**：基于既定模式的建议
- **需要测试**：建议应通过实际用例进行验证
- **人类判断**：不会取代关键应用中的人类专业知识

---

## 🎯 常见用例

### 1. 完善模糊提示
将不明确的提示转化为具体的、可操作的提示。
→ 请参阅：EXAMPLES.md，示例 1

### 2. 创建专门的提示
为特定领域或任务设计提示。
→ 请参阅：EXAMPLES.md，示例 2

### 3.设计代理指令
为 AI 代理和技能创建自定义指令。
→ 请参阅：EXAMPLES.md，示例 2

### 4. 优化一致性
提高可靠性并减少变异性。
→ 请参阅：BEST_PRACTICES.md，技能结构部分

### 5.调试提示问题
识别并修复现有提示的问题。
→ 请参阅：故障排除.md

### 6. 教学最佳实践
学习及时的工程原理和技术。
→ 请参阅：BEST_PRACTICES.md、TECHNIQUES.md

### 7. 构建评估框架
开发测试用例和成功标准。
→ 请参阅：BEST_PRACTICES.md，评估和测试部分

### 8. 多模式提示
视觉、嵌入和文件的设计提示。
→ 请参阅：TECHNIQUES.md，第 8 节

---

## 📞 支持和资源

### Within This Skill
- 详细的文档
- 现实世界的例子
- 故障排除指南
- 最佳实践清单
- 快速参考表

### 外部资源
- 克劳德文档：https://docs.claude.com
- 人类博客：https://www.anthropic.com/blog
- 克劳德食谱：https://github.com/anthropics/claude-cookbooks
- 提示工程指南：https://www.promptingguide.ai

---

## 🚀 后续步骤

1. **探索文档** - 从 README.md 开始
2. **查看示例** - 检查示例/EXAMPLES.md
3. **尝试一下** - 分享您的提示或描述您的需求
4. **迭代** - 使用反馈来改进
5. **分享** - 帮助其他人完成提示

---

**准备好掌握提示工程了吗？** 从 [README.md](README.md) 开始！
