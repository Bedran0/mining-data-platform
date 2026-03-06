CREATE TABLE purchase_orders (
    id                  SERIAL PRIMARY KEY,
    supplier_id         INTEGER REFERENCES suppliers(id),
    order_date          DATE NOT NULL,
    expected_delivery   DATE,
    actual_delivery     DATE,
    status              VARCHAR(50) DEFAULT 'pending',  -- pending, delivered, cancelled
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE purchase_order_items (
    id              SERIAL PRIMARY KEY,
    order_id        INTEGER REFERENCES purchase_orders(id),
    product_id      INTEGER REFERENCES products(id),
    quantity        INTEGER NOT NULL,
    unit_price      NUMERIC(12,2) NOT NULL,
    total           NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);