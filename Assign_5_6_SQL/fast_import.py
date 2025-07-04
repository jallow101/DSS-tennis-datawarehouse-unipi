import pyodbc
import csv
import time
from dotenv import load_dotenv
import os
from itertools import islice

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment
server = os.getenv('DB_HOST', 'localhost')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME', 'tennis_dw')

# Database connection string
DATABASE_CONNECTION_STRING = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
)

# Connect to DB
def connect_to_db():
    return pyodbc.connect(DATABASE_CONNECTION_STRING)

# Optimized loader function
def load_csv_to_table(file_path, table_name, columns, batch_size=10000, max_retries=2):
    checkpoint_file = f"{table_name}_checkpoint.txt"

    start_from = 0
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as cp:
            start_from = int(cp.read().strip())

    print(f"\n📦 Uploading {table_name} starting at row {start_from}...")

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.fast_executemany = True  # 🧠 critical for performance

    inserted = start_from if start_from > 0 else 0

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        total = sum(1 for _ in open(file_path)) - 1
        file.seek(0)
        next(reader)  # Skip header

        batch = []
        current_row = 0

        for row in reader:
            if current_row < start_from:
                current_row += 1
                continue

            batch.append([row[col] for col in columns])
            current_row += 1

            if len(batch) == batch_size:
                for attempt in range(1, max_retries + 1):
                    try:
                        placeholders = ', '.join(['?'] * len(columns))
                        sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
                        cursor.executemany(sql, batch)
                        conn.commit()

                        inserted += len(batch)
                        batch.clear()

                        # Save checkpoint
                        with open(checkpoint_file, 'w') as cp:
                            cp.write(str(current_row))

                        print(f"   → Inserted {inserted}/{total} rows...")
                        break

                    except pyodbc.Error as e:
                        print(f"⚠️ Attempt {attempt} failed. Retrying in 5s... Error: {e}")
                        time.sleep(5)

                        if attempt == max_retries:
                            print("❌ Max retries reached. Aborting.")
                            conn.close()
                            return

        # Final insert if remaining rows
        if batch:
            try:
                placeholders = ', '.join(['?'] * len(columns))
                sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
                cursor.executemany(sql, batch)
                conn.commit()
                inserted += len(batch)
                print(f"   → Inserted final {len(batch)} rows.")
            except Exception as e:
                print("❌ Final batch insert failed:", e)

    print(f"✅ Finished uploading {table_name} ({inserted}/{total} rows inserted).")
    conn.close()


# Define the list of tables to load
tables = [
    #("../Dimensions/dimension tables/country_dim.csv", "country", ["country_id", "country_name", "continent"]),
    ("../Dimensions/dimension tables/player_dim.csv", "player", ["player_id", "player_name", "hand", "age", "height", "country_id",]),
    #("../Dimensions/dimension tables/date_dim.csv", "date", ["date_id", "date", "day", "day_of_week", "is_weekend", "week", "month", "quarter", "year"]),
    #("../Dimensions/dimension tables/tourney_dim.csv", "tourney", ["tourney_id", "tourney_range","tourney_name", "surface", "draw_size", "tourney_level", "tourney_date_id"]),
    #("../Dimensions/dimension tables/player_dim.csv", "player", ["player_id", "player_name", "hand", "age", "height", "country_id", ]),
    #("../Dimensions/dimension tables/fact_dim.csv", "match_fact", ["match_id", "winner_id", "loser_id", "tourney_id", "no_spectators", "avg_ticket", "match_expense","winner_rank_points","loser_rank_points","winner_rank","loser_rank", "round", "score", "best_of"]),
]

# Load each table
for file_path, table_name, cols in tables:
    load_csv_to_table(file_path, table_name, cols)
    print(f"✅ Finished loading {table_name} table.")