import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.title("📊 Statistiques de production")
st.markdown("Visualisez les tendances des inspections effectuées.")

history_file = Path(__file__).parent.parent.parent / "history" / "inspections.json"

if not history_file.exists() or history_file.stat().st_size == 0:
    st.info("Aucune donnée disponible. Effectuez d'abord quelques inspections dans la page 'Importer une image'.")
else:
    with open(history_file, "r") as f:
        history = json.load(f)
        
    if len(history) == 0:
        st.info("L'historique est vide.")
    else:
        df = pd.DataFrame(history)
        
        # --- Métriques globales ---
        col1, col2, col3 = st.columns(3)
        total = len(df)
        suspects = len(df[df["label"] == "suspect"])
        normaux = len(df[df["label"] == "normal"])
        taux_anomalie = (suspects / total) * 100 if total > 0 else 0
        
        with col1:
            st.metric("Total des inspections", total)
        with col2:
            st.metric("Pièces normales", normaux)
        with col3:
            st.metric("Taux d'anomalie", f"{taux_anomalie:.1f} %")
            
        st.markdown("---")
        
        # --- Graphiques ---
        col_graph1, col_graph2 = st.columns(2)
        
        # 1. Camembert (Répartition Normal / Suspect)
        with col_graph1:
            st.subheader("Répartition des résultats")
            fig1, ax1 = plt.subplots(figsize=(4, 4))
            labels = ['Normal', 'Suspect']
            sizes = [normaux, suspects]
            colors = ['#2ecc71', '#e74c3c']
            
            # Gérer le cas où une des catégories est à 0
            if normaux == 0 and suspects > 0:
                ax1.pie([suspects], labels=['Suspect'], colors=['#e74c3c'], autopct='%1.1f%%')
            elif suspects == 0 and normaux > 0:
                ax1.pie([normaux], labels=['Normal'], colors=['#2ecc71'], autopct='%1.1f%%')
            else:
                ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                
            ax1.axis('equal')
            st.pyplot(fig1)
            
        # 2. Histogramme (Distribution des scores)
        with col_graph2:
            st.subheader("Distribution des scores d'anomalie")
            fig2, ax2 = plt.subplots(figsize=(5, 4))
            ax2.hist(df["score"], bins=10, color='#3498db', edgecolor='black')
            ax2.set_xlabel("Score")
            ax2.set_ylabel("Nombre d'images")
            ax2.set_title("Scores d'anomalie")
            st.pyplot(fig2)
            
        # 3. Évolution temporelle (optionnel mais sympa)
        st.markdown("---")
        st.subheader("Évolution des inspections")
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")
            fig3, ax3 = plt.subplots(figsize=(10, 3))
            ax3.plot(df["timestamp"], df["score"], marker='o', linestyle='-', color='#9b59b6')
            ax3.set_ylabel("Score")
            ax3.set_xlabel("Date/Heure")
            plt.xticks(rotation=45)
            st.pyplot(fig3)
