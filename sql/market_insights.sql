-- =========================================================================
-- BiH REAL ESTATE MARKET INTELLIGENCE - ANALYTICAL SQL QUERIES
-- Database: DuckDB / Compatible with PostgreSQL
-- =========================================================================

-- 1. Average price per square meter and total price by city
SELECT 
    city,
    COUNT(*) AS total_listings,
    ROUND(AVG(price_per_m2), 2) AS avg_price_per_m2,
    ROUND(AVG(price_bam), 2) AS avg_total_price,
    MIN(price_per_m2) AS min_price_per_m2,
    MAX(price_per_m2) AS max_price_per_m2
FROM fact_listings
GROUP BY city
ORDER BY avg_price_per_m2 DESC;


-- 2. Price comparison: New Buildings vs Older Buildings
SELECT 
    CASE 
        WHEN is_new_building = 1 THEN 'New Building (2020+)' 
        ELSE 'Older Building' 
    END AS building_status,
    COUNT(*) AS listings_count,
    ROUND(AVG(price_per_m2), 2) AS avg_price_per_m2,
    ROUND(AVG(area_m2), 2) AS avg_area_m2
FROM fact_listings
GROUP BY is_new_building
ORDER BY avg_price_per_m2 DESC;


-- 3. Market breakdown by property type and number of rooms
SELECT 
    property_type,
    rooms,
    COUNT(*) AS listings_count,
    ROUND(AVG(price_bam), 2) AS avg_price_bam,
    ROUND(AVG(price_per_m2), 2) AS avg_price_per_m2
FROM fact_listings
GROUP BY property_type, rooms
ORDER BY property_type, rooms;


-- 4. Top 10 most expensive listings relative to their size (Outlier/Luxury check)
SELECT 
    listing_id,
    city,
    property_type,
    area_m2,
    price_bam,
    price_per_m2,
    construction_year
FROM fact_listings
ORDER BY price_per_m2 DESC
LIMIT 10;