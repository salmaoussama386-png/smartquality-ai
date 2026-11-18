import streamlit as st
import sys
from pathlib import Path

css_path = Path(__file__).parent / "app" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sys.path.insert(0, str(Path(__file__).parent / "app"))

st.set_page_config(page_title="SmartQuality AI", page_icon="🏭", layout="wide")

# --- Barre latérale ---
with st.sidebar:
    st.markdown("<h1>🏭 SmartQuality AI</h1>", unsafe_allow_html=True)
    st.caption("Vision Quality Inspection")
    st.markdown("---")
    page = st.radio("", ["📊 Dashboard", "📁 Importer une image", "📜 Historique", "📈 Statistiques"])
    st.markdown("---")
    st.markdown("🟢 **Statut** : En ligne")
    st.caption("Version 2.0 | Projet IA")

# --- Page Dashboard ---
if page == "📊 Dashboard":
    # Barre supérieure
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid #E2E8F0; margin-bottom: 20px;">
        <h2 style="margin: 0;">Vision Quality Inspection</h2>
        <span style="color: #64748B; font-size: 0.9rem;">Ligne 3 - Station 38</span>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Inspections", "2,148", "98.7% PASS")
    with col2:
        st.metric("Anomalies", "14", "0.6% REJECT")
    with col3:
        st.metric("Vitesse", "120", "pièces/min")
    with col4:
        st.metric("Confiance IA", "98.2%", "+1.2%")
    
    st.markdown("---")
    
    # Zone principale (remplacée par une action utile)
    st.markdown("### 🔍 Démarrer une inspection")
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.info("📸 **Prêt à analyser ?** Utilisez le menu **'Importer une image'** pour charger une photo de pièce et lancer la détection de défauts par l'IA.")
    
    with col_right:
        st.markdown("### 📋 Derniers défauts (Simulation)")
        st.markdown("""
        - **Rayure** sur Zone A (98%) <span class="badge-fail">REJECT</span>
        - **Bosse** sur Zone B (94%) <span class="badge-fail">REJECT</span>
        - **Assemblage** (96%) <span class="badge-pass">PASS</span>
        """, unsafe_allow_html=True)

# --- Autres pages ---
elif page == "📁 Importer une image":
    exec(open("app/pages/import_image.py").read())
elif page == "📜 Historique":
    exec(open("app/pages/history.py").read())
elif page == "📈 Statistiques":
    exec(open("app/pages/stats.py").read())
