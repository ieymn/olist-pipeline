"""
ingest_olist.py

Loads the 9 Olist CSV files (already downloaded via Kaggle API into ./data/)
into the PostgreSQL 'raw' schema (Bronze layer).
 
Stage 1: FULL LOAD — loads all rows every run, replacing existing tables.
Watermark/incremental logic will be added in a later version once this
is confirmed working end-to-end.
 
Run inside Docker: connects to host 'olist-db', port 5432.
"""

import os 
import pandas as pd 
from sqlalchemy import create_engine, text

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Connection string — inside Docker, host is the service name 'olist-db'.
# If  run this locally instead, swap host to 'localhost' and port to 5433.

DB_USER = os.getenv("OLIST_DB_USER", "olist")
DB_PASS = os.getenv("OLIST_DB_PASS", "olist")
DB_HOST = os.getenv("OLIST_DB_HOST", "olist-db")
DB_PORT = os.getenv("OLIST_DB_PORT", "5432")
DB_NAME = os.getenv("OLIST_DB_NAME", "olist")

CONN_STRING = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Maps: csv filename -> target table name inthe 'raw' schema
CSV_TABLE_MAP ={
     "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "payments",
    "olist_order_reviews_dataset.csv": "reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation"
}

def get_engine():
     """Create and return a SQLAlchemy engine for the olist-db connection."""
     return create_engine(CONN_STRING)


def ensure_raw_schema(engine):
    """Create the 'raw' schema if it doesn't already exist."""
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
        conn.commit()
    print("[OK] raw schema ready")

   
def load_csv_to_table(engine, csv_filename, table_name):
    """Read one CSV and load it into raw.<table_name>, replacing existing data."""
    csv_path = os.path.join(DATA_DIR, csv_filename)

    if not os.path.exists(csv_path):
        print(f"[SKIP] {csv_filename} not found at {csv_path}")
        return 0
    
    df = pd.read_csv(csv_path)
    row_count = len(df)

    df.to_sql(
        name=table_name,
        con=engine,
        schema="raw",
        if_exists="replace", #full load: drop and recreate each run
        index=False,
        chunksize=5000,
    )

    print(f"[OK] {csv_filename} -> raw {table_name} {row_count} rows")
    return row_count


def main():
    print("===Olist Ingestion: Full Load===")
    engine = get_engine()

    ensure_raw_schema(engine)

    total_rows =0
    for csv_filename, table_name in CSV_TABLE_MAP.items():
        rows = load_csv_to_table(engine, csv_filename, table_name)
        total_rows += rows

    print(f"=== Done. Total rows loaded: {total_rows} ===")

if __name__ == "__main__":
    main()

