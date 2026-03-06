CREATE TABLE inventory_movements (
    id              SERIAL PRIMARY KEY,
    product_id      INTEGER REFERENCES products(id),
    warehouse_id    INTEGER REFERENCES warehouses(id),
    movement_type   VARCHAR(50) NOT NULL,  -- purchase_in, sale_out, adjustment, return
    quantity        INTEGER NOT NULL,       -- positive = in, negative = out
    reference_id    INTEGER,               -- order_id or purchase_order_id
    movement_date   DATE NOT NULL,
    notes           TEXT
);