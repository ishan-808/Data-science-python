import sqlite3
import pandas as pd

# Load Excel data into SQLite
excel_file = "SQL_Sales_Dataset_200_Rows.xlsx"
df = pd.read_excel(excel_file)

conn = sqlite3.connect("sales.db")

# Create normalized tables
customers_df = (
    df[["customer_name", "region"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
customers_df["customer_id"] = customers_df.index + 1

orders_df = df.merge(customers_df, on=["customer_name", "region"])
orders_df = orders_df[
    [
        "order_id",
        "customer_id",
        "order_date",
        "category",
        "sub_category",
        "product_name",
        "quantity",
        "unit_price",
        "total_price",
    ]
]

customers_df.to_sql("customers", conn, if_exists="replace", index=False)
orders_df.to_sql("orders", conn, if_exists="replace", index=False)


def run_query(title, query):
    print("=" * 50)
    print(f"📌 {title}")
    print("=" * 50)
    print(pd.read_sql_query(query, conn).to_string(index=False))
    print("\n")


# 1. Top Customers (JOIN & Aggregation)
run_query(
    "1. Top 5 Customers by Revenue",
    """
SELECT c.customer_name, c.region, SUM(o.total_price) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.region
ORDER BY total_revenue DESC LIMIT 5;
""",
)

# 2. Average Order Value by Category
run_query(
    "2. Average Order Value by Category",
    """
SELECT category, COUNT(order_id) AS orders, ROUND(AVG(total_price), 2) AS avg_order_value
FROM orders
GROUP BY category ORDER BY avg_order_value DESC;
""",
)

# 3. Order Classification (CASE Statement)
run_query(
    "3. Revenue Tiers (CASE Statement)",
    """
SELECT order_id, product_name, total_price,
       CASE 
           WHEN total_price >= 15000 THEN 'High Value'
           WHEN total_price >= 5000 THEN 'Medium Value'
           ELSE 'Standard'
       END AS tier
FROM orders ORDER BY total_price DESC LIMIT 10;
""",
)

# 4. Subquery: Orders Above Average
run_query(
    "4. Orders Above Average Value",
    """
SELECT order_id, category, total_price
FROM orders
WHERE total_price > (SELECT AVG(total_price) FROM orders)
ORDER BY total_price DESC LIMIT 5;
""",
)

conn.close()