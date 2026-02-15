#!/usr/bin/env python3
"""
Genera thumbnails comprimidos para la grilla del catálogo.
Crea una carpeta thumbs/ paralela a cada categoría.

Uso: python generate_thumbnails.py
"""

import os
from PIL import Image

PHOTOS_DIR = os.path.join(os.path.dirname(__file__), "downloads", "clamacalma")
THUMB_SIZE = (400, 400)
QUALITY = 72


def main():
    count = 0
    for cat in os.listdir(PHOTOS_DIR):
        cat_path = os.path.join(PHOTOS_DIR, cat)
        if not os.path.isdir(cat_path):
            continue

        thumb_dir = os.path.join(cat_path, "thumbs")
        os.makedirs(thumb_dir, exist_ok=True)

        for fname in os.listdir(cat_path):
            if fname == "thumbs":
                continue
            if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue

            src = os.path.join(cat_path, fname)
            # Output always as .jpg for smaller size
            out_name = os.path.splitext(fname)[0] + ".jpg"
            dst = os.path.join(thumb_dir, out_name)

            if os.path.exists(dst):
                continue

            try:
                img = Image.open(src)
                img = img.convert("RGB")
                img.thumbnail(THUMB_SIZE, Image.LANCZOS)
                img.save(dst, "JPEG", quality=QUALITY, optimize=True)
                count += 1
            except Exception as e:
                print(f"  Error: {fname}: {e}")

    print(f"Generated {count} thumbnails")


if __name__ == "__main__":
    main()
