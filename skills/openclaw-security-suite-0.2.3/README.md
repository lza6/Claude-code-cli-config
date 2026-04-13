# OpenClaw Security (OpenClaw 安全套件)

> OpenClaw 技能的安全保护层 — 扫描、审查和防范恶意代码。

## 架构

```
security_skill_scanner/
├── index.ts                 # 插件入口 — 导出 scanSkill & reviewSkill
├── config/
│   ├── policy.json          # 已屏蔽的模块、函数和权限
│   └── malicious_patterns.json  # 危险关键字模式
├── scanner/
│   ├── skill_scanner.ts     # 编排器 — 扫描目录下所有 .ts/.js 文件
│   ├── ast_scanner.ts       # 基于 AST 的检测（已屏蔽的导入和调用）
│   ├── keyword_scanner.ts   # 基于文本的危险关键字匹配
│   └── vm_runner.ts         # 沙箱代码执行 (Node vm)
├── guard/
│   └── runtime_guard.ts     # 运行时保护（屏蔽元数据和 Shell 访问）
├── llm/
│   └── ai_review.ts         # 基于 LLM 的代码审查
├── signature/
│   └── verify_signature.ts  # SHA256 文件签名验证
└── skills/
    ├── scan_skill/index.ts  # 技能：静态安全扫描
    └── review_skill/index.ts # 技能：AI 辅助代码审查
```

### `openclaw-security-suite`

统一的安全工具，提供静态分析和 AI 辅助代码审查。

**输入：**
```json
{ 
  "action": "scan", // 或 "review"
  "path": "/path/to/skill/directory" 
}
```

**输出（扫描）：**
```json
{
  "safe": false,
  "results": [
    {
      "file": "index.ts",
      "issues": [
        { "type": "blocked_module", "module": "child_process" },
        { "type": "keyword", "keyword": "eval(" }
      ]
    }
  ]
}
```

## 安全层

| 层级 | 方法 | 捕捉内容 |
|--------|--------------------|-----------------|
| **AST 扫描器** | Babel AST 遍历 | 阻止模块导入（`child_process`、`cluster`）、危险函数调用（`exec`、`spawn`） |
| **关键字扫描器** | 文本匹配 | `eval(`、`__proto__`、`process.env`、`fs.writeFileSync` 等 |
| **VM 运行器** | Node.js `vm` 沙箱 | 具有内存隔离和 1 秒超时的运行时行为分析 |
| **运行时防护** | 参数检查 | 云元数据访问（`169.254.169.254`）、Shell 命令执行 |
| **AI 审查** | LLM 分析 | 数据泄露、凭据泄露、系统修改 |
| **签名验证** | SHA256 + 公钥 | 文件完整性和真实性 |

## 设置

```bash
npm install
```

## 配置

### `config/policy.json`

```json
{
  "blocked_modules": ["child_process", "cluster"],
  "blocked_functions": ["exec", "spawn", "execSync"],
  "allowed_permissions": ["network", "memory"],
  "blocked_permissions": ["shell", "process"]
}
```

### `config/malicious_patterns.json`

包含通过文本搜索匹配的“危险关键字 (dangerous_keywords)”列表（例如 “eval(”、“Function(”、“__proto__”）。

## 许可证

MIT
