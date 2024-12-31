"""
This module provides a function to establish a connection to a PostgreSQL database
using the psycopg2 library and environment variables for configuration.
"""

import psycopg2
from config.constants import DatabaseConfig
from config.config import get_env_var


def connect_db():
    """
    Establishes a connection to the PostgreSQL database.

    The database configuration values are read from environment variables
    specified in the `DatabaseConfig` constants.
    """
    try:
        conn = psycopg2.connect(
            dbname=get_env_var(DatabaseConfig.DB_NAME.value),
            user=get_env_var(DatabaseConfig.DB_USER.value),
            password=get_env_var(DatabaseConfig.DB_PASSWORD.value),
            host=get_env_var(DatabaseConfig.DB_HOST.value),
            port=get_env_var(DatabaseConfig.DB_PORT.value)
        )
        return conn
    except psycopg2.Error as e:
        print(f"資料庫連線錯誤: {e}")
        return None
