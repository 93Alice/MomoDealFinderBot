"""
This module handles database operations related to product information, 
such as inserting, updating, and querying product data.
"""

from datetime import datetime
from database.db_connection import connect_db
from config.constants import ProductTable

def execute_query(query, params=None, fetch=False, fetch_all=False):
    """
    Executes a SQL query and returns the result if required.

    :param query: The SQL query to execute.
    :param params: The parameters to pass to the query.
    :param fetch: Whether to fetch a single result.
    :param fetch_all: Whether to fetch all results.
    """    
    conn = connect_db()
    if conn is None:
        print("Database connection failed.")
        return None
    
    try:
        with conn: 
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                else:
                    conn.commit()
    except Exception as e:
        print(f"Database query error: {e}")
    finally:
        if conn:
            conn.close()
    return None


def build_query(table, columns, condition):
    """
    Builds an UPDATE SQL query based on the provided table, columns, and condition.
    """    
    set_clause_parts = []
    for col in columns:
        set_clause_parts.append(f"{col} = %s")
    set_clause = ", ".join(set_clause_parts)
    return f"""UPDATE "{table}" SET {set_clause} WHERE {condition};"""


def is_product_in_database(product_info_block):
    """
    Checks if a product exists in the database based on the product_info_block.
    """    
    query = f"""
        SELECT 1 FROM "{ProductTable.TABLE_NAME.value}"     
        WHERE "{ProductTable.PRODUCT_INFO_BLOCK.value}" = %s;
    """
    result = execute_query(query, (product_info_block,), fetch=True)

    return result is not None



def insert_product_info(product_info):
    """
    Inserts product information in the database.
    """    
    processed_countdown = product_info["countdown"].replace(",", "")

    categories = ', '.join(product_info.get("categories", ["其他"]))


    # Insert new product information
    insert_query = (
        f"""INSERT INTO "{ProductTable.TABLE_NAME.value}" (
        "{ProductTable.ID.value}", "{ProductTable.PRODUCT_INFO_BLOCK.value}", "{ProductTable.PRODUCT_NAME.value}", "{ProductTable.BRAND.value}", 
        "{ProductTable.IMAGE_URL.value}", "{ProductTable.PRICE.value}", "{ProductTable.PURCHASE_START_TIME.value}", 
        "{ProductTable.PURCHASE_END_TIME.value}", "{ProductTable.COUNTDOWN.value}", "{ProductTable.ORIGINAL_COUNT.value}", 
        "{ProductTable.LAST_UPDATED.value}", "{ProductTable.CATEGORY.value}")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT ("{ProductTable.PRODUCT_INFO_BLOCK.value}") DO NOTHING;
        """
    )
    
    try:
        execute_query(insert_query, (
            product_info["id"],     
            product_info["product_info_block"],
            product_info["product_name"],
            product_info["brand"],
            product_info["image"],
            product_info["price"],
            product_info["purchase_start_time"],
            product_info["purchase_end_time"],
            processed_countdown,
            processed_countdown,    
            datetime.now(),                
            categories
        ))
    except Exception as e:
        print(f"Error inserting or updating product: {e}")


# Upsate product information
def update_product_info(product_info):
    update_fields = []
    update_values = []
    product_info_block = product_info.get("product_info_block")

    if not product_info_block:
        print("No PRODUCT_INFO_BLOCK provided. Skipping update.")
        return
    
    if "categories" in product_info and product_info["categories"]:
        update_fields.append(f'"{ProductTable.CATEGORY.value}" = %s')
        update_values.append(", ".join(product_info["categories"]))
    
    if "price" in product_info:       
        update_fields.append(f'"{ProductTable.PRICE.value}" = %s')
        update_values.append(float(product_info["price"])) 
    
    if "countdown" in product_info:
        countdown_value = str(product_info["countdown"]).replace(",", "")
        update_fields.append(f'"{ProductTable.COUNTDOWN.value}" = %s')
        update_values.append(int(countdown_value))

    update_fields.append(f'"{ProductTable.LAST_UPDATED.value}" = %s')
    update_values.append(datetime.now())

    update_query = f"""
        UPDATE "{ProductTable.TABLE_NAME.value}"
        SET {", ".join(update_fields)}
        WHERE "{ProductTable.PRODUCT_INFO_BLOCK.value}" = %s;
    """
    update_values.append(product_info_block)

    execute_query(update_query, tuple(update_values))


def get_all_products_today():
    """
    Fetches all products whose purchase end time is today.
    """
    query = f"""
        SELECT DISTINCT ON ("{ProductTable.ID.value}")
            "{ProductTable.ID.value}", "{ProductTable.PRODUCT_NAME.value}", "{ProductTable.BRAND.value}", 
            "{ProductTable.IMAGE_URL.value}", "{ProductTable.PRICE.value}", 
            "{ProductTable.COUNTDOWN.value}", "{ProductTable.PURCHASE_START_TIME.value}", 
            "{ProductTable.PURCHASE_END_TIME.value}"
        FROM "{ProductTable.TABLE_NAME.value}"
        WHERE DATE("{ProductTable.PURCHASE_END_TIME.value}") = CURRENT_DATE;
    """
    results = execute_query(query, fetch_all=True)

    products = []
    for row in results:
        product = {
            "id": row[0],
            "product_name": row[1],
            "brand": row[2],
            "image_url": row[3],
            "price": row[4],
            "countdown": row[5],
            "purchase_start_time": row[6].strftime("%Y-%m-%d %H:%M:%S"),
            "purchase_end_time": row[7].strftime("%Y-%m-%d %H:%M:%S"),
        }
        products.append(product)

    return products    

def get_products_with_empty_category():
    """
    Fetches products that have empty categories.
    """
    query = f"""
        SELECT "{ProductTable.ID.value}", "{ProductTable.PRODUCT_NAME.value}", "{ProductTable.BRAND.value}", 
            "{ProductTable.IMAGE_URL.value}", "{ProductTable.PRICE.value}", 
            "{ProductTable.COUNTDOWN.value}", "{ProductTable.PURCHASE_START_TIME.value}", 
            "{ProductTable.PURCHASE_END_TIME.value}", "{ProductTable.PRODUCT_INFO_BLOCK.value}"
        FROM "{ProductTable.TABLE_NAME.value}"
        WHERE "{ProductTable.CATEGORY.value}" = '';
    """

    results = execute_query(query, fetch_all=True) 

    products = []
    for row in results:
        product = {
            "id": row[0],
            "product_name": row[1],
            "brand": row[2],
            "image_url": row[3],
            "price": row[4],
            "countdown": row[5],
            "purchase_start_time": row[6].strftime("%Y-%m-%d %H:%M:%S"),
            "purchase_end_time": row[7].strftime("%Y-%m-%d %H:%M:%S"),
            "product_info_block": row[8],
        }
        products.append(product)

    return products    


def get_all_categories(): 
    """
    Fetches all distinct product categories.
    """    
    query = f"""
        SELECT DISTINCT "{ProductTable.CATEGORY.value}"
        FROM "{ProductTable.TABLE_NAME.value}"
        WHERE "{ProductTable.CATEGORY.value}" IS NOT NULL AND "{ProductTable.CATEGORY.value}" != '';
    """
    results = execute_query(query, fetch_all=True)

    categories = []
    for row in results:
        categories.append(row[0])
    
    return categories    


def get_products_by_category(category):
    """
    Fetches products by a specific category.
    """    
    query = f"""
        SELECT "{ProductTable.ID.value}", "{ProductTable.PRODUCT_NAME.value}", "{ProductTable.BRAND.value}", "{ProductTable.PRICE.value}"
        FROM "{ProductTable.TABLE_NAME.value}"
        WHERE "{ProductTable.CATEGORY.value}" = %s
        AND DATE("{ProductTable.PURCHASE_END_TIME.value}") = CURRENT_DATE;
    """

    results = execute_query(query, (category,), fetch_all=True)


    products = []
    for row in results:
        product = {
            "id": row[0],
            "product_name": row[1],
            "brand": row[2],
            "price": row[3],
        }
        products.append(product)
    
    return products    