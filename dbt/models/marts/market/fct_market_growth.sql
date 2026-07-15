
with orders as (
    select * from {{ ref('stg_orders')}}
),

order_items as (
    select * from {{ ref('stg_order_items')}}
)

select
    date_trunc('month', order_purchase_timestamp) as order_month,
    sum(price) as total_gmv
from orders
join order_items on orders.order_id = order_items.order_id
group by order_month