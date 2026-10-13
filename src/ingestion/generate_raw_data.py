import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_bih_real_estate_data(num_records=5000, seed=42):
    """
    Generates a realistic synthetic dataset representing real estate listings 
    across major cities in Bosnia and Herzegovina.
    Includes deliberate missing values and outliers for ETL data cleaning tasks.
    """
    np.random.seed(seed)
    random.seed(seed)

    cities_distribution = {
        'Sarajevo': 0.35,
        'Banja Luka': 0.25,
        'Mostar': 0.10,
        'Tuzla': 0.10,
        'Bijeljina': 0.08,
        'Trebinje': 0.07,
        'Zenica': 0.05
    }

    cities = list(cities_distribution.keys())
    city_probs = list(cities_distribution.values())

    property_types = ['Apartment', 'House', 'Commercial Space']
    prop_probs = [0.75, 0.20, 0.05]

    data = []
    start_date = datetime(2023, 1, 1)

    for i in range(1, num_records + 1):
        listing_id = f"BIH-RE-{i:06d}"
        city = np.random.choice(cities, p=city_probs)
        prop_type = np.random.choice(property_types, p=prop_probs)

        # Base pricing per square meter (BAM / KM) depending on city
        base_price_m2 = {
            'Sarajevo': 3200,
            'Banja Luka': 2900,
            'Trebinje': 2800,
            'Mostar': 2200,
            'Tuzla': 1900,
            'Bijeljina': 1800,
            'Zenica': 1600
        }[city]

        # Property attributes
        if prop_type == 'Apartment':
            area_m2 = round(float(np.random.normal(65, 20)), 1)
            area_m2 = max(20.0, min(area_m2, 200.0))
            rooms = int(np.clip(np.random.poisson(2.2), 1, 5))
            floor = random.randint(0, 12)
        elif prop_type == 'House':
            area_m2 = round(float(np.random.normal(150, 50)), 1)
            area_m2 = max(50.0, min(area_m2, 500.0))
            rooms = int(np.clip(np.random.poisson(4.5), 2, 10))
            floor = 0
        else:
            area_m2 = round(float(np.random.normal(100, 40)), 1)
            area_m2 = max(25.0, min(area_m2, 400.0))
            rooms = None
            floor = random.randint(0, 4)

        construction_year = random.randint(1960, 2025)
        is_new_building = 1 if construction_year >= 2020 else 0

        # Calculate price with variations
        m2_price_var = base_price_m2 * np.random.uniform(0.8, 1.3)
        if is_new_building:
            m2_price_var *= 1.25

        price_bam = round(area_m2 * m2_price_var, 2)

        # Random listing date within last 2 years
        days_offset = random.randint(0, 730)
        listing_date = (start_date + timedelta(days=days_offset)).strftime('%Y-%m-%d')

        # Introduce deliberate data quality issues for ETL demonstration
        # 1. Missing floor values for some apartments
        if prop_type == 'Apartment' and random.random() < 0.05:
            floor = None
        
        # 2. Outliers / typos in price
        if random.random() < 0.01:
            price_bam = price_bam * 10  # Typo extra zero
        
        # 3. Missing construction year
        if random.random() < 0.08:
            construction_year = None

        data.append({
            'listing_id': listing_id,
            'city': city,
            'property_type': prop_type,
            'area_m2': area_m2,
            'rooms': rooms,
            'floor': floor,
            'construction_year': construction_year,
            'is_new_building': is_new_building,
            'price_bam': price_bam,
            'listing_date': listing_date
        })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("🚀 Generating raw dataset for BiH Real Estate Market...")
    df_raw = generate_bih_real_estate_data(num_records=5000)

    # Ensure target folder exists
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "bih_real_estate_raw.csv")
    df_raw.to_csv(output_path, index=False)

    print(f"✅ Raw dataset successfully generated!")
    print(f"📍 Location: {output_path}")
    print(f"📊 Total records generated: {len(df_raw)}")