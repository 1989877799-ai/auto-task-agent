import json
import os
from openai import OpenAI

# 1. 导入旧技能
from skills.arxiv_search.tool import search_arxiv
from skills.arxiv_search.schema import ARXIV_SEARCH_SCHEMA

# 2. 【新增】导入新技能
from skills.email_sender.tool import send_email
from skills.email_sender.schema import EMAIL_SENDER_SCHEMA

class AutoTaskAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("BASE_URL")
        )
        self.model = "deepseek-chat" # 或者 "deepseek-chat"
        
        # 3. 【修改】将新 Schema 加入工具箱
        self.tools = [
            ARXIV_SEARCH_SCHEMA,
            EMAIL_SENDER_SCHEMA  # <-- 新增这一行
        ]
        
        # 4. 【修改】注册工具路由，映射真实的 Python 函数
        self.available_functions = {
            "search_arxiv": search_arxiv,
            "send_email": send_email,    # <-- 新增这一行
        }
        
    # run() 方法的代码完全不需要改动！它会自动处理新的工具！


    def run(self, user_prompt: str) -> str:
        """
        核心的 ReAct 循环 (Reason + Act)
        """
        # 初始化 System Prompt 和用户的消息历史
        messages = [
            {"role": "system", "content": "你是一个严谨的学术调研Agent。请使用提供的工具来查找信息，并基于工具返回的结果生成结构化的Markdown报告。"},
            {"role": "user", "content": user_prompt}
        ]

        # 设置最大循环次数，防止大模型陷入死循环
        max_iterations = 5
        iteration = 0

        print(f"\n[Agent 启动] 收到任务: {user_prompt}\n")

        while iteration < max_iterations:
            iteration += 1
            print(f"--- 思考迭代 第 {iteration} 轮 ---")

            # 第 1 步：调用大模型，传入当前的对话历史和工具箱
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto" # 让大模型自己决定是否调用工具
            )
            
            response_message = response.choices[0].message
            
            # 第 2 步：检查大模型是否决定调用工具 (Tool Calling 机制)
            tool_calls = response_message.tool_calls

            if tool_calls:
                # 大模型决定调用工具，我们需要把它的这个“决定”也存入历史记录
                messages.append(response_message)
                
                # 第 3 步：遍历并执行所有工具调用 (处理 Action)
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = self.available_functions.get(function_name)
                    
                    if not function_to_call:
                        print(f"[错误] 大模型尝试调用未知的工具: {function_name}")
                        continue
                        
                    # 解析大模型生成的 JSON 参数
                    function_args = json.loads(tool_call.function.arguments)
                    print(f"[Action] 大模型请求调用工具: {function_name}, 参数: {function_args}")
                    
                    # 真正执行本地 Python 函数
                    function_response = function_to_call(**function_args)
                    print(f"[Observation] 工具执行完毕，获取到数据长度: {len(function_response)} 字符")
                    
                    # 第 4 步：将工具执行的结果拼接到对话历史中，作为下一次思考的上下文
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })
                
                # 工具执行完毕，进入下一轮 while 循环，大模型会基于 Observation 继续思考
                continue
                
            else:
                # 第 5 步：如果没有 tool_calls，说明大模型认为信息已经充足，输出了最终文本 (Final Answer)
                print("[Final Answer] Agent 思考完毕，生成最终回答。\n")
                return response_message.content

        return "抱歉，任务过于复杂，Agent 在达到最大循环次数后仍未完成。"