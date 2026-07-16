
with order_items as (
    select * from {{ ref('stg_order_items') }}
)

select
    seller_id,
    count(distinct order_id) as unique_order_count,
    count(order_id) as total_items_sold,
    sum(price) as total_revenue,
    sum(freight_value) as total_freight
from order_items
group by seller_id