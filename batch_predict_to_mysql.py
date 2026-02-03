import os
import joblib
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
from xgboost import XGBRegressor

load_dotenv()

MYSQL = dict(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
    connection_timeout=60
)

TABLE_SOURCE = "songs_features"
TABLE_TARGET = "song_popularity_predictions_v2"
CHUNK_SIZE = 5000
MODEL_VERSION = "xgb_v1"

def get_connection():
    return mysql.connector.connect(**MYSQL)

def main():
    # Load model + features
    features = joblib.load("features.pkl")
    model = XGBRegressor()
    model.load_model("xgb_spotify_model.json")

    conn = get_connection()

    total_rows = pd.read_sql(
        f"SELECT COUNT(*) AS cnt FROM {TABLE_SOURCE}",
        conn
    )["cnt"][0]

    print(f"🔢 Total rows to predict: {total_rows}")

    offset = 0

    while offset < total_rows:
        query = f"""
        SELECT
            artist_name, track_name,
            {", ".join([f"`{c}`" if c == "key" else c for c in features])}
        FROM {TABLE_SOURCE}
        LIMIT {CHUNK_SIZE} OFFSET {offset}
        """

        df = pd.read_sql(query, conn)

        if df.empty:
            break

        preds = model.predict(df[features])
        df["predicted_popularity"] = preds
        df["model_version"] = MODEL_VERSION
        df["prediction_time"] = datetime.now()

        insert_cols = [
            "artist_name","track_name",
            *features,
            "predicted_popularity","model_version","prediction_time"
        ]

        insert_sql = f"""
        INSERT INTO {TABLE_TARGET}
        ({", ".join([f"`{c}`" if c=="key" else c for c in insert_cols])})
        VALUES ({", ".join(["%s"]*len(insert_cols))})
        """

        data = [
            tuple(row[c] for c in insert_cols)
            for _, row in df.iterrows()
        ]

        cur = conn.cursor()
        cur.executemany(insert_sql, data)
        conn.commit()
        cur.close()

        offset += CHUNK_SIZE
        print(f"✅ Predicted + saved rows: {offset}/{total_rows}")

    conn.close()
    print("🎉 Batch prediction completed successfully!")

if __name__ == "__main__":
    main()
