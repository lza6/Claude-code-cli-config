# Markdown 短绒

一个 CLI 工具，用于检查 Markdown 文件的格式问题、损坏的链接和样式一致性。

## 快速入门

```bash
# Lint a single file
./scripts/main.py run --input README.md

# Lint multiple files
./scripts/main.py run --input "docs/*.md"
```

＃＃ 安装

该技能是通过 OpenClaw 安装的。安装后，您可以直接从 OpenClaw 代理使用它。

＃＃ 特征

- **标头层次结构验证**
- **图像替代文本检查**
- **内部链接验证**
- **线长度检查**
- **尾随空白检测**
- **列表一致性检查**
- **代码块语言推荐**
- **空链接检测**
- **重复标题警告**
- **外部链接检查**（可选）

＃＃ 配置

使用命令行选项自定义 linting 行为：

- `--max-line-length`：设置最大行长度（默认值：80）
- `--check-external-links`：启用外部 URL 验证
- `--ignore-rules`：要忽略的规则 ID 的逗号分隔列表

＃＃ 输出

该工具输出 JSON 以及详细的问题报告，包括行号、严重性级别和建议的修复。

## 贡献

欢迎提出问题和请求。请参阅“scripts/main.py”中的源代码。

＃＃ 执照

麻省理工学院