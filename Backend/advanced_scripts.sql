
-- ---------------------------------------------------------------------
-- Q4. Top customers by lifetime spend, with loyalty balance
-- Business use: VIP/loyalty marketing targeting.
-- LEFT JOIN on loyalty_card because not every buyer has enrolled.
-- ---------------------------------------------------------------------
SELECT TOP 5
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(s.sale_id) AS num_purchases,
    SUM(s.total_amount) AS lifetime_spend,
    lc.points_balance
FROM customer c
JOIN sale s ON s.customer_id = c.customer_id
LEFT JOIN loyalty_card lc ON lc.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, lc.points_balance
ORDER BY lifetime_spend DESC;
 
 
-- ---------------------------------------------------------------------
-- Q5. Products that have never sold (anti-join)
-- Business use: flag dead stock for clearance/discontinuation review.
-- ---------------------------------------------------------------------
SELECT p.product_id, p.name, p.unit_price
FROM product p
LEFT JOIN sale_item si ON si.product_id = p.product_id
WHERE si.sale_item_id IS NULL
ORDER BY p.product_id;
 
 
-- ---------------------------------------------------------------------
-- Q6. Low-stock reorder report with supplier contact
-- Business use: feeds directly into raising a new purchase_order.
-- ---------------------------------------------------------------------
SELECT
    p.product_id,
    p.name,
    i.quantity_on_hand,
    i.reorder_level,
    s.name AS supplier_name,
    s.contact_phone,
    s.email
FROM inventory i
JOIN product p ON p.product_id = i.product_id
JOIN supplier s ON s.supplier_id = p.supplier_id
WHERE i.quantity_on_hand <= i.reorder_level
ORDER BY (i.quantity_on_hand - i.reorder_level) ASC;
 
 
-- ---------------------------------------------------------------------
-- Q7. Revenue contribution % by category (window function)
-- Business use: category mix analysis for buying/merchandising decisions.
-- ---------------------------------------------------------------------
WITH category_revenue AS (
    SELECT
        c.name AS category_name,
        SUM(si.line_total) AS category_revenue
    FROM sale_item si
    JOIN product p ON p.product_id = si.product_id
    JOIN category c ON c.category_id = p.category_id
    GROUP BY c.name
)
SELECT
    category_name,
    category_revenue,
    ROUND(100 * category_revenue / NULLIF(SUM(category_revenue) OVER (), 0), 2) AS pct_of_total_revenue
FROM category_revenue
ORDER BY category_revenue DESC;
 
 
-- ---------------------------------------------------------------------
-- Q8. Running cumulative daily revenue (window function: SUM() OVER (ORDER BY ...))
-- Business use: cash-flow tracking, cumulative sales-to-date charts.
-- ---------------------------------------------------------------------
SELECT
    sale_date_only,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY sale_date_only) AS cumulative_revenue
FROM (
    SELECT CONVERT(DATE, sale_date) AS sale_date_only, SUM(total_amount) AS daily_revenue
    FROM sale
    GROUP BY CONVERT(DATE, sale_date)
) AS daily
ORDER BY sale_date_only;
 
 
-- ---------------------------------------------------------------------
-- Q9. Discount effectiveness: discounted vs. full-price line items
-- Business use: does discounting actually move more revenue per line?
-- ---------------------------------------------------------------------
SELECT
    CASE WHEN si.discount_id IS NULL THEN 'No Discount' ELSE 'Discounted' END AS line_type,
    COUNT(*) AS num_lines,
    ROUND(AVG(si.line_total), 2) AS avg_line_total,
    SUM(si.line_total) AS total_revenue
FROM sale_item si
GROUP BY CASE WHEN si.discount_id IS NULL THEN 'No Discount' ELSE 'Discounted' END;
 
 
-- ---------------------------------------------------------------------
-- Q10. Near-expiry markdown report (uses product.expiry_date)
-- Business use: directly powers the checkout API's automatic 50%
-- near-expiry discount and physical markdown tagging on the shop floor.
-- ---------------------------------------------------------------------
SELECT
    p.product_id,
    p.name,
    p.expiry_date,
    DATEDIFF(DAY, GETDATE(), p.expiry_date) AS days_until_expiry,
    i.quantity_on_hand,
    s.name AS supplier_name
FROM product p
JOIN inventory i ON i.product_id = p.product_id
JOIN supplier s ON s.supplier_id = p.supplier_id
WHERE p.expiry_date IS NOT NULL
  AND DATEDIFF(DAY, GETDATE(), p.expiry_date) <= 45
ORDER BY days_until_expiry ASC;
 
 
-- ---------------------------------------------------------------------
-- Q11. Top suppliers by total purchase-order value
-- Business use: identify which suppliers the store depends on most,
-- useful for negotiating terms or diversifying supply risk.
-- ---------------------------------------------------------------------
SELECT TOP 5
    s.supplier_id,
    s.name,
    COUNT(DISTINCT po.po_id) AS num_orders,
    SUM(poi.quantity * poi.unit_cost) AS total_po_value
FROM supplier s
JOIN purchase_order po ON po.supplier_id = s.supplier_id
JOIN purchase_order_item poi ON poi.po_id = po.po_id
GROUP BY s.supplier_id, s.name
ORDER BY total_po_value DESC;
 
 
-- ---------------------------------------------------------------------
-- Q12. Customer segmentation (CTE + CASE)
-- Business use: quick Gold/Silver/Bronze/Inactive tiering for targeted
-- promotions, without needing a separate reporting tool.
-- ---------------------------------------------------------------------
WITH customer_spend AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        COALESCE(SUM(s.total_amount), 0) AS total_spend,
        COUNT(s.sale_id) AS num_purchases
    FROM customer c
    LEFT JOIN sale s ON s.customer_id = c.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT
    *,
    CASE
        WHEN total_spend >= 150 THEN 'Gold'
        WHEN total_spend >= 50 THEN 'Silver'
        WHEN total_spend > 0 THEN 'Bronze'
        ELSE 'Inactive'
    END AS customer_tier
FROM customer_spend
ORDER BY total_spend DESC;
 
 
-- ---------------------------------------------------------------------
-- Q13. Second-highest-spending customer (window function: DENSE_RANK)
-- Business use: DENSE_RANK (rather than LIMIT 1 OFFSET 1) correctly
-- handles ties for 1st place, which OFFSET-based paging would miss.
-- ---------------------------------------------------------------------
SELECT customer_id, first_name, last_name, total_spend
FROM (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        SUM(s.total_amount) AS total_spend,
        DENSE_RANK() OVER (ORDER BY SUM(s.total_amount) DESC) AS spend_rank
    FROM customer c
    JOIN sale s ON s.customer_id = c.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
) AS ranked
WHERE spend_rank = 2;
 
 
-- ---------------------------------------------------------------------
-- Q14. Products outperforming their own category's average product revenue
-- Business use: identify standout performers within their category.
-- ---------------------------------------------------------------------
WITH product_revenue AS (
    SELECT p.product_id, p.name, p.category_id, SUM(si.line_total) AS product_revenue
    FROM product p
    JOIN sale_item si ON si.product_id = p.product_id
    GROUP BY p.product_id, p.name, p.category_id
),
category_avg AS (
    SELECT category_id, AVG(product_revenue) AS avg_category_product_revenue
    FROM product_revenue
    GROUP BY category_id
)
SELECT
    pr.product_id,
    pr.name,
    pr.category_id,
    pr.product_revenue,
    ROUND(ca.avg_category_product_revenue, 2) AS avg_category_product_revenue
FROM product_revenue pr
JOIN category_avg ca ON ca.category_id = pr.category_id
WHERE pr.product_revenue > ca.avg_category_product_revenue
ORDER BY pr.category_id, pr.product_revenue DESC;
 
 
-- ---------------------------------------------------------------------
-- Q15. Average transaction value by employee role
-- Business use: sanity-check whether more experienced roles ring up larger baskets than Cashiers.
-- ---------------------------------------------------------------------
SELECT
    e.role,
    COUNT(DISTINCT e.employee_id) AS num_employees,
    COUNT(s.sale_id) AS num_transactions,
    ROUND(AVG(s.total_amount), 2) AS avg_transaction_value
FROM employee e
JOIN sale s ON s.employee_id = e.employee_id
GROUP BY e.role
HAVING COUNT(s.sale_id) > 0
ORDER BY avg_transaction_value DESC;
