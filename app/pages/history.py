import streamlit as st
import json
import pandas as pd
from pathlib import Path

st.title("📜 Historique des inspections")
st.markdown("Retrouvez ici toutes les analyses effectuées.")

history_file = Path(__file__).parent.parent.parent / "history" / "inspections.json"

if not history_file.exists() or history_file.stat().st_size == 0:
    st.info("Aucune inspection enregistrée pour le moment. Allez dans 'Importer une image' pour commencer.")
else:
    with open(history_file, "r") as f:
        history = json.load(f)
    
    if len(history) == 0:
        st.info("L'historique est vide.")
    else:
        # Convertir en DataFrame pour un bel affichage
        df = pd.DataFrame(history)
        
        # Inverser pour voir les plus récents en premier
        df = df.iloc[::-1].reset_index(drop=True)
        
        st.dataframe(df, use_container_width=True)
        
        # Statistiques rapides
        st.markdown("---")
        st.subheader("Résumé rapide")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total inspections", len(df))
        with col2:
            nb_suspects = len(df[df["label"] == "suspect"])
            st.metric("Anomalies détectées", nb_suspects)
