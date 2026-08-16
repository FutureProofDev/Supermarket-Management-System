USE supermarket_db;

-- USER-DEFINED FUNCTIONS 


DELIMITER //

--  Calculate discounted price
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

-- Determine loyalty tier based on points balance
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


-- STORED PROCEDURES 

-- Auto-generate Purchase Orders for Low Stock Items
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

-- Apply promotional discount percentage to an entire category
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

--  Monthly Sales Summary Report
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