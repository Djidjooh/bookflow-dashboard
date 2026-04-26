import os
import pandas as pd
import psycopg2
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

POSTGRES_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "database": os.getenv("POSTGRES_DB", "bookshop"),
    "user": os.getenv("POSTGRES_USER", "bookuser"),
    "password": os.getenv("POSTGRES_PASSWORD", "bookpass"),
}

SNOWFLAKE_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    "database": os.getenv("SNOWFLAKE_DATABASE", "BOOKSHOP"),
    "schema": "RAW",
}

TABLES = ["category", "books", "customers", "factures", "ventes"]


def postgres_to_dataframe(table_name, pg_conn):
    query = f"SELECT * FROM {table_name};"
    print(f"Lecture PostgreSQL : {table_name}")
    return pd.read_sql(query, pg_conn)


def create_snowflake_table(table_name, df, sf_cursor):
    columns = []

    for col, dtype in zip(df.columns, df.dtypes):
        col_name = col.upper()

        if "int" in str(dtype):
            sf_type = "NUMBER"
        elif "float" in str(dtype):
            sf_type = "FLOAT"
        else:
            sf_type = "VARCHAR"

        columns.append(f"{col_name} {sf_type}")

    columns_sql = ", ".join(columns)

    create_query = f"""
    CREATE OR REPLACE TABLE RAW.{table_name.upper()} (
        {columns_sql}
    );
    """

    print(f"Création table Snowflake : RAW.{table_name.upper()}")
    sf_cursor.execute(create_query)


def load_dataframe_to_snowflake(table_name, df, sf_conn):
    df.columns = [col.upper() for col in df.columns]

    print(f"Chargement vers Snowflake : RAW.{table_name.upper()}")

    success, nchunks, nrows, output = write_pandas(
        conn=sf_conn,
        df=df,
        table_name=table_name.upper(),
        database=SNOWFLAKE_CONFIG["database"],
        schema="RAW",
        overwrite=False,
    )

    if success:
        print(f"✅ {nrows} lignes chargées dans RAW.{table_name.upper()}")
    else:
        print(f"❌ Erreur chargement : {table_name}")
        print(output)


def main():
    print("Connexion à PostgreSQL...")
    pg_conn = psycopg2.connect(**POSTGRES_CONFIG)

    print("Connexion à Snowflake...")
    sf_conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    sf_cursor = sf_conn.cursor()

    sf_cursor.execute("USE DATABASE BOOKSHOP")
    sf_cursor.execute("USE SCHEMA RAW")

    for table in TABLES:
        df = postgres_to_dataframe(table, pg_conn)

        create_snowflake_table(table, df, sf_cursor)

        load_dataframe_to_snowflake(table, df, sf_conn)

    sf_cursor.close()
    sf_conn.close()
    pg_conn.close()

    print("✅ Ingestion PostgreSQL vers Snowflake RAW terminée avec succès.")


if __name__ == "__main__":
    main()
