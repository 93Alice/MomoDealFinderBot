"""
This module contains various configuration constants 
for database, email, product table, and telegram settings.
"""

from enum import Enum

class DatabaseConfig(Enum):
    """
    Enum for database configuration settings.
    """    
    DB_NAME = "DB_NAME"
    DB_USER = "DB_USER"
    DB_PASSWORD = "DB_PASSWORD"
    DB_HOST = "DB_HOST"
    DB_PORT = "DB_PORT"

class EmailConfig(Enum):
    """
    Enum for email configuration settings.
    """    
    EMAIL_ACCOUNT = "EMAIL_ACCOUNT"
    EMAIL_PASSWORD = "EMAIL_PASSWORD"
    RECEIVER_EMAIL = "RECEIVER_EMAIL"

class ProductTable(Enum):
    """
    Enum for product table column names.
    """    
    TABLE_NAME = "products"
    ID = "id"
    PRODUCT_INFO_BLOCK = "product_info_block"
    PRODUCT_NAME = "product_name"
    BRAND = "brand"
    IMAGE_URL = "image_url"
    PRICE = "price"
    PURCHASE_START_TIME = "purchase_start_time"
    PURCHASE_END_TIME = "purchase_end_time"
    LAST_UPDATED = "last_updated"
    COUNTDOWN = "countdown"
    ORIGINAL_COUNT = "original_count"
    CATEGORY = "category"

class TelegramConfig(Enum):
    """
    Enum for telegram configuration settings.
    """    
    TELEGRAM_API_TOKEN = "TELEGRAM_API_TOKEN"
    TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"
    