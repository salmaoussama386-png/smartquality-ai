import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from utils.inference_client import predict

def main():
    print("=== TEST DU FLUX D'INFÉRENCE ===")
    demo_dir = Path(__file__).parent.parent / "data" / "demo_images"
    
    if not demo_dir.exists():
        print(f"Dossier introuvable : {demo_dir}")
        return
        
    images = list(demo_dir.glob("*.png"))
    if not images:
        print("Aucune image de test trouvée.")
        return
        
    for img_path in images:
        print(f"\n--- Test sur : {img_path.name} ---")
        with open(img_path, "rb") as f:
            img_bytes = f.read()
        try:
            result = predict(img_bytes)
            assert "label" in result and "score" in result and "heatmap" in result
            print(f"  Label   : {result['label']}")
            print(f"  Score   : {result['score']}")
            print(f"  Heatmap : {len(result['heatmap'])} caractères")
        except Exception as e:
            print(f"  ERREUR  : {e}")
            
    print("\n✅ Test terminé.")

if __name__ == "__main__":
    main()
