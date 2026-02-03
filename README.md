# Spotify Song Popularity Prediction (ML + MySQL + Streamlit)

## Overview
End-to-end ML project that predicts Spotify song popularity using audio features and artist metrics.

## Tech Stack
- Python, Pandas
- MySQL
- XGBoost
- Streamlit

## Pipeline
1. Load CSV -> MySQL (`songs_raw`)
2. SQL feature engineering -> `songs_features`
3. Train model from MySQL -> `xgb_spotify_model.json`
4. Streamlit real-time prediction -> stores output in MySQL
5. Batch inference -> saves predictions for all records

## Setup
1. Install requirements:
   ```bash
   pip install -r requirements.txt
