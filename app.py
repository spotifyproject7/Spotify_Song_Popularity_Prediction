import streamlit as st

st.set_page_config(page_title="Spotify ML Project", page_icon="🎵", layout="centered")

st.markdown("""
<style>
/* Pull content UP (removes extra top spacing) */
section.main > div { padding-top: 1.2rem; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 1.2rem; }

/* Background */
.stApp {
  background: radial-gradient(circle at top, #1DB95422, #0e1117);
}

/* Page title */
.hero {
  text-align: center;
  margin: 0.2rem 0 1.2rem 0;
}
.hero h1 {
  font-size: 2.1rem;
  font-weight: 800;
  margin-bottom: 0.2rem;
}
.hero p {
  opacity: 0.85;
  margin-top: 0;
}

/* Clickable cards (single entity: card = button) */
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 26px;
  margin-top: 12px;
}

.card-link {
  text-decoration: none !important;
  color: white !important;
}

.card {
  border-radius: 18px;
  padding: 26px;
  min-height: 200px;
  box-shadow: 0 10px 35px rgba(0,0,0,.35);
  transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 55px rgba(0,0,0,.45);
  filter: brightness(1.03);
}

/* Fancy glow */
.card::after{
  content:"";
  position:absolute;
  inset:-40%;
  background: radial-gradient(circle, rgba(255,255,255,0.18), transparent 55%);
  transform: translateX(-35%);
  transition: transform .25s ease;
}
.card:hover::after{ transform: translateX(10%); }

.pred { background: linear-gradient(135deg, #1DB954, #128a3e); }
.tab  { background: linear-gradient(135deg, #3b82f6, #6d28d9); }

.title {
  font-size: 1.55rem;
  font-weight: 800;
  margin-bottom: 8px;
  position: relative;
  z-index: 1;
}

.desc {
  font-size: 0.95rem;
  opacity: .92;
  line-height: 1.5;
  position: relative;
  z-index: 1;
}

.badge {
  display: inline-block;
  margin-top: 14px;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(0,0,0,0.18);
  font-size: 0.85rem;
  position: relative;
  z-index: 1;
}

/* Team section compact + interactive cards */
.team-wrap {
  margin-top: 16px;
  text-align: center;
}
.team-title {
  margin: 8px 0 10px 0;
  font-size: 1.25rem;
  font-weight: 800;
}
.team-grid {
  display:flex;
  justify-content:center;
  gap:12px;
  flex-wrap:wrap;
}

.team-card{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 14px;
  padding: 12px 14px;
  min-width: 210px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.25);
  transition: transform .18s ease, box-shadow .18s ease;
}
.team-card:hover{
  transform: translateY(-4px);
  box-shadow: 0 12px 38px rgba(0,0,0,0.35);
}

.team-name { font-weight: 800; }
.team-id { opacity: 0.85; font-size: 0.9rem; }

.smallcap{
  margin-top: 10px;
  opacity: 0.75;
  font-size: 0.85rem;
}

/* Responsive */
@media (max-width: 900px){
  .grid{ grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🎵 Spotify Popularity ML Project</h1>
  <p>Choose a module to explore</p>
</div>
""", unsafe_allow_html=True)

# Clickable cards (no extra buttons)
st.markdown("""
<div class="grid">
  <a class="card-link" href="/prediction_app">
    <div class="card pred">
      <div class="title">🚀 Prediction App</div>
      <div class="desc">Predict song popularity using ML and save results to MySQL in real time.</div>
      <div class="badge">Click to open →</div>
    </div>
  </a>

  <a class="card-link" href="/tableau_dashboard">
    <div class="card tab">
      <div class="title">📊 Tableau Dashboard</div>
      <div class="desc">Explore KPIs, top artists, trends, and feature impact on popularity.</div>
      <div class="badge">Click to open →</div>
    </div>
  </a>
</div>
""", unsafe_allow_html=True)

# Compact team section (no big plain text)
st.markdown("""+
<div class="team-wrap">
  <div class="team-title">👥 Project Team</div>

  <div class="team-grid">
    <div class="team-card">
      <div class="team-name">Atharv Gurav</div>
      <div class="team-id">250843025011</div>
    </div>
    <div class="team-card">
      <div class="team-name">Pankaj Padulkar</div>
      <div class="team-id">250843025035</div>
    </div>
    <div class="team-card">
      <div class="team-name">Rohit Holkar</div>
      <div class="team-id">250843025045</div>
    </div>
  </div>

  <div class="smallcap">Developed by Group 7</div>
</div>
""", unsafe_allow_html=True)
