USE supermarket__db;


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

-- View 5: Supplier Procurement Summary
CREATE OR REPLACE VIEW vw_supplier_po_summary AS
SELECT 
    sup.supplier_id,
    sup.name AS supplier_name,
    COUNT(DISTINCT po.po_id) AS total_purchase_orders,
    COALESCE(SUM(poi.quantity * poi.unit_cost), 0) AS total_procurement_spend
FROM supplier sup
LEFT JOIN purchase_order po ON sup.supplier_id = po.supplier_id
LEFT JOIN purchase_order_item poi ON po.po_id = poi.po_id
GROUP BY sup.supplier_id, sup.name;


-- ========================================================
-- 2. AUTOMATED TRIGGERS (3 TRIGGERS)
-- ========================================================

DELIMITER //

-- Trigger 1: Auto-deduct stock after sale item insert
CREATE TRIGGER trg_after_sale_item_insert
AFTER INSERT ON sale_item
FOR EACH ROW
BEGIN
    UPDATE inventory
    SET quantity_on_hand = quantity_on_hand - NEW.quantity
    WHERE product_id = NEW.product_id;
END//

-- Trigger 2: Auto-add loyalty points on completed checkout (1 point per GHS 10 spent)
CREATE TRIGGER trg_after_sale_loyalty_update
AFTER INSERT ON sale
FOR EACH ROW
BEGIN
    IF NEW.customer_id IS NOT NULL THEN
        UPDATE loyalty_card
        SET points_balance = points_balance + FLOOR(NEW.total_amount / 10)
        WHERE customer_id = NEW.customer_id;
    END IF;
END//

-- Trigger 3: Prevent sale item insert if stock on hand is insufficient
CREATE TRIGGER trg_prevent_insufficient_stock
BEFORE INSERT ON sale_item
FOR EACH ROW
BEGIN
    DECLARE v_available_qty INT;
    
    SELECT quantity_on_hand INTO v_available_qty
    FROM inventory
    WHERE product_id = NEW.product_id;
    
    IF v_available_qty < NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transaction aborted: Insufficient stock on hand for this product.';
    END IF;
END//

DELIMITER ;


-- ========================================================
-- 3. USER-DEFINED FUNCTIONS (2 UDFs)
-- ========================================================

DELIMITER //

-- Function 1: Calculate discounted price
CREATE FUNCTION fn_calculate_discounted_price(
    p_unit_price DECIMAL(10,2),
    p_quantity INT,
    p_discount_id INT
) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_percent DECIMAL(5,2) DEFAULT 0.00;
    DECLARE v_total DECIMAL(10,2);
    
    IF p_discount_id IS NOT NULL THEN
        SELECT percent_off INTO v_percent 
        FROM discount 
        WHERE discount_id = p_discount_id;
    END IF;
    
    SET v_total = (p_unit_price * p_quantity) * (1 - (v_percent / 100));
    RETURN ROUND(v_total, 2);
END//

-- Function 2: Determine loyalty tier based on points balance
CREATE FUNCTION fn_get_customer_tier(p_points INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    IF p_points >= 200 THEN
        RETURN 'Gold';
    ELSEIF p_points >= 100 THEN
        RETURN 'Silver';
    ELSE
        RETURN 'Bronze';
    END IF;
END//

DELIMITER ;


-- ========================================================
-- 4. STORED PROCEDURES (3 STORED PROCEDURES)
-- ========================================================

DELIMITER //

-- Procedure 1: Auto-generate Purchase Orders for Low Stock Items
CREATE PROCEDURE sp_auto_generate_low_stock_po(
    IN p_employee_id INT,
    IN p_supplier_id INT
)
BEGIN
    DECLARE v_po_id INT;
    
    INSERT INTO purchase_order (supplier_id, employee_id, status)
    VALUES (p_supplier_id, p_employee_id, 'Draft');
    
    SET v_po_id = LAST_INSERT_ID();
    
    INSERT INTO purchase_order_item (po_id, product_id, quantity, unit_cost)
    SELECT 
        v_po_id,
        p.product_id,
        (i.reorder_level * 2) AS recommended_qty,
        ROUND(p.unit_price * 0.70, 2)
    FROM inventory i
    JOIN product p ON i.product_id = p.product_id
    WHERE i.quantity_on_hand <= i.reorder_level;
    
    SELECT CONCAT('Purchase Order #', v_po_id, ' drafted successfully.') AS result;
END//

-- Procedure 2: Apply promotional discount percentage to an entire category
CREATE PROCEDURE sp_apply_category_discount(
    IN p_category_id INT,
    IN p_discount_name VARCHAR(100),
    IN p_percent_off DECIMAL(5,2),
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    INSERT INTO discount (name, percent_off, start_date, end_date)
    VALUES (p_discount_name, p_percent_off, p_start_date, p_end_date);
    
    SELECT CONCAT('Discount "', p_discount_name, '" added for category ID ', p_category_id) AS confirmation;
END//

-- Procedure 3: Monthly Sales Summary Report
CREATE PROCEDURE sp_generate_monthly_sales_report(
    IN p_year INT,
    IN p_month INT
)
BEGIN
    SELECT 
        COUNT(s.sale_id) AS total_sales_count,
        COALESCE(SUM(s.total_amount), 0) AS total_monthly_revenue,
        COALESCE(AVG(s.total_amount), 0) AS average_transaction_value
    FROM sale s
    WHERE YEAR(s.sale_date) = p_year AND MONTH(s.sale_date) = p_month;
END//

DELIMITER ;


-- ========================================================
-- 5. ADVANCED SQL QUERIES (10 QUERIES)
-- ========================================================

-- Query 1: Rank products by sales revenue within each category using DENSE_RANK()
SELECT 
    c.name AS category_name,
    p.name AS product_name,
    SUM(si.line_total) AS total_revenue,
    DENSE_RANK() OVER (PARTITION BY c.category_id ORDER BY SUM(si.line_total) DESC) AS revenue_rank
FROM product p
JOIN category c ON p.category_id = c.category_id
JOIN sale_item si ON p.product_id = si.product_id
GROUP BY c.category_id, c.name, p.product_id, p.name;

-- Query 2: Identify high-value customers who spend more than the average customer spending
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

-- Query 3: Running total of daily sales revenue using window functions
SELECT 
    DATE(sale_date) AS sales_date,
    SUM(total_amount) AS daily_revenue,
    SUM(SUM(total_amount)) OVER (ORDER BY DATE(sale_date)) AS cumulative_running_revenue
FROM sale
GROUP BY DATE(sale_date);

-- Query 4: Month-over-Month (MoM) revenue comparison using LAG()
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

-- Query 5: Find products with retail price margins compared to procurement cost
SELECT 
    p.product_id,
    p.name AS product_name,
    p.unit_price AS retail_price,
    ROUND(AVG(poi.unit_cost), 2) AS avg_procurement_cost,
    ROUND(p.unit_price - AVG(poi.unit_cost), 2) AS estimated_profit_margin
FROM product p
JOIN purchase_order_item poi ON p.product_id = poi.product_id
GROUP BY p.product_id, p.name, p.unit_price;

-- Query 6: Find all registered customers who have never placed an order
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

-- Query 7: Category revenue breakdown with percentage contribution to total sales
SELECT 
    c.name AS category_name,
    SUM(si.line_total) AS category_revenue,
    ROUND((SUM(si.line_total) / (SELECT SUM(line_total) FROM sale_item)) * 100, 2) AS percentage_contribution
FROM category c
JOIN product p ON c.category_id = p.category_id
JOIN sale_item si ON p.product_id = si.product_id
GROUP BY c.category_id, c.name
ORDER BY category_revenue DESC;

-- Query 8: Cashiers processing more transactions than the overall cashier average
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

-- Query 9: Customers who bought products across more than 2 distinct categories
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(DISTINCT p.category_id) AS distinct_categories_purchased
FROM customer c
JOIN sale s ON c.customer_id = s.customer_id
JOIN sale_item si ON s.sale_id = si.sale_id
JOIN product p ON si.product_id = p.product_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(DISTINCT p.category_id) > 2
ORDER BY c.last_name, c.first_name;

-- Query 10: Evaluate customer loyalty tiers dynamically using the UDF
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    lc.points_balance,
    fn_get_customer_tier(lc.points_balance) AS calculated_loyalty_tier
FROM customer c
JOIN loyalty_card lc ON c.customer_id = lc.customer_id
ORDER BY lc.points_balance DESC, c.last_name, c.first_name;