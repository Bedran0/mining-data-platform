CREATE TABLE products (
    id              SERIAL PRIMARY KEY,
    code            VARCHAR(100) UNIQUE NOT NULL,
    name            VARCHAR(255) NOT NULL,
    category        VARCHAR(100) NOT NULL,  -- drill_rod, drill_bit, machine, spare_part
    unit_price      NUMERIC(12,2) NOT NULL,
    cost_price      NUMERIC(12,2) NOT NULL,
    min_stock       INTEGER DEFAULT 0,
    unit            VARCHAR(50) DEFAULT 'piece',  -- piece, meter, kg
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);