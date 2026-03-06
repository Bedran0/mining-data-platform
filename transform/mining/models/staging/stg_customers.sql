with source as (
    select * from {{ source('public', 'customers') }}
),

renamed as (
    select
        id              as customer_id,
        company_name,
        industry,
        city,
        country,
        credit_limit,
        is_active,
        created_at::date as created_date
    from source
    where is_active = true
)

select * from renamed