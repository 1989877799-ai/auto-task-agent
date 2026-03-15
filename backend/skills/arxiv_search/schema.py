# backend/skills/arxiv_search/schema.py

ARXIV_SEARCH_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_arxiv",
        "description": "搜索 Arxiv 论文数据库。当你需要查找最新的学术文献、论文或研究背景时，必须调用此工具。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词，请使用英文，例如 'large language models' 或 'ReAct agent'"
                },
                "max_results": {
                    "type": "integer",
                    "description": "返回的最大论文数量，默认为 3，最大不超过 5"
                }
            },
            "required": ["query"]
        }
    }
}