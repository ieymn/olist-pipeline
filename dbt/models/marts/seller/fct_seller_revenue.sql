
with order_items as (
    select * from {{ ref('stg_order_items') }}
)

select
    seller_id,
    sum(price) as total_revenue
from order_items
group by seller_id