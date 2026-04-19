"""JSON 内存管理"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any


class Memory:
    """使用 JSON 文件存储长期记忆"""

    def __init__(self, file_path: str = "memory.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({
                    "conversations": [],
                    "summaries": []
                }, f, ensure_ascii=False, indent=2)

    def save_conversation(self, user_input: str, agent_response: str):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": agent_response
        })

        # 只保留最新 20 条对话
        if len(data["conversations"]) > 20:
            data["conversations"] = data["conversations"][-20:]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_conversations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """获取最近的对话"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data["conversations"][-limit:]

    def add_summary(self, summary: str):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["summaries"].append({
            "timestamp": datetime.now().isoformat(),
            "summary": summary
        })

        # 只保留最新 10 条摘要
        if len(data["summaries"]) > 10:
            data["summaries"] = data["summaries"][-10:]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_context(self) -> str:
        """获取上下文用于 Agent"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        context = "最近的对话摘要:\n"
        for summary in data["summaries"][-3:]:
            context += f"- {summary['summary']}\n"

        return context if len(data["summaries"]) > 0 else ""

    def clear(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump({
                "conversations": [],
                "summaries": []
            }, f, ensure_ascii=False, indent=2)

    def get_stats(self) -> Dict[str, Any]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "total_conversations": len(data["conversations"]),
            "total_summaries": len(data["summaries"]),
            "latest_conversation": data["conversations"][-1] if data["conversations"] else None
        }
