import pyodbc
import csv
import time


#call .env file to get the connection string
from dotenv import load_dotenv
import os
load_dotenv()

conn_string = os.getenv('DB_HOST')
if not conn_string:
     raise ValueError("Connection string not found in .env file.")

# Connect to SQL Server
import pyodbc
import os
import csv
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


'''def load_csv_to_table(file_path, table_name, columns):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        total = sum(1 for _ in open(file_path)) - 1
        file.seek(0)
        #next(reader)  # skip header -- remove as its causing the errro, headers already excluded

        print(f"\n📦 Uploading {table_name} ({total} rows)...")

        count = 0
        for row in reader:
            placeholders = ', '.join(['?'] * len(columns))
            values = [row[col] for col in columns]

            try:
                cursor.execute(f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})", values)
                count += 1
                if count % 3000 == 0:
                    print(f"   → Inserted {count}/{total} rows...")
            except pyodbc.IntegrityError as e:
                if "duplicate" in str(e).lower():
                    print(f"⚠️ Duplicate found. Skipping row: {values}")
                    continue
                else:
                    print(f"❌ Failed on row: {row}")
                    print("🚨 SQL Error:", e)
                    break

        conn.commit()
        print(f"✅ Finished uploading {table_name} ({count} inserted, {total - count} skipped).")
'''


def load_csv_to_table(file_path, table_name, columns, batch_size=10000, max_retries=2):
    checkpoint_file = f"{table_name}_checkpoint.txt"

    # Read last inserted line index (if any)
    start_from = 0
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as cp:
            start_from = int(cp.read().strip())

    print(f"\n📦 Uploading {table_name} starting at row {start_from}...")

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        total = len(rows)
        
        inserted = start_from if start_from > 0 else 0

        while start_from < total:
            batch = rows[start_from:start_from + batch_size]

            for attempt in range(1, max_retries + 1):
                try:
                    for row in batch:
                        placeholders = ', '.join(['?'] * len(columns))
                        values = [row[col] for col in columns]
                        cursor.execute(f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})", values)

                    conn.commit()
                    inserted += len(batch)
                    start_from += batch_size

                    # Save checkpoint
                    with open(checkpoint_file, 'w') as cp:
                        cp.write(str(start_from))

                    print(f"   → Inserted {inserted}/{total} rows...")

                    break  # exit retry loop on success

                except pyodbc.Error as e:
                    print(f"⚠️ Attempt {attempt} failed. Retrying in 5s... Error: {e}")
                    time.sleep(5)

                    if attempt == max_retries:
                        print("❌ Max retries reached. Aborting.")
                        return

    print(f"✅ Finished uploading {table_name} ({inserted}/{total} rows inserted).")


# Define what to load and in what order (dimensions before fact)
tables = [
    #("../Dimensions/dimension tables/country_dim.csv", "country", ["country_id", "country_name", "continent"]),
    ("../Dimensions/dimension tables/player_dim.csv", "player", ["player_id", "player_name", "hand", "age", "height", "country_id",]),
    #("../Dimensions/dimension tables/date_dim.csv", "date", ["date_id", "date", "day", "day_of_week", "is_weekend", "week", "month", "quarter", "year"]),
    #("../Dimensions/dimension tables/tourney_dim.csv", "tourney", ["tourney_id", "tourney_range","tourney_name", "surface", "draw_size", "tourney_level", "tourney_date_id"]),
     ("../Dimensions/dimension tables/fact_dim.csv", "match_fact", ["match_id", "winner_id", "loser_id", "tourney_id", "no_spectators", "avg_ticket", "match_expense","winner_rank_points","loser_rank_points","winner_rank","loser_rank", "round", "score", "best_of"]),
]

# Load all
for file_path, table_name, cols in tables:
    load_csv_to_table(file_path, table_name, cols)

conn.close()
