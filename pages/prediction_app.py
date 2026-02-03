import streamlit as st
import pandas as pd
import joblib
import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

# ---------------------------------
# Load env vars
# ---------------------------------
load_dotenv()

# ---------------------------------
# Page config (UI only)
# ---------------------------------
st.set_page_config(
    page_title="Spotify Popularity Predictor",
    page_icon="🎵",
    layout="centered"
)

# ---------------------------------
# Custom CSS (UI only)
# ---------------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1DB95422, #0e1117);
}
div[data-testid="stSlider"] {
    padding: 5px 0px;
}
.pred-box {
    background: linear-gradient(135deg, #1DB954, #1aa34a);
    padding: 18px;
    border-radius: 12px;
    color: black;
    font-size: 24px;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Load model and features
# ---------------------------------
from xgboost import XGBRegressor

model = XGBRegressor()
model.load_model("xgb_spotify_model.json")

features = joblib.load("features.pkl")

# ---------------------------------
# MySQL connection
# ---------------------------------
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

# ---------------------------------
# Title
# ---------------------------------
st.markdown("## 🎵 Spotify Song Popularity Predictor")
st.markdown("Predict how popular a song could be using audio features and artist metrics.")

# ---------------------------------
# Basic info
# ---------------------------------
st.subheader("🎤 Song Information")

artist_name = st.text_input("Artist Name")
track_name = st.text_input("Track Name")

# ---------------------------------
# Audio features
# ---------------------------------
st.subheader("🎚️ Audio Features")

col1, col2 = st.columns(2)

with col1:
    danceability = st.slider("💃 Danceability", 0.0, 1.0, 0.65)
    energy = st.slider("⚡ Energy", 0.0, 1.0, 0.65)
    loudness = st.slider("🔊 Loudness (dB)", -20.0, 0.0, -6.5)
    speechiness = st.slider("🗣️ Speechiness", 0.0, 1.0, 0.04)
    acousticness = st.slider("🎸 Acousticness", 0.0, 1.0, 0.35)
    instrumentalness = st.slider("🎹 Instrumentalness", 0.0, 1.0, 0.0)

with col2:
    liveness = st.slider("🔥 Liveness", 0.0, 1.0, 0.1)
    valence = st.slider("😊 Valence", 0.0, 1.0, 0.65)
    tempo = st.number_input("🥁 Tempo (BPM)", 50.0, 200.0, 120.0)
    duration_ms = st.number_input("⏱️ Duration (ms)", 60000, 600000, 210000)
    key = st.selectbox("🎼 Key", list(range(12)))
    mode = st.selectbox("🎵 Mode", [0, 1])

# ---------------------------------
# Artist features
# ---------------------------------
st.subheader("⭐ Artist Metrics")

artist_avg_popularity = st.slider("Average Artist Popularity", 0, 100, 70)
artist_song_count = st.number_input("Total Songs by Artist", 1, 500, 20)

# ---------------------------------
# Prediction
# ---------------------------------
st.markdown("---")

if st.button("🎯 Predict & Save to MySQL", use_container_width=True):

    input_data = pd.DataFrame([{
        "danceability": danceability,
        "energy": energy,
        "loudness": loudness,
        "speechiness": speechiness,
        "acousticness": acousticness,
        "instrumentalness": instrumentalness,
        "liveness": liveness,
        "valence": valence,
        "tempo": tempo,
        "duration_ms": duration_ms,
        "key": key,
        "mode": mode,
        "artist_avg_popularity": artist_avg_popularity,
        "artist_song_count": artist_song_count
    }])

    input_data = input_data[features]
    prediction = model.predict(input_data)[0]

    st.markdown(
        f"<div class='pred-box'>🎯 Predicted Popularity: {prediction:.2f}</div>",
        unsafe_allow_html=True
    )

    # ---------------------------------
    # Save prediction (NO schema creation here)
    # ---------------------------------
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO song_popularity_predictions_v2 (
            artist_name, track_name,
            danceability, energy, loudness, speechiness,
            acousticness, instrumentalness, liveness, valence,
            tempo, duration_ms, `key`, mode,
            artist_avg_popularity, artist_song_count,
            predicted_popularity, prediction_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            artist_name, track_name,
            danceability, energy, loudness, speechiness,
            acousticness, instrumentalness, liveness, valence,
            tempo, duration_ms, key, mode,
            artist_avg_popularity, artist_song_count,
            float(prediction), datetime.now()
        ))

        conn.commit()
        cursor.close()
        conn.close()

        st.success("✅ Prediction saved successfully!")

    except Exception as e:
        st.error(f"❌ Database error: {e}")
    st.subheader("🧾 Recent Predictions (from MySQL)")




    try:
        conn = get_mysql_connection()
        df_hist = pd.read_sql("""
            SELECT 
                artist_name, 
                track_name, 
                predicted_popularity, 
                prediction_time
            FROM song_popularity_predictions_v2
            ORDER BY prediction_time DESC
            LIMIT 20
        """, conn)
        conn.close()

        st.dataframe(df_hist, use_container_width=True)

    except Exception as e:
        st.warning(f"Could not load history: {e}")

