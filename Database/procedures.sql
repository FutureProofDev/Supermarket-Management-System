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


-- STORED PROCEDURES

DELIMITER //

DROP PROCEDURE IF EXISTS sp_customer_order_history //

CREATE PROCEDURE sp_customer_order_history(IN p_customer_id INT)
BEGIN
    SELECT 
        s.sale_id,
        s.sale_date,
        s.total_amount,
        CONCAT(e.first_name, ' ', e.last_name) AS served_by
    FROM sale s
    JOIN employee e ON s.employee_id = e.employee_id
    WHERE s.customer_id = p_customer_id
    ORDER BY s.sale_date DESC;
END //

DELIMITER ;