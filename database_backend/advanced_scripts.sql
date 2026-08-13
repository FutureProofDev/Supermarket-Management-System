use supermarket_db;


-- 1. ENTERPRISE VIEWS

-- Low Stock Alert View: Identifies products at or below reorder threshold
create or replace view vw_low_stock_alerts as
select 
    p.product_id,
    p.barcode,
    p.name as product_name,
    c.name as category_name,
    i.quantity_on_hand,
    i.reorder_level,
    (i.reorder_level - i.quantity_on_hand) as shortage_amount,
    case 
        when i.quantity_on_hand = 0 then 'out of stock'
        else 'reorder required'
    end as alert_status
from inventory i
join product p on i.product_id = p.product_id
join category c on p.category_id = c.category_id
where i.quantity_on_hand <= i.reorder_level;

-- Daily Cashier Performance View
create or replace view vw_cashier_daily_sales as
select 
    e.employee_id,
    e.name as cashier_name,
    date(s.sale_date) as sales_date,
    count(distinct s.sale_id) as total_transactions,
    coalesce(sum(s.total_amount), 0) as gross_revenue
from employee e
join sale s on e.employee_id = s.employee_id
group by e.employee_id, e.name, date(s.sale_date);



-- 2. AUTOMATED TRIGGERS


delimiter //

-- Trigger 1: Auto-deduct inventory after a sale item is inserted
create trigger trg_after_sale_item_insert
after insert on sale_item
for each row
begin
    update inventory
    set quantity_on_hand = quantity_on_hand - new.quantity
    where product_id = new.product_id;
end//

-- Trigger 2: Auto-add loyalty points on completed checkout (1 point per GHS 10 spent)
create trigger trg_after_sale_loyalty_update
after insert on sale
for each row
begin
    if new.customer_id is not null then
        update loyalty_card
        set points_balance = points_balance + floor(new.total_amount / 10)
        where customer_id = new.customer_id;
    end if;
end//

delimiter ;

-- ========================================================
-- 3. STORED PROCEDURES & FUNCTIONS
-- ========================================================

delimiter //

-- Function: Calculate discounted line total
create function fn_calculate_discounted_price(
    p_unit_price decimal(10,2),
    p_quantity int,
    p_discount_id int
) 
returns decimal(10,2)
deterministic
begin
    declare v_percent decimal(5,2) default 0.00;
    declare v_total decimal(10,2);
    
    if p_discount_id is not null then
        select percent_off into v_percent 
        from discount 
        where discount_id = p_discount_id;
    end if;
    
    set v_total = (p_unit_price * p_quantity) * (1 - (v_percent / 100));
    return round(v_total, 2);
end//

-- Procedure: Auto-generate Purchase Orders for Low Stock Items
create procedure sp_auto_generate_low_stock_po(
    in p_employee_id int,
    in p_supplier_id int
)
begin
    declare v_po_id int;
    
    -- create po header
    insert into purchase_order (supplier_id, employee_id, status)
    values (p_supplier_id, p_employee_id, 'Draft');
    
    set v_po_id = last_insert_id();
    
    -- populate po items with recommended reorder quantities
    insert into purchase_order_item (po_id, product_id, quantity, unit_cost)
    select 
        v_po_id,
        p.product_id,
        (i.reorder_level * 2) as recommended_qty,
        round(p.unit_price * 0.70, 2) -- estimated cost price
    from inventory i
    join product p on i.product_id = p.product_id
    where i.quantity_on_hand <= i.reorder_level;
    
    select concat('purchase order #', v_po_id, ' drafted successfully.') as result;
end//

delimiter ;