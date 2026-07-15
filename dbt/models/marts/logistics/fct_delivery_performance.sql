
with orders as(
    select * from {{ ref('stg_orders') }}
)

select
    order_id,
    order_estimated_delivery_date,
    order_delivered_customer_date,
    case
        when order_delivered_customer_date is null then null
        when order_delivered_customer_date > order_estimated_delivery_date then true 
        else false 
    end as is_late
from orders
