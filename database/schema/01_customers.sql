CREATE TABLE customers (
    id              SERIAL PRIMARY KEY,
    company_name    VARCHAR(255) NOT NULL,
    industry        VARCHAR(100) NOT NULL,  -- mining, construction, oil_gas
    country         VARCHAR(100) DEFAULT 'Turkey',
    city            VARCHAR(100),
    contact_name    VARCHAR(255),
    contact_email   VARCHAR(255),
    contact_phone   VARCHAR(50),
    credit_limit    NUMERIC(12,2) DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);