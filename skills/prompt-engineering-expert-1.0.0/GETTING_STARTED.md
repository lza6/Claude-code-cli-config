# 如何使用这种快速的工程专家技能

## 📦 你拥有什么

完整的克劳德技能可提供快速的工程专业知识，位于：
```
~/Documents/prompt-engineering-expert/
```

## 🚀 如何上传和使用

### 选项 1：通过 Claude.com 上传（最简单）

1. **访问 Claude.com** 并开始对话
2. **Click the "+" button** next to the message input
3. **选择“上传技能”**
4. **Choose the skill folder**: `~/Documents/prompt-engineering-expert/`
5. **Claude will load the skill** and you can start using it

### 选项 2：通过 Claude Code 上传

1. **在 Claude.com 中打开 Claude 代码**
2. **创建一个新项目**
3. **上传技能文件夹**到您的项目
4. **在提示中引用技能**

### 选项 3：与 Agent SDK 一起使用（编程）

```python
from anthropic import Anthropic

client = Anthropic()

# Load the skill
skill_path = "~/Documents/prompt-engineering-expert"

# Use in your agent
response = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=2048,
    system=f"You have access to the prompt engineering expert skill at {skill_path}",
    messages=[
        {
            "role": "user",
            "content": "Review this prompt and suggest improvements: [PROMPT]"
        }
    ]
)
```

## 💡 如何使用技能

### 基本用法

上传后，您可以询问Claude：

```
"Review this prompt and suggest improvements:
[YOUR PROMPT]"
```

### 高级用法

```
"Using your prompt engineering expertise:
1. Analyze this prompt: [PROMPT]
2. Identify issues
3. Suggest specific improvements
4. Provide a refined version
5. Explain what changed and why"
```

### 自定义说明

```
"Design custom instructions for an agent that:
- Analyzes customer feedback
- Extracts key themes
- Generates recommendations
- Outputs structured JSON"
```

### 用于故障排除

```
"This prompt isn't working:
[PROMPT]

Issues I'm seeing:
- [ISSUE 1]
- [ISSUE 2]

How can I fix it?"
```

## 📚 技能内容

### 核心文件
- **SKILL.md** - 元数据和概述
- **CLAUDE.md** - 主要说明
- **README.md** - 用户指南

### 文档
- **docs/BEST_PRACTICES.md** - 最佳实践指南
- **docs/TECHNIQUES.md** - 高级技术
- **docs/TROUBLESHOOTING.md** - 常见问题

### 示例
- **examples/EXAMPLES.md** - 真实示例

### 导航
- **INDEX.md** - 完整的索引和导航
- **SUMMARY.md** - 创建了什么

## 🎯 快速入门示例

### 示例 1：分析提示
```
"Analyze this prompt for clarity and effectiveness:

'Summarize this article'

What could be improved?"
```

### 示例 2：生成提示
```
"Create a prompt for analyzing customer support tickets.
The prompt should:
- Classify tickets by category
- Extract key issues
- Suggest responses
- Output as JSON"
```

### 示例 3：优化指令
```
"I'm creating a custom instruction for an AI agent.
Here's my draft:

[YOUR DRAFT]

Please improve it using prompt engineering best practices."
```

### 示例 4：故障排除
```
"My prompt keeps producing inconsistent results.
Here's the prompt:

[YOUR PROMPT]

What's wrong and how do I fix it?"
```

## 📖 文档指南

### 对于初学者
1.从**README.md**开始
2.阅读**docs/BEST_PRACTICES.md**（核心原则）
3. 查看 **examples/EXAMPLES.md** （示例 1-3）

### 对于中级用户
1. 阅读 **docs/TECHNIQUES.md**（第 1-4 节）
2. 查看**examples/EXAMPLES.md**（示例 4-7）
3. 根据需要使用**docs/TROUBLESHOOTING.md**

### 对于高级用户
1.学习**docs/TECHNIQUES.md**（所有部分）
2. 查看 **examples/EXAMPLES.md** （所有示例）
3. 结合多种技术

## ✨ 主要特点

### 专业领域
- 提示写作最佳实践
- 先进技术（CoT、few-shot、XML 等）
- 定制说明设计
- 及时优化
- 反模式识别
- 评估框架
- 多模式提示

### 能力
- 分析现有提示
- 生成新的提示
- 细化和优化
- 设计定制说明
- 教授最佳实践
- 识别问题
- 开发测试用例
- 创建文档

## 🔧 定制

### 添加特定于域的示例
编辑“examples/EXAMPLES.md”为您的域添加示例。

### 扩展最佳实践
将特定于域的最佳实践添加到“docs/BEST_PRACTICES.md”。

### 添加故障排除案例
将常见问题添加到“docs/TROUBLESHOOTING.md”。

## 📊 文件结构

```
prompt-engineering-expert/
├── INDEX.md                    # Navigation guide
├── SUMMARY.md                  # What was created
├── README.md                   # User guide
├── SKILL.md                    # Metadata
├── CLAUDE.md                   # Main instructions
├── docs/
│   ├── BEST_PRACTICES.md       # Best practices
│   ├── TECHNIQUES.md           # Advanced techniques
│   └── TROUBLESHOOTING.md      # Troubleshooting
└── examples/
    └── EXAMPLES.md             # Examples
```

## 🎓 学习资源

### 在技能范围内
- 全面的文档
- 现实世界的例子
- 最佳实践清单
- 故障排除指南
- 快速参考表

### 外部资源
- 克劳德文档：https://docs.claude.com
- 人类博客：https://www.anthropic.com/blog
- 克劳德食谱：https://github.com/anthropics/claude-cookbooks

## ⚡ 专业提示

1. **从简单开始** - 从基本提示开始，然后再进行高级技术
2. **使用示例** - 提供示例来指导 Claude 的回答
3. **具体** - 您的要求越具体，结果就越好
4. **彻底测试** - 始终用真实数据测试完善的提示
5. **迭代** - 利用反馈不断改进
6. **文档** - 记录适合您的用例的内容

## 🚀 后续步骤

1. **使用上述方法之一上传技能**
2. **尝试一个简单的例子**来熟悉它
3. **查看文档**以进行更深入的学习
4. **应用您的提示**并迭代
5. **与您的团队分享**以促进协作改进

## 📞 支持

### 如果您需要帮助

1. **检查 INDEX.md** 进行导航
2. **查看 TROUBLESHOOTING.md** 了解常见问题
3. **查看 Examples.md** 类似案例
4. **阅读 BEST_PRACTICES.md** 获取指导

### 常见问题

**问：如何上传技能？**
答：请参阅上面的“选项 1：通过 Claude.com 上传”

**问：我可以自定义技能吗？**
答：是的！编辑 Markdown 文件以添加特定于域的内容

**问：如果我的提示仍然不起作用怎么办？**
A：检查TROUBLESHOOTING.md或者让Claude调试一下

**问：我可以将其与 API 一起使用吗？**
答：是的！请参阅上面的“选项 3：与 Agent SDK 一起使用”

## 🎉 你准备好了！

您的快速工程专家技能已准备好使用。首先上传它并要求克劳德查看您的提示之一！

---

**有问题吗？** 查看文档文件或直接询问 Claude！
