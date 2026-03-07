# Mining Equipment Data Platform

End-to-end data platform for a mining and excavation equipment company. Includes a normalized PostgreSQL database, realistic synthetic data, business analytics queries, and a machine learning demand forecasting model.

## Architecture
```
PostgreSQL Database
    ↓
Python Data Generator (Faker)
    ↓
Business Analytics (SQL)
    ↓
ML — Demand Forecasting (scikit-learn)
```

## Database Schema

15 tables covering the full business:

- **customers** — companies that buy equipment
- **products** — drill rods, bits, machines, spare parts
- **suppliers** — procurement sources
- **employees** — sales and technical staff
- **warehouses** — storage locations
- **sales_orders / sales_order_items** — sales transactions
- **invoices / payments** — financial records
- **inventory_movements** — every stock in/out event
- **purchase_orders / purchase_order_items** — procurement
- **operational_costs** — transport, storage, personnel
- **service_records / service_parts** — post-sale maintenance

## Setup
```bash
git clone https://github.com/Bedran0/mining-data-platform.git
cd mining-data-platform
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Create a `.env` file:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mining_db
DB_USER=your_username
DB_PASSWORD=
```

Create the database and run migrations:
```bash
psql postgres -c "CREATE DATABASE mining_db;"
python database/migrate.py
```

Generate synthetic data (2 years, 300 sales orders):
```bash
python ingestion/generate_data.py
```

## Analytics

Run all business queries:
```bash
psql mining_db -f database/queries.sql
```

Includes: monthly revenue & profit, top customers, overdue invoices, stock levels, salesperson performance, supplier reliability.

## Machine Learning

Train the demand forecasting model:
```bash
python ml/demand_forecasting/train.py
```

Predicts monthly sales quantity per product using lag features and time-based signals. MAE ~32 units on test set.

## Project Structure
```
├── database/
│   ├── schema/          # 11 SQL table definitions
│   ├── queries.sql      # Business analytics queries
│   └── migrate.py       # Migration runner
├── ingestion/
│   └── generate_data.py # Synthetic data generator
├── ml/
│   └── demand_forecasting/
│       └── train.py     # GBM model training
└── pyproject.toml
```

## Tech Stack

| Layer | Tool |
|---|---|
| Database | PostgreSQL 16 |
| Data Generation | Faker, NumPy |
| Data Analysis | pandas, SQL |
| Machine Learning | scikit-learn (GradientBoosting) |
| Language | Python 3.14 |