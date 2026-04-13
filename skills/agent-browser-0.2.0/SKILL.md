---
---
name: Agent Browser description: "一个基于 Rust 的快速无头浏览器自动化 CLI，具有 Node.js 后备功能，使 AI 代理能够通过结构化命令导航、单击、键入和快照页面。" read_when: 
  - Automating web interactions
  - Extracting structured data from pages
  - Filling forms programmatically
  - Testing web UIs
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["node","npm"]}}} allowed-tools: "Bash（代理浏览器：*）"
---
---



# 使用代理浏览器实现浏览器自动化

## 安装

# # # npm 推荐

PH0

### 来自来源

PH1

## 快速开始

PH2

## 核心工作流程

导航1. PH26
2. 快照PH27 （ PH28返回具有、、PH29 等引用的元素）
3. 使用快照中的引用进行交互
4. 导航或重大 DOM 更改后重新快照

## 命令

导航

PH3

### 快照（页面分析 ）

PH4

# # # 交互（使用快照中的 @ refs ）

PH5

### 获取信息

PH6

### 检查状态

PH7

# # # 屏幕截图和 PDF

PH8

### 视频录制

PH9

录制会创建一个新的上下文，但会保留会话中的 cookie/存储。如果未提供 URL，它将自动返回到您当前的页面。为了获得流畅的演示，请先探索，然后开始录制。

### 等待

PH10

### 鼠标控制

PH11

# # # 语义定位器（替代 refs ）

PH12

### 浏览器设置

PH13

### Cookie 和存储

PH14

Network

PH15

### 选项卡和窗口

PH16

### 框架

PH17

### 对话框

PH18

### JavaScript

PH19

### 状态管理

PH20

## 示例：表单提交

PH21

## 示例：保存状态的身份验证

PH22

## 会话（并行浏览器 ）

PH23

## JSON 输出（用于解析）

添加 PH30 以实现机器可读输出：

PH24

调试

PH25

<bpt i="1" x="1"/> 故障排除<ept i="1"/>

- 如果在 Linux ARM64 上找不到该命令，请使用 bin 文件夹中的完整路径。
- 如果未找到某个元素，请使用快照来查找正确的引用。
- 如果页面未加载，请在导航后添加等待命令。
- 使用 --headed 查看浏览器窗口进行调试。

选项

- --session __ HTML_0 __ 使用隔离会话。
- --json 提供 JSON 输出。
- --full 截取整页屏幕截图。
- --headed 显示浏览器窗口。
- --timeout 设置命令超时时间（超时以毫秒为单位）。
- --cdp __ HTML_1 __ 通过 Chrome开发者工具 协议连接。

Comments

- 参考在每个页面加载时都是稳定的，但在导航时会发生变化。
- 导航后始终拍摄快照以获取新参考。
- 在输入字段中使用填充而不是键入，以确保清除现有文本。

## 报告问题

- 技能问题：在 PH31 提出问题
- 代理浏览器 CLI 问题：在 PH32 提出问题
