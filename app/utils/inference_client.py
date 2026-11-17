import base64
import cv2
import numpy as np
import os

# On utilise une variable d'environnement pour basculer facilement
# Par défaut, on est en mock (True) tant que Personne 1 n'a pas livré
USE_MOCK = os.environ.get("USE_MOCK", "True").lower() == "true"

def predict(image_bytes: bytes, threshold: float = 0.5) -> dict:
    if USE_MOCK:
        return _mock_predict(image_bytes, threshold)
    
    try:
        # --- C'est ici que l'on branchera le vrai PatchCore ---
        from ai_module.inference import predict as ai_predict
        return ai_predict(image_bytes, threshold=threshold)
    except ImportError:
        raise RuntimeError("Le module IA réel n'est pas encore installé. Vérifiez ai_module/inference.py.")
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'inférence réelle : {e}")

def _mock_predict(image_bytes: bytes, threshold: float) -> dict:
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Image invalide ou corrompue")
    h, w = img.shape[:2]
    heatmap = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(heatmap, (w // 2, h // 2), min(h, w) // 4, 255, -1)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    _, buffer = cv2.imencode(".png", heatmap_color)
    heatmap_b64 = base64.b64encode(buffer).decode("utf-8")
    score = 0.87
    label = "suspect" if score >= threshold else "normal"
    return {"label": label, "score": score, "heatmap": heatmap_b64, "zones": []}
