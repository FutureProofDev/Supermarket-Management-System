USE supermarket_db;

-- USER-DEFINED FUNCTIONS 


DELIMITER //

DROP FUNCTION IF EXISTS fn_greeting_for_hour //

CREATE FUNCTION fn_greeting_for_hour(p_hour INT)
RETURNS VARCHAR(30)
DETERMINISTIC
BEGIN
    DECLARE v_greeting VARCHAR(30);
    
    IF p_hour BETWEEN 5 AND 11 THEN
        SET v_greeting = 'Good Morning';
    ELSEIF p_hour BETWEEN 12 AND 16 THEN
        SET v_greeting = 'Good Afternoon';
    ELSEIF p_hour BETWEEN 17 AND 21 THEN
        SET v_greeting = 'Good Evening';
    ELSE
        SET v_greeting = 'Welcome';
    END IF;

    RETURN v_greeting;
END //

DELIMITER ;




-- STORED PROCEDURE

-- Auto-generate Purchase Orders for Low Stock Items
DELIMITER //

DROP PROCEDURE IF EXISTS sp_customer_order_history //

CREATE PROCEDURE sp_customer_order_history(IN p_customer_id INT)
BEGIN
    -- Customer core profile and lifetime metrics
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.phone_number,
        c.created_at AS member_since,
        COUNT(s.sale_id) AS total_orders,
        COALESCE(SUM(s.total_amount), 0.00) AS lifetime_spend
    FROM customer c
    LEFT JOIN sale s ON c.customer_id = s.customer_id
    WHERE c.customer_id = p_customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone_number, c.created_at;

    -- Recent transactions
    SELECT 
        sale_id,
        sale_date,
        total_amount,
        payment_method
    FROM sale
    WHERE customer_id = p_customer_id
    ORDER BY sale_date DESC
    LIMIT 5;
END //

DELIMITER ;

DELIMITER //

DROP PROCEDURE IF EXISTS sp_customer_order_history //

CREATE PROCEDURE sp_customer_order_history(IN p_customer_id INT)
BEGIN
    SELECT 
        s.id AS sale_id,
        s.created_at AS sale_date,
        s.total_amount,
        s.payment_method
    FROM sale s
    WHERE s.customer_id = p_customer_id
    ORDER BY s.created_at DESC;
END //

DELIMITER ;