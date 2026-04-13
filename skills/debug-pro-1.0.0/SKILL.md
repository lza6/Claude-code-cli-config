# 调试专业版

系统的调试方法和特定于语言的调试命令。

## 七步调试协议

1. **重现** — 让它稳定复现。记录确切的步骤、输入和环境。
2. **隔离** — 缩小范围。注释掉代码，使用二分搜索，使用 `git bisect` 检查最近的提交。
3. **假设** — 形成关于根本原因的具体、可测试的理论。
4. **添加检测** — 添加目标日志记录、断点或断言。
5. **验证** — 确认根本原因。如果假设错误，则返回步骤 3。
6. **修复** — 应用最小的正确修复。在调试时抵制重构的冲动。
7. **回归测试** — 编写一个测试来捕获此错误。验证是否通过。

## 特定语言的调试

### JavaScript / TypeScript
```bash
# Node.js 调试器
node --inspect-brk app.js
# Chrome DevTools: chrome://inspect

# 控制台调试
console.log(JSON.stringify(obj, null, 2))
console.trace('Call stack here')
console.time('perf'); /* code */ console.timeEnd('perf')

# 内存泄漏
node --expose-gc --max-old-space-size=4096 app.js
```

### Python
```bash
# 内置调试器
python -m pdb script.py

# 代码中的断点
breakpoint()  # Python 3.7+

# 详细追踪
python -X tracemalloc script.py

# 性能分析
python -m cProfile -s cumulative script.py
```

### Swift
```bash
# LLDB 调试
lldb ./MyApp
(lldb) breakpoint set --name main
(lldb) run
(lldb) po myVariable

# Xcode: Product → Profile (Instruments)
```

### CSS / 布局
```css
/* 为所有元素添加轮廓 */
* { outline: 1px solid red !important; }

/* 调试特定元素 */
.debug { background: rgba(255,0,0,0.1) !important; }
```

### 网络
```bash
# HTTP 调试
curl -v https://api.example.com/endpoint
curl -w "@curl-format.txt" -o /dev/null -s https://example.com

# DNS
dig example.com
nslookup example.com

# 端口
lsof -i :3000
netstat -tlnp
```

### Git 二分查找
```bash
git bisect start
git bisect bad              # 当前提交有问题
git bisect good abc1234     # 已知良好的提交
# Git 检出中间提交 — 测试它，然后：
git bisect good  # 或 git bisect bad
# 重复直到找到根本原因的提交
git bisect reset
```

## 常见错误模式

| 错误 | 可能的原因 | 修复 |
|--------|-------------|-----|
| `Cannot read properties of undefined` | 缺少空值检查或数据结构错误 | 添加可选链（`?.`）或验证数据 |
| `ENOENT` | 文件/目录不存在 | 检查路径，创建目录，使用 `existsSync` |
| `CORS 错误` | 后端缺少 CORS 头 | 添加具有正确来源的 CORS 中间件 |
| `Module not found` | 缺少依赖或导入路径错误 | `npm install`，检查 tsconfig 路径 |
| `Hydration mismatch`（React） | 服务器/客户端渲染的 HTML 不同 | 确保一致的渲染，仅客户端使用 `useEffect` |
| `Segmentation fault` | 内存损坏，空指针 | 检查数组边界、指针有效性 |
| `Connection refused` | 服务未在预期端口上运行 | 检查服务是否启动，验证端口/主机 |
| `Permission denied` | 文件/网络权限问题 | 检查 chmod、防火墙、sudo |

## 快速诊断命令

```bash
# 什么占用了这个端口？
lsof -i :PORT

# 这个进程在做什么？
ps aux | grep PROCESS

# 监控文件变更
fswatch -r ./src

# 磁盘空间
df -h

# 系统资源使用情况
top -l 1 | head -10
```
