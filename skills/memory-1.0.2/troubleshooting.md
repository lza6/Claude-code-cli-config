# 故障排除 (Troubleshooting)

## 找不到信息

**症状：**
- “我在记忆系统中没看到这一点”
- 信息确实存在但无法通过搜索找到

**解决方案：**

| 可能原因 | 检查项 | 修复方案 |
|--------|--------|-----|
| 未编入索引 | `grep -l "主题" ~/memory/*/INDEX.md` | 将其添加到相关的 `INDEX.md` 文件中 |
| 类别归纳错误 | 查看其它类别目录 | 将文件移动到正确的类别目录下 |
| 搜索关键词太窄 | 尝试使用不同的关键词 | 在文件头部添加常用关键字 (Keywords) |
| 在内置内存中，不在本系统 | 检查代理的 `MEMORY.md` | 如有需要，将其同步到本系统中 |

**快速搜索命令：**
```bash
# 在所有记忆文件中查找
grep -r "关键字" ~/memory/

# 仅在索引文件中查找（速度更快）
grep -r "关键字" ~/memory/*/INDEX.md
```

---

## 记忆系统变慢

**症状：**
- 查找内容需要很长时间
- 某个类别的索引文件变得非常庞大

**解决方案：**

1. **检查索引文件行数：**
```bash
wc -l ~/memory/*/INDEX.md
# 超过 100 行的索引文件建议进行拆分
```

2. **拆分大型类别：**
```
之前: projects/INDEX.md (150 个条目)
之后: projects/active/INDEX.md (30 个条目)
      projects/archived/INDEX.md (120 个条目)
```

3. **归档旧内容：**
```bash
# 将旧条目移动到存档目录
mv ~/memory/projects/old.md ~/memory/archive/
# 同时更新原类别和存档类别的两个索引文件
```

---

## 与内置内存 (Built-in) 冲突

**症状：**
- 代理混淆了该使用哪个记忆系统
- 出现重复信息

**核心规则：** 本系统 (`~/memory/`) 与代理内置内存系统是完全分离的。

**解决方案：**

1. **绝对不要通过本技能修改内置内存系统**
2. **核对存储位置：**
   - 内置系统：工作区根目录的 `MEMORY.md`、工作区的 `memory/` 文件夹
   - 本系统：家目录下的 `~/memory/`
3. **处理重复：** 在本系统中保留详细版本，在内置系统中保留简要摘要

---

## 结构混乱

**症状：**
- 文件散落在各处
- 很难确定某个信息应该放在哪里

**解决方案：**

1. **建立明确的类别：**
```bash
ls ~/memory/
# 应该只显示清晰的类别文件夹，而不是零散的文件
```

2. **确保根目录下没有杂乱文件：**
```
~/memory/
├── config.md     # OK (系统配置文件)
├── INDEX.md      # OK (根索引文件)
├── projects/     # OK (类别目录)
├── random.md     # 错误做法 - 应该放入某个类别中
```

3. **利用收件箱 (Inbox) 处理未分类项：**
```bash
mkdir ~/memory/inbox
# 将暂时不确定位置的条目放入此处，每周定期清理分类
```

---

## 同步功能失效

**症状：**
- 同步文件夹 (`sync/`) 为空或内容陈旧
- 未能反映内置内存中的最新更改

**解决方案：**

1. **检查是否启用了同步：**
```bash
cat ~/memory/config.md | grep sync
```

2. **手动触发同步：**
   - 读取代理的 `MEMORY.md`
   - 提取相关部分
   - 写入 `~/memory/sync/`
   - 使用当前日期更新 `~/memory/sync/INDEX.md`

3. **请记住：** 同步是手动触发的，不是实时的自动同步。请定期手动重新同步。

---

## 忘记了存在哪些类别

**快速检查命令：**
```bash
# 查看所有已定义的类别
cat ~/memory/INDEX.md

# 查看文件夹物理结构
ls ~/memory/
```

---

## 索引文件 (INDEX.md) 已过时

**症状：**
- 文件存在但未列在 `INDEX` 中
- `INDEX` 中列出了已不存在的文件

**解决方案：**

```bash
# 检查未列入索引的文件
for f in ~/memory/projects/*.md; do
  name=$(basename "$f")
  grep -q "$name" ~/memory/projects/INDEX.md || echo "未入索引: $name"
done

# 检查死链接
grep -oE '[a-z0-9\-]+\.md' ~/memory/projects/INDEX.md | while read f; do
  [ ! -f ~/memory/projects/"$f" ] && echo "缺失文件: $f"
done
```

**如果索引损坏严重，请重新生成：**
```bash
# 从现有文件生成新索引
ls ~/memory/projects/*.md | while read f; do
  name=$(basename "$f" .md)
  echo "| $name | ? | $(date +%Y-%m-%d) | $name.md |"
done
```

---

## 不确定该把内容放在哪里

**决策树：**

```
是否关于特定项目?
  → projects/ (项目)

是否关于某个人?
  → people/ (人物)

是否是带有推理过程的决策?
  → decisions/ (决策)

是否是参考资料或学习材料?
  → knowledge/ (知识)

是否是你收集的一系列事物清单?
  → collections/ (收藏)

以上都不是?
  → inbox/ (收件箱，稍后再分类)
```

---

## 快速健康检查脚本

```bash
#!/bin/bash
echo "=== 记忆系统健康检查 ==="

# 检查根目录
[ -d ~/memory ] && echo "✓ ~/memory 目录存在" || echo "✗ ~/memory 缺失"
[ -f ~/memory/INDEX.md ] && echo "✓ 根 INDEX.md 存在" || echo "✗ 根 INDEX.md 缺失"
[ -f ~/memory/config.md ] && echo "✓ config.md 存在" || echo "✗ config.md 缺失"

# 检查类别索引
echo ""
echo "类别索引状态:"
for dir in ~/memory/*/; do
  name=$(basename "$dir")
  if [ "$name" != "config.md" ]; then
    [ -f "$dir/INDEX.md" ] && echo "  ✓ $name/INDEX.md" || echo "  ✗ $name/INDEX.md 缺失"
  fi
done

# 统计总文件数
total=$(find ~/memory -name "*.md" | wc -l)
echo ""
echo "总文件数: $total"

echo "=== 检查完成 ==="
```
