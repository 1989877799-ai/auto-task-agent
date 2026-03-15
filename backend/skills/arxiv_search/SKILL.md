# Skill: Arxiv Search (学术论文搜索)

## 简介
该技能允许 Agent 自动查询 Arxiv 开放数据库，获取相关领域最新的学术论文标题和摘要。主要用于“学术调研”、“文献综述”等复杂任务节点。

## 技术实现
- **依赖库**: 纯 Python 标准库 (`urllib`, `xml.etree`)，无第三方依赖。
- **接口**: Arxiv Public API (`http://export.arxiv.org/api/query`)

## 输入参数 (Schema)
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `query` | `string` | 是 | 搜索关键词（推荐使用英文） |
| `max_results`| `integer`| 否 | 返回条数（默认 3） |

## 输出格式
返回格式化后的纯文本字符串，包含论文编号、标题和摘要，各篇论文之间使用 `---` 分隔，专为 LLM 的上下文窗口优化阅读体验。