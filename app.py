"""Flask 应用"""
import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from agent import SimpleAgent
from memory import Memory

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# 初始化
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("请设置 ANTHROPIC_API_KEY 环境变量")

agent = SimpleAgent(api_key=api_key)
memory = Memory()

# 存储对话历史
conversation_history = []


@app.route("/")
def index():
    """主页"""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Chat 端点"""
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "消息不能为空"}), 400

        # 运行 Agent
        result = agent.run(user_input, conversation_history)

        # 保存对话
        memory.save_conversation(user_input, result["final_answer"])
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": result["final_answer"]})

        # 只保留最近 10 条消息
        if len(conversation_history) > 10:
            conversation_history.pop(0)
            conversation_history.pop(0)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    try:
        conversations = memory.get_conversations(limit=10)
        return jsonify({
            "success": True,
            "conversations": conversations
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """获取统计"""
    try:
        stats = memory.get_stats()
        return jsonify({
            "success": True,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear_memory():
    """清空记忆"""
    try:
        memory.clear()
        global conversation_history
        conversation_history = []
        return jsonify({"success": True, "message": "已清空所有记忆"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
