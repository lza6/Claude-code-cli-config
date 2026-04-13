# AI Desktop Agent - 认知自动化指南

## 🤖 这是什么？

**AI 桌面代理**是基本桌面控制之上的一个智能层，它**理解**您想要什么，并弄清楚如何自主地完成它。

与需要精确指令的基本自动化不同，AI 代理：
- **理解自然语言**（“在画图中画一只猫”）
- **自动计划步骤**
- **自主执行** 
- **根据所看到的内容进行调整**

---

## 🎯 它能做什么？

### ✅ 自主绘图
```python
from skills.desktop_control.ai_agent import AIDesktopAgent

agent = AIDesktopAgent()

# Just describe what you want!
agent.execute_task("Draw a circle in Paint")
agent.execute_task("Draw a star in MS Paint")
agent.execute_task("Draw a house with a sun")
```

**它的作用：**
1. 打开 MS Paint
2.选择铅笔工具
3. 弄清楚如何绘制所需的形状
4. 自主绘制
5.结果截图

### ✅ 自主文本输入
```python
# It figures out where to type
agent.execute_task("Type 'Hello World' in Notepad")
agent.execute_task("Write an email saying thank you")
```

**它的作用：**
1. 打开记事本（或找到活动文本编辑器）
2. 自然地输入文本
3. 需要时的格式

### ✅ 自主应用程序控制
```python
# It knows how to open apps
agent.execute_task("Open Calculator")
agent.execute_task("Launch Microsoft Paint")
agent.execute_task("Open File Explorer")
```

### ✅ 自主游戏（高级）
```python
# It will try to play the game!
agent.execute_task("Play Solitaire for me")
agent.execute_task("Play Minesweeper")
```

**它的作用：**
1.分析游戏画面
2.检测游戏状态（卡牌、地雷等）
3. 决定最佳行动
4. 执行移动
5. 重复直到赢/输

---

## 🏗️ 它是如何运作的

＃＃＃ 建筑学

```
User Request ("Draw a cat")
    ↓
Natural Language Understanding
    ↓
Task Planning (Step-by-step plan)
    ↓
Step Execution Loop:
    - Observe Screen (Computer Vision)
    - Decide Action (AI Reasoning)
    - Execute Action (Desktop Control)
    - Verify Result
    ↓
Task Complete!
```

### 关键组件

1. **任务规划器** - 将高级任务分解为步骤
2. **视觉系统** - 了解屏幕上的内容（屏幕截图、OCR、物体检测）
3. **推理引擎** - 决定下一步做什么
4. **动作执行器** - 执行实际的鼠标/键盘动作
5. **反馈循环** - 验证操作是否成功

---

## 📋 支持的任务（当前）

### 第 1 层：全自动 ✅

|任务模式|示例|状态 |
|-------------|---------|---------|
|在“画图”中绘制形状 | “画一个圆”| ✅ 工作 |
|基本文本输入 | “输入你好” | ✅ 工作 |
|启动应用程序 | “打开油漆”| ✅ 工作 |

### 第 2 层：部分自动化 🔨

|任务模式|示例|状态 |
|-------------|---------|---------|
|表格填写 | “填写此表格”| 🔨 进行中 |
|文件操作 | “复制这些文件”| 🔨 进行中 |
|网页导航| “在 Google 上查找”| 🔨 计划 |

### 第 3 层：实验性 🧪

|任务模式|示例|状态 |
|-------------|---------|---------|
|游戏玩法| “玩纸牌”| 🧪 实验 |
|图像编辑 | “调整这张照片的大小” | 🧪 计划 |
|代码编辑| “修复此错误” | 🧪 研究 |

---

## 🎨 示例：在 Paint 中绘图

### 简单请求
```python
agent = AIDesktopAgent()
result = agent.execute_task("Draw a circle in Paint")

# Check result
print(f"Status: {result['status']}")
print(f"Steps taken: {len(result['steps'])}")
```

### 幕后发生了什么

**1.规划阶段：**
```
Plan generated:
  Step 1: Launch MS Paint
  Step 2: Wait 2s for Paint to load
  Step 3: Activate Paint window
  Step 4: Select pencil tool (press 'P')
  Step 5: Draw circle at canvas center
  Step 6: Screenshot the result
```

**2.执行阶段：**
```
[✓] Launched Paint via Win+R → mspaint
[✓] Waited 2.0s
[✓] Activated window "Paint"
[✓] Pressed 'P' to select pencil
[✓] Drew circle with 72 points
[✓] Screenshot saved: drawing_result.png
```

**3.结果：**
```python
{
    "task": "Draw a circle in Paint",
    "status": "completed",
    "success": True,
    "steps": [... 6 steps ...],
    "screenshots": [... 6 screenshots ...],
}
```

---

## 🎮 示例：玩游戏

```python
agent = AIDesktopAgent()

# Play a simple game
result = agent.execute_task("Play Solitaire for me")
```

### 游戏循环

```
1. Analyze screen → Detect cards, positions
2. Identify valid moves → Find legal plays
3. Evaluate moves → Which is best?
4. Execute move → Click and drag card
5. Repeat until game ends
```

### 游戏特定情报

代理可以学习以下模式：
- **纸牌**：纸牌堆叠规则、花色搭配
- **扫雷**：概率计算，安全点击
- **2048**：平铺合并策略
- **国际象棋**（如果与引擎集成）：移动评估

---

## 🧠 增强人工智能

### 添加应用知识

```python
# In ai_agent.py, add to app_knowledge:

self.app_knowledge = {
    "photoshop": {
        "name": "Adobe Photoshop",
        "launch_command": "photoshop",
        "common_actions": {
            "new_layer": {"hotkey": ["ctrl", "shift", "n"]},
            "brush_tool": {"hotkey": ["b"]},
            "eraser": {"hotkey": ["e"]},
        }
    }
}
```

### 添加自定义任务模式

```python
# Add a custom planning method
def _plan_photo_edit(self, task: str) -> List[Dict]:
    """Plan for photo editing tasks."""
    return [
        {"type": "launch_app", "app": "photoshop"},
        {"type": "wait", "duration": 3.0},
        {"type": "open_file", "path": extracted_path},
        {"type": "apply_filter", "filter": extracted_filter},
        {"type": "save_file"},
    ]
```

---

## 🔥 进阶：视觉+推理

### 屏幕分析

代理可以分析屏幕截图以：
- **检测 UI 元素**（按钮、文本字段、菜单）
- **阅读文本**（标签、说明的 OCR）
- **识别对象**（图标、图像、游戏片段）
- **了解布局**（东西在哪里）

```python
# Analyze what's on screen
analysis = agent._analyze_screen()

print(analysis)
# Output:
# {
#     "active_window": "Untitled - Paint",
#     "mouse_position": (640, 480),
#     "detected_elements": [...],
#     "text_found": [...],
# }
```

### 与 OpenClaw LLM 集成

```python
# Future: Use OpenClaw's LLM for reasoning
agent = AIDesktopAgent(llm_client=openclaw_llm)

# The agent can now:
# - Reason about complex tasks
# - Understand context better
# - Plan more sophisticated workflows
# - Learn from feedback
```

---

## 🛠️ 满足您的需求扩展

### 添加对新应用程序的支持

1. **识别应用程序**
2. **记录常见操作**
3. **添加到知识库**
4. **创建计划方法**

示例：添加 Excel 支持

```python
# Step 1: Add to app_knowledge
"excel": {
    "name": "Microsoft Excel",
    "launch_command": "excel",
    "common_actions": {
        "new_sheet": {"hotkey": ["shift", "f11"]},
        "sum_formula": {"action": "type", "text": "=SUM()"},
    }
}

# Step 2: Create planner
def _plan_excel_task(self, task: str) -> List[Dict]:
    return [
        {"type": "launch_app", "app": "excel"},
        {"type": "wait", "duration": 2.0},
        # ... specific Excel steps
    ]

# Step 3: Hook into main planner
if "excel" in task_lower or "spreadsheet" in task_lower:
    return self._plan_excel_task(task)
```

---

## 🎯 现实世界用例

### 1. 自动填写表格
```python
agent.execute_task("Fill out the job application with my resume data")
```

### 2. 批量图像处理
```python
agent.execute_task("Resize all images in this folder to 800x600")
```

### 3. 社交媒体发布
```python
agent.execute_task("Post this image to Instagram with caption 'Beautiful sunset'")
```

### 4. 数据输入
```python
agent.execute_task("Copy data from this PDF to Excel spreadsheet")
```

### 5. 测试
```python
agent.execute_task("Test the login form with invalid credentials")
```

---

## ⚙️ 配置

### 启用/禁用故障保护
```python
# Safe mode (default)
agent = AIDesktopAgent(failsafe=True)

# Fast mode (no failsafe)
agent = AIDesktopAgent(failsafe=False)
```

### 设置最大步数
```python
# Prevent infinite loops
result = agent.execute_task("Play game", max_steps=100)
```

### 访问操作历史记录
```python
# Review what the agent did
print(agent.action_history)
```

---

## 🐛 调试

### 查看逐步执行
```python
result = agent.execute_task("Draw a star in Paint")

for i, step in enumerate(result['steps'], 1):
    print(f"Step {i}: {step['step']['description']}")
    print(f"  Success: {step['success']}")
    if 'error' in step:
        print(f"  Error: {step['error']}")
```

### 查看截图
```python
# Each step captures before/after screenshots
for screenshot_pair in result['screenshots']:
    before = screenshot_pair['before']
    after = screenshot_pair['after']
    
    # Display or save for analysis
    before.save(f"step_{screenshot_pair['step']}_before.png")
    after.save(f"step_{screenshot_pair['step']}_after.png")
```

---

## 🚀 未来的增强

计划的功能：

- [ ] **计算机视觉**：OCR、对象检测、UI 元素识别
- [ ] **LLM 集成**：使用 OpenClaw LLM 进行自然语言理解
- [ ] **学习**：记住成功的模式，随着时间的推移不断改进
- [ ] **多应用程序工作流程**：“从 Chrome 获取数据并放入 Excel”
- [ ] **语音控制**：“Alexa，在画图中画一只猫”
- [ ] **自主调试**：自动修复错误
- [ ] **游戏人工智能**：玩游戏的强化学习
- [ ] **Web 自动化**：通过理解实现完全浏览器控制

---

## 📚 完整 API

### 主要方法

```python
# Execute a task
result = agent.execute_task(task: str, max_steps: int = 50)

# Analyze screen
analysis = agent._analyze_screen()

# Manual mode: Execute individual steps
step = {"type": "launch_app", "app": "paint"}
result = agent._execute_step(step)
```

### 结果结构

```python
{
    "task": str,                    # Original task
    "status": str,                  # "completed", "failed", "error"
    "success": bool,                # Overall success
    "steps": List[Dict],            # All steps executed
    "screenshots": List[Dict],      # Before/after screenshots
    "failed_at_step": int,          # If failed, which step
    "error": str,                   # Error message if failed
}
```

---

**🦞 Built for OpenClaw - The future of desktop automation!**
