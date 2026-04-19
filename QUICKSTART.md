# ⚡ 5 分钟快速开始

## 🎯 目标
在 5 分钟内运行 Simple Agent Demo，看到 ReAct 模式 AI Agent 的工作过程。

## 📋 前置条件
- Python 3.9+
- Anthropic API Key（从 https://console.anthropic.com 获取）

## 🚀 快速开始步骤

### 第 1 步：准备（1 分钟）

**Windows:**
```bash
cd C:\Users\PC\simple-agent-demo
run.bat
```

**Mac/Linux:**
```bash
cd /c/Users/PC/simple-agent-demo
bash run.sh
```

脚本会自动：
- ✅ 创建虚拟环境
- ✅ 安装依赖
- ✅ 启动应用

### 第 2 步：配置 API Key（1 分钟）

如果 run 脚本提示需要配置：

1. 用文本编辑器打开 `.env` 文件
2. 找到这一行：`ANTHROPIC_API_KEY=sk-your-api-key-here`
3. 替换为你的真实 API Key
4. 保存文件
5. 重新运行启动脚本

### 第 3 步：打开浏览器（1 分钟）

访问：**http://localhost:5000**

你应该看到：
```
🤖 Simple Agent Demo
基于 LangGraph 的 ReAct 模式 AI Agent
```

### 第 4 步：尝试提问（2 分钟）

点击示例问题或输入自己的问题：

#### 示例 1：计算（最简单）
```
输入：计算 2 + 2 * 5
```
你会看到 Agent 的执行过程：
```
Thought: 用户要求计算数学表达式
Action: calculate
Action Input: {"expression": "2 + 2 * 5"}
Observation: 2 + 2 * 5 = 12
Final Answer: 2 + 2 * 5 = 12
```

#### 示例 2：天气
```
输入：北京的天气怎么样
```

#### 示例 3：翻译
```
输入：翻译 Hello World 为中文
```

#### 示例 4：时间
```
输入：现在几点了
```

## 🎓 理解执行过程

在界面右侧"执行过程"选项卡，你会看到 Agent 的完整思考过程：

```
┌─────────────────────────────────────┐
│ Step 1:                              │
│ Thought: Agent 的思考               │
│ Action: 选择的工具                  │
│ Action Input: 工具的参数            │
│ Observation: 工具执行结果           │
│ Final Answer: 最终答案              │
└─────────────────────────────────────┘
```

这就是 **ReAct (Reasoning + Acting) 模式**！

## 📊 界面说明

### 左侧 - 对话区
- 输入框：输入你的问题
- 消息区：显示对话内容

### 右侧 - 信息面板

**执行过程**：显示 Agent 的思考和工具调用
```
Thought → Action → Observation → Final Answer
```

**对话历史**：所有之前的对话
```
👤 用户: 你的问题
🤖 Agent: Agent 的回答
```

**统计数据**：
```
总对话数: X
对话摘要: Y
```

## 🛠️ 5 个可用工具

| 工具 | 例子 |
|------|------|
| 计算 | "计算 10 / 2" |
| 天气 | "上海的天气" |
| 搜索 | "搜索 Python" |
| 翻译 | "翻译 Good morning 为中文" |
| 时间 | "现在几点" |

## 💾 数据存储

所有对话自动保存到 `memory.json`：
```json
{
  "conversations": [
    {
      "timestamp": "2026-04-19T10:30:00",
      "user": "计算 2 + 2",
      "assistant": "2 + 2 = 4"
    }
  ]
}
```

点击"清空历史"可以清空所有数据。

## 🐛 遇到问题？

### Q: "API Key 无效"
**A:** 
- 检查 .env 文件中的 API Key 是否正确
- 访问 https://console.anthropic.com 确认 API Key 有效
- 重新启动应用

### Q: "无法连接到服务器"
**A:**
- 确保应用仍在运行（检查终端窗口）
- 尝试访问 http://localhost:5000/health
- 如果显示 {"status": "ok"} 表示服务器正常

### Q: "Agent 很慢"
**A:**
- 第一次请求会比较慢（API 调用需要时间）
- 这是正常的，通常需要 5-10 秒
- 之后会变快

## 📚 下一步

理解代码后，你可以：

1. **添加新工具**（编辑 `tools.py`）
   ```python
   def my_tool(param: str) -> str:
       return "结果"
   ```

2. **修改 Agent Prompt**（编辑 `agent.py`）
   改变 Agent 的思考方式

3. **自定义 UI**（编辑 `static/` 中的文件）
   改变前端界面

4. **数据分析**（查看 `memory.json`）
   分析 Agent 的对话模式

## 🎉 恭喜！

你已经成功运行了一个基于 LangGraph 的 ReAct Agent！

**接下来：**
- 📖 阅读 README.md 了解更多细节
- 🔍 查看源代码理解实现细节
- 🚀 尝试扩展和自定义

---

**遇到问题？**
- 检查终端错误信息
- 查看 README.md 的常见问题部分
- 检查 Agent 的执行过程（可能会显示具体错误）

祝你使用愉快！🎊
