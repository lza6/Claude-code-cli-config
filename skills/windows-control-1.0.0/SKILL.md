---
name: windows-control
description: "完整的 Windows 桌面控制。鼠标、键盘、屏幕截图 - 像人类一样与任何 Windows 应用程序交互。"
---

# Windows 控制技巧

Windows 的完整桌面自动化。像人类用户一样控制鼠标、键盘和屏幕。

## 快速入门

所有脚本都位于“skills/windows-control/scripts/”中

### 截屏
```bash
py screenshot.py > output.b64
```
返回整个屏幕的 base64 PNG。

### 点击
```bash
py click.py 500 300              # Left click at (500, 300)
py click.py 500 300 right        # Right click
py click.py 500 300 left 2       # Double click
```

### 输入文本
```bash
py type_text.py "Hello World"
```
在当前光标位置键入文本（按键之间间隔 10 毫秒）。

### 按键
```bash
py key_press.py "enter"
py key_press.py "ctrl+s"
py key_press.py "alt+tab"
py key_press.py "ctrl+shift+esc"
```

### 移动鼠标
```bash
py mouse_move.py 500 300
```
将鼠标移动到坐标（平滑的 0.2 秒动画）。

### 滚动
```bash
py scroll.py up 5      # Scroll up 5 notches
py scroll.py down 10   # Scroll down 10 notches
```

### 窗口管理（新！）
```bash
py focus_window.py "Chrome"           # Bring window to front
py minimize_window.py "Notepad"       # Minimize window
py maximize_window.py "VS Code"       # Maximize window
py close_window.py "Calculator"       # Close window
py get_active_window.py               # Get title of active window
```

### 高级操作（新！）
```bash
# Click by text (No coordinates needed!)
py click_text.py "Save"               # Click "Save" button anywhere
py click_text.py "Submit" "Chrome"    # Click "Submit" in Chrome only

# Drag and Drop
py drag.py 100 100 500 300            # Drag from (100,100) to (500,300)

# Robust Automation (Wait/Find)
py wait_for_text.py "Ready" "App" 30  # Wait up to 30s for text
py wait_for_window.py "Notepad" 10    # Wait for window to appear
py find_text.py "Login" "Chrome"      # Get coordinates of text
py list_windows.py                    # List all open windows
```

### 读取窗口文本
```bash
py read_window.py "Notepad"           # Read all text from Notepad
py read_window.py "Visual Studio"     # Read text from VS Code
py read_window.py "Chrome"            # Read text from browser
```
使用 Windows UI 自动化提取实际文本（不是 OCR）。比截图更快、更准确！

### 读取 UI 元素（新！）
```bash
py read_ui_elements.py "Chrome"               # All interactive elements
py read_ui_elements.py "Chrome" --buttons-only  # Just buttons
py read_ui_elements.py "Chrome" --links-only    # Just links
py read_ui_elements.py "Chrome" --json          # JSON output
```
返回带有点击坐标的按钮、链接、选项卡、复选框、下拉列表。

### 阅读网页内容（新！）
```bash
py read_webpage.py                     # Read active browser
py read_webpage.py "Chrome"            # Target Chrome specifically
py read_webpage.py "Chrome" --buttons  # Include buttons
py read_webpage.py "Chrome" --links    # Include links with coords
py read_webpage.py "Chrome" --full     # All elements (inputs, images)
py read_webpage.py "Chrome" --json     # JSON output
```
增强了浏览器内容提取，包括标题、文本、按钮和链接。

### 处理对话框（新！）
```bash
# List all open dialogs
py handle_dialog.py list

# Read current dialog content
py handle_dialog.py read
py handle_dialog.py read --json

# Click button in dialog
py handle_dialog.py click "OK"
py handle_dialog.py click "Save"
py handle_dialog.py click "Yes"

# Type into dialog text field
py handle_dialog.py type "myfile.txt"
py handle_dialog.py type "C:\path\to\file" --field 0

# Dismiss dialog (auto-finds OK/Close/Cancel)
py handle_dialog.py dismiss

# Wait for dialog to appear
py handle_dialog.py wait --timeout 10
py handle_dialog.py wait "Save As" --timeout 5
```
处理保存/打开对话框、消息框、警报、确认等。

### 按名称单击元素（新！）
```bash
py click_element.py "Save"                    # Click "Save" anywhere
py click_element.py "OK" --window "Notepad"   # In specific window
py click_element.py "Submit" --type Button    # Only buttons
py click_element.py "File" --type MenuItem    # Menu items
py click_element.py --list                    # List clickable elements
py click_element.py --list --window "Chrome"  # List in specific window
```
按名称单击按钮、链接、菜单项，无需坐标。

### 读取屏幕区域（OCR - 可选）
```bash
py read_region.py 100 100 500 300     # Read text from coordinates
```
注意：需要安装 Tesseract OCR。使用 read_window.py 代替以获得更好的结果。

## 工作流程模式

1. **阅读窗口** - 从特定窗口提取文本（快速、准确）
2. **读取UI元素** - 获取带有坐标的按钮、链接
3. **屏幕截图**（如果需要）- 查看视觉布局
4. **Act** - 按名称或坐标单击元素
5. **处理对话框** - 与弹出窗口/保存对话框交互
6. **阅读窗口** - 验证更改

## 屏幕坐标

- 原点 (0, 0) 是左上角
- 您的屏幕：2560x1440（查看屏幕截图）
- 使用屏幕截图分析中的坐标

## 示例

### 打开记事本并输入
```bash
# Press Windows key
py key_press.py "win"

# Type "notepad"
py type_text.py "notepad"

# Press Enter
py key_press.py "enter"

# Wait a moment, then type
py type_text.py "Hello from AI!"

# Save
py key_press.py "ctrl+s"
```

### 单击 VS Code
```bash
# Read current VS Code content
py read_window.py "Visual Studio Code"

# Click at specific location (e.g., file explorer)
py click.py 50 100

# Type filename
py type_text.py "test.js"

# Press Enter
py key_press.py "enter"

# Verify new file opened
py read_window.py "Visual Studio Code"
```

### 监视记事本更改
```bash
# Read current content
py read_window.py "Notepad"

# User types something...

# Read updated content (no screenshot needed!)
py read_window.py "Notepad"
```

## 文本阅读方法

**方法 1：Windows UI 自动化（最佳）**
- 对任何窗口使用“read_window.py”
- 对带有坐标的按钮/链接使用“read_ui_elements.py”
- 使用“read_webpage.py”来获取具有结构的浏览器内容
- 获取实际的文本数据（不是基于图像的）

**Method 2: Click by Name (NEW)**
- 使用“click_element.py”按名称单击按钮/链接
- 无需坐标 - 自动查找元素
- 适用于所有窗口或目标特定窗口

**方法 3：对话框处理（新）**
- 使用“handle_dialog.py”弹出窗口、保存对话框、警报
- 阅读对话框内容，单击按钮，输入文本
- 使用常用按钮自动关闭（确定、取消等）

**方法4：屏幕截图+视觉（后备）**
- 截取完整屏幕截图
- 人工智能以视觉方式读取文本
- 速度较慢，但适用于任何内容

**方法 5：OCR（可选）**
- 将 `read_region.py` 与 Tesseract 一起使用
- 需要额外安装
- 适合带有文本的图像/PDF

## 安全特性

- `pyautogui.FAILSAFE = True`（将鼠标移至左上角以中止）
- 动作之间的小延迟
- 平滑的鼠标移动（不是即时跳跃）

## 要求

- Python 3.11+
- pyautogui（已安装✅）
- 枕头（已安装✅）

## 尖端

- 始终先截图以查看当前状态
- 坐标是绝对的（不相对于窗口）
- 点击后短暂等待 UI 更新
- 尽可能使用“ctrl+z”友好操作

---

**状态：** ✅ 准备使用（v2.0 - 对话框和 UI 元素）
**创建时间：** 2026-02-01
**更新时间：** 2026-02-02
