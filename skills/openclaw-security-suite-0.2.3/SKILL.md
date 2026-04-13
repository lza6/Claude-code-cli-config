---
name: openclaw-security-suite
description: "针对 OpenClaw 技能的综合安全套件。包括静态扫描（AST + 关键字）和人工智能驱动的语义行为审查以检测恶意代码。"
version: 0.2.3
tags:
  - security
  - scanner
  - code-review
  - static-analysis
  - ai-review
requirements:
  binaries:
    - node
  environment: []
input_schema:
  type: object
  properties:
    action:
      type: string
      enum: ["scan", "review"]
      description: 执行的操作。"scan" 用于静态分析，"review" 用于 AI 语义审查。
    path:
      type: string
      description: 技能目录（扫描）或文件（审查）的绝对路径。
  required:
    - action
    - path
---

# OpenClaw 安全套件 (OpenClaw Security Suite)

OpenClaw 扩展的全面安全保护层，提供静态分析和 AI 辅助行为审查。

## 特性

该套件整合了两个核心安全功能：

### 1. 静态安全扫描 (`action: "scan"`)
对整个技能目录进行分析，以识别确定的威胁：
- **已屏蔽的导入**：例如 `child_process`、`cluster`
- **危险函数**：例如 `exec()`、`spawn()`
- **已知的恶意关键字**：例如 `eval(`、`__proto__`、`rm -rf`
- **敏感文件访问**：例如 `/etc/passwd`、`/.env`
- **可疑的正则模式**：例如 `curl ... | bash`

### 2. AI 代码审查 (`action: "review"`)
利用活跃的 LLM 上下文 (`ctx.llm`) 对特定文件进行语义分析，查找隐藏威胁：
- **数据外泄**
- **凭据泄露**
- **混淆后的 Shell 执行**
- **系统篡改**

## 用法

您必须指定 `action` 和 `path` 参数。

**示例 1：静态扫描**
```json
{
  "action": "scan",
  "path": "/path/to/skill/directory"
}
```

**示例 2：AI 审查**
```json
{
  "action": "review",
  "path": "/path/to/skill/index.ts"
}
```

## 输出示例

**扫描输出：**
```json
{
  "safe": false,
  "results": [
    {
      "file": "index.ts",
      "issues": [{ "type": "blocked_module", "module": "child_process" }]
    }
  ]
}
```

**审查输出：**
```json
{
  "risk_level": "high",
  "reason": "代码从环境变量读取 AWS 凭据并将其发送至外部 IP 地址。"
}
```
