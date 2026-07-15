
with order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
)

select
    order_items.seller_id,
    count(distinct order_items.order_id) as unique_order_count,
    count(order_items.order_id) as total_items_sold,
    sum(order_items.price) as total_revenue,
    sum(order_items.freight_value) as total_freight
from order_items
left join orders on order_items.order_id = orders.order_id
group by 
    order_items.seller_id