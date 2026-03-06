CREATE TABLE employees (
    id              SERIAL PRIMARY KEY,
    full_name       VARCHAR(255) NOT NULL,
    role            VARCHAR(100),  -- sales, technician, warehouse, manager
    email           VARCHAR(255),
    phone           VARCHAR(50),
    hire_date       DATE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);