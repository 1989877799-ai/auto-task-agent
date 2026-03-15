# 🤖 Auto-Task Agent: 基于 ReAct 架构的轻量级自主智能体

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-18.x-green)
![OpenAI API](https://img.shields.io/badge/LLM-OpenAI%20%2F%20DeepSeek-orange)
![License](https://img.shields.io/badge/License-MIT-success)

## 📖 项目简介

**Auto-Task Agent** 是一个从零手写（From Scratch）的轻量级自主任务智能体。本项目摒弃了 LangChain 等厚重框架，直接基于大模型原生 Function Calling 能力构建了底层的 **ReAct (Reasoning + Acting)** 状态机循环。

它可以根据用户的自然语言指令，自主进行任务拆解、逻辑推理，并动态调用本地工具库（Skills）来完成复杂的闭环任务（如：自动化前沿学术检索、总结并发送邮件报告）。

### ✨ 核心技术亮点 (Why this project?)

- 🧠 **纯手写 ReAct 核心引擎**：自主管理 `Thought -> Action -> Observation` 上下文链路，精准控制迭代深度，展现对 Agent 底层调度逻辑的深刻理解。
- 🔌 **极致解耦的 Skill 架构**：基于大模型 JSON Schema 与 Python `**kwargs` 动态解包技术，实现调度中心与底层业务逻辑的完全解耦。新增技能符合**开闭原则 (OCP)**，核心引擎零修改。
- 🌐 **跨语言微服务设计**：后端采用 Python 驱动核心 Agent，前端通过 Node.js (Express) 构建轻量级 API Gateway，通过 IPC 进程间通信实现流式调度。
- 📦 **工业级工程规范**：每个 Skill 均作为独立模块封装，配备完善的 `SKILL.md` 文档与 Pytest 单元测试，具备极强的可插拔性和扩展性。

---

## 🏗️ 项目架构与目录树

```text
auto-task-agent/
├── backend/                  # 🐍 Python 核心引擎层
│   ├── core/                 # 调度大脑
│   │   └── agent.py          # ReAct 循环与动态 Tool Calling 实现
│   ├── skills/               # 独立技能挂载区
│   │   ├── arxiv_search/     # Skill: 学术论文检索 (XML解析)
│   │   └── email_sender/     # Skill: SMTP 邮件自动发送
│   ├── main.py               # 后端进程入口
│   └── requirements.txt      # Python 依赖清单
├── gateway/                  # 🟢 Node.js API 网关层
│   ├── index.js              # Express 服务与子进程调度
│   └── package.json
└── README.md
🚀 快速开始 (Quick Start)
1. 克隆项目
Bash

git clone [https://github.com/YOUR_USERNAME/auto-task-agent.git](https://github.com/YOUR_USERNAME/auto-task-agent.git)
cd auto-task-agent
2. 配置环境变量
在项目根目录下创建 .env 文件，并填入以下配置（请不要将真实的 API Key 提交到版本库）：

Code snippet

# 大模型 API 配置 (支持 OpenAI 或兼容接口如 DeepSeek)
OPENAI_API_KEY=your_api_key_here
BASE_URL=[https://api.deepseek.com/v1](https://api.deepseek.com/v1)  # 可选，使用兼容接口时配置

# 邮件发送技能配置 (SMTP 授权码)
SMTP_SERVER=smtp.qq.com
SMTP_PORT=465
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_smtp_auth_code
3. 初始化 Python 核心引擎
Bash

cd backend
python -m venv venv
source venv/bin/activate  # Windows 用户使用 venv\Scripts\activate
pip install -r requirements.txt
4. 启动 Node.js API 网关
打开一个新的终端窗口：

Bash

cd gateway
npm install
node index.js
服务将在 http://localhost:3000 启动。

🎯 使用用例 (Demo)
向网关发送一个包含复合任务意图的 POST 请求，观察 Agent 是如何自主思考并连续调用工具的：

Bash

curl -X POST http://localhost:3000/api/task \
-H "Content-Type: application/json" \
-d '{"prompt": "帮我调研一下关于 Agentic Workflow 的最新论文，提取摘要。然后把这份报告发送到 test@example.com，邮件标题叫《AI前沿追踪》。"}'
Agent 内部执行流示例：

[Thought] 需要先检索论文库...

[Action] 动态路由调用 search_arxiv...

[Observation] 获取 XML 数据并解析摘要...

[Thought] 资料已就绪，准备发送邮件...

[Action] 动态解包调用 send_email...

[Final Answer] 整合执行结果返回给用户！

🛠️ 未来规划 (TODO)
[x] 搭建基础 ReAct 循环与网关通信

[x] 实现 arxiv_search 与 email_sender 基础技能

[ ] 增加 web_scraper 技能，支持通用网页信息抓取

[ ] 引入轻量级记忆机制 (Memory)，支持多轮对话上下文

[ ] 将 Python 脚本的输出改为 SSE (Server-Sent Events) 流式返回，提升网关响应体验

Created with ❤️ by [Your Name]. Open to Agentic AI Engineer opportunities!