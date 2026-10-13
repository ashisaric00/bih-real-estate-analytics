import os
import duckdb

def run_market_analysis():
    print("📊 Running Real Estate Market Intelligence Analysis...\n")

    db_path = os.path.join("data", "warehouse", "bih_real_estate.duckdb")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}. Run etl_pipeline.py first!")

    conn = duckdb.connect(db_path)

    # 1. Average price per square meter by city
    print("--- 1. AVERAGE PRICE PER M2 BY CITY (BAM) ---")
    query_1 = """
        SELECT 
            city,
            ROUND(AVG(price_per_m2), 2) AS avg_price_per_m2,
            ROUND(AVG(price_bam), 2) AS avg_total_price,
            COUNT(*) as total_listings
        FROM fact_listings
        GROUP BY city
        ORDER BY avg_price_per_m2 DESC;
    """
    df_city = conn.execute(query_1).fetchdf()
    print(df_city.to_string(index=False))
    print("\n" + "="*50 + "\n")

    # 2. Price comparison: New Building vs Older Building
    print("--- 2. NEW BUILDINGS VS OLDER BUILDINGS (Price per m2) ---")
    query_2 = """
        SELECT 
            CASE WHEN is_new_building = 1 THEN 'New Building (2020+)' ELSE 'Older Building' END AS building_status,
            ROUND(AVG(price_per_m2), 2) AS avg_price_per_m2,
            COUNT(*) as listings_count
        FROM fact_listings
        GROUP BY is_new_building
        ORDER BY avg_price_per_m2 DESC;
    """
    df_status = conn.execute(query_2).fetchdf()
    print(df_status.to_string(index=False))
    print("\n" + "="*50 + "\n")

    # 3. Top property types breakdown
    print("--- 3. PROPERTY TYPES MARKET SHARE & AVG PRICE ---")
    query_3 = """
        SELECT 
            property_type,
            COUNT(*) as total_listings,
            ROUND(AVG(area_m2), 1) AS avg_area_m2,
            ROUND(AVG(price_bam), 2) AS avg_price_bam
        FROM fact_listings
        GROUP BY property_type
        ORDER BY total_listings DESC;
    """
    df_types = conn.execute(query_3).fetchdf()
    print(df_types.to_string(index=False))

    conn.close()
    print("\n✅ Market analysis successfully executed!")

if __name__ == "__main__":
    run_market_analysis()