with source as (
    select * from {{ source('public', 'products') }}
),

renamed as (
    select
        id              as product_id,
        code            as product_code,
        name            as product_name,
        category,
        unit_price,
        cost_price,
        unit_price - cost_price as margin,
        min_stock,
        is_active
    from source
    where is_active = true
)

select * from renamed