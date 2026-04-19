"""Agent 工具定义"""
import json
import math
from datetime import datetime
from typing import Any


def get_weather(city: str) -> str:
    """获取天气（模拟）"""
    weather_data = {
        "北京": "晴，23°C",
        "上海": "多云，21°C",
        "深圳": "晴，25°C",
        "广州": "多云，24°C",
        "杭州": "晴，20°C",
    }
    return weather_data.get(city, f"{city}的天气数据暂不可用")

def search(query: str) -> str:
    """网络搜索（模拟）"""
    search_results = {
        "python": "Python 是一种高级编程语言，以简洁易读著称。",
        "ai": "人工智能(AI)是计算机科学的重要分支。",
        "机器学习": "机器学习是AI的核心技术，使计算机能从数据中学习。",
    }
    for key, value in search_results.items():
        if key in query.lower():
            return value
    return f"关于 '{query}' 的搜索结果：暂无结果"

def translate(text: str, target_lang: str = "中文") -> str:
    """文本翻译（模拟）"""
    translations = {
        ("hello", "中文"): "你好",
        ("world", "中文"): "世界",
        ("hello world", "中文"): "你好世界",
        ("good morning", "中文"): "早上好",
        ("thank you", "中文"): "谢谢你",
    }
    key = (text.lower(), target_lang)
    return translations.get(key, f"'{text}' 的 {target_lang} 翻译暂不可用")

def get_current_time() -> str:
    """获取当前时间"""
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M:%S")

def get_myname() -> str:
    """获取我的姓名"""
    str="叶晓忠"
    return str


# 工具定义字典
TOOLS = {
    "get_weather": {
        "function": get_weather,
        "description": "获取城市天气信息",
        "parameters": ["city"]
    },
    "search": {
        "function": search,
        "description": "搜索信息",
        "parameters": ["query"]
    },
    "translate": {
        "function": translate,
        "description": "翻译文本到指定语言",
        "parameters": ["text", "target_lang"]
    },
    "get_current_time": {
        "function": get_current_time,
        "description": "获取当前时间",
        "parameters": []
    },
    "get_myname": {
        "function": get_myname,
        "description": "获取我的姓名",
        "parameters": []
    }

}

def execute_tool(tool_name: str, **kwargs) -> str:
    """执行指定工具"""
    if tool_name not in TOOLS:
        return f"工具 {tool_name} 不存在"

    tool = TOOLS[tool_name]
    try:
        return tool["function"](**kwargs)
    except Exception as e:
        return f"执行 {tool_name} 出错: {str(e)}"

def get_tools_prompt() -> str:
    """获取工具描述用于 LLM"""
    prompt = "你可以使用以下工具:\n\n"
    for name, tool in TOOLS.items():
        prompt += f"- {name}: {tool['description']}\n"
    return prompt
