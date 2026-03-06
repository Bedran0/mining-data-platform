import os
import random
import psycopg2
import numpy as np
from faker import Faker
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()
fake = Faker("tr_TR")
random.seed(42)
np.random.seed(42)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
conn.autocommit = True
cur = conn.cursor()

START_DATE = date(2023, 1, 1)
END_DATE   = date(2024, 12, 31)

def random_date(start=START_DATE, end=END_DATE):
    return start + timedelta(days=random.randint(0, (end - start).days))


# ── CUSTOMERS ──────────────────────────────────────────────────────────────

industries = ["mining", "construction", "oil_gas", "quarrying", "tunneling"]
cities = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Konya", "Adana", "Gaziantep"]

customers = []
for _ in range(80):
    cur.execute("""
        INSERT INTO customers (company_name, industry, country, city, contact_name,
                               contact_email, contact_phone, credit_limit)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (
        fake.company(),
        random.choice(industries),
        "Turkey",
        random.choice(cities),
        fake.name(),
        fake.email(),
        fake.phone_number(),
        random.choice([100000, 250000, 500000, 1000000]),
    ))
    customers.append(cur.fetchone()[0])

print(f"✓ {len(customers)} customers")


# ── SUPPLIERS ──────────────────────────────────────────────────────────────

supplier_countries = ["Turkey", "Germany", "Sweden", "USA", "China"]
suppliers = []
for _ in range(15):
    cur.execute("""
        INSERT INTO suppliers (name, country, city, contact_name, contact_email, contact_phone)
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id
    """, (
        fake.company(),
        random.choice(supplier_countries),
        fake.city(),
        fake.name(),
        fake.email(),
        fake.phone_number(),
    ))
    suppliers.append(cur.fetchone()[0])

print(f"✓ {len(suppliers)} suppliers")


# ── EMPLOYEES ──────────────────────────────────────────────────────────────

roles = ["sales", "sales", "sales", "technician", "warehouse", "manager"]
employees = []
for _ in range(20):
    cur.execute("""
        INSERT INTO employees (full_name, role, email, phone, hire_date)
        VALUES (%s,%s,%s,%s,%s) RETURNING id
    """, (
        fake.name(),
        random.choice(roles),
        fake.email(),
        fake.phone_number(),
        random_date(date(2018, 1, 1), date(2023, 1, 1)),
    ))
    employees.append(cur.fetchone()[0])

sales_employees = employees[:12]  # first 12 are sales
print(f"✓ {len(employees)} employees")


# ── WAREHOUSES ─────────────────────────────────────────────────────────────

warehouse_data = [
    ("Istanbul Main Warehouse", "Istanbul"),
    ("Ankara Branch",           "Ankara"),
    ("Izmir Depot",             "Izmir"),
]
warehouses = []
for name, city in warehouse_data:
    cur.execute("""
        INSERT INTO warehouses (name, city) VALUES (%s,%s) RETURNING id
    """, (name, city))
    warehouses.append(cur.fetchone()[0])

print(f"✓ {len(warehouses)} warehouses")


# ── PRODUCTS ───────────────────────────────────────────────────────────────

product_data = [
    ("DR-32-3M",   "Drill Rod 32mm 3m",          "drill_rod",   850,   520,  100),
    ("DR-32-6M",   "Drill Rod 32mm 6m",          "drill_rod",   1600,  980,  80),
    ("DR-38-6M",   "Drill Rod 38mm 6m",          "drill_rod",   1950,  1200, 60),
    ("DR-45-6M",   "Drill Rod 45mm 6m",          "drill_rod",   2400,  1500, 40),
    ("DB-35-R32",  "Drill Bit 35mm R32",         "drill_bit",   280,   150,  200),
    ("DB-45-T38",  "Drill Bit 45mm T38",         "drill_bit",   420,   230,  150),
    ("DB-64-T51",  "Drill Bit 64mm T51",         "drill_bit",   680,   380,  100),
    ("DB-89-T51",  "Drill Bit 89mm T51",         "drill_bit",   950,   540,  80),
    ("DM-HYD-200", "Hydraulic Drill 200kN",      "machine",     185000,120000,3),
    ("DM-HYD-350", "Hydraulic Drill 350kN",      "machine",     285000,190000,2),
    ("DM-DTH-150", "DTH Hammer Drill 150mm",     "machine",     95000, 62000, 4),
    ("SP-HOSE-10", "Hydraulic Hose 10m",         "spare_part",  1200,  700,  50),
    ("SP-FILTER",  "Air Filter Kit",             "spare_part",  450,   250,  100),
    ("SP-PISTON",  "Piston Assembly",            "spare_part",  8500,  5200, 20),
    ("SP-VALVE",   "Control Valve",              "spare_part",  3200,  1900, 30),
]

products = []
for code, name, cat, price, cost, min_stock in product_data:
    cur.execute("""
        INSERT INTO products (code, name, category, unit_price, cost_price, min_stock)
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id
    """, (code, name, cat, price, cost, min_stock))
    products.append(cur.fetchone()[0])

print(f"✓ {len(products)} products")


# ── PURCHASE ORDERS ────────────────────────────────────────────────────────

for _ in range(60):
    order_date = random_date()
    expected   = order_date + timedelta(days=random.randint(7, 30))
    actual     = expected + timedelta(days=random.randint(-3, 10))
    cur.execute("""
        INSERT INTO purchase_orders (supplier_id, order_date, expected_delivery, actual_delivery, status)
        VALUES (%s,%s,%s,%s,'delivered') RETURNING id
    """, (random.choice(suppliers), order_date, expected, actual))
    po_id = cur.fetchone()[0]

    for product_id in random.sample(products, random.randint(1, 4)):
        qty   = random.randint(20, 200)
        price = random.uniform(100, 5000)
        cur.execute("""
            INSERT INTO purchase_order_items (order_id, product_id, quantity, unit_price)
            VALUES (%s,%s,%s,%s)
        """, (po_id, product_id, qty, round(price, 2)))

        cur.execute("""
            INSERT INTO inventory_movements
                (product_id, warehouse_id, movement_type, quantity, reference_id, movement_date)
            VALUES (%s,%s,'purchase_in',%s,%s,%s)
        """, (product_id, random.choice(warehouses), qty, po_id, order_date))

print("✓ 60 purchase orders + inventory movements")


# ── SALES ORDERS ───────────────────────────────────────────────────────────

invoice_counter = 1000

for _ in range(300):
    order_date  = random_date()
    customer_id = random.choice(customers)
    employee_id = random.choice(sales_employees)

    cur.execute("""
        INSERT INTO sales_orders (order_date, customer_id, employee_id, status)
        VALUES (%s,%s,%s,'delivered') RETURNING id
    """, (order_date, customer_id, employee_id))
    order_id = cur.fetchone()[0]

    order_total = 0
    for product_id in random.sample(products, random.randint(1, 5)):
        qty        = random.randint(1, 50)
        cur.execute("SELECT unit_price FROM products WHERE id=%s", (product_id,))
        unit_price = float(cur.fetchone()[0])
        total      = qty * unit_price
        order_total += total

        cur.execute("""
            INSERT INTO sales_order_items (order_id, product_id, quantity, unit_price)
            VALUES (%s,%s,%s,%s) RETURNING id
        """, (order_id, product_id, qty, unit_price))
        item_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO inventory_movements
                (product_id, warehouse_id, movement_type, quantity, reference_id, movement_date)
            VALUES (%s,%s,'sale_out',%s,%s,%s)
        """, (product_id, random.choice(warehouses), -qty, order_id, order_date))

    # invoice
    due_date = order_date + timedelta(days=random.choice([30, 60, 90]))
    cur.execute("""
        INSERT INTO invoices (invoice_number, order_id, issue_date, due_date, total_amount, status)
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id
    """, (f"INV-{invoice_counter}", order_id, order_date, due_date,
          round(order_total, 2), random.choice(["paid", "paid", "unpaid", "partial"])))
    invoice_id = cur.fetchone()[0]
    invoice_counter += 1

    # payment
    cur.execute("SELECT status FROM invoices WHERE id=%s", (invoice_id,))
    status = cur.fetchone()[0]
    if status == "paid":
        cur.execute("""
            INSERT INTO payments (invoice_id, payment_date, amount, method)
            VALUES (%s,%s,%s,%s)
        """, (invoice_id, due_date, round(order_total, 2),
              random.choice(["bank_transfer", "cheque", "cash"])))
    elif status == "partial":
        partial = round(order_total * random.uniform(0.3, 0.7), 2)
        cur.execute("""
            INSERT INTO payments (invoice_id, payment_date, amount, method)
            VALUES (%s,%s,%s,%s)
        """, (invoice_id, due_date, partial, "bank_transfer"))

print("✓ 300 sales orders + invoices + payments")


# ── OPERATIONAL COSTS ──────────────────────────────────────────────────────

cost_categories = ["transport", "storage", "personnel", "maintenance"]
for _ in range(200):
    cur.execute("""
        INSERT INTO operational_costs (cost_date, category, amount, description)
        VALUES (%s,%s,%s,%s)
    """, (
        random_date(),
        random.choice(cost_categories),
        round(random.uniform(500, 25000), 2),
        fake.sentence(nb_words=6),
    ))

print("✓ 200 operational costs")


# ── SERVICE RECORDS ────────────────────────────────────────────────────────

cur.execute("""
    SELECT soi.id FROM sales_order_items soi
    JOIN products p ON soi.product_id = p.id
    WHERE p.category = 'machine'
    LIMIT 40
""")
machine_items = [row[0] for row in cur.fetchall()]

technicians = [e for e in employees if e not in sales_employees]

for item_id in machine_items:
    for _ in range(random.randint(1, 3)):
        cur.execute("""
            INSERT INTO service_records (sold_item_id, service_date, service_type, technician_id, notes)
            VALUES (%s,%s,%s,%s,%s) RETURNING id
        """, (
            item_id,
            random_date(),
            random.choice(["preventive", "corrective", "warranty"]),
            random.choice(technicians) if technicians else None,
            fake.sentence(nb_words=8),
        ))
        sr_id = cur.fetchone()[0]

        spare_parts = [p for p in products[-4:]]
        for part_id in random.sample(spare_parts, random.randint(1, 2)):
            cur.execute("""
                INSERT INTO service_parts (service_record_id, product_id, quantity, unit_price)
                VALUES (%s,%s,%s,%s)
            """, (sr_id, part_id, random.randint(1, 3), round(random.uniform(200, 5000), 2)))

print("✓ service records")

cur.close()
conn.close()
print("\n✅ All data generated successfully.")