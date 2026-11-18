import streamlit as st
import sys
from pathlib import Path

sys.path.append("/content/drive/MyDrive/SmartQuality_IA")

# On met l'import en cache pour ne pas recharger le modèle à chaque fois
@st.cache_resource
def _load_ai():
    from inference import predict
    return predict

def predict(image_bytes: bytes, threshold: float = 0.5) -> dict:
    try:
        ai_func = _load_ai()
        return ai_func(image_bytes, threshold=threshold)
    except Exception as e:
        raise RuntimeError(f"Erreur dans le module IA : {e}")
