CREATE TABLE sales_orders (
    id              SERIAL PRIMARY KEY,
    order_date      DATE NOT NULL,
    customer_id     INTEGER REFERENCES customers(id),
    employee_id     INTEGER REFERENCES employees(id),
    status          VARCHAR(50) DEFAULT 'pending',  -- pending, confirmed, delivered, cancelled
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sales_order_items (
    id              SERIAL PRIMARY KEY,
    order_id        INTEGER REFERENCES sales_orders(id),
    product_id      INTEGER REFERENCES products(id),
    quantity        INTEGER NOT NULL,
    unit_price      NUMERIC(12,2) NOT NULL,
    total           NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);