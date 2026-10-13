import os
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="BiH Real Estate Intelligence",
    page_icon="🏢",
    layout="wide"
)

# Database connection path
DB_PATH = os.path.join("data", "warehouse", "bih_real_estate.duckdb")

@st.cache_resource
def get_data():
    if not os.path.exists(DB_PATH):
        return None
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT * FROM fact_listings").fetchdf()
    conn.close()
    return df

df = get_data()

if df is None:
    st.error("⚠️ Database not found! Please run the ETL pipeline first (`python src/processing/etl_pipeline.py`).")
else:
    # Sidebar Filters
    st.sidebar.header("🔍 Filter Options")
    
    selected_city = st.sidebar.selectbox(
        "Select City",
        options=["All Cities"] + sorted(df['city'].unique().tolist())
    )
    
    selected_type = st.sidebar.multiselect(
        "Property Type",
        options=df['property_type'].unique().tolist(),
        default=df['property_type'].unique().tolist()
    )

    # Filter dataframe based on selections
    filtered_df = df.copy()
    if selected_city != "All Cities":
        filtered_df = filtered_df[filtered_df['city'] == selected_city]
    if selected_type:
        filtered_df = filtered_df[filtered_df['property_type'].isin(selected_type)]

    # Main Dashboard Title
    st.title("🏢 Bosnia & Herzegovina Real Estate Market Intelligence")
    st.markdown("An interactive analytics dashboard tracking property prices, trends, and market distributions.")

    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Listings", f"{len(filtered_df):,}")
    with col2:
        avg_price = filtered_df['price_bam'].mean() if len(filtered_df) > 0 else 0
        st.metric("Avg Total Price", f"{avg_price:,.2f} BAM")
    with col3:
        avg_m2 = filtered_df['price_per_m2'].mean() if len(filtered_df) > 0 else 0
        st.metric("Avg Price / m²", f"{avg_m2:,.2f} BAM")
    with col4:
        avg_area = filtered_df['area_m2'].mean() if len(filtered_df) > 0 else 0
        st.metric("Avg Area", f"{avg_area:.1f} m²")

    st.markdown("---")

    # Charts Row 1
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📊 Average Price per m² by City")
        if not filtered_df.empty:
            city_price = filtered_df.groupby('city')['price_per_m2'].mean().reset_index().sort_values(by='price_per_m2', ascending=False)
            fig_city = px.bar(
                city_price, x='city', y='price_per_m2',
                text_auto='.2s', color='price_per_m2',
                color_continuous_scale='Blues',
                labels={'price_per_m2': 'Avg Price per m² (BAM)', 'city': 'City'}
            )
            st.plotly_chart(fig_city, use_container_width=True)
        else:
            st.warning("No data available for selected filters.")

    with col_b:
        st.subheader("🏠 Price vs. Area (Scatter Plot)")
        if not filtered_df.empty:
            fig_scatter = px.scatter(
                filtered_df, x='area_m2', y='price_bam',
                color='property_type', opacity=0.7,
                labels={'area_m2': 'Area (m²)', 'price_bam': 'Price (BAM)'},
                hover_data=['city', 'rooms']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No data available for selected filters.")

    # Data Table Preview
    st.subheader("📋 Raw Data Explorer")
    st.dataframe(filtered_df.head(100), use_container_width=True)