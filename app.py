import streamlit as st
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "app"))

st.set_page_config(
    page_title="SmartQuality AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Dashboard", "Importer une image", "Historique", "Statistiques"])

st.sidebar.markdown("---")
st.sidebar.info("Version 0.9\nPrêt pour l'intégration IA.")

if page == "Dashboard":
    st.title("🔍 SmartQuality AI")
    st.subheader("Détection intelligente des défauts industriels")
    st.markdown("---")
    
    use_mock = os.environ.get("USE_MOCK", "True").lower() == "true"
    mode_texte = "Mock (en attente)" if use_mock else "PatchCore (Réel)"
    statut = "🟡 En développement" if use_mock else "🟢 En ligne"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Modèle", mode_texte)
    with col2:
        st.metric("Dataset", "MVTec AD — metal_nut")
    with col3:
        st.metric("Statut", statut)
        
    st.markdown("---")
    st.markdown("""
    ### Bienvenue dans SmartQuality AI
    Cette application permet de :
    - **Importer** une image d'un produit industriel
    - **Analyser** sa conformité via le module IA
    - **Visualiser** la carte thermique des anomalies
    - **Consulter** l'historique des inspections
    - **Suivre** les statistiques de production
    """)

elif page == "Importer une image":
    exec(open("app/pages/import_image.py").read())
elif page == "Historique":
    exec(open("app/pages/history.py").read())
elif page == "Statistiques":
    exec(open("app/pages/stats.py").read())
