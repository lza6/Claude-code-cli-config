# 学习机制

## 什么触发学习

|触发|信心|行动|
|--------|------------|--------|
| “不，改做X” |高|立即记录更正|
| “我之前就告诉过你了……” |高|标记为重复，碰撞优先级 |
| “总是/从不做X” |已确认 |提升至偏好 |
|用户编辑您的输出 |中等|记录为暂定模式 |
|相同修正 3x |已确认 |要求永久|
| “对于这个项目......” |范围 |写入项目命名空间 |

## 什么不会触发学习

- 沉默（不确认）
- 任何事物的单一实例
- 假设性讨论
- 第三方偏好（“约翰喜欢......”）
- 群聊模式（除非用户确认）
- 隐含的偏好（绝不推断）

## 修正分类

### 按类型
|类型 |示例|命名空间|
|------|---------|------------|
|格式| “使用子弹而不是散文”|全球|
|技术| “SQLite 不是 Postgres”|域名/代码 |
|通讯 | “较短的消息” |全球|
|项目特定| “此存储库使用 Tailwind”|项目/{名称} |
|因人而异 | “马库斯想要BLUF”|域/通信 |

### 按范围
```
Global: applies everywhere
  └── Domain: applies to category (code, writing, comms)
       └── Project: applies to specific context
            └── Temporary: applies to this session only
```

## 确认流程

3次类似修正后：
```
Agent: "I've noticed you prefer X over Y (corrected 3 times).
        Should I always do this?
        - Yes, always
        - Only in [context]
        - No, case by case"

User: "Yes, always"

Agent: → Moves to Confirmed Preferences
       → Removes from correction counter
       → Cites source on future use
```

## 模式演变

### 阶段
1. **暂定** — 单次更正，注意重复
2. **新兴** — 2 次修正，可能的模式
3. **待处理** — 3 处更正，要求确认
4. **已确认** — 用户批准，永久有效，除非撤销
5. **已存档** — 90 多天未使用，保留但不活动

### 逆转
用户可以随时反转：
```
User: "Actually, I changed my mind about X"

Agent: 
1. Archive old pattern (keep history)
2. Log reversal with timestamp
3. Add new preference as tentative
4. "Got it. I'll do Y now. (Previous: X, archived)"
```

## 反模式

### 永远不会学习
- 是什么让用户更快地遵守（操纵）
- 情绪触发因素或脆弱性
- 来自其他用户的模式（即使共享设备）
- 任何表面上感觉“令人毛骨悚然”的东西

### 避免
- 从单个实例过度概括
- 学习方式重于内容
- 假设偏好稳定
- 忽略上下文变化

## 质量信号

### 好好学习
- 用户明确说明偏好
- 跨上下文的模式一致
- 纠正可以改善结果
- 用户在询问时确认

### 学习不好
- 从沉默中推断
- 与最近的行为相矛盾
- 仅适用于狭窄的环境
- 用户从未确认
