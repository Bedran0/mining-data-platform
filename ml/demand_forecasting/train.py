import os
import pandas as pd
import numpy as np
import psycopg2
from dotenv import load_dotenv
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle

load_dotenv()

# ── 1. LOAD DATA ───────────────────────────────────────────────────────────

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

query = """
    SELECT
        DATE_TRUNC('month', so.order_date)  AS month,
        p.id                                AS product_id,
        p.name                              AS product_name,
        p.category,
        SUM(soi.quantity)                   AS total_quantity
    FROM sales_order_items soi
    JOIN sales_orders so ON soi.order_id = so.id
    JOIN products p      ON soi.product_id = p.id
    GROUP BY 1, 2, 3, 4
    ORDER BY 1, 2
"""

df = pd.read_sql(query, conn)
conn.close()

print(f"Loaded {len(df)} rows")
print(df.head())

# ── 2. FEATURE ENGINEERING ─────────────────────────────────────────────────

df["month"] = pd.to_datetime(df["month"])
df = df.sort_values(["product_id", "month"])

# Time features
df["month_num"]  = df["month"].dt.month
df["year"]       = df["month"].dt.year
df["quarter"]    = df["month"].dt.quarter

# Lag features — what sold last 1, 2, 3 months
df["lag_1"] = df.groupby("product_id")["total_quantity"].shift(1)
df["lag_2"] = df.groupby("product_id")["total_quantity"].shift(2)
df["lag_3"] = df.groupby("product_id")["total_quantity"].shift(3)

# Rolling average — smooths out noise
df["rolling_mean_3"] = (
    df.groupby("product_id")["total_quantity"]
    .transform(lambda x: x.shift(1).rolling(3).mean())
)

# Category encoding
df["category_code"] = df["category"].astype("category").cat.codes

df = df.dropna()
print(f"\nAfter feature engineering: {len(df)} rows")

# ── 3. TRAIN ───────────────────────────────────────────────────────────────

features = ["product_id", "month_num", "year", "quarter",
            "lag_1", "lag_2", "lag_3", "rolling_mean_3", "category_code"]
target   = "total_quantity"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4,
    random_state=42,
)
model.fit(X_train, y_train)

# ── 4. EVALUATE ────────────────────────────────────────────────────────────

y_pred = model.predict(X_test)
mae  = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\n── Model Performance ──")
print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

# Feature importance
importance = pd.Series(model.feature_importances_, index=features)
print(f"\n── Feature Importance ──")
print(importance.sort_values(ascending=False).to_string())

# ── 5. SAVE MODEL ──────────────────────────────────────────────────────────

os.makedirs("ml/demand_forecasting", exist_ok=True)
with open("ml/demand_forecasting/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model saved to ml/demand_forecasting/model.pkl")