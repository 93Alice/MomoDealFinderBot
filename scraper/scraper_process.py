"""Module for processing product information from a webpage."""
from scraper.dom_helpers import extract_product_info, get_mental_blocks, extract_purchase_time ,get_products_from_block
from database.database_handler import is_product_in_database

async def momo_limited_sales(page):
    """Extract product information from the webpage and classify them for insertion or update in the database."""    

    products_insert = [] 
    product_update = []

    mental_blocks = await get_mental_blocks(page)
    for block in mental_blocks:

        purchase_time = await extract_purchase_time(block)

        products = await get_products_from_block(block)

        for product in products:
            product_info = await extract_product_info(product, purchase_time)

            # Skip products without an i_code
            if not product_info or not product_info["id"]:
                print("Missing i_code.")
                continue

            # Skip products without purchase start and end times
            if product_info["purchase_start_time"] is None or product_info["purchase_end_time"] is None:
                print(f"Skipping product due to missing purchase time: {product_info}")
                continue       

            # Check if the product already exists in the database
            if is_product_in_database(product_info["product_info_block"]):
                product_update.append(product_info)
            else:
                products_insert.append(product_info)   # Add new product to insertion list
                

    return {
        'toInsert': products_insert,
        'toUpdate': product_update
    }
