import os
import math
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = "spotify_data.csv"  

MYSQL = dict(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DB", "spotify_db"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
    connection_timeout=60,
    autocommit=False,
)

TABLE = "songs_raw"
BATCH_SIZE = 2000  # you can lower to 500 if still failing

COLS = [
    "artist_name","track_name","track_id","popularity","year","genre",
    "danceability","energy","key","loudness","mode","speechiness",
    "acousticness","instrumentalness","liveness","valence","tempo",
    "duration_ms","time_signature"
]

INSERT_SQL = f"""
INSERT INTO {TABLE} (
    artist_name, track_name, track_id, popularity, year, genre,
    danceability, energy, `key`, loudness, mode, speechiness,
    acousticness, instrumentalness, liveness, valence, tempo,
    duration_ms, time_signature
) VALUES (
    %s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s
)
"""

def connect():
    conn = mysql.connector.connect(**MYSQL)
    # Helps prevent "gone away" on long inserts
    conn.cmd_query("SET SESSION net_write_timeout=600")
    conn.cmd_query("SET SESSION net_read_timeout=600")
    conn.cmd_query("SET SESSION wait_timeout=28800")
    return conn

def to_tuples(df: pd.DataFrame):
    # Convert NaN -> None so MySQL accepts nulls
    df = df.where(pd.notnull(df), None)
    return [tuple(row[c] for c in COLS) for _, row in df.iterrows()]

def main():
    df = pd.read_csv(CSV_PATH)

    # If your CSV has different column names, rename here:
    # df = df.rename(columns={"track_id_col": "track_id", ...})

    missing = [c for c in COLS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing columns: {missing}\nFound columns: {list(df.columns)}")

    df = df[COLS].copy()
    data = to_tuples(df)

    total = len(data)
    batches = math.ceil(total / BATCH_SIZE)

    conn = connect()
    cur = conn.cursor()

    # Optional: clear old data
    cur.execute(f"TRUNCATE TABLE {TABLE}")
    conn.commit()

    try:
        for b in range(batches):
            start = b * BATCH_SIZE
            end = min(start + BATCH_SIZE, total)
            chunk = data[start:end]

            try:
                cur.executemany(INSERT_SQL, chunk)
                conn.commit()
                print(f"✅ Inserted batch {b+1}/{batches}: rows {start}..{end-1}")
            except Error as e:
                print(f"⚠️ Batch {b+1} failed: {e}. Reconnecting and retrying once...")
                try:
                    cur.close()
                    conn.close()
                except Exception:
                    pass

                conn = connect()
                cur = conn.cursor()

                # retry once
                cur.executemany(INSERT_SQL, chunk)
                conn.commit()
                print(f"✅ Retried batch {b+1}/{batches} successfully.")

    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

    print(f"🎉 Done. Loaded {total} rows into {TABLE}.")

if __name__ == "__main__":
    main()
