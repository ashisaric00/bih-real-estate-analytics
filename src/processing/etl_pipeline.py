import os
import pandas as pd
import duckdb

def run_etl():
    print("🔄 Starting ETL Pipeline for BiH Real Estate...")

    # 1. EXTRACT
    raw_path = os.path.join("data", "raw", "bih_real_estate_raw.csv")
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}. Run generate_raw_data.py first!")
    
    df = pd.read_csv(raw_path)
    print(f"📥 Extracted {len(df)} records from raw storage.")

    # 2. TRANSFORM
    # Drop exact duplicates if any
    initial_count = len(df)
    df.drop_duplicates(subset=['listing_id'], inplace=True)
    print(f"🧹 Removed {initial_count - len(df)} duplicate records.")

    # Handle missing floors for apartments (fill with median floor or default to 0)
    df['floor'] = df['floor'].fillna(df['floor'].median())

    # Handle missing construction year (fill with median)
    df['construction_year'] = df['construction_year'].fillna(df['construction_year'].median())

    # Clean extreme price outliers (e.g., typos where price was multiplied by 10)
    # We can filter out listings with price_per_m2 unrealistically high (> 8000 BAM/m2) or too low (< 800 BAM/m2)
    df['price_per_m2'] = df['price_bam'] / df['area_m2']
    
    valid_market_mask = (df['price_per_m2'] >= 800) & (df['price_per_m2'] <= 8000)
    filtered_out_count = len(df) - valid_market_mask.sum()
    df = df[valid_market_mask].copy()
    print(f"✂️ Filtered out {filtered_out_count} extreme price outlier records.")

    # Feature Engineering: Price per m2 rounded
    df['price_per_m2'] = df['price_per_m2'].round(2)

    # Ensure correct data types
    df['rooms'] = df['rooms'].fillna(2).astype(int) # default to 2 rooms if missing
    df['floor'] = df['floor'].astype(int)
    df['construction_year'] = df['construction_year'].astype(int)

    # Save processed data to CSV as well for safety/backup
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    processed_csv_path = os.path.join(processed_dir, "bih_real_estate_cleaned.csv")
    df.to_csv(processed_csv_path, index=False)
    print(f"💾 Saved cleaned dataset to: {processed_csv_path}")

    # 3. LOAD (Data Warehouse - DuckDB)
    db_dir = os.path.join("data", "warehouse")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "bih_real_estate.duckdb")

    # Connect to DuckDB database (creates file if it doesn't exist)
    conn = duckdb.connect(db_path)

    # Load dataframe into a SQL table
    conn.execute("CREATE OR REPLACE TABLE fact_listings AS SELECT * FROM df")
    
    # Verify load
    table_count = conn.execute("SELECT COUNT(*) FROM fact_listings").fetchone()[0]
    print(f"🚀 Successfully loaded {table_count} rows into DuckDB table 'fact_listings'.")

    conn.close()
    print("✅ ETL Pipeline executed successfully!")

if __name__ == "__main__":
    run_etl()