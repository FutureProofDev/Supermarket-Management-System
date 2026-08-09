create view v_low_stock_alert as
select 
    p.product_id,
    p.name as product_name,
    c.name as category_name,
    i.quantity_on_hand,
    i.reorder_level,
    s.name as supplier_name,
    s.contact_phone as supplier_phone
from inventory i
join product p on i.product_id = p.product_id
join category c on p.category_id = c.category_id
join supplier s on p.supplier_id = s.supplier_id
where i.quantity_on_hand <= i.reorder_level;

-- View 2: Cashier / Employee sales summary
create view v_employee_sales_summary as
select 
    e.employee_id,
    concat(e.first_name, ' ', e.last_name) as employee_name,
    e.role,
    count(s.sale_id) as total_transactions,
    coalesce(sum(s.total_amount), 0.00) as total_revenue_generated
from employee e
left join sale s on e.employee_id = s.employee_id
group by e.employee_id, e.first_name, e.last_name, e.role;

-- View 3: Customer spending and loyalty card points
create view v_customer_loyalty_summary as
select 
    c.customer_id,
    concat(c.first_name, ' ', c.last_name) as customer_name,
    c.phone,
    lc.card_id,
    coalesce(lc.points_balance, 0) as loyalty_points,
    count(distinct s.sale_id) as total_purchases,
    coalesce(sum(s.total_amount), 0.00) as total_spent
from customer c
left join loyalty_card lc on c.customer_id = lc.customer_id
left join sale s on c.customer_id = s.customer_id
group by c.customer_id, c.first_name, c.last_name, c.phone, lc.card_id, lc.points_balance;

-- View 4: Product performance overview
create view v_product_performance as
select 
    p.product_id,
    p.name as product_name,
    p.unit_price,
    coalesce(sum(si.quantity), 0) as total_units_sold,
    coalesce(sum(si.line_total), 0.00) as total_revenue
from product p
left join sale_item si on p.product_id = si.product_id
group by p.product_id, p.name, p.unit_price;

-- View 5: Pending purchase orders with supplier contacts
create view v_pending_purchase_orders as
select 
    po.po_id,
    s.name as supplier_name,
    s.contact_phone,
    s.email,
    po.order_date,
    count(poi.po_item_id) as total_items_ordered,
    coalesce(sum(poi.quantity * poi.unit_cost), 0.00) as estimated_order_cost
from purchase_order po
join supplier s on po.supplier_id = s.supplier_id
left join purchase_order_item poi on po.po_id = poi.po_id
where po.status = 'Pending'
group by po.po_id, s.name, s.contact_phone, s.email, po.order_date;