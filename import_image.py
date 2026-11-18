import streamlit as st
import sys
from pathlib import Path
import base64
import json
import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.inference_client import predict

st.markdown("<h2>📁 Inspection Visuelle</h2>", unsafe_allow_html=True)
st.markdown("Chargez une image pour lancer l'analyse IA.")

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("#### 📷 Image d'entrée")
        st.image(image_bytes, use_container_width=True)
    
    if st.button("▶ Lancer l'Inspection", type="primary"):
        with st.spinner("Analyse IA en cours..."):
            try:
                result = predict(image_bytes)
                
                with col2:
                    st.markdown("#### 🎯 Résultat de l'IA")
                    
                    if result['label'] == 'suspect':
                        st.markdown('<div class="badge-fail" style="font-size: 1.5rem; text-align: center; padding: 15px;">❌ NOK (Défectueux)</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # --- AFFICHAGE DES RECOMMANDATIONS ---
                        st.info(f"**Type de défaut détecté :** {result.get('type_defaut', 'Inconnu')}")
                        st.warning(f"**🛠️ Action corrective recommandée :** {result.get('recommandation', 'Vérifier la pièce manuellement.')}")
                        
                    else:
                        st.markdown('<div class="badge-pass" style="font-size: 1.5rem; text-align: center; padding: 15px;">✅ OK (Conforme)</div>', unsafe_allow_html=True)
                    
                    st.metric("Score d'anomalie", f"{result['score']:.2f}")
                    
                    if result.get("heatmap"):
                        heatmap_bytes = base64.b64decode(result["heatmap"])
                        st.markdown("#### 🌡️ Carte thermique (Localisation)")
                        st.image(heatmap_bytes, use_container_width=True)
                
                # Sauvegarde Historique (avec les nouveaux champs)
                history_file = Path(__file__).parent.parent.parent / "history" / "inspections.json"
                history_file.parent.mkdir(exist_ok=True)
                
                new_entry = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "filename": uploaded_file.name,
                    "label": result["label"],
                    "score": round(result["score"], 4),
                    "type_defaut": result.get("type_defaut", "Aucun"),
                    "recommandation": result.get("recommandation", "")
                }
                
                history = []
                if history_file.exists():
                    with open(history_file, "r") as f:
                        history = json.load(f)
                history.append(new_entry)
                with open(history_file, "w") as f:
                    json.dump(history, f, indent=4)
                    
                st.toast("✅ Inspection sauvegardée !")
                
            except Exception as e:
                st.error(f"Erreur : {e}")
