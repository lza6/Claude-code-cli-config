# 变更日志

## 0.2.0 (2026-03-11)

### 新增
- 为 “scan_skill” 和 “review_skill” 添加了 “SKILL.md”（与 ClawHub 兼容）
- `malicious_patterns.json` 包含 4 个检测类别：
  - `dangerous_keywords`（22 种模式）
  - `sensitive_files`（4 个路径）
  - `suspicious_urls`（2 个 URL）
  - `suspicious_patterns`（4 个正则表达式规则）
- `tsconfig.json` (ESNext + NodeNext)
- 测试固件和验证脚本（`test/verify.ts`）
- `.gitignore` 和 `README.md`

### 变更
- 用 Node 内置的 `node:vm` 模块替换了已弃用的 `vm2`
- 增强了 “keyword_scanner.ts” 以支持所有 4 个模式类别
- 修复了 `ast_scanner.ts` ESM 与 `@babel/traverse` 的兼容性问题
- 通过适当的类型收窄改进了 “callee.name” 的访问方式

### 安全
- 删除了 “vm2” 依赖项（修复 CVE-2023-37466 及其他沙箱逃逸漏洞）

## 0.1.0

### 新增
- 初步实现
- 基于 Babel 的 AST 扫描器
- 关键字扫描器
- VM 沙箱运行器 (基于 vm2)
- 运行时防护 (Runtime Guard)
- 通过 LLM 进行 AI 审查
- 签名验证
