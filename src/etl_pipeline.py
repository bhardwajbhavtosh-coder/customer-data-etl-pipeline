
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "customers.csv"
ENV_FILE = BASE_DIR / ".env"


# Load environment variables
load_dotenv(ENV_FILE)

DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD:
    raise ValueError(
        "DB_PASSWORD missing. Check your .env file."
    )


# PostgreSQL connection
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=DB_PASSWORD,
    host="localhost",
    port=5432,
    database="etl_demo",
)

engine = create_engine(DATABASE_URL)


def extract_data():
    print("Extracting customer data...")

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE}"
        )

    df = pd.read_csv(CSV_FILE)

    print(f"Rows extracted: {len(df)}")
    return df


def transform_data(df):
    print("Transforming customer data...")

    # Remove rows with missing values
    df = df.dropna().copy()

    # Clean text columns
    for column in ["name", "city"]:
        df[column] = df[column].astype(str).str.strip()

    # Convert numeric columns
    df["customer_id"] = pd.to_numeric(
        df["customer_id"], errors="coerce"
    )
    df["age"] = pd.to_numeric(
        df["age"], errors="coerce"
    )

    # Remove invalid numeric records
    df = df.dropna(
        subset=["customer_id", "age"]
    ).copy()

    df = df[
        (df["customer_id"] > 0)
        & (df["age"] > 0)
        & (df["name"] != "")
        & (df["city"] != "")
    ].copy()

    df["customer_id"] = df["customer_id"].astype(int)
    df["age"] = df["age"].astype(int)

    # Remove duplicate customer details
    df = df.drop_duplicates(
        subset=["name", "city", "age"]
    ).copy()

    print(f"Rows after cleaning: {len(df)}")
    print("\nClean customer data:")
    print(df.to_string(index=False))

    return df


def load_data(clean_df):
    print("\nLoading data into PostgreSQL...")

    clean_df.to_sql(
        name="customers",
        con=engine,
        if_exists="replace",
        index=False,
    )

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM customers")
        )
        row_count = result.scalar()

    print(
        f"Data loaded successfully! "
        f"Rows in database: {row_count}"
    )


def main():
    try:
        df = extract_data()
        clean_df = transform_data(df)
        load_data(clean_df)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
