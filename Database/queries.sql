USE supermarket_db;


-- ADVANCED SQL QUERIES (10 QUERIES)
-- 1: Rank products by sales revenue within each category using DENSE_RANK()
SELECT 
    c.name AS category_name,
    p.name AS product_name,
    SUM(si.line_total) AS total_revenue,
    DENSE_RANK() OVER (PARTITION BY c.category_id ORDER BY SUM(si.line_total) DESC) AS revenue_rank
FROM product p
JOIN category c ON p.category_id = c.category_id
JOIN sale_item si ON p.product_id = si.product_id
GROUP BY c.category_id, c.name, p.product_id, p.name;

-- 2: Identify high-value customers who spend more than the average customer spending
WITH CustomerSpending AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        SUM(s.total_amount) AS total_spent
    FROM customer c
    JOIN sale s ON c.customer_id = s.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT 
    first_name,
    last_name,
    total_spent
FROM CustomerSpending
WHERE total_spent > (SELECT AVG(total_spent) FROM CustomerSpending)
ORDER BY last_name, first_name;

--  3: Running total of daily sales revenue using window functions
SELECT 
    DATE(sale_date) AS sales_date,
    SUM(total_amount) AS daily_revenue,
    SUM(SUM(total_amount)) OVER (ORDER BY DATE(sale_date)) AS cumulative_running_revenue
FROM sale
GROUP BY DATE(sale_date);

-- 4: Month-over-Month revenue comparison using LAG()
WITH MonthlyRevenue AS (
    SELECT 
        DATE_FORMAT(sale_date, '%Y-%m') AS sales_month,
        SUM(total_amount) AS current_month_revenue
    FROM sale
    GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
)
SELECT 
    sales_month,
    current_month_revenue,
    LAG(current_month_revenue, 1) OVER (ORDER BY sales_month) AS previous_month_revenue,
    ROUND(((current_month_revenue - LAG(current_month_revenue, 1) OVER (ORDER BY sales_month)) / 
           LAG(current_month_revenue, 1) OVER (ORDER BY sales_month)) * 100, 2) AS mom_growth_percent
FROM MonthlyRevenue;

-- 5: Find products with retail price margins compared to cost
SELECT 
    p.product_id,
    p.name AS product_name,
    p.unit_price AS retail_price,
    ROUND(AVG(poi.unit_cost), 2) AS avg_procurement_cost,
    ROUND(p.unit_price - AVG(poi.unit_cost), 2) AS estimated_profit_margin
FROM product p
JOIN purchase_order_item poi ON p.product_id = poi.product_id
GROUP BY p.product_id, p.name, p.unit_price;

-- 6: Find all registered customers who have never placed an order
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.phone,
    c.email
FROM customer c
LEFT JOIN sale s ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
ORDER BY c.last_name, c.first_name;

-- 7: Category revenue breakdown with percentage contribution to total sales
SELECT 
    c.name AS category_name,
    SUM(si.line_total) AS category_revenue,
    ROUND((SUM(si.line_total) / (SELECT SUM(line_total) FROM sale_item)) * 100, 2) AS percentage_contribution
FROM category c
JOIN product p ON c.category_id = p.category_id
JOIN sale_item si ON p.product_id = si.product_id
GROUP BY c.category_id, c.name
ORDER BY category_revenue DESC;

-- 8: Cashiers processing more transactions than the cashier average
WITH CashierStats AS (
    SELECT 
        e.employee_id,
        e.first_name,
        e.last_name,
        COUNT(s.sale_id) AS total_sales_handled
    FROM employee e
    JOIN sale s ON e.employee_id = s.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
)
SELECT 
    first_name,
    last_name,
    total_sales_handled
FROM CashierStats
WHERE total_sales_handled >= (SELECT AVG(total_sales_handled) FROM CashierStats)
ORDER BY last_name, first_name;

