import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.markdown("<h2>📈 Statistiques de Production</h2>", unsafe_allow_html=True)
st.markdown("Visualisez les tendances et la performance de votre ligne de production.")

history_file = Path(__file__).parent.parent.parent / "history" / "inspections.json"

if not history_file.exists():
    st.info("Aucune donnée disponible. Effectuez d'abord quelques inspections.")
else:
    with open(history_file, "r") as f:
        history = json.load(f)
    
    if len(history) == 0:
        st.info("L'historique est vide.")
    else:
        df = pd.DataFrame(history)
        
        # --- KPI Cards ---
        col1, col2, col3 = st.columns(3)
        total = len(df)
        suspects = len(df[df["label"] == "suspect"])
        normaux = len(df[df["label"] == "normal"])
        taux_anomalie = (suspects / total) * 100 if total > 0 else 0
        
        with col1:
            st.metric("Total Inspections", total)
        with col2:
            st.metric("Pièces Conformes", normaux)
        with col3:
            st.metric("Taux d'Anomalie", f"{taux_anomalie:.1f} %")
            
        st.markdown("---")
        
        # --- Graphiques ---
        col_graph1, col_graph2 = st.columns(2)
        
        # 1. Camembert (Répartition)
        with col_graph1:
            st.subheader("🥧 Répartition des résultats")
            fig1, ax1 = plt.subplots(figsize=(5, 5))
            labels = ['Normal', 'Suspect']
            sizes = [normaux, suspects]
            colors = ['#10B981', '#EF4444'] # Vert et Rouge
            
            if normaux == 0 and suspects > 0:
                ax1.pie([suspects], labels=['Suspect'], colors=['#EF4444'], autopct='%1.1f%%')
            elif suspects == 0 and normaux > 0:
                ax1.pie([normaux], labels=['Normal'], colors=['#10B981'], autopct='%1.1f%%')
            else:
                ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
                
            ax1.axis('equal')
            st.pyplot(fig1)
            
        # 2. Histogramme (Distribution des scores)
        with col_graph2:
            st.subheader("📊 Distribution des scores")
            fig2, ax2 = plt.subplots(figsize=(6, 5))
            ax2.hist(df["score"], bins=10, color='#2F81F7', edgecolor='white')
            ax2.set_xlabel("Score d'anomalie")
            ax2.set_ylabel("Nombre d'images")
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            st.pyplot(fig2)
            
        # 3. Évolution temporelle
        st.markdown("---")
        st.subheader("📅 Évolution des inspections")
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")
            
            fig3, ax3 = plt.subplots(figsize=(12, 4))
            ax3.plot(df["timestamp"], df["score"], marker='o', linestyle='-', color='#8B5CF6')
            ax3.set_ylabel("Score d'anomalie")
            ax3.set_xlabel("Date/Heure")
            plt.xticks(rotation=45)
            ax3.grid(axis='y', linestyle='--', alpha=0.7)
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            st.pyplot(fig3)
