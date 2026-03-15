import os
import sys
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.agent import AutoTaskAgent

def main():
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("DEEPSEEK_API_KEY"):
        print("错误：请先配置 API_KEY。")
        sys.exit(1)

    agent = AutoTaskAgent()
    
    # 获取命令行传入的参数作为任务，如果没有则使用默认任务
    if len(sys.argv) > 1:
        task = sys.argv[1]
    else:
        task = "请帮我调研一下 'ReAct Agent Architecture' 的最新进展。搜索 2 篇相关论文并总结。"
    
    final_report = agent.run(task)
    
    # 纯净输出最终结果，方便 Node.js 捕获
    print(final_report)

if __name__ == "__main__":
    main()