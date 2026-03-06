with sales as (
    select * from {{ ref('stg_sales') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

final as (
    select
        DATE_TRUNC('month', s.order_date)   as month,
        c.industry,
        p.category,
        p.product_name,
        SUM(s.quantity)                     as total_quantity,
        SUM(s.total)                        as total_revenue,
        SUM(s.quantity * p.cost_price)      as total_cost,
        SUM(s.total - s.quantity * p.cost_price) as gross_profit
    from sales s
    join products p  on s.product_id  = p.product_id
    join customers c on s.customer_id = c.customer_id
    group by 1, 2, 3, 4
)

select * from final