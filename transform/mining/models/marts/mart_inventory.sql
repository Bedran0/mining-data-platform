with movements as (
    select * from {{ source('public', 'inventory_movements') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

stock as (
    select
        p.product_code,
        p.product_name,
        p.category,
        p.min_stock,
        SUM(m.quantity)     as current_stock,
        case
            when SUM(m.quantity) < p.min_stock       then 'LOW'
            when SUM(m.quantity) < p.min_stock * 1.5 then 'WARNING'
            else 'OK'
        end                 as stock_status
    from movements m
    join products p on m.product_id = p.product_id
    group by 1, 2, 3, 4
)

select * from stock