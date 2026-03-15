EMAIL_SENDER_SCHEMA = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "发送电子邮件给指定收件人。当你完成了报告生成、总结或其他任务，并且用户要求将结果发送到某个邮箱时，必须调用此工具。",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient_email": {
                    "type": "string",
                    "description": "收件人的标准电子邮件地址，例如 'user@example.com'"
                },
                "subject": {
                    "type": "string",
                    "description": "邮件的主题/标题，应简洁明了概括邮件内容"
                },
                "body": {
                    "type": "string",
                    "description": "邮件的正文内容。如果你要发送报告，请将完整的 Markdown 报告文本放在这里"
                }
            },
            "required": ["recipient_email", "subject", "body"]
        }
    }
}