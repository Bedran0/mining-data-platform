import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle


load_dotenv()


def load_churn_dataset() -> pd.DataFrame:
    """
    Build a simple churn dataset at the customer level.

    Definition (heuristic):
    - For each customer, compute last_order_date.
    - Customers whose last order is older than 6 months from the max order date
      in the dataset are labeled as churned (churn = 1), otherwise 0.
    """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    query = """
        WITH customer_orders AS (
            SELECT
                c.id                      AS customer_id,
                c.industry,
                c.city,
                c.credit_limit,
                COUNT(DISTINCT so.id)     AS total_orders,
                SUM(soi.total)            AS total_revenue,
                MIN(so.order_date)        AS first_order_date,
                MAX(so.order_date)        AS last_order_date
            FROM customers c
            LEFT JOIN sales_orders so
                ON so.customer_id = c.id
            LEFT JOIN sales_order_items soi
                ON soi.order_id = so.id
            GROUP BY 1, 2, 3, 4
        ),
        boundaries AS (
            SELECT
                MAX(last_order_date)                       AS global_max_order_date
            FROM customer_orders
            WHERE last_order_date IS NOT NULL
        )
        SELECT
            co.*,
            b.global_max_order_date,
            CASE
                WHEN co.last_order_date IS NULL THEN 1
                WHEN co.last_order_date < b.global_max_order_date - INTERVAL '6 months'
                     THEN 1
                ELSE 0
            END AS churn
        FROM customer_orders co
        CROSS JOIN boundaries b;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


def engineer_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    # Drop customers with no order history but keep them as churned examples
    # (label already encodes that via churn column).

    # Encode categoricals
    df["industry_code"] = df["industry"].astype("category").cat.codes
    df["city_code"] = df["city"].astype("category").cat.codes

    # Time deltas (in days)
    df["first_order_date"] = pd.to_datetime(df["first_order_date"])
    df["last_order_date"] = pd.to_datetime(df["last_order_date"])
    df["global_max_order_date"] = pd.to_datetime(df["global_max_order_date"])

    df["days_since_last_order"] = (
        df["global_max_order_date"] - df["last_order_date"]
    ).dt.days.fillna(9999)

    df["customer_lifetime_days"] = (
        df["last_order_date"] - df["first_order_date"]
    ).dt.days.fillna(0)

    df["avg_order_revenue"] = (
        df["total_revenue"] / df["total_orders"].where(df["total_orders"] > 0, 1)
    ).fillna(0)

    features = [
        "credit_limit",
        "total_orders",
        "total_revenue",
        "avg_order_revenue",
        "days_since_last_order",
        "customer_lifetime_days",
        "industry_code",
        "city_code",
    ]

    X = df[features].fillna(0)
    y = df["churn"].astype(int)
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series) -> LogisticRegression:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n── Churn model evaluation ──")
    print(classification_report(y_test, y_pred, digits=3))

    return model


def save_model(model: LogisticRegression, path: str = "ml/churn_prediction/model.pkl") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"\n✅ Churn model saved to {path}")


def main() -> None:
    df = load_churn_dataset()
    print(f"Loaded {len(df)} customers into churn dataset")

    X, y = engineer_features(df)
    model = train_model(X, y)
    save_model(model)


if __name__ == "__main__":
    main()

