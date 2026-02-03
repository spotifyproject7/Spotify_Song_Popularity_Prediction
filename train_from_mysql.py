import os
import joblib
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

load_dotenv()

MYSQL = dict(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
)

FEATURES = [
    "danceability","energy","loudness","speechiness","acousticness",
    "instrumentalness","liveness","valence","tempo","duration_ms",
    "key","mode","artist_avg_popularity","artist_song_count"
]
TARGET = "popularity"

def main():
    conn = mysql.connector.connect(**MYSQL)
    df = pd.read_sql("SELECT * FROM songs_features", conn)
    conn.close()

    df = df.dropna(subset=FEATURES + [TARGET])
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds) ** 0.5
    print(f"✅ RMSE = {rmse:.4f}")

    # Save model in XGBoost native format (stable)
    model.save_model("xgb_spotify_model.json")

    # Save feature order 
    joblib.dump(FEATURES, "features.pkl")

    print("✅ Saved: xgb_spotify_model.json")
    print("✅ Saved: features.pkl")



if __name__ == "__main__":
    main()
