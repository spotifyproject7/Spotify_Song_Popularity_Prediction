import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Spotify Analytics Dashboard", page_icon="📊", layout="wide")
st.markdown("## 📊 Spotify Analytics Dashboard")

TABLEAU_URL = "https://public.tableau.com/views/CDAC_Project_17697563691810/Dashboard1?:showVizHome=no"


c1, c2, c3 = st.columns([3,1,3])

with c1:
    st.link_button(
        "🔗 Open in Tableau Public",
        f"{TABLEAU_URL}?:showVizHome=no",
        help="Open dashboard in new tab",
    )

components.iframe(TABLEAU_URL, width=1600, height=1000, scrolling=True)
