import streamlit as st
import sys
from pathlib import Path
import base64
import json
import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.inference_client import predict

st.title("📁 Importer une image")
st.markdown("Chargez une image de produit industriel pour l'analyser.")

uploaded_file = st.file_uploader("Choisissez une image (JPG ou PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    
    # Affichage côte à côte
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_bytes, caption="Image originale", use_container_width=True)
    
    if st.button("🔍 Analyser l'image", type="primary"):
        with st.spinner("Analyse en cours..."):
            try:
                result = predict(image_bytes)
                
                # Affichage du résultat dans la colonne de droite
                with col2:
                    if result['label'] == 'suspect':
                        st.error(f"⚠️ Résultat : **{result['label'].upper()}**")
                    else:
                        st.success(f"✅ Résultat : **{result['label'].upper()}**")
                        
                    st.metric("Score d'anomalie", f"{result['score']:.2f}")
                    
                    if result.get("heatmap"):
                        heatmap_bytes = base64.b64decode(result["heatmap"])
                        st.image(heatmap_bytes, caption="Carte thermique", use_container_width=True)
                
                # --- SAUVEGARDE DANS L'HISTORIQUE ---
                history_file = Path(__file__).parent.parent.parent / "history" / "inspections.json"
                history_file.parent.mkdir(exist_ok=True)
                
                new_entry = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "filename": uploaded_file.name,
                    "label": result["label"],
                    "score": round(result["score"], 4)
                }
                
                # Lire l'historique existant
                history = []
                if history_file.exists():
                    with open(history_file, "r") as f:
                        history = json.load(f)
                
                history.append(new_entry)
                
                # Écrire le nouvel historique
                with open(history_file, "w") as f:
                    json.dump(history, f, indent=4)
                    
                st.info("✅ Inspection sauvegardée dans l'historique.")
                
            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")
