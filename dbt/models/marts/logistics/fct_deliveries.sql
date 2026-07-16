
with orders as (
    select * from {{ ref('stg_orders') }}
)

select
    order_id,
    order_purchase_timestamp,
    order_delivered_customer_date,
    extract(day from (order_delivered_customer_date - order_purchase_timestamp)) as delivery_days
from orders