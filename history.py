import streamlit as st
import json
import pandas as pd
from pathlib import Path

st.markdown("<h2>📜 Historique des inspections</h2>", unsafe_allow_html=True)
st.markdown("Retrouvez ici toutes les analyses effectuées.")

history_file = Path(__file__).parent.parent.parent / "history" / "inspections.json"

if not history_file.exists():
    st.info("Aucune inspection enregistrée pour le moment.")
else:
    with open(history_file, "r") as f:
        history = json.load(f)
    
    if len(history) == 0:
        st.info("L'historique est vide.")
    else:
        df = pd.DataFrame(history).iloc[::-1].reset_index(drop=True)
        
        # Ajouter une colonne de sélection
        df.insert(0, "Sélectionner", False)
        
        st.markdown("### 📋 Liste des inspections")
        edited_df = st.data_editor(
            df,
            column_config={
                "Sélectionner": st.column_config.CheckboxColumn(
                    "Supprimer ?",
                    help="Cochez pour supprimer cette ligne",
                    default=False,
                )
            },
            disabled=["timestamp", "filename", "label", "score", "type_defaut", "recommandation"],
            hide_index=True,
            use_container_width=True,
        )
        
        # Bouton de suppression
        selected_rows = edited_df[edited_df["Sélectionner"] == True]
        
        if not selected_rows.empty:
            st.warning(f"⚠️ {len(selected_rows)} inspection(s) sélectionnée(s) pour suppression.")
            if st.button("🗑️ Supprimer la sélection"):
                df_to_keep = edited_df[edited_df["Sélectionner"] == False].drop(columns=["Sélectionner"])
                new_history = df_to_keep.iloc[::-1].to_dict(orient="records")
                
                with open(history_file, "w") as f:
                    json.dump(new_history, f, indent=4)
                
                st.success("✅ Suppression effectuée !")
                st.rerun()
