import os
import snowflake.connector

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
)

cur = conn.cursor()

queries = [
    """
    CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
    WITH WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    """,

    "CREATE DATABASE IF NOT EXISTS BOOKSHOP",

    "CREATE SCHEMA IF NOT EXISTS BOOKSHOP.RAW",
    "CREATE SCHEMA IF NOT EXISTS BOOKSHOP.STAGGING",
    "CREATE SCHEMA IF NOT EXISTS BOOKSHOP.WAREHOUSE",
    "CREATE SCHEMA IF NOT EXISTS BOOKSHOP.MARTS",
]

for query in queries:
    print(f"Exécution : {query}")
    cur.execute(query)

cur.close()
conn.close()

print("✅ Base BOOKSHOP et schémas créés avec succès dans Snowflake.")
