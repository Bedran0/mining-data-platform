CREATE TABLE warehouses (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    city            VARCHAR(100),
    address         TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);