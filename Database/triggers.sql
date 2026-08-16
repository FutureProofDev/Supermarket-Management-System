USE supermarket_db;


-- AUTOMATED TRIGGERS 

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

-- Trigger 2: Auto-add loyalty points on completed checkout 
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

-- Trigger 3: Prevent sale item insert if stock on hand is not enough
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