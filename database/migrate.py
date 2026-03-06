import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
conn.autocommit = True
cursor = conn.cursor()

schema_dir = Path(__file__).parent / "schema"
sql_files = sorted(schema_dir.glob("*.sql"))

for sql_file in sql_files:
    print(f"Running {sql_file.name}...")
    cursor.execute(sql_file.read_text())
    print(f"  ✓ done")

cursor.close()
conn.close()
print("\n✅ All tables created.")