import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def search_arxiv(query: str, max_results: int = 3) -> str:
    """
    搜索 Arxiv 论文数据库并返回相关论文的标题和摘要。
    """
    try:
        # 处理查询字符串中的空格等特殊字符
        safe_query = urllib.parse.quote(query)
        url = f'http://export.arxiv.org/api/query?search_query=all:{safe_query}&start=0&max_results={max_results}'
        
        # 发送请求
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        
        # 解析 XML
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'} # Arxiv 的 XML 命名空间
        
        entries = root.findall('atom:entry', ns)
        if not entries:
            return "未找到相关论文，请尝试更换搜索关键词。"
        
        results = []
        for i, entry in enumerate(entries, 1):
            # 提取并清理文本（去除多余的换行符）
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            results.append(f"[{i}] 标题: {title}\n    摘要: {summary}\n")
            
        return "\n---\n".join(results)
        
    except Exception as e:
        return f"Arxiv 搜索接口调用失败: {str(e)}"