# arXiv 投稿指南

## 文件清单
- `main.tex` — 主论文
- `references.bib` — 参考文献

## 投稿步骤

### 1. 注册 arXiv 账号
- 访问 https://arxiv.org/user/register
- 需要学术邮箱（gmail 也可以但可能需要等待审核）
- 首次投稿可能需要 endorsement（cs.SE 通常不需要）

### 2. 开始投稿
- 登录后点击 "Submit" → "Start New Submission"
- 上传 `main.tex` 和 `references.bib`（打包成 .zip 或逐个上传）

### 3. 填写 Metadata

**Title:**
Trust Over Fear: How Motivation Framing in System Prompts Affects AI Agent Debugging Depth

**Authors:**
WUJI (Independent Researcher)

**Abstract:** (复制 .tex 中的 abstract，去掉 LaTeX 命令)

**Primary Category:** cs.SE (Software Engineering)
**Secondary Category:** cs.CL (Computation and Language)

**Comments:** 10 pages, 6 tables, 2 studies
**License:** CC BY 4.0 (推荐，允许他人引用和衍生)

### 4. 提交
- Preview → 检查 PDF 渲染
- 确认无误后 Submit
- 通常 1-2 个工作日内上线（moderation review）

### 5. 上线后
- 会获得一个 arXiv ID（如 2603.XXXXX）
- 可以分享 https://arxiv.org/abs/2603.XXXXX
- 更新版本用 "Replace" 功能

## 注意事项
- arXiv 用自己的 TeX Live 编译，与 Overleaf 可能有微小差异
- 如果编译失败，检查是否缺少宏包
- `acl_natbib` 样式文件可能需要替换为 `plainnat`（如果 arXiv 没有）
