USE supermarket_db;

--  VIEWS 
-- View 1: Low Stock Alerts
CREATE OR REPLACE VIEW vw_low_stock_alerts AS
SELECT 
    p.product_id,
    p.barcode,
    p.name AS product_name,
    c.name AS category_name,
    i.quantity_on_hand,
    i.reorder_level,
    (i.reorder_level - i.quantity_on_hand) AS shortage_amount,
    CASE 
        WHEN i.quantity_on_hand = 0 THEN 'Out of Stock'
        ELSE 'Reorder Required'
    END AS alert_status
FROM inventory i
JOIN product p ON i.product_id = p.product_id
JOIN category c ON p.category_id = c.category_id
WHERE i.quantity_on_hand <= i.reorder_level;

-- View 2: Daily Cashier Performance
CREATE OR REPLACE VIEW vw_cashier_daily_sales AS
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    CONCAT(e.first_name, ' ', e.last_name) AS cashier_name,
    DATE(s.sale_date) AS sales_date,
    COUNT(DISTINCT s.sale_id) AS total_transactions,
    COALESCE(SUM(s.total_amount), 0) AS total_revenue
FROM employee e
JOIN sale s ON e.employee_id = s.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name, DATE(s.sale_date)
ORDER BY e.last_name, e.first_name;

-- View 3: Customer Loyalty Summary
CREATE OR REPLACE VIEW vw_customer_summary AS
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.phone,
    c.email,
    COALESCE(lc.points_balance, 0) AS points_balance,
    COUNT(DISTINCT s.sale_id) AS total_orders,
    COALESCE(SUM(s.total_amount), 0) AS total_spent
FROM customer c
LEFT JOIN loyalty_card lc ON c.customer_id = lc.customer_id
LEFT JOIN sale s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.phone, c.email, lc.points_balance
ORDER BY c.last_name, c.first_name;

-- View 4: Product Sales Performance
CREATE OR REPLACE VIEW vw_product_sales_performance AS
SELECT 
    p.product_id,
    p.name AS product_name,
    c.name AS category_name,
    COALESCE(SUM(si.quantity), 0) AS total_quantity_sold,
    COALESCE(SUM(si.line_total), 0) AS total_revenue_generated
FROM product p
JOIN category c ON p.category_id = c.category_id
LEFT JOIN sale_item si ON p.product_id = si.product_id
GROUP BY p.product_id, p.name, c.name;


-- View 5: Category Overview

CREATE OR REPLACE VIEW vw_category_overview AS
SELECT
    c.category_id,
    c.name AS category_name,
    COUNT(p.product_id) AS product_count,
    ROUND(AVG(p.unit_price), 2) AS avg_unit_price,
    ROUND(MIN(p.unit_price), 2) AS min_price,
    ROUND(MAX(p.unit_price), 2) AS max_price
FROM category c
LEFT JOIN product p ON c.category_id = p.category_id
GROUP BY c.category_id, c.name;


-- View 6: Active Discounts

CREATE OR REPLACE VIEW vw_active_discounts AS
SELECT
    discount_id,
    name,
    percent_off,
    start_date,
    end_date,
    DATEDIFF(end_date, CURDATE()) AS days_remaining
FROM discount
WHERE CURDATE() BETWEEN start_date AND end_date;


-- View 7: Near-Expiry Products

CREATE OR REPLACE VIEW vw_near_expiry_products AS
SELECT
    p.product_id,
    p.name AS product_name,
    p.expiry_date,
    DATEDIFF(p.expiry_date, CURDATE()) AS days_until_expiry,
    i.quantity_on_hand
FROM product p
JOIN inventory i ON p.product_id = i.product_id
WHERE p.expiry_date IS NOT NULL
  AND p.expiry_date <= DATE_ADD(CURDATE(), INTERVAL 45 DAY)
ORDER BY p.expiry_date ASC;


-- View 8: Employees Without a Linked Login

CREATE OR REPLACE VIEW vw_unlinked_employees AS
SELECT
    employee_id,
    CONCAT(first_name, ' ', last_name) AS employee_name,
    role,
    email
FROM employee
WHERE user_id IS NULL;


-- View 9: Customers Without a Loyalty Card

CREATE OR REPLACE VIEW vw_customers_without_loyalty AS
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.phone,
    c.email
FROM customer c
LEFT JOIN loyalty_card lc ON c.customer_id = lc.customer_id
WHERE lc.card_id IS NULL;