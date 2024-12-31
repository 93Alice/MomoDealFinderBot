# **Discount Products Crawler and Notification Project**

> This project is an automated system designed to scrape discount products from websites, store the data, and notify users through email and Telegram. The system also provides an interactive Telegram interface for querying products by category.

## 🎯 **Features**

-   **Discount Product Scraping**: Periodically scrape discounted products from targeted websites.
-   **Data Storage and Management**: Store scraped product data in a PostgreSQL database.
-   **Multi-Channel Notifications**:
    -   Email notifications of daily product updates.
    -   Telegram Bot to provide interactive product inquiries.
-   **Interactive Interface**: Users can search for products by category or view all products through Telegram.
-   **Task Scheduling**: Use `APScheduler` for automated scraping and notification tasks.

## ⚙️ Prerequisites

-   **PostgreSQL**：A PostgreSQL database should be set up and running to store the scraped product data.
-   **Environment Variables**：Create a .env file with the necessary environment variables for database, email and telegram configuration.

### **Database Schema**

PostgreSQL Database schema: Table name, columns, and data types:

```sql
CREATE TABLE Products (
    id INTEGER,
    product_info_block TEXT UNIQUE,
    product_name TEXT,
    brand TEXT,
    image_url TEXT,
    price INTEGER,
    purchase_start_time TIMESTAMPTZ,
    purchase_end_time TIMESTAMPTZ,
    last_updated TIMESTAMPTZ,
    countdown INTEGER,
    original_count INTEGER,
    category  VARCHAR(10)
);
```

### **Environment Variables**

The .env file should include the following:

```env
# Database connection details for PostgreSQL.
DB_NAME=<your db name>
DB_USER=<your db user>
DB_PASSWORD=<your db password> # The password set for the database user when the database was created.
DB_HOST=<your db host> # The host address of the database (e.g., localhost)
DB_PORT=<your db port> # default for PostgreSQL is 5432

# Email account credentials to send notifications.
EMAIL_ACCOUNT=<sending email address>
EMAIL_PASSWORD=<system provided application password>
RECEIVER_EMAIL=<Receiving email address>

# Telegram Bot configuration.
TELEGRAM_API_TOKEN=<your telegram api token>
TELEGRAM_CHAT_ID=<your telegram chat id>
```

> ⚠️**Notes:**
>
> 1. Database Queries：
>
> -   To get the DB_NAME: `SELECT current_database();`
> -   To get the DB_USER: `SELECT current_user;`
>
> 2. EMAIL_PASSWORD: If using Gmail, not your Google account password. You need to go to your Google account(Google 帳戶), search for "App Passwords" (應用程式密碼), create an "App Name" (應用程式名稱), and then generate the system-generated App Password (應用程式密碼).

## 🚀 Usage

1. Install Module:

```bash
pip install -r requirements.txt
```

2. Start the Scraper and Notification System:

```bash
python main.py
```

3. Run the Telegram Bot:

```bash
python telegram_bot.py
```

## 🗂️ Project Structure

```
project_root/
│
├── .env  # Environment variables configuration
├── requirements.txt #  Lists the Python packages and their versions required for the project
│
├── config/ # Configuration and constants-related files
│ ├── config.py  # To load environment variables for database, email, and Telegram
│ └── constants.py # Defines global constants required by the system
│
├── database/  # Database-related modules
│ ├── db_connection.py # Handles database connection with the PostgreSQL database using
│ └── database_handler.py # Provides functions for database operations (query, insert, update)
│
├── scraper/ # Web scraping modules
│ ├── scraper.py  # Core logic for web scraping
│ ├── scraper_process.py # Controls scraping workflows
│ └── dom_helpers.py # Helper functions for parsing and extracting data from web pages
│
├── jobs/  # Task scheduling and notification modules
│ ├── schedule_job.py # Defines and controls scheduled tasks
│ └── notify_job.py # Handles notification tasks (email, Telegram)
│
├── messages/ # Message formatting and sending modules
│ ├── message_format.py # Logic for formatting messages
│ └── sender.py # Sends messages by email or Telegram
│
├── telegram_bot.py  # Logic and commands for Telegram Bot interaction
└── main.py # Entry point of the application
```
