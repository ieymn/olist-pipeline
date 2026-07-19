"""
download_from_kaggle.py

Downloads the Olist dataset from Kaggle into ./data/,
so ingest_olist.py can load it into Postgres.
"""

import os
from kaggle.api.kaggle_api_extended import KaggleApi

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATASET = "olistbr/brazilian-ecommerce"

def main():
    api = KaggleApi()
    api.authenticate()  # reads KAGGLE_USERNAME / KAGGLE_KEY from env automatically

    os.makedirs(DATA_DIR, exist_ok=True)

    api.dataset_download_files(
        dataset=DATASET,
        path=DATA_DIR,
        unzip=True
    )

    print(f"[OK] Downloaded and extracted to {DATA_DIR}")

if __name__ == "__main__":
    main()