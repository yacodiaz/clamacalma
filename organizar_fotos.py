"""
Organiza las fotos descargadas de Instagram en carpetas por producto/juego.
Mueve archivos desde la raíz de downloads/clamacalma/ a subcarpetas.
NO toca archivos que ya están en subcarpetas.
"""

import os
import shutil
import sys

BASE_DIR = os.path.join("downloads", "clamacalma")

# ═══════════════════════════════════════════════════════════════
# CATALOGO: shortcode -> carpeta destino
#
# Mapeo manual basado en el contenido de cada post.
# Usa "/" para jerarquía: "Encastre/Torres" crea carpeta anidada.
# ═══════════════════════════════════════════════════════════════

CATALOG = {
    # ── Arrastre ──────────────────────────────────────────────
    "DPbvuB7kY4E": "Arrastre/Perro",              # Perrito de arrastre
    "C4tSY-jPrbz": "Arrastre/Animalitos",          # Animalitos de arrastre (llama, oveja, etc.)
    "ChKo2ntLSaN": "Arrastre/Carrito con bloques", # Carrito de arrastre + 24 bloques
    "C_L8QnGPtfY": "Arrastre/Perro",              # Estos perritos nos tienen asi (perritos con rueditas)

    # ── Tangram ───────────────────────────────────────────────
    "DCIEjerPXJc": "Tangram",                      # TANGRAM
    "C8LDO7JPRNj": "Tangram",                      # TANGRAM! (figuras)
    "CuIEdxVu3Tg": "Tangram",                      # T A N G R A M

    # ── Encastre ──────────────────────────────────────────────
    "DARglWlPV0z": "Encastre/Encastrables colores", # Encastrables en colores pasteles
    "CmcDQQrrxXo": "Encastre/Encastrables",         # ENCASTRABLES (formas y colores, con números)
    "CfSCjs5JJU1": "Encastre/Formas geometricas",   # JUEGO DE ENCASTRE formas geométricas apilables
    "CdtcAIXpx2N": "Encastre/Lineal de formas",     # JUEGO DE ENCASTRE LINEAL DE FORMAS
    "Cdtc4uypsRI": "Encastre/Torres multicolor",    # TORRES DE ENCASTRE MULTICOLOR
    "CecQIRkp9-A": "Encastre/Tetris",               # TETRIS DE ENCASTRE
    "ChK-dmrJKvt": "Encastre/Macetas y flores",     # Juego de encastre - macetas, hojas y flores
    "Cjuho6NO3W0": "Encastre/Piramide conica",      # PIRÁMIDE CÓNICA (anillos apilables)
    "C8-jvHSvRRi": "Encastre/Torre de colores",     # Torre de colores

    # ── Rompecabezas ──────────────────────────────────────────
    "DOjTUZVEW3k": "Rompecabezas/Decorativo",       # Rompecabezas decorativo (madera y MDF)
    "CtUVPAaO6JZ": "Rompecabezas/Decorativo",       # ROMPECABEZAS DECORATIVO
    "DItp9CPReuI": "Rompecabezas/4 elementos",      # 4 ELEMENTOS (rompecabezas naturaleza)
    "Cjv1_G7JcmA": "Rompecabezas/Mosaico",          # ROMPECABEZAS MOSAICO (bloques de colores)
    "Ch0caH3LGpQ": "Rompecabezas/Puzzle de vocales", # PUZZLE DE VOCALES

    # ── Mosaico ───────────────────────────────────────────────
    "C-GKjjAvYUN": "Mosaico",                       # MOSAICO (mil posibilidades)
    "Cw-1hU0O7kx": "Mosaico/Circular",              # Mosaico circular (piezas curvas)
    "CmcEHboLBzW": "Mosaico/Bloques de construccion", # MOSAICO DE BLOQUES DE CONSTRUCCIÓN

    # ── Jenga ─────────────────────────────────────────────────
    "Cfwz9olp36s": "Jenga/Grande",                   # YENGA GRANDE (54 bloques, 18 pisos)
    "Ce1B0N1OAUb": "Jenga",                          # JENGA
    "CdzFNSNs6kf": "Jenga",                          # JENGA
    "CdeMnvMJv19": "Jenga",                          # (sin desc, pero es jenga por contexto de posts cercanos)

    # ── Ola de equilibrio ─────────────────────────────────────
    "DBmVcAERwYc": "Ola de equilibrio",              # OLA DE EQUILIBRIO
    "ChvEBPfJSqd": "Ola de equilibrio",              # OLA DE EQUILIBRIO

    # ── Cubo Soma ─────────────────────────────────────────────
    "C793mj6PFo2": "Cubo Soma",                     # CUBO SOMA
    "Cg75L5CL_2r": "Cubo Soma",                     # CUBO SOMA

    # ── Arco iris ─────────────────────────────────────────────
    "C7nJIgcRR0k": "Arco iris",                     # Juego arcoíris
    "Ct2P_jPvbmY": "Arco iris",                     # ARCO IRIS WALDORF

    # ── Ta-Te-Ti ──────────────────────────────────────────────
    "ChgKYQ7r46E": "Ta-Te-Ti",                      # TA-TE-TI pequeño
    "CdeM43rpnyF": "Ta-Te-Ti",                      # TA TE TI
    "CeWca0KOTuW": "Ta-Te-Ti",                      # (hashtags + TA-TE-TI al final)

    # ── Tren ──────────────────────────────────────────────────
    "CiGZLc4LA6P": "Tren",                          # TRENCITO DE MADERA
    "ChfYxE0LVil": "Tren",                          # Trencito de madera

    # ── Frutas y verduras ─────────────────────────────────────
    "Ch0lXHZrzJw": "Frutas y verduras",              # JUEGO DE FRUTAS Y VERDURAS

    # ── Biblioteca ────────────────────────────────────────────
    "CipqPsuLybx": "Biblioteca infantil",            # BIBLIOTECA INFANTIL

    # ── Autos ─────────────────────────────────────────────────
    "Cgp8xU6rvmy": "Autos",                         # Dos autos de madera con encastre

    # ── Avion ─────────────────────────────────────────────────
    "C43lahmPYDw": "Avion",                          # Avioncitos de madera

    # ── Animalitos para tejer ─────────────────────────────────
    "C85ZmOMP37T": "Animalitos para tejer",          # Animalitos para tejer (llama y oveja)

    # ── Sin descripcion / genéricos ───────────────────────────
    "CdtcTxGJYKd": "Encastre/Torres multicolor",    # (sin desc, mismo batch que torres multicolor)
    "CdtcdDfJ8z5": "Encastre/Torres multicolor",    # (sin desc, mismo batch que torres multicolor)
    "CdeMsQBppjk": "Jenga",                         # (sin desc, mismo batch que jenga/ta-te-ti)

    # ── Fotos de feria / generales / sorteos -> Varios ────────
    "DA4REmXPKw3": "Varios/Feria",                  # Los domingos en la feria
    "DAMRglvv8Gc": "Varios/Feria",                  # Feliz día de la primavera (feria)
    "CgF773yrTyP": "Varios/Feria",                  # Feria Ateneo
    "Cgo6_rPLkPa": "Varios/Feria",                  # ES HOY!!! Feria
    "C-ljexIvbYL": "Varios/Sorteo",                 # SORTEOOOO
    "C-yZvrwv-bZ": "Varios/Sorteo",                 # Ultimo dia sorteo
    "CsPgL0wu5aY": "Varios/Catalogo general",       # Juguetes y juegos artesanales
    "Ceougfpp8gW": "Varios/Catalogo general",       # Juguetes artesanales de madera (10 fotos)
    "C7XNFj_PjxB": "Varios/Catalogo general",       # (sin desc, fotos varias)
    "C2fn91hRsnq": "Varios/Catalogo general",       # (sin desc, fotos varias)

    # ── Solo hashtags (sin producto claro) ────────────────────
    "DMlDkTjxHtw": "Varios/Catalogo general",       # solo hashtags
    "CtmpTr1PKXY": "Varios/Catalogo general",       # solo hashtags
    "Cgrtp-FLa6r": "Varios/Catalogo general",       # solo hashtags
    "CeWahQkrs5f": "Varios/Catalogo general",       # solo hashtags
}


def main():
    if not os.path.isdir(BASE_DIR):
        print(f"Error: No se encontró la carpeta {BASE_DIR}")
        sys.exit(1)

    # Collect files in root (not in subfolders)
    root_files = [
        f for f in os.listdir(BASE_DIR)
        if os.path.isfile(os.path.join(BASE_DIR, f)) and f.endswith(".jpg")
    ]

    if not root_files:
        print("No hay fotos sueltas para organizar en la raíz.")
        return

    print(f"Fotos sueltas encontradas: {len(root_files)}")
    print()

    moved = 0
    not_found = []

    for filename in sorted(root_files):
        # Extract shortcode from filename: 2022-05-12_20-43-24__CdeMnvMJv19.jpg
        # or 2022-05-18_18-46-25__CdtcAIXpx2N_1.jpg (multi-image)
        parts = filename.split("__")
        if len(parts) < 2:
            not_found.append(filename)
            continue

        shortcode_part = parts[1].replace(".jpg", "")
        # Remove _N suffix for multi-image posts
        shortcode = shortcode_part.rsplit("_", 1)[0] if "_" in shortcode_part and shortcode_part.rsplit("_", 1)[1].isdigit() else shortcode_part

        if shortcode in CATALOG:
            dest_folder = os.path.join(BASE_DIR, CATALOG[shortcode])
            os.makedirs(dest_folder, exist_ok=True)

            src = os.path.join(BASE_DIR, filename)
            dst = os.path.join(dest_folder, filename)

            if os.path.exists(dst):
                print(f"  SKIP (ya existe): {filename} -> {CATALOG[shortcode]}/")
            else:
                shutil.move(src, dst)
                moved += 1
                print(f"  OK: {filename} -> {CATALOG[shortcode]}/")
        else:
            not_found.append(filename)

    print(f"\n{'=' * 50}")
    print(f"Movidas: {moved}")

    if not_found:
        print(f"\nSin catalogar ({len(not_found)}):")
        for f in not_found:
            print(f"  - {f}")

    # Show final structure
    print(f"\nEstructura final:")
    for root, dirs, files in os.walk(BASE_DIR):
        dirs.sort()
        level = root.replace(BASE_DIR, "").count(os.sep)
        indent = "  " * level
        folder_name = os.path.basename(root) or "clamacalma"
        jpg_count = len([f for f in files if f.endswith(".jpg")])
        if jpg_count > 0:
            print(f"{indent}{folder_name}/ ({jpg_count} fotos)")
        elif not files:
            print(f"{indent}{folder_name}/ (vacía)")


if __name__ == "__main__":
    main()
