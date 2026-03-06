CREATE TABLE service_records (
    id              SERIAL PRIMARY KEY,
    sold_item_id    INTEGER REFERENCES sales_order_items(id),
    service_date    DATE NOT NULL,
    service_type    VARCHAR(100),  -- preventive, corrective, warranty
    technician_id   INTEGER REFERENCES employees(id),
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE service_parts (
    id                  SERIAL PRIMARY KEY,
    service_record_id   INTEGER REFERENCES service_records(id),
    product_id          INTEGER REFERENCES products(id),
    quantity            INTEGER NOT NULL,
    unit_price          NUMERIC(12,2)
);