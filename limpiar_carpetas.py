"""
Limpia y simplifica la estructura de carpetas de fotos.
- Aplana subcategorías (Encastre/Tetris → Encastre)
- Elimina duplicados (mismo nombre de archivo)
- Elimina la carpeta "Avión" que tiene todo duplicado
- Elimina carpetas vacías
"""

import os
import shutil
import sys
from collections import defaultdict

BASE_DIR = os.path.join("downloads", "clamacalma")

# Categorías flat objetivo (sin subcarpetas)
SHORTCODE_TO_CATEGORY = {
    # Arrastre
    "DPbvuB7kY4E": "Arrastre",
    "C4tSY-jPrbz": "Arrastre",
    "ChKo2ntLSaN": "Arrastre",
    "C_L8QnGPtfY": "Arrastre",

    # Tangram
    "DCIEjerPXJc": "Tangram",
    "C8LDO7JPRNj": "Tangram",
    "CuIEdxVu3Tg": "Tangram",

    # Encastre (todo junto)
    "DARglWlPV0z": "Encastre",
    "CmcDQQrrxXo": "Encastre",
    "CfSCjs5JJU1": "Encastre",
    "CdtcAIXpx2N": "Encastre",
    "Cdtc4uypsRI": "Encastre",
    "CecQIRkp9-A": "Encastre",
    "ChK-dmrJKvt": "Encastre",
    "Cjuho6NO3W0": "Encastre",
    "C8-jvHSvRRi": "Encastre",
    "CdtcTxGJYKd": "Encastre",
    "CdtcdDfJ8z5": "Encastre",

    # Rompecabezas (todo junto)
    "DOjTUZVEW3k": "Rompecabezas",
    "CtUVPAaO6JZ": "Rompecabezas",
    "DItp9CPReuI": "Rompecabezas",
    "Cjv1_G7JcmA": "Rompecabezas",
    "Ch0caH3LGpQ": "Rompecabezas",

    # Mosaico (todo junto)
    "C-GKjjAvYUN": "Mosaico",
    "Cw-1hU0O7kx": "Mosaico",
    "CmcEHboLBzW": "Mosaico",

    # Jenga (todo junto)
    "Cfwz9olp36s": "Jenga",
    "Ce1B0N1OAUb": "Jenga",
    "CdzFNSNs6kf": "Jenga",
    "CdeMnvMJv19": "Jenga",
    "CdeMsQBppjk": "Jenga",

    # Ola de equilibrio
    "DBmVcAERwYc": "Ola de equilibrio",
    "ChvEBPfJSqd": "Ola de equilibrio",

    # Cubo Soma
    "C793mj6PFo2": "Cubo Soma",
    "Cg75L5CL_2r": "Cubo Soma",

    # Arco iris
    "C7nJIgcRR0k": "Arco iris",
    "Ct2P_jPvbmY": "Arco iris",

    # Ta-Te-Ti
    "ChgKYQ7r46E": "Ta-Te-Ti",
    "CdeM43rpnyF": "Ta-Te-Ti",
    "CeWca0KOTuW": "Ta-Te-Ti",

    # Tren
    "CiGZLc4LA6P": "Tren",
    "ChfYxE0LVil": "Tren",

    # Frutas y verduras
    "Ch0lXHZrzJw": "Frutas y verduras",

    # Biblioteca infantil
    "CipqPsuLybx": "Biblioteca infantil",

    # Autos
    "Cgp8xU6rvmy": "Autos",

    # Avion
    "C43lahmPYDw": "Avion",

    # Animalitos para tejer
    "C85ZmOMP37T": "Animalitos para tejer",

    # Varios (todo junto)
    "DA4REmXPKw3": "Varios",
    "DAMRglvv8Gc": "Varios",
    "CgF773yrTyP": "Varios",
    "Cgo6_rPLkPa": "Varios",
    "C-ljexIvbYL": "Varios",
    "C-yZvrwv-bZ": "Varios",
    "CsPgL0wu5aY": "Varios",
    "Ceougfpp8gW": "Varios",
    "C7XNFj_PjxB": "Varios",
    "C2fn91hRsnq": "Varios",
    "DMlDkTjxHtw": "Varios",
    "CtmpTr1PKXY": "Varios",
    "Cgrtp-FLa6r": "Varios",
    "CeWahQkrs5f": "Varios",
}


def extract_shortcode(filename):
    """Extrae el shortcode del nombre de archivo."""
    parts = filename.split("__")
    if len(parts) < 2:
        return None
    shortcode_part = parts[1].replace(".jpg", "")
    if "_" in shortcode_part and shortcode_part.rsplit("_", 1)[1].isdigit():
        return shortcode_part.rsplit("_", 1)[0]
    return shortcode_part


def guess_category_from_path(filepath):
    """Intenta adivinar la categoría basándose en la carpeta actual."""
    rel = filepath.replace(BASE_DIR + os.sep, "")
    parts = rel.split(os.sep)

    # Ignorar "Avión" como raíz (es duplicado)
    if parts[0] == "Avión" and len(parts) > 2:
        parts = parts[1:]

    # La primera carpeta después de filtrar es la categoría
    folder = parts[0]

    # Mapeo de nombres de subcarpeta a categoría padre
    FOLDER_MAP = {
        "Perro": "Arrastre",
        "Animalitos": "Arrastre",
        "Carrito con bloques": "Arrastre",
        "Perro arrastre": "Arrastre",
        "Llama arrastre": "Arrastre",
        "Grande": "Jenga",
        "Circular": "Mosaico",
        "Bloques de construccion": "Mosaico",
        "Bloques": "Mosaico",
        "Decorativo": "Rompecabezas",
        "4 elementos": "Rompecabezas",
        "Puzzle de vocales": "Rompecabezas",
        "Rompecabezas pez": "Rompecabezas",
        "Mosaico": "Mosaico",
        "Encastrables": "Encastre",
        "Encastrables colores": "Encastre",
        "Formas geometricas": "Encastre",
        "Lineal de formas": "Encastre",
        "Macetas y flores": "Encastre",
        "Piramide conica": "Encastre",
        "Tetris": "Encastre",
        "Tetris encastre": "Encastre",
        "Torre de colores": "Encastre",
        "Torres multicolor": "Encastre",
        "Torres encastre": "Encastre",
        "Catalogo general": "Varios",
        "Feria": "Varios",
        "Sorteo": "Varios",
        "Barco equilibrio": "Ola de equilibrio",
    }

    # Si la carpeta está en nuestro mapa, usar eso
    if folder in FOLDER_MAP:
        return FOLDER_MAP[folder]

    # Categorías válidas de primer nivel
    VALID = {
        "Arrastre", "Tangram", "Encastre", "Rompecabezas", "Mosaico",
        "Jenga", "Ola de equilibrio", "Cubo Soma", "Arco iris",
        "Ta-Te-Ti", "Tren", "Frutas y verduras", "Biblioteca infantil",
        "Autos", "Avion", "Animalitos para tejer", "Piramide", "Varios",
    }

    if folder in VALID:
        return folder

    return "Varios"


def main():
    if not os.path.isdir(BASE_DIR):
        print(f"Error: No se encontró {BASE_DIR}")
        sys.exit(1)

    # 1. Encontrar TODOS los .jpg recursivamente
    all_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.lower().endswith(".jpg"):
                all_files.append(os.path.join(root, f))

    print(f"Total de archivos .jpg encontrados: {len(all_files)}")

    # 2. Agrupar por nombre de archivo (detectar duplicados)
    by_name = defaultdict(list)
    for fpath in all_files:
        fname = os.path.basename(fpath)
        by_name[fname].append(fpath)

    unique = len(by_name)
    dupes = len(all_files) - unique
    print(f"Archivos únicos: {unique}")
    print(f"Duplicados: {dupes}")

    # 3. Para cada archivo único, determinar categoría y mover
    moved = 0
    already_ok = 0
    uncategorized = []

    for fname, paths in sorted(by_name.items()):
        shortcode = extract_shortcode(fname)

        # Determinar categoría
        if shortcode and shortcode in SHORTCODE_TO_CATEGORY:
            category = SHORTCODE_TO_CATEGORY[shortcode]
        else:
            # Usar la ruta del primer archivo que NO está en "Avión"
            non_avion = [p for p in paths if os.sep + "Avión" + os.sep not in p]
            ref_path = non_avion[0] if non_avion else paths[0]
            category = guess_category_from_path(ref_path)

        dest_dir = os.path.join(BASE_DIR, category)
        dest_path = os.path.join(dest_dir, fname)

        # Verificar si ya está en el lugar correcto
        if dest_path in paths:
            already_ok += 1
            # Eliminar las copias extra
            for p in paths:
                if p != dest_path:
                    os.remove(p)
                    if dupes > 0:
                        dupes -= 1
            continue

        # Mover desde la primera copia disponible
        os.makedirs(dest_dir, exist_ok=True)
        src = paths[0]
        if not os.path.exists(dest_path):
            shutil.move(src, dest_path)
            moved += 1
        # Eliminar todas las demás copias
        for p in paths:
            if os.path.exists(p) and p != dest_path:
                os.remove(p)

    # 4. Eliminar carpetas vacías
    deleted_dirs = 0
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        if root == BASE_DIR:
            continue
        try:
            if not os.listdir(root):
                os.rmdir(root)
                deleted_dirs += 1
        except OSError:
            pass

    print(f"\n{'=' * 50}")
    print(f"Movidos: {moved}")
    print(f"Ya estaban bien: {already_ok}")
    print(f"Duplicados eliminados: {len(all_files) - unique}")
    print(f"Carpetas vacías eliminadas: {deleted_dirs}")

    # 5. Mostrar estructura final
    print(f"\nEstructura final:")
    for root, dirs, files in os.walk(BASE_DIR):
        dirs.sort()
        level = root.replace(BASE_DIR, "").count(os.sep)
        indent = "  " * level
        folder_name = os.path.basename(root) or "clamacalma"
        jpg_count = len([f for f in files if f.lower().endswith(".jpg")])
        if jpg_count > 0:
            print(f"{indent}{folder_name}/ ({jpg_count} fotos)")
        elif level == 0:
            print(f"{indent}{folder_name}/")


if __name__ == "__main__":
    main()
