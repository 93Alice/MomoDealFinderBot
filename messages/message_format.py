"""
This module provides functions to format product information for email and Telegram messages.
"""

def format_email_message(products_info):
    """
    Formats product information into an HTML email format.
    """    
    html_content = "<ul>"
    for product_info in products_info:
        formatted_price = f"${int(product_info['price']):,}" 
        product_link = f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={product_info['id']}" 
        html_content += f"""
            <img src="{product_info['image_url']}" alt="product image" width="100"><br>
            <strong>品牌名稱:</strong> {product_info['brand']}<br>
            <strong>商品名稱:</strong> {product_info['product_name']}<br>
            <strong>價格:</strong> {formatted_price}<br>
            <strong>購買連結:</strong> <a href="{product_link}">{product_link}</a><br><br>
        """

    html_content += "</ul>"

    return html_content


def format_telegram_message(products_info, max_message_length=4096, batch_size=100):
    """
    Formats product information into Telegram messages, splitting them into batches.
    """    
    messages = []
    for i in range(0, len(products_info), batch_size):
        batch = products_info[i:i + batch_size]
        message = ""
        for product_info in batch:
            formatted_price = f"${int(product_info['price']):,}"
            product_link = f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={product_info['id']}"
            product_message = (
                f"✨ <b>{product_info['brand']}</b> - {product_info['product_name']}\n"
                f"💰 價格: {formatted_price}\n"
                f"🔗 <b>購買連結:</b> <a href=\"{product_link}\">{product_link}</a>\n\n"
            )

            if len(message) + len(product_message) > max_message_length:
                split_index = message[:max_message_length].rfind("\n\n")
                if split_index == -1:  # Cannot split by paragraphs, truncate directly
                    split_index = max_message_length
                messages.append(message[:split_index])
                message = message[split_index:]  # Retain remaining portion for further processing
            message += product_message

        # Append any remaining message
        if message:
            messages.append(message)
    
    return messages