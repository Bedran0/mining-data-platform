# Mining Equipment Data Platform

A full end-to-end data platform built for a mining and excavation equipment company. Covers everything from raw database design to business analytics, machine learning, and a visual dashboard — all runnable with a single command via Docker.

---

## Quick Start (Docker)

The fastest way to run the project. No Python or PostgreSQL installation needed.

**Requirements:** [Docker Desktop](https://www.docker.com/products/docker-desktop/)

```bash
git clone https://github.com/Bedran0/mining-data-platform.git
cd mining-data-platform
docker compose up --build
```

That's it. Docker will:
1. Start a PostgreSQL 16 database
2. Automatically create all 15 tables
3. Seed the database with 2 years of realistic synthetic data
4. Start Metabase at `http://localhost:3000`

Then open your browser and go to `http://localhost:3000` to explore the data visually.

> **First-time Metabase setup:** Create an account, then connect to the database using:
> - Host: `db` · Port: `5432` · Database: `mining_db`
> - Username: `mining_user` · Password: `mining_password`

---

## Architecture

```
generate_data.py
      │
      ▼
PostgreSQL 16          ◄──── 15 normalized tables
      │
      ▼
dbt (transform layer)  ◄──── staging + marts
      │
      ├──► Metabase    ◄──── visual dashboard at localhost:3000
      │
      └──► ML Model    ◄──── demand forecasting (scikit-learn)
```

---

## Database Schema

15 tables covering the full business lifecycle:

| Group | Tables |
|---|---|
| Master data | `customers`, `products`, `suppliers`, `employees`, `warehouses` |
| Sales | `sales_orders`, `sales_order_items` |
| Finance | `invoices`, `payments` |
| Inventory | `inventory_movements` |
| Procurement | `purchase_orders`, `purchase_order_items` |
| Operations | `operational_costs` |
| After-sales | `service_records`, `service_parts` |

All tables are fully normalized with foreign key relationships. The synthetic dataset covers ~2 years of activity including 300 sales orders, 80 customers, 15 products, and 1000+ inventory movements.

---

## Analytics (dbt)

The `transform/` layer uses [dbt](https://www.getdbt.com/) to build a clean analytics schema on top of the raw tables.

```
raw tables (public schema)
      │
      ▼
staging/         stg_customers, stg_products, stg_sales
      │
      ▼
marts/           mart_revenue, mart_inventory
```

**mart_revenue** — monthly revenue, cost, and gross profit broken down by industry and product category.

**mart_inventory** — current stock levels per product with `OK / WARNING / LOW` status flags.

To run dbt manually:
```bash
cd transform/mining
source ../../venv-dbt/bin/activate
dbt run
```

---

## Machine Learning

A **demand forecasting model** that predicts monthly sales quantity per product.

**Approach:** Gradient Boosting Regressor with lag features and time-based signals.

| Feature | Description |
|---|---|
| `lag_1`, `lag_2`, `lag_3` | Sales from previous 1–3 months |
| `rolling_mean_3` | 3-month rolling average |
| `month_num`, `quarter` | Seasonality signals |

**Result:** MAE ~32 units on the test set.

```bash
python ml/demand_forecasting/train.py
```

The trained model is saved to `ml/demand_forecasting/model.pkl`.

---

## Project Structure

```
mining-data-platform/
├── database/
│   ├── schema/              # 11 SQL table definitions
│   ├── queries.sql          # 10 business analytics queries
│   └── migrate.py           # Migration runner
├── ingestion/
│   └── generate_data.py     # Synthetic data generator (Faker)
├── ml/
│   └── demand_forecasting/
│       ├── train.py         # Model training
│       └── model.pkl        # Saved model
├── transform/
│   └── mining/              # dbt project
│       └── models/
│           ├── staging/     # stg_customers, stg_products, stg_sales
│           └── marts/       # mart_revenue, mart_inventory
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

---

## Manual Setup (without Docker)

If you prefer to run without Docker:

**1. Install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**2. Create `.env` file**
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mining_db
DB_USER=your_username
DB_PASSWORD=
```

**3. Set up the database**
```bash
psql postgres -c "CREATE DATABASE mining_db;"
python database/migrate.py
python ingestion/generate_data.py
```

**4. Run business queries**
```bash
psql mining_db -f database/queries.sql
```

**5. Train the ML model**
```bash
pip install scikit-learn
python ml/demand_forecasting/train.py
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Database | PostgreSQL 16 |
| Data Generation | Python, Faker, NumPy |
| Transform | dbt-postgres |
| Machine Learning | scikit-learn (GradientBoosting) |
| Dashboard | Metabase |
| Containerization | Docker, Docker Compose |
| Language | Python 3.11+ |
