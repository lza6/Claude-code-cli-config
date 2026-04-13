---
name: markdown-linter
description: '检查 Markdown 文件的格式问题、断链和样式一致性。**Auto-trigger**: 当用户创建/编辑 Markdown 文件时自动使用。'
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - markdown
        - requests
---

# Markdown 检查器

## 功能说明

一个 CLI 工具，用于检查 Markdown 文件的常见格式问题、样式一致性和断链。帮助在发布前捕获错误，维护文档质量。

主要功能：
- **标题层级验证** — 确保正确的嵌套关系（不跳过层级）
- **图片替代文本检查** — 标记没有描述性 alt 文本的图片
- **内部链接验证** — 检查内部链接（同一文档内）是否指向现有的锚点
- **行长度检查** — 警告超过可配置长度的行（默认 80 个字符）
- **尾随空白检测** — 查找并报告尾随空格/制表符
- **列表一致性** — 确保同一文档内列表标记（-、*、+）保持一致
- **代码块语言标注** — 建议为代码块添加语言规范
- **空链接检测** — 标记文本或 URL 为空的链接
- **重复标题** — 警告同一文件内重复的标题文本
- **外部链接检查** — 可选地验证外部 URL（需要联网）

## 使用方法

运行此技能：
```bash
./scripts/main.py run --input path/to/file.md
```

或检查多个文件：
```bash
./scripts/main.py run --input "*.md"
```

### 选项

- `--input`：Markdown 文件路径（支持 glob 模式）
- `--max-line-length`：最大允许行长度（默认：80）
- `--check-external-links`：启用外部 URL 验证（默认：false）
- `--ignore-rules`：要忽略的规则 ID 列表（逗号分隔）

### 输出

返回包含检查结果的 JSON：
```json
{
  "file": "example.md",
  "issues": [
    {
      "line": 10,
      "column": 1,
      "rule": "MD001",
      "severity": "warning",
      "message": "标题级别每次只能递增一级",
      "fix": "将 ## 改为 #"
    }
  ],
  "summary": {
    "total_issues": 5,
    "errors": 2,
    "warnings": 3
  }
}
```

## 局限性

- 外部链接检查需要网络连接，可能较慢
- 可读性评分功能尚未实现
- 某些 Markdown 扩展（表格、脚注）可能无法完全验证
- 大文件（>10k 行）处理时间可能较长
- 内部链接的锚点检测仅适用于简单的锚点模式

## 示例

基本检查：
```bash
./scripts/main.py run --input README.md
```

自定义行长度：
```bash
./scripts/main.py run --input docs/*.md --max-line-length 100
```

启用外部链接验证：
```bash
./scripts/main.py run --input "**/*.md" --check-external-links
```

## 规则参考

- **MD001**：标题层级违规
- **MD002**：缺少图片替代文本
- **MD003**：内部链接失效
- **MD004**：行过长
- **MD005**：尾随空白
- **MD006**：列表标记不一致
- **MD007**：代码块缺少语言标注
- **MD008**：空链接
- **MD009**：重复标题
- **MD010**：外部链接失效（启用时）
