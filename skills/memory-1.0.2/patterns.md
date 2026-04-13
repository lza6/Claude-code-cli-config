# 组织模式

## 模式 1：基于类别的结构

最常见。按信息类型组织：

```
~/memory/
├── projects/
├── people/
├── decisions/
├── knowledge/
└── collections/
```

**最适合：** 一般用途，多个领域。

---

## 模式 2：以领域为中心的结构

一切都围绕一个领域组织起来：

```
~/memory/
├── clients/
├── deals/
├── products/
├── competitors/
└── market-research/
```

**最适合：** 专注于某一领域（销售、研究等）的专业人士。

---

## 模式 3：基于时间的结构

按事情发生的时间整理：

```
~/memory/
├── 2026/
│   ├── q1/
│   └── q2/
├── 2025/
└── archive/
```

**最适合：** 日记、记录、历史跟踪。

---

## 模式 4：混合结构

类别和时间的混合：

```
~/memory/
├── active/           # 当前焦点
│   ├── projects/
│   └── people/
├── reference/        # 始终相关
│   ├── knowledge/
│   └── preferences/
└── archive/          # 历史
    ├── 2025/
    └── 2024/
```

**最适合：** 需要当前和历史上下文的人。

---

## 模式 5：发展类别

当一个类别变大时，将其拆分：

**之前（100 多个条目）：**
```
~/memory/projects/INDEX.md  # 太长了
```

**之后（按状态划分）：**
```
~/memory/projects/
├── INDEX.md          # 仅指向子目录
├── active/
│   └── INDEX.md      # 20 个条目
├── paused/
│   └── INDEX.md      # 15 个条目
└── archived/
    └── INDEX.md      # 100+ 条目（可以接受，很少访问）
```

---

## 模式 6：从内置内存同步

如果用户想从代理的内置内存中复制信息：

```
~/memory/sync/
├── INDEX.md
├── preferences.md    # 复制自 MEMORY.md
└── key-decisions.md  # 复制自 MEMORY.md
```

**同步过程：**
1. 从内置读取（MEMORY.md 等）
2. 本系统的重新格式化
3. 写入 ~/memory/sync/
4. 使用同步日期更新 ~/memory/sync/INDEX.md

**切勿修改内置内存。** 同步是只读的。

---

## 模式 7：快速捕获 → 稍后组织

为了快速记录而不考虑结构：

```
~/memory/
├── inbox/
│   └── INDEX.md      # 未分类项目
├── projects/
└── ...
```

**流程：**
1. 立即捕获到收件箱 (inbox)
2. 每周：将收件箱项分类到适当的类别
3. 分类后从收件箱中删除

---

## 模式 8：交叉引用

当项目涉及多个类别时：

```markdown
# ~/memory/projects/alpha.md

## 团队
- Alice (PM) → 参见 people/alice.md
- Bob (Dev) → 参见 people/bob.md

## 关键决策
- 数据库选择 → 参见 decisions/2026.md#database-alpha
```

**使用相对链接。** 切勿重复内容。

---

## 模式 9：归档旧内容

当内容陈旧但可能需要时：

**请勿删除。进行归档：**
```bash
# 移动到存档
mv ~/memory/projects/old-thing.md ~/memory/archive/projects/

# 更新索引
# 1. 从 projects/INDEX.md 中移除
# 2. 添加到 archive/INDEX.md
```

**archive/INDEX.md 示例：**
```markdown
# 存档 (Archive)

| 项目 | 类型 | 归档日期 | 原因 |
|------|------|----------|--------|
| OldProject | 项目 | 2026-01 | 已完成 |
```

---

## 模式 10：搜索优化

使用良好的关键字使内容易于查找：

```markdown
# ~/memory/people/alice.md

# Alice Smith

**关键字:** PM, 产品经理, Acme Corp, alpha 项目, 每周同步

## 个人资料
...
```

搜索时，顶部的关键字有助于 grep/语义搜索找到正确的文件。
