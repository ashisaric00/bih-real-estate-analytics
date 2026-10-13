# 🏢 Bosnia & Herzegovina Real Estate Market Intelligence Platform

An end-to-end Data Engineering and Analytics platform designed to ingest, process, store, analyze, and visualize real estate market trends in Bosnia and Herzegovina.

---

## 📌 Project Overview
This project provides a robust, scalable data pipeline that aggregates property listings, transforms raw data into structured analytical models, and provides interactive visualizations alongside SQL analytical queries.

---

## 🏗️ Architecture & Data Pipeline
1. **Ingestion Layer:** Python script generating realistic property listings across major BiH cities with deliberate data anomalies.
2. **Storage & Warehouse Layer:** Embedded SQL Data Warehouse built on **DuckDB**.
3. **Transformation Layer:** Pandas-based ETL pipeline handling data cleaning, outlier filtering, and feature engineering.
4. **Analytics Layer:** Pre-written analytical SQL queries (`sql/market_insights.sql`).
5. **Presentation Layer:** Interactive analytics dashboard built with **Streamlit** and **Plotly**.

---

## 📂 Repository Structure
```text
bih-real-estate-analytics/
├── data/                  # Raw, processed data and DuckDB warehouse
├── src/                   # Python scripts (ingestion, ETL, models)
├── sql/                   # Analytical SQL queries
├── dashboard/             # Streamlit interactive web application
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation



How to Run Locally

1. Clone the repository and install dependencies:
pip install -r requirements.txt

2.Run ingestion & ETL pipeline:
python src/ingestion/generate_raw_data.py
python src/processing/etl_pipeline.py

3.Launch the Streamlit dashboard:
streamlit run dashboard/app.py