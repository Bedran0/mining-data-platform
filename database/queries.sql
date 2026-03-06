-- ─────────────────────────────────────────────────────────
-- 1. Monthly revenue, cost, and gross profit
-- ─────────────────────────────────────────────────────────
SELECT
    DATE_TRUNC('month', so.order_date)   AS month,
    SUM(soi.total)                        AS revenue,
    SUM(soi.quantity * p.cost_price)      AS cogs,
    SUM(soi.total - soi.quantity * p.cost_price) AS gross_profit
FROM sales_order_items soi
JOIN sales_orders so ON soi.order_id = so.id
JOIN products p      ON soi.product_id = p.id
GROUP BY 1
ORDER BY 1;


-- ─────────────────────────────────────────────────────────
-- 2. Top 10 customers by revenue
-- ─────────────────────────────────────────────────────────
SELECT
    c.company_name,
    c.industry,
    COUNT(DISTINCT so.id)   AS total_orders,
    SUM(soi.total)          AS total_revenue
FROM sales_order_items soi
JOIN sales_orders so ON soi.order_id = so.id
JOIN customers c     ON so.customer_id = c.id
GROUP BY 1, 2
ORDER BY 4 DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────
-- 3. Best selling products by quantity and revenue
-- ─────────────────────────────────────────────────────────
SELECT
    p.code,
    p.name,
    p.category,
    SUM(soi.quantity)   AS total_quantity,
    SUM(soi.total)      AS total_revenue
FROM sales_order_items soi
JOIN products p ON soi.product_id = p.id
GROUP BY 1, 2, 3
ORDER BY 5 DESC;


-- ─────────────────────────────────────────────────────────
-- 4. Overdue invoices (accounts receivable)
-- ─────────────────────────────────────────────────────────
SELECT
    c.company_name,
    i.invoice_number,
    i.due_date,
    i.total_amount,
    COALESCE(SUM(pay.amount), 0)                    AS paid,
    i.total_amount - COALESCE(SUM(pay.amount), 0)   AS outstanding,
    CURRENT_DATE - i.due_date                        AS days_overdue
FROM invoices i
JOIN sales_orders so ON i.order_id = so.id
JOIN customers c     ON so.customer_id = c.id
LEFT JOIN payments pay ON pay.invoice_id = i.id
WHERE i.due_date < CURRENT_DATE
  AND i.status != 'paid'
GROUP BY 1, 2, 3, 4
HAVING i.total_amount - COALESCE(SUM(pay.amount), 0) > 0
ORDER BY 7 DESC;


-- ─────────────────────────────────────────────────────────
-- 5. Current stock levels per product
-- ─────────────────────────────────────────────────────────
SELECT
    p.code,
    p.name,
    p.category,
    p.min_stock,
    SUM(im.quantity)    AS current_stock,
    CASE
        WHEN SUM(im.quantity) < p.min_stock THEN 'LOW'
        WHEN SUM(im.quantity) < p.min_stock * 1.5 THEN 'WARNING'
        ELSE 'OK'
    END AS stock_status
FROM inventory_movements im
JOIN products p ON im.product_id = p.id
GROUP BY 1, 2, 3, 4
ORDER BY 5 ASC;


-- ─────────────────────────────────────────────────────────
-- 6. Salesperson performance
-- ─────────────────────────────────────────────────────────
SELECT
    e.full_name,
    COUNT(DISTINCT so.id)   AS total_orders,
    SUM(soi.total)          AS total_revenue,
    AVG(soi.total)          AS avg_order_value
FROM sales_order_items soi
JOIN sales_orders so ON soi.order_id = so.id
JOIN employees e     ON so.employee_id = e.id
GROUP BY 1
ORDER BY 3 DESC;


-- ─────────────────────────────────────────────────────────
-- 7. Supplier delivery performance
-- ─────────────────────────────────────────────────────────
SELECT
    s.name,
    COUNT(*)                                            AS total_orders,
    AVG(po.actual_delivery - po.expected_delivery)      AS avg_delay_days,
    MAX(po.actual_delivery - po.expected_delivery)      AS max_delay_days
FROM purchase_orders po
JOIN suppliers s ON po.supplier_id = s.id
WHERE po.actual_delivery IS NOT NULL
GROUP BY 1
ORDER BY 3 DESC;


-- ─────────────────────────────────────────────────────────
-- 8. Monthly operational costs by category
-- ─────────────────────────────────────────────────────────
SELECT
    DATE_TRUNC('month', cost_date)  AS month,
    category,
    SUM(amount)                     AS total_cost
FROM operational_costs
GROUP BY 1, 2
ORDER BY 1, 2;


-- ─────────────────────────────────────────────────────────
-- 9. Revenue by customer industry
-- ─────────────────────────────────────────────────────────
SELECT
    c.industry,
    COUNT(DISTINCT c.id)    AS customer_count,
    SUM(soi.total)          AS total_revenue,
    AVG(soi.total)          AS avg_order_value
FROM sales_order_items soi
JOIN sales_orders so ON soi.order_id = so.id
JOIN customers c     ON so.customer_id = c.id
GROUP BY 1
ORDER BY 3 DESC;


-- ─────────────────────────────────────────────────────────
-- 10. Net profit per month (revenue - cogs - operational costs)
-- ─────────────────────────────────────────────────────────
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', so.order_date) AS month,
        SUM(soi.total - soi.quantity * p.cost_price) AS gross_profit
    FROM sales_order_items soi
    JOIN sales_orders so ON soi.order_id = so.id
    JOIN products p      ON soi.product_id = p.id
    GROUP BY 1
),
monthly_costs AS (
    SELECT
        DATE_TRUNC('month', cost_date) AS month,
        SUM(amount) AS total_costs
    FROM operational_costs
    GROUP BY 1
)
SELECT
    r.month,
    r.gross_profit,
    c.total_costs,
    r.gross_profit - c.total_costs AS net_profit
FROM monthly_revenue r
JOIN monthly_costs c ON r.month = c.month
ORDER BY 1;