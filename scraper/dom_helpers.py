"""
This module provides utility functions to extract information from DOM elements
using Playwright's async API.
"""
import re
from datetime import datetime

# 尋找所有商品區塊
async def get_mental_blocks(page):
    """
    Find all mental blocks on the page.
    """    
    return await page.query_selector_all("div.MENTAL")

# 商品區塊
async def get_products_from_block(block):
    """
    Extract all product elements from a mental block.
    """    
    return await block.query_selector_all("ul.product_Area li.box1")

# 搶購時間
async def extract_purchase_time(block):
        """
        Extract purchase time information from a mental block.
        """        
        period = await block.query_selector("div.dateTime div.period span")
        if period:
            purchase_time = await period.inner_text()
            return purchase_time    
        else:
            return "purchase time not found"

async def extract_product_info(product, purchase_time):
    """
    Extract detailed information for a single product.
    """
    # 商品編號(i_code)
    a_element = await product.query_selector('a[id^="gdsHref_1"]')
    if a_element:
        href = await a_element.get_attribute("href")
        if href:
            match = re.search(r"i_code=(\d+)", href)
            if match:
                i_code = match.group(1)
            else:
                print("Invalid href format, could not extract i_code.")
                i_code = None
        else:
            i_code = None
    else:
        print("a_element not found.")
        i_code = None

    # 商品照片
    image_element = await product.query_selector("img#nowPImg_1")
    if image_element:
        image = (await image_element.get_attribute("src")).strip()
    else:
        image = "image not found"
    
    # 品牌名稱
    brand_element = await product.query_selector("div.brand")
    if brand_element:
        brand = (await brand_element.inner_text()).strip()
    else:
        brand = "brand not found"

    # 商品名稱
    product_name_element = await product.query_selector("div.brand2")
    if product_name_element:
        product_name = (await product_name_element.inner_text()).strip()
    else:
        product_name = "product name not found"

    # 倒數數量
    countdown_element = await product.query_selector("div.last #gdsStock_1")
    if countdown_element:
        countdown = (await countdown_element.inner_text()).strip()
    else:
        countdown = "countdown not found"

    # 價格
    price_element = await product.query_selector("div.price")
    if price_element:
        processed_price = (await price_element.inner_text()).strip().replace("$", "").replace(",", "").strip()
    else:
        processed_price = "price not found"
    
    # 處理搶購時間
    try:
        start_time_str, end_time_str = purchase_time.split("~")
        current_year = datetime.now().year
        purchase_start_time = datetime.strptime(start_time_str.strip(), "%m/%d %H:%M").replace(year=current_year)
        purchase_end_time = datetime.strptime(end_time_str.strip(), "%m/%d %H:%M").replace(year=current_year)

    except ValueError as e:
        print(f"Error parsing purchase time: {e}")
        purchase_start_time = purchase_end_time = None

    product_info_block = f"{purchase_start_time}|{purchase_end_time}|{brand}|{product_name}"

    return {
        "id": i_code, 
        "product_info_block": product_info_block,
        "image": image,
        "brand": brand,
        "product_name": product_name,
        "price": processed_price,
        "purchase_start_time": purchase_start_time,
        "purchase_end_time": purchase_end_time,
        "countdown": countdown,
    }

async def extract_categories(page):
    """
    Extract product category information.
    """
    category_element = await page.query_selector("div#bt_996_layout div.navcontent_list ul#toothUl")
    if category_element:
        category_items = await category_element.query_selector_all("li.FBGO")
        categories = []
        for item in category_items:
            category_text = await item.inner_text()
            categories.append(category_text)
        return categories
    return []