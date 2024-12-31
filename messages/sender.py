
"""
This module handles notification sending by email and Telegram.
"""

from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot
from config.config import get_env_var
from config.constants import EmailConfig, TelegramConfig
from database.database_handler import get_all_products_today
from messages.message_format import format_email_message, format_telegram_message


def send_email(subject, body):
    """
    Sends an email with the specified subject and body.
    """    
    from_email = get_env_var(EmailConfig.EMAIL_ACCOUNT.value)
    from_password = get_env_var(EmailConfig.EMAIL_PASSWORD.value)
    to_email = get_env_var(EmailConfig.RECEIVER_EMAIL.value)

    # Ensure required environment variables are set
    if not from_email or not from_password or not to_email:
        print("Email environment variables are not set properly.")
        return

    # Create the email content
    msg = MIMEMultipart()  # 建立MIMEMultipart物件
    msg['From'] = from_email  # 寄件者
    msg['To'] = to_email  # 收件者
    msg['Subject'] = subject  # email 標題

    msg.attach(MIMEText(body, 'html'))
    try:
        with SMTP('smtp.gmail.com', 587) as server:  # 設定SMTP伺服器
            server.starttls()  # 建立 TLS 加密傳輸
            server.login(from_email, from_password)  # 登入寄件者 gmail
            server.send_message(msg)   # 寄送 email
            print("Email 發送成功")

    except SMTPException as e:
        print(f"SMTP error when sending email: {e}")
    except OSError as e:
        print(f"Network error when sending email: {e}")



async def send_telegram(messages):
    """
    Sends messages to Telegram chat.
    """    
    bot_token = get_env_var(TelegramConfig.TELEGRAM_API_TOKEN.value)
    chat_id = get_env_var(TelegramConfig.TELEGRAM_CHAT_ID.value)

    # Ensure required environment variables are set
    if not bot_token or not chat_id:
        print("Ensure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables are set")
        return

    try:
        bot = Bot(token=bot_token)
        for message in messages:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
        print("Telegram 訊息發送成功")

    except Exception as e:
        print(f"Error in send_telegram: {e}")




async def send_notifications():
    """
    Fetches products from the database and sends out notifications by email and Telegram.
    """
    products = get_all_products_today()

    if not products:
        print("No products to notify.")
        return

    # Prepare email content
    subject = "特價商品資訊"
    email_message = format_email_message(products)

    # Prepare Telegram messages
    telegram_message = format_telegram_message(products)

    # Send notifications
    send_email(subject, email_message)
    await send_telegram(telegram_message)