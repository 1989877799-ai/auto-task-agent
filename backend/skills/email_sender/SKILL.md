# Skill: Email Sender (邮件发送器)

## 简介
赋予 Agent 通过 SMTP 协议向外部发送电子邮件的能力。常用于任务流的最终节点（如：调研完毕后自动发送报告）。

## 技术实现
- **依赖库**: Python 纯标准库 (`smtplib`, `email.mime`)。
- **协议**: SMTP_SSL (默认端口 465)。

## 环境变量要求
使用此工具前，必须在 `.env` 中配置：
- `SMTP_SERVER`
- `SMTP_PORT`
- `SENDER_EMAIL`
- `SENDER_PASSWORD` (SMTP 授权码)

## 输入参数 (Schema)
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `recipient_email` | `string` | 是 | 目标收件人地址 |
| `subject`| `string`| 是 | 邮件主题 |
| `body`| `string`| 是 | 邮件正文（支持较长的 Markdown 文本） |