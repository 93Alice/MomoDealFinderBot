"""
This module defines the scraping logic for fetching limited sales products
and their categories from the momo website and updating the database.
"""

import asyncio
import random
from playwright.sync_api import Playwright
from playwright.async_api import async_playwright
from scraper.scraper_process import momo_limited_sales
from scraper.dom_helpers import extract_categories
from database.database_handler import insert_product_info, get_products_with_empty_category, update_product_info

SEMAPHORE_LIMIT = 5  # 最多可以同時處理 5 個商品
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

async def fetch_product_category(product_info, playwright):
    """
    Fetch the category information for a product.
    """    
    async with semaphore:  # 使用 Semaphore 限制同時處理數量
        try:
            delay = random.uniform(1, 3)  # Random delay 1 to 3 seconds
            await asyncio.sleep(delay)

            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            product_link = f"https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={product_info['id']}"
            await page.goto(product_link, timeout=60000)

            categories = await extract_categories(page)
            await browser.close()


            # Handle returned categories
            if categories is None:
                product_info["categories"] = []  # Failed to load categories
            elif not categories:
                product_info["categories"] = ["其他"]  # Default to "其他" if categories are empty
            else:
                product_info["categories"] = categories  # Successfully fetched categories

            return product_info
        except Exception as e:
            print(f"Failed to fetch details for product {product_info['id']}: {e}")
            product_info["categories"] = []  # Failed categories
            return product_info

async def fetch_limited_sales_products (local_playwright: Playwright, max_retries=3) -> None:
    """
    Fetch limited sales products and process their details.
    """    
    retries = 0
    while retries < max_retries:
        try:
            print("開始爬取商品資料...")
            browser = await local_playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto("https://www.momoshop.com.tw/main/Main.jsp", timeout=60000)
            await page.get_by_role("link", name="看全部 >").click()
            await page.wait_for_load_state('networkidle')

            # 抓取頁面上的產品資訊
            products = await momo_limited_sales(page)
            print("爬取商品成功，開始處理資料...")

            # 處理需要插入的產品資料 (toInsert)
            if(len(products['toInsert'])) != 0:
                async with async_playwright() as playwright:

                    tasks = []
                    for product in products["toInsert"]:
                        task = fetch_product_category(product, playwright)
                        tasks.append(task)

                    detailed_products_info = await asyncio.gather(*tasks, return_exceptions=True)

                # 插入成功爬取的產品資料到資料庫
                for products_info in detailed_products_info:
                    if isinstance(products_info, dict):
                        insert_product_info(products_info)
                        print(f"插入產品資料成功: {products_info['id']}")           

            # 處理需要更新的產品資料 (toUpdate)
            if len(products["toUpdate"]) != 0:
                for product in products["toUpdate"]:
                    try:
                        update_product_info(product)
                        print(f"更新產品資料成功: {product['id']}")
                    except Exception as e:
                        print(f"更新產品資料失敗: {product['id']} - {e}")                    

            # 查詢資料庫中類別為空的產品
            empty_category_products = get_products_with_empty_category()

            # 爬取並更新類別資料
            if empty_category_products:
                async with async_playwright() as playwright:
                    tasks = []
                    for product in empty_category_products:
                        task = fetch_product_category(product, playwright)
                        tasks.append(task)
                    detailed_products_info = await asyncio.gather(*tasks, return_exceptions=True)

                # 更新成功爬取的產品資料
                for products_info in detailed_products_info:
                    if isinstance(products_info, dict):
                        print(f"爬取產品類別成功: {products_info['id']}")
                        update_product_info(products_info)

            await context.close()
            await browser.close()
            return
        except Exception as e:
            retries += 1
            print(f"Error in run: {type(e).__name__} - {e}. Retrying {retries}/{max_retries}...")
            await asyncio.sleep(2)
        finally:
            try:
                await browser.close()
            except Exception as e:
                print(f"Error closing browser: {e}")

    print("Max retries reached. Exiting run.")



async def scrape_job():
    """
    Run the scrape job to fetch limited sales products.
    """    
    async with async_playwright() as local_playwright:
        await fetch_limited_sales_products (local_playwright)
    
    print("執行完畢")