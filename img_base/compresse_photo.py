import os
from PIL import Image

INPUT_DIR = "img"
OUTPUT_DIR = "img_compressed"

# Résolution maximale en largeur (change si tu veux)
MAX_WIDTH = 4096

def compress_image(input_path, output_path):
    img = Image.open(input_path)

    # Réduction de taille si trop grande
    w, h = img.size
    if w > MAX_WIDTH:
        ratio = MAX_WIDTH / w
        img = img.resize((MAX_WIDTH, int(h * ratio)), Image.LANCZOS)

    # Création du dossier de sortie si nécessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Sauvegarde en WebP compressé
    img.save(
        output_path,
        "webp",
        quality=60,      # Compression efficace
        method=6,        # Meilleur algo
        optimize=True,   # Retire les métadonnées inutiles
    )

    print(f"OK : {output_path}")

def traverse_and_compress():
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                input_path = os.path.join(root, file)

                # Sous-dossier équivalent dans img_compressed
                relative = os.path.relpath(root, INPUT_DIR)
                new_dir = os.path.join(OUTPUT_DIR, relative)

                filename_no_ext = os.path.splitext(file)[0] + ".webp"
                output_path = os.path.join(new_dir, filename_no_ext)

                compress_image(input_path, output_path)

    print("\n--- Terminé ! Toutes les images sont compressées. ---")

traverse_and_compress()
