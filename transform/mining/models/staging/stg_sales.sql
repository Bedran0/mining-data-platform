with orders as (
    select * from {{ source('public', 'sales_orders') }}
),

items as (
    select * from {{ source('public', 'sales_order_items') }}
),

joined as (
    select
        i.id            as item_id,
        o.id            as order_id,
        o.order_date,
        o.customer_id,
        o.employee_id,
        i.product_id,
        i.quantity,
        i.unit_price,
        i.total,
        o.status
    from orders o
    join items i on i.order_id = o.id
)

select * from joined