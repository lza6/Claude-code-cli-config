# 桌面控制 - 快速参考卡

## 🚀 立即开始

```python
from skills.desktop_control import DesktopController

dc = DesktopController()
```

## 🖱️ 鼠标控制（前 10 名）

```python
# 1. Move mouse
dc.move_mouse(500, 300, duration=0.5)

# 2. Click
dc.click(500, 300)  # Left click at position
dc.click()           # Click at current position

# 3. Right click
dc.right_click(500, 300)

# 4. Double click
dc.double_click(500, 300)

# 5. Drag & drop
dc.drag(100, 100, 500, 500, duration=1.0)

# 6. Scroll
dc.scroll(-5)  # Scroll down 5 clicks

# 7. Get position
x, y = dc.get_mouse_position()

# 8. Move relative
dc.move_relative(100, 50)  # Move 100px right, 50px down

# 9. Smooth movement
dc.move_mouse(1000, 500, duration=1.0, smooth=True)

# 10. Middle click
dc.middle_click()
```

## ⌨️ 键盘控制（前 10 名）

```python
# 1. Type text (instant)
dc.type_text("Hello World")

# 2. Type text (human-like, 60 WPM)
dc.type_text("Hello World", wpm=60)

# 3. Press key
dc.press('enter')
dc.press('tab')
dc.press('escape')

# 4. Hotkeys (shortcuts)
dc.hotkey('ctrl', 'c')      # Copy
dc.hotkey('ctrl', 'v')      # Paste  
dc.hotkey('ctrl', 's')      # Save
dc.hotkey('win', 'r')       # Run dialog
dc.hotkey('alt', 'tab')     # Switch window

# 5. Hold & release
dc.key_down('shift')
dc.type_text("hello")  # Types "HELLO"
dc.key_up('shift')

# 6. Arrow keys
dc.press('up')
dc.press('down')
dc.press('left')
dc.press('right')

# 7. Function keys
dc.press('f5')  # Refresh

# 8. Multiple presses
dc.press('backspace', presses=5)

# 9. Special keys
dc.press('home')
dc.press('end')
dc.press('pagedown')
dc.press('delete')

# 10. Fast combo
dc.hotkey('ctrl', 'alt', 'delete')
```

## 📸 屏幕操作（前 5 名）

```python
# 1. Screenshot (full screen)
img = dc.screenshot()
dc.screenshot(filename="screen.png")

# 2. Screenshot (region)
img = dc.screenshot(region=(100, 100, 800, 600))

# 3. Get pixel color
r, g, b = dc.get_pixel_color(500, 300)

# 4. Find image on screen
location = dc.find_on_screen("button.png")

# 5. Get screen size
width, height = dc.get_screen_size()
```

## 🪟 窗口管理（前 5 名）

```python
# 1. Get all windows
windows = dc.get_all_windows()

# 2. Activate window
dc.activate_window("Chrome")

# 3. Get active window
active = dc.get_active_window()

# 4. List windows
for title in dc.get_all_windows():
    print(title)

# 5. Switch to app
dc.activate_window("Visual Studio Code")
```

## 📋 剪贴板（前 2 个）

```python
# 1. Copy to clipboard
dc.copy_to_clipboard("Hello!")

# 2. Get from clipboard
text = dc.get_from_clipboard()
```

## 🔥 现实世界的例子

### 示例 1：自动填写表格
```python
dc.click(300, 200)  # Name field
dc.type_text("John Doe", wpm=80)
dc.press('tab')
dc.type_text("john@email.com", wpm=80)
dc.press('tab')
dc.type_text("Password123", wpm=60)
dc.press('enter')
```

### 示例 2：复制粘贴自动化
```python
# Select all
dc.hotkey('ctrl', 'a')
# Copy
dc.hotkey('ctrl', 'c')
# Wait
dc.pause(0.5)
# Switch window
dc.hotkey('alt', 'tab')
# Paste
dc.hotkey('ctrl', 'v')
```

### 示例 3：文件操作
```python
# Select multiple files
dc.key_down('ctrl')
dc.click(100, 200)
dc.click(100, 250)
dc.click(100, 300)
dc.key_up('ctrl')
# Copy
dc.hotkey('ctrl', 'c')
```

### 示例 4：屏幕截图工作流程
```python
# Take screenshot
dc.screenshot(filename=f"capture_{time.time()}.png")
# Open in Paint
dc.hotkey('win', 'r')
dc.pause(0.5)
dc.type_text('mspaint')
dc.press('enter')
```

### 示例 5：搜索和替换
```python
# Open Find & Replace
dc.hotkey('ctrl', 'h')
dc.pause(0.3)
# Type find text
dc.type_text("old_text")
dc.press('tab')
# Type replace text
dc.type_text("new_text")
# Replace all
dc.hotkey('alt', 'a')
```

## ⚙️ 配置

```python
# With failsafe (move to corner to abort)
dc = DesktopController(failsafe=True)

# With approval mode (ask before each action)
dc = DesktopController(require_approval=True)

# Maximum speed (no safety checks)
dc = DesktopController(failsafe=False)
```

## 🛡️ 安全

```python
# Check if safe to continue
if dc.is_safe():
    dc.click(500, 500)

# Pause execution
dc.pause(2.0)  # Wait 2 seconds

# Emergency abort: Move mouse to any screen corner
```

## 🎯 专业提示

1. **即时输入**：`interval=0` 或 `wpm=None`
2. **人工打字**：`wpm=60`（60 个字/分钟）
3. **平滑鼠标**：`duration=0.5，smooth=True`
4. **即时鼠标**: `duration=0`
5. **等待 UI**：操作之间的 `dc.pause(0.5)`
6. **故障安全**：始终启用以确保安全
7. **先测试**：使用`demo.py`来测试功能
8. **坐标**：使用`get_mouse_position()`来找到它们
9. **屏幕截图**：捕获之前/之后进行验证
10. **热键>菜单**：更快、更可靠

## 📦 依赖关系

```bash
pip install pyautogui pillow opencv-python pygetwindow pyperclip
```

## 🚨 常见问题

**鼠标无法正确移动？**
- 检查 Windows 设置中的 DPI 缩放
- 使用“get_mouse_position()”验证坐标

**键盘无法使用？**
- 确保目标应用程序具有焦点
- 某些应用程序会阻止自动化（游戏、安全应用程序）

**故障安全触发？**
- 让鼠标远离屏幕角落
- 如果需要禁用：`failsafe=False`

---

**专为 OpenClaw 打造** 🦞 - 桌面自动化变得简单！
