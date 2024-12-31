"""
Telegram Bot for Special Offer Product Inquiry.
"""

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from config.config import get_env_var
from database.database_handler import get_all_categories, get_products_by_category, get_all_products_today
from messages.message_format import format_telegram_message

bot_token = get_env_var("TELEGRAM_API_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command and show a welcome message with options.
    """    
    keyboard = [
        [KeyboardButton("/start")],
        [KeyboardButton("/about")],
        [KeyboardButton("/categories")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        (
            "歡迎使用 <b>特價查詢機器人</b>！\n\n"
            "請直接點擊選單按鈕或選擇以下指令：\n"
            "/about - 關於機器人\n"
            "/categories - 選擇類別\n"
            "/all - 所有商品"
        ),
        parse_mode="HTML",
        reply_markup=reply_markup,
    )
    
async def about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /about command and display information about the bot.
    """    
    await update.message.reply_text(
        (
        "這是一個 <b>特價查詢機器人</b>，提供商品特價資訊查詢功能！\n\n"
        "目前支持以下功能：\n"
        "1. <b>查詢商品類別</b>\n"
        "   ● 使用 /categories 或選單，選擇不同商品類別進行查詢。\n"
        "2. <b>查詢搶購商品</b>\n"
        "   ● 根據選擇的類別，顯示符合條件的商品資訊。\n"
        "3. <b>查詢所有商品</b>\n"
        "   ● 直接輸入 /all ，查看當日所有商品的特價資訊\n\n"
        "<i>機器人每天 <b>00:00</b> 會主動發送當日的商品資訊\n\n</i>"
        "<i>此資料非即時性更新，若有與官網不符請依照官網為準。祝您使用愉快！</i>"
    ),
    parse_mode="HTML",
    reply_markup=ReplyKeyboardRemove()
    )

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /categories command and provide a list of categories for users to select.
    """    
    categories_list  = get_all_categories()

    if not categories_list :
        await update.message.reply_text("目前沒有可用的類別。")
        return

    keyboard = []
    for category in categories_list:
        keyboard.append([KeyboardButton(category)])

    keyboard.append([KeyboardButton("全部")])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("請選擇一個類別：", reply_markup=reply_markup)


async def all_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /all command and display all products for the current day.
    """
    products = get_all_products_today()

    if not products:
        await update.message.reply_text("今天沒有任何商品資訊。")
        return

    messages = format_telegram_message(products)

    for message in messages:
        await update.message.reply_text(
            text=message,
            parse_mode="HTML"
        )

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the category selection by the user and display matching products.
    """    
    selected_category = update.message.text  # Get the category selected by the user
    products = get_products_by_category(selected_category)

    if selected_category == "全部":
        products = get_all_products_today()
    else:
        products = get_products_by_category(selected_category)

    if not products:
        await update.message.reply_text(f"「{selected_category}」不是有效的商品類別。請選擇一個有效的類別或使用指令。")
        return
    messages = format_telegram_message(products)


    for message in messages:
        await update.message.reply_text(
            text=message,
            parse_mode="HTML"
        )




def main():
    """
    Main entry point of the bot application. Configures command handlers and starts polling.
    """    
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about_bot))
    application.add_handler(CommandHandler("categories", categories))
    application.add_handler(CommandHandler("all", all_products))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_category_selection))  # Handle text input for category selection

    application.run_polling()


if __name__ == "__main__":
    main()
    