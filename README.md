# Olist E-Commerce Data Pipeline

A data engineering portfolio project that ingests Brazilian e-commerce data from the Olist dataset via the Kaggle API, transforms it using dbt, and serves business-ready KPIs to three departments through a Power BI dashboard.

---

## Architecture

![Architecture](docs/architecture.png)

```
Kaggle API → Ingestion (Python) → PostgreSQL (Raw)
→ dbt (Staging → Marts) → Power BI Dashboard + SQL Analysis
```

Orchestrated by Apache Airflow. Everything containerized with Docker Compose.

---

## Why this project

The Olist dataset is one of the most realistic public e-commerce datasets available. It contains 8 related tables covering orders, customers, sellers, products, payments, reviews, and geolocation — closely resembling a real production database schema.

I chose this dataset because it allowed me to practice the full data engineering lifecycle — ingestion, transformation, modelling, and serving — on data that reflects real business problems rather than a toy dataset.

This project also demonstrates my retail background. Having worked in retail operations, I understand the business context behind the metrics — why delivery performance matters, what drives seller revenue, and how to measure market growth.

---

## Business context

This pipeline serves three internal departments:

**Logistics team**
Tracks delivery performance across Brazilian states. Key questions: Are orders arriving on time? Which routes have the worst delays? How does estimated delivery compare to actual delivery?

**Seller analytics team**
Monitors individual seller performance. Key questions: Which sellers generate the most revenue? What is the average review score per seller? How is seller revenue trending month over month?

**Investor / executive team**
Tracks overall market growth. Key questions: What is the monthly GMV trend? How fast is the customer base growing? Which product categories are driving revenue?

---

## Data source

**Olist Brazilian E-Commerce Dataset** via Kaggle API

| File | Description | Rows |
|---|---|---|
| `olist_orders_dataset.csv` | Order header — status, timestamps | ~100k |
| `olist_customers_dataset.csv` | Customer location and ID | ~100k |
| `olist_sellers_dataset.csv` | Seller location and ID | ~3k |
| `olist_products_dataset.csv` | Product category and dimensions | ~33k |
| `olist_order_items_dataset.csv` | Line items — price, freight | ~115k |
| `olist_order_payments_dataset.csv` | Payment type and value | ~104k |
| `olist_order_reviews_dataset.csv` | Customer review scores | ~100k |
| `olist_geolocation_dataset.csv` | Brazilian zip code coordinates | ~1M |

---

## Tech stack

| Tool | Purpose | Why |
|---|---|---|
| Python 3.13 | Ingestion scripts | Industry standard for data engineering |
| Kaggle API | Download dataset | Automates data sourcing — no manual download |
| PostgreSQL | Raw and transformed data storage | Reliable, SQL-queryable, runs in Docker |
| Apache Airflow | Pipeline orchestration | Industry standard workflow scheduler |
| dbt | Data transformation | SQL-based, version controlled, testable |
| Power BI | Business dashboard | Most in-demand BI tool in Malaysian market |
| Docker Compose | Infrastructure | Reproducible environment on any machine |
| Git | Version control | Every project needs this |

---

## Project structure

```
olist-pipeline/
├── dags/
│   └── olist_pipeline.py          # Airflow DAG — orchestrates all steps
├── ingestion/
│   ├── ingest_olist.py            # Downloads from Kaggle, loads to PostgreSQL
│   └── Dockerfile
├── dbt/
│   ├── models/
│   │   ├── staging/               # Silver layer — cleaned source data
│   │   │   ├── stg_orders.sql
│   │   │   ├── stg_customers.sql
│   │   │   ├── stg_sellers.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── stg_order_items.sql
│   │   │   ├── stg_payments.sql
│   │   │   ├── stg_reviews.sql
│   │   │   └── stg_geolocation.sql
│   │   └── marts/                 # Gold layer — business KPI models
│   │       ├── seller/
│   │       │   ├── fct_seller_revenue.sql
│   │       │   ├── fct_seller_orders.sql
│   │       │   └── dim_sellers.sql
│   │       ├── logistics/
│   │       │   ├── fct_deliveries.sql
│   │       │   └── fct_delivery_performance.sql
│   │       └── market/
│   │           ├── fct_market_growth.sql
│   │           └── fct_customer_acquisition.sql
├── analysis/
│   └── analysis.sql               # Business questions answered in SQL
├── docs/
│   └── architecture.png           # Pipeline architecture diagram
├── docker-compose.yaml            # PostgreSQL + Airflow + pgAdmin
├── requirements.txt
└── README.md
```

---

## Pipeline flow

```
1. download_from_kaggle     → pulls 8 CSV files via Kaggle API
2. load_raw_to_postgres     → loads CSVs into raw schema in PostgreSQL
3. run_dbt_staging          → cleans and standardises raw tables
4. run_dbt_marts            → builds KPI models for all 3 departments
5. notify_complete          → logs pipeline completion
```

All 5 steps are orchestrated as an Airflow DAG running on a scheduled basis.

---

## Incremental loading

This pipeline implements watermark-based incremental loading. On the first run, all historical data is loaded. On subsequent runs, only records newer than the last loaded timestamp are processed.

```sql
-- Check last loaded order
SELECT MAX(order_purchase_timestamp) FROM raw.orders

-- Load only new orders
WHERE order_purchase_timestamp > last_loaded_timestamp
```

This simulates how a real production pipeline handles daily data updates.

---

## KPIs by department

**Logistics**
- Average delivery time by state
- On-time delivery rate
- Estimated vs actual delivery gap
- Late orders by product category
- Worst performing delivery routes

**Seller Analytics**
- Monthly revenue per seller
- Top 10 sellers by GMV
- Seller order fulfillment rate
- Average review score per seller
- Revenue growth month over month

**Market Growth**
- Monthly GMV trend
- New customer acquisition by month
- Revenue by product category
- Month over month growth rate
- Average order value trend

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/ieymn/olist-pipeline.git
cd olist-pipeline
```

### 2. Set up Kaggle API credentials

Download `kaggle.json` from your Kaggle account settings and place it at:

```
C:\Users\yourname\.kaggle\kaggle.json
```

### 3. Create required folders

```bash
mkdir -p dags logs plugins config
```

### 4. Start all services

```bash
docker-compose up airflow-init   # first time only
docker-compose up -d
```

### 5. Access services

| Service | URL | Credentials |
|---|---|---|
| Airflow | http://localhost:8080 | airflow / airflow |
| pgAdmin | http://localhost:8085 | admin@admin.com / root |

### 6. Trigger the pipeline

Open Airflow at http://localhost:8080, find the `olist_pipeline` DAG and trigger it manually.

---

## Design decisions

**Why Kaggle API instead of manual download?**
Automating data sourcing is a core DE practice. The API call can be version controlled, scheduled, and reproduced by anyone with a Kaggle account — no manual steps.

**Why dbt for transformation?**
dbt transforms SQL scripts into version-controlled, testable, documented models. It separates staging (cleaning) from marts (business logic), making the pipeline maintainable and auditable.

**Why Airflow instead of a simple cron job?**
Airflow provides dependency management between tasks, retry logic, monitoring, and a visual UI. It is the industry standard for workflow orchestration and is used by most Malaysian tech companies.

**Why PostgreSQL instead of SQLite?**
PostgreSQL is production-grade. It supports concurrent connections, proper data types, schemas, and is the same database companies use in production. SQLite is fine for learning but not appropriate for a multi-department analytics pipeline.

**Why Docker Compose?**
The entire infrastructure — PostgreSQL, Airflow, pgAdmin — starts with one command and runs identically on any machine. No environment mismatch, no manual setup.

---

## Roadmap

- [ ] Kaggle API ingestion script
- [ ] Raw schema and table creation
- [ ] dbt staging models (Silver layer)
- [ ] dbt mart models (Gold layer)
- [ ] Airflow DAG
- [ ] Power BI dashboard
- [ ] analysis.sql — business queries
- [ ] Data quality tests with dbt test
- [ ] Migrate to cloud (GCS + BigQuery)

---

## License

MIT
