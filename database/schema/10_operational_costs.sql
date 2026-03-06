CREATE TABLE operational_costs (
    id              SERIAL PRIMARY KEY,
    cost_date       DATE NOT NULL,
    category        VARCHAR(100) NOT NULL,  -- transport, storage, personnel, maintenance
    amount          NUMERIC(12,2) NOT NULL,
    description     TEXT,
    employee_id     INTEGER REFERENCES employees(id),
    created_at      TIMESTAMP DEFAULT NOW()
);