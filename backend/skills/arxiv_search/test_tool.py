# backend/skills/arxiv_search/test_tool.py
from .tool import search_arxiv

def test_search_arxiv_success():
    # 测试常规搜索
    result = search_arxiv("ReAct Agent", max_results=2)
    
    # 断言返回结果不是错误信息
    assert "调用失败" not in result
    assert "未找到" not in result
    
    # 断言确实返回了标题和摘要的结构
    assert "标题:" in result
    assert "摘要:" in result

def test_search_arxiv_empty():
    # 测试一些绝对搜不到的乱码组合
    result = search_arxiv("asdfghjklqwertyuiop1234567890", max_results=1)
    assert "未找到相关论文" in result