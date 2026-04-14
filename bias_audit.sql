-- AI GOVERNANCE AUDIT: PROXIMITY DISCRIMINATION CHECK
-- TARGET: Detect price gouging based on user device type.

SELECT 
    device_type,
    COUNT(*) as total_users,
    ROUND(AVG(base_price), 2) as avg_base_price,
    ROUND(AVG(final_price), 2) as avg_final_price,
    -- Calculate the "Markup Percentage"
    ROUND(((AVG(final_price) - AVG(base_price)) / AVG(base_price)) * 100, 2) as markup_pct
FROM 
    booking_logs_mock
GROUP BY 
    device_type
ORDER BY 
    markup_pct DESC;