import csv
import pyodbc
import os
import time
from dotenv import load_dotenv
import os
load_dotenv()

# Load environment variables from .env file

# Get credentials securely from environment
server = os.getenv('DB_HOST', 'localhost')  # default to localhost
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME', 'tennis_dw')  # default to tennis_dw

# Database connection string
DATABASE_CONNECTION_STRING = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
)

# Establish a database connection
def connect_to_db():
    return pyodbc.connect(DATABASE_CONNECTION_STRING)

conn = connect_to_db()
cursor = conn.cursor()


# File and table config for new columns only
fact_file_path = "../Dimensions/dimension tables/fact_dim.csv"
fact_table_name = "match_fact"
new_columns = ["match_id", "round", "score", "best_of"]

def update_existing_facts(file_path, table_name, columns):
    print(f"\n📦 Updating {table_name} with columns {columns}...")

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        total = len(rows)
        update_count = 0

        for idx, row in enumerate(rows, start=1):
            try:
                values = [row[col] for col in columns[1:]]  # skip match_id
                values.append(row["match_id"])  # for WHERE
            except KeyError as e:
                print(f"❌ Column not found in CSV row: {e} → Row: {row}")
                continue

            set_clause = ", ".join([f"{col} = ?" for col in columns[1:]])
            sql = f"UPDATE {table_name} SET {set_clause} WHERE match_id = ?"

            try:
                cursor.execute(sql, values)
                update_count += 1
            except pyodbc.Error as e:
                print(f"❌ Failed to update match_id {row['match_id']}: {e}")
                continue

            # Progress print every 1000 rows or last one
            if idx % 15000 == 0 or idx == total:
                print(f"  → {idx}/{total} rows processed...")

        conn.commit()
        print(f"\n✅ Finished updating {table_name} — {update_count}/{total} rows updated.")

# Run the update
update_existing_facts(fact_file_path, fact_table_name, new_columns)
