
with orders as (
    select * from {{ ref('stg_orders') }}
),

first_purchase as (
    select
        customer_id,
        min(order_purchase_timestamp) as first_purchase_date
    from orders 
    group by customer_id
)

select
    date_trunc('month', first_purchase_date) as acquisition_month,
    count(customer_id) as new_customers
from first_purchase
group by date_trunc('month', first_purchase_date)