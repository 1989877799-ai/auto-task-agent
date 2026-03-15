import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(recipient_email: str, subject: str, body: str) -> str:
    """
    发送电子邮件到指定地址。
    """
    # 从环境变量获取配置
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not all([smtp_server, sender_email, sender_password]):
        return "邮件发送失败：Agent 未正确配置邮箱环境变量 (SMTP_SERVER, SENDER_EMAIL, SENDER_PASSWORD)。"

    try:
        # 构建邮件内容
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # 将正文作为纯文本/Markdown 附加到邮件中
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 连接到 SMTP 服务器并发送
        # 这里默认使用 SSL 加密连接 (465 端口)，这是目前主流邮箱的标准
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        return f"成功！邮件已发送至 {recipient_email}，主题为：{subject}"
        
    except Exception as e:
        return f"邮件发送遇到不可预知的错误: {str(e)}"