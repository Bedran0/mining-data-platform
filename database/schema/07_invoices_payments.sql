CREATE TABLE invoices (
    id              SERIAL PRIMARY KEY,
    invoice_number  VARCHAR(100) UNIQUE NOT NULL,
    order_id        INTEGER REFERENCES sales_orders(id),
    issue_date      DATE NOT NULL,
    due_date        DATE NOT NULL,
    total_amount    NUMERIC(12,2) NOT NULL,
    status          VARCHAR(50) DEFAULT 'unpaid',  -- unpaid, partial, paid
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE payments (
    id              SERIAL PRIMARY KEY,
    invoice_id      INTEGER REFERENCES invoices(id),
    payment_date    DATE NOT NULL,
    amount          NUMERIC(12,2) NOT NULL,
    method          VARCHAR(50),  -- bank_transfer, cash, cheque
    notes           TEXT
);