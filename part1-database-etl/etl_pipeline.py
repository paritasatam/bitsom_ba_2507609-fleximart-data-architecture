"""
ETL Pipeline for FlexiMart
Part 1.1 – Extract + Duplicates + Missing Values
"""

import pandas as pd
import mysql.connector

# File paths
CUSTOMERS_FILE = "data/customers_raw.csv"
PRODUCTS_FILE = "data/products_raw.csv"
SALES_FILE = "data/sales_raw.csv"

def extract_data():
    customers_df = pd.read_csv(CUSTOMERS_FILE)
    products_df = pd.read_csv(PRODUCTS_FILE)
    sales_df = pd.read_csv(SALES_FILE)
    return customers_df, products_df, sales_df


def remove_duplicates(customers_df, products_df, sales_df):
    customers_df = customers_df.drop_duplicates(subset=["email"], keep="first")
    products_df = products_df.drop_duplicates()
    sales_df = sales_df.drop_duplicates()
    return customers_df, products_df, sales_df


def handle_missing_values(customers_df, products_df, sales_df):
    print("Handling missing values...")
    print("Customers columns:", list(customers_df.columns))
    print("Products columns:", list(products_df.columns))
    print("Sales columns:", list(sales_df.columns))


    # Track initial counts
    c_before = len(customers_df)
    p_before = len(products_df)
    s_before = len(sales_df)

    # Customers
    customers_df = customers_df.dropna(subset=["email", "registration_date"])
    customers_df["phone"] = customers_df["phone"].fillna("Unknown")
    customers_df["city"] = customers_df["city"].fillna("Unknown")

    # Products
    products_df = products_df.dropna(subset=["price"])
    products_df["stock_quantity"] = products_df["stock_quantity"].fillna(0)
    products_df["category"] = products_df["category"].fillna("Uncategorized")

    # Sales
    sales_df = sales_df.dropna(subset=["customer_id", "product_id", "transaction_date"])

    print(f"Customers rows removed due to missing values: {c_before - len(customers_df)}")
    print(f"Products rows removed due to missing values: {p_before - len(products_df)}")
    print(f"Sales rows removed due to missing values: {s_before - len(sales_df)}")

    return customers_df, products_df, sales_df

def standardize_dates(sales_df):
    print("Standardizing transaction_date format...")

    sales_df["transaction_date"] = pd.to_datetime(
        sales_df["transaction_date"],
        dayfirst=True,
        errors="coerce"
    )

    invalid_dates = sales_df["transaction_date"].isna().sum()
    print(f"Invalid dates converted to NaT: {invalid_dates}")

    sales_df = sales_df.dropna(subset=["transaction_date"])

    sales_df["transaction_date"] = sales_df["transaction_date"].dt.strftime("%Y-%m-%d")

    return sales_df

def rename_sales_columns(sales_df):
    print("Renaming transaction_date to order_date...")
    sales_df = sales_df.rename(columns={"transaction_date": "order_date"})
    return sales_df

def standardize_categories(products_df):
    print("Standardizing product category names...")

    # Make sure category is a string (avoid issues with NaN)
    products_df["category"] = products_df["category"].astype(str)

    # Standardize: strip -> lowercase -> title case
    products_df["category"] = products_df["category"].str.strip().str.lower().str.title()

    return products_df

def standardize_phone_numbers(customers_df):
    print("Standardizing customer phone numbers...")

    def format_phone(x):
        if pd.isna(x):
            return "Unknown"
        x = str(x).strip()
        if x.lower() == "unknown" or x == "":
            return "Unknown"

        digits = "".join(ch for ch in x if ch.isdigit())

        # If number includes country code and becomes longer, take last 10 digits
        if len(digits) >= 10:
            digits = digits[-10:]

        if len(digits) == 10:
            return f"+91-{digits}"

        return "Unknown"

    customers_df["phone"] = customers_df["phone"].apply(format_phone)
    return customers_df

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="viditsql",   # your password
        database="fleximart",
        port=3306
    )

def load_customers(customers_df):
    print("Loading customers into database...")

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT IGNORE INTO customers
        (first_name, last_name, email, phone, city, registration_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    inserted = 0
    for _, row in customers_df.iterrows():
        cursor.execute(
            insert_query,
            (
                row["first_name"],
                row["last_name"],
                row["email"],
                row["phone"],
                row["city"],
                row["registration_date"],
            ),
        )
        # rowcount = 1 if inserted, 0 if ignored (duplicate email)
        inserted += cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Customers inserted: {inserted}")
    print(f"Customers skipped (duplicates): {len(customers_df) - inserted}")

def load_products(products_df):
    print("Loading products into database...")

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO products
        (product_name, category, price, stock_quantity)
        VALUES (%s, %s, %s, %s)
    """

    inserted = 0
    for _, row in products_df.iterrows():
        cursor.execute(
            insert_query,
            (
                row["product_name"],
                row["category"],
                float(row["price"]),
                int(row["stock_quantity"]),
            ),
        )
        inserted += cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Products inserted: {inserted}")

def build_customer_id_map(customers_df):
    """
    Map raw customer codes (e.g., C001) -> DB customer_id
    Assumption: customers_raw.csv has a column named 'customer_id' holding codes like C001.
    """
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    customer_map = {}
    for _, row in customers_df.iterrows():
        raw_code = str(row["customer_id"]).strip()   # raw code like C001
        email = row["email"]

        cursor.execute("SELECT customer_id FROM customers WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            customer_map[raw_code] = result[0]

    cursor.close()
    conn.close()
    return customer_map


def build_product_id_map(products_df):
    """
    Map raw product codes (e.g., P001) -> DB product_id
    Assumption: products_raw.csv has a column named 'product_id' holding codes like P001.
    """
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    product_map = {}
    for _, row in products_df.iterrows():
        raw_code = str(row["product_id"]).strip()   # raw code like P001
        name = row["product_name"]

        cursor.execute("SELECT product_id FROM products WHERE product_name = %s", (name,))
        result = cursor.fetchone()
        if result:
            product_map[raw_code] = result[0]

    cursor.close()
    conn.close()
    return product_map

def build_customer_id_map(customers_df):
    """
    customer_code (C001) -> db_customer_id (int)
    Uses email to find the inserted DB record.
    """
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)


    customer_map = {}
    for _, row in customers_df.iterrows():
        code = str(row["customer_code"]).strip()
        email = row["email"]

        cursor.execute("SELECT customer_id FROM customers WHERE email = %s", (email,))
        res = cursor.fetchone()
        if res:
            customer_map[code] = res[0]

    cursor.close()
    conn.close()
    return customer_map


def build_product_id_map(products_df):
    """
    product_code (P001) -> db_product_id (int)
    Uses product_name to find the inserted DB record.
    """
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    product_map = {}
    for _, row in products_df.iterrows():
        code = str(row["product_code"]).strip()
        name = row["product_name"]

        cursor.execute("SELECT product_id FROM products WHERE product_name = %s", (name,))
        res = cursor.fetchone()
        if res:
            product_map[code] = res[0]

    cursor.close()
    conn.close()
    return product_map

def load_orders_and_items(sales_df, customer_map, product_map):
    print("Loading orders and order_items into database...")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Optional: clear existing orders/items while developing
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE order_items")
    cursor.execute("TRUNCATE TABLE orders")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()

    orders_inserted = 0
    items_inserted = 0
    skipped_rows = 0

    for _, row in sales_df.iterrows():
        cust_code = str(row["customer_id"]).strip()
        prod_code = str(row["product_id"]).strip()

        if cust_code not in customer_map or prod_code not in product_map:
            skipped_rows += 1
            continue

        db_customer_id = customer_map[cust_code]
        db_product_id = product_map[prod_code]

        order_date = row["order_date"]  # already YYYY-MM-DD after your rename step
        status = row.get("status", "Pending")

        quantity = int(row["quantity"])
        unit_price = float(row["unit_price"])
        subtotal = quantity * unit_price

        # 1) Insert into orders (one order per sales row)
        cursor.execute(
            """
            INSERT INTO orders (customer_id, order_date, total_amount, status)
            VALUES (%s, %s, %s, %s)
            """,
            (db_customer_id, order_date, subtotal, status),
        )
        order_id = cursor.lastrowid
        orders_inserted += 1

        # 2) Insert into order_items
        cursor.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (order_id, db_product_id, quantity, unit_price, subtotal),
        )
        items_inserted += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Orders inserted: {orders_inserted}")
    print(f"Order items inserted: {items_inserted}")
    print(f"Sales rows skipped (missing customer/product mapping): {skipped_rows}")

def standardize_customer_registration_dates(customers_df):
    print("Standardizing customer registration_date format...")

    customers_df["registration_date"] = pd.to_datetime(
        customers_df["registration_date"],
        dayfirst=True,
        errors="coerce"
    )

    invalid = customers_df["registration_date"].isna().sum()
    print(f"Invalid customer registration_date values removed: {invalid}")

    customers_df = customers_df.dropna(subset=["registration_date"])
    customers_df["registration_date"] = customers_df["registration_date"].dt.strftime("%Y-%m-%d")

    return customers_df

if __name__ == "__main__":
    customers_df, products_df, sales_df = extract_data()
    
    # Rename raw-code columns to avoid confusion with DB auto-increment IDs
    customers_df = customers_df.rename(columns={"customer_id": "customer_code"})
    products_df = products_df.rename(columns={"product_id": "product_code"})

    customers_df, products_df, sales_df = remove_duplicates(
        customers_df, products_df, sales_df
    )

    customers_df, products_df, sales_df = handle_missing_values(customers_df, products_df, sales_df)

    customers_df = standardize_customer_registration_dates(customers_df)
    products_df = standardize_categories(products_df)
    customers_df = standardize_phone_numbers(customers_df)

    sales_df = standardize_dates(sales_df)
    sales_df = rename_sales_columns(sales_df)

    load_customers(customers_df)
    load_products(products_df)

    customer_map = build_customer_id_map(customers_df)
    product_map = build_product_id_map(products_df)

    load_orders_and_items(sales_df, customer_map, product_map)






