"""LangGraph Agent 实现 - ReAct 模式"""
import re
import json
from typing import Dict, List, Any, TypedDict
from langgraph.graph import StateGraph, END
from anthropic import Anthropic
from tools import execute_tool, TOOLS, get_tools_prompt


class AgentState(TypedDict):
    input: str
    messages: List[Dict[str, str]]
    scratchpad: str
    final_answer: str
    tools_used: List[Dict[str, Any]]
    step: int


class SimpleAgent:

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.max_iterations = 5

    def _format_scratchpad(self, scratchpad: str) -> str:
        """格式化思考过程"""
        return scratchpad

    def think(self, state: AgentState) -> AgentState:
        """思考阶段"""
        messages = state["messages"] + [{"role": "user", "content": state["input"]}]

        prompt = f"""你是一个助手，使用 ReAct (Reasoning + Acting) 模式工作。

{get_tools_prompt()}

当前对话历史:
{json.dumps(state['messages'][-5:], ensure_ascii=False)}

用户问题: {state['input']}

当前思考过程:
{state['scratchpad']}

请按照以下格式思考和行动:

Thought: [你的分析]
Action: [工具名称]
Action Input: [JSON 格式的参数]

如果没有需要的工具，直接给出最终答案:
Final Answer: [答案]

请只输出一个 Thought/Action 组合或 Final Answer。"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        thought_text = response.content[0].text
        state["scratchpad"] += f"\nStep {state['step']}:\n{thought_text}"

        return state

    def act(self, state: AgentState) -> AgentState:
        scratchpad = state["scratchpad"]

        # 检查是否已有最终答案
        if "Final Answer:" in scratchpad:
            return state

        # 提取 Action 和 Action Input
        action_match = re.search(r'Action:\s*(\w+)', scratchpad)
        input_match = re.search(r'Action Input:\s*({.*?})', scratchpad, re.DOTALL)

        if action_match and input_match:
            tool_name = action_match.group(1)
            try:
                tool_input = json.loads(input_match.group(1))
                result = execute_tool(tool_name, **tool_input)

                state["scratchpad"] += f"\nObservation: {result}"
                state["tools_used"].append({
                    "tool": tool_name,
                    "input": tool_input,
                    "output": result
                })
                state["step"] += 1
            except json.JSONDecodeError as e:
                state["scratchpad"] += f"\nObservation: JSON 解析错误: {str(e)}"

        return state

    def conclude(self, state: AgentState) -> AgentState:
        if "Final Answer:" in state["scratchpad"]:
            # 提取已有的最终答案
            match = re.search(r'Final Answer:\s*(.+?)(?:\n|$)', state["scratchpad"], re.DOTALL)
            if match:
                state["final_answer"] = match.group(1).strip()
        else:
            # 生成最终答案
            prompt = f"""基于以下对话和思考过程，生成一个清晰的最终答案:

用户问题: {state['input']}

思考过程:
{state['scratchpad']}

请提供最终答案:"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

            state["final_answer"] = response.content[0].text

        return state

    def should_continue(self, state: AgentState) -> str:
        if "Final Answer:" in state["scratchpad"] or state["step"] >= self.max_iterations:
            return "end"
        return "continue"

    def build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("think", self.think)
        workflow.add_node("act", self.act)
        workflow.add_node("conclude", self.conclude)

        workflow.add_edge("think", "act")
        workflow.add_conditional_edges(
            "act",
            self.should_continue,
            {"continue": "think", "end": "conclude"}
        )
        workflow.add_edge("conclude", END)

        workflow.set_entry_point("think")
        return workflow.compile()

    def run(self, user_input: str, messages: List[Dict[str, str]] = None) -> Dict[str, Any]:
        if messages is None:
            messages = []

        initial_state: AgentState = {
            "input": user_input,
            "messages": messages,
            "scratchpad": "",
            "final_answer": "",
            "tools_used": [],
            "step": 1
        }

        graph = self.build_graph()
        final_state = graph.invoke(initial_state)

        return {
            "input": user_input,
            "scratchpad": final_state["scratchpad"],
            "final_answer": final_state["final_answer"],
            "tools_used": final_state["tools_used"]
        }
