/*
==========================================================
Applied Retail Customer Analytics
Author: Mike Lan

Synthetic data only. No proprietary client/employer data.

Purpose:
Demonstrate business-oriented SQL analysis across customer,
transaction, channel, category, and promotion data.
==========================================================
*/

-- Q1: Which customer segment generates the most revenue?
-- Revenue and order behavior by loyalty status and region

SELECT
    c.region,
    c.loyalty_member,
    COUNT(DISTINCT t.customer_id) AS active_customers,
    COUNT(DISTINCT t.order_id) AS orders,
    ROUND(SUM(t.revenue), 2) AS total_revenue,
    ROUND(AVG(t.revenue), 2) AS avg_order_value,
    ROUND(
        SUM(t.revenue) / COUNT(DISTINCT t.customer_id),
        2
    ) AS revenue_per_active_customer
FROM transactions t
JOIN customers c
    ON t.customer_id = c.customer_id
GROUP BY
    1, 2
ORDER BY
    total_revenue DESC;
	

-- Q2: Who are the highest-value customers within each region?
-- Top five customers by lifetime revenue within each region

WITH customer_value AS (
    SELECT
        c.customer_id,
        c.region,
        c.loyalty_member,
        COUNT(DISTINCT t.order_id) AS total_orders,
        ROUND(SUM(t.revenue), 2) AS total_revenue
    FROM customers c
    JOIN transactions t
        ON c.customer_id = t.customer_id
    GROUP BY
        c.customer_id,
        c.region,
        c.loyalty_member
),

ranked_customers AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY total_revenue DESC
        ) AS regional_rank
    FROM customer_value
)

SELECT *
FROM ranked_customers
WHERE regional_rank <= 5
ORDER BY
    region,
    regional_rank;
	
	
-- Q3: How does repeat beahvior vary by first-purchase cohort?
-- Repeat purchase behavior by observed first-purchase

WITH first_purchase AS (
    SELECT
        customer_id,
        DATE_TRUNC(
            'month',
            MIN(CAST(order_date AS DATE))
        ) AS first_purchase_month
    FROM transactions
    GROUP BY customer_id
),

customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(revenue) AS total_revenue
    FROM transactions
    GROUP BY customer_id
)

SELECT
    fp.first_purchase_month,
    COUNT(*) AS customers,
    ROUND(
        AVG(
            CASE
                WHEN co.total_orders > 1 THEN 1.0
                ELSE 0.0
            END
        ),
        3
    ) AS repeat_customer_rate,
    ROUND(
        AVG(co.total_orders),
        2
    ) AS avg_orders_per_customer,
    ROUND(
        AVG(co.total_revenue),
        2
    ) AS avg_revenue_per_customer
FROM first_purchase fp
JOIN customer_orders co
    ON fp.customer_id = co.customer_id
GROUP BY 1
ORDER BY 1;


-- Q4: How do channel and category economics differ?
-- Channel x category groupby performance

SELECT
    channel,
    category,
    COUNT(DISTINCT order_id) AS orders,
    SUM(units) AS units,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    ROUND(AVG(discount_pct), 2) AS avg_discount_pct
FROM transactions
GROUP BY
    channel,
    category
ORDER BY
    revenue DESC;
	
	
-- Q5: Which categories are accelerating or slowing down?
-- Month-over-month category revenue growth

WITH monthly_category AS (
    SELECT
        DATE_TRUNC(
            'month',
            CAST(order_date AS DATE)
        ) AS month,
        category,
        SUM(revenue) AS monthly_revenue
    FROM transactions
    GROUP BY
        month,
        category
),

with_previous AS (
    SELECT
        month,
        category,
        monthly_revenue,
        LAG(monthly_revenue) OVER (
            PARTITION BY category
            ORDER BY month
        ) AS previous_month_revenue
    FROM monthly_category
)

SELECT
    month,
    category,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        100.0 *
        (
            monthly_revenue - previous_month_revenue
        )
        / NULLIF(previous_month_revenue, 0),
        2
    ) AS mom_growth_pct
FROM with_previous
ORDER BY
    category,
    month;
	
	
-- Q6: Naive observation of promotion campaign performance
-- IMPORTANT: This is association, not causal lift.

SELECT
    promotion_received,
    COUNT(*) AS customers,
    SUM(purchased_30d) AS buyers,
    ROUND(
        AVG(purchased_30d),
        4
    ) AS purchase_rate,
    ROUND(
        AVG(revenue_30d),
        2
    ) AS avg_revenue_30d
FROM campaign_exposure
GROUP BY promotion_received
ORDER BY promotion_received;