#!/usr/bin/env python3
"""Scarica e ottimizza le foto del sito (Unsplash) a partire da assets/img/photos/credits.json.

    pip install pillow
    python3 tools/photos.py            # crea solo le varianti mancanti
    python3 tools/photos.py --force    # le rigenera tutte

Per ogni foto con `image_id` (es. "photo-1566251037378-5e04e3bec343") crea
<slug>-640.webp, <slug>-1024.webp, <slug>-1600.webp (e <slug>-2400.webp se "hero": true)
e aggiorna in credits.json larghezza, altezza e colore dominante.
Le foto senza `image_id` (es. quelle vostre) vanno messe a mano nella cartella, con gli stessi nomi.

Per usare foto vostre al posto di quelle di Unsplash: salvate il JPG in tools/originals/<slug>.jpg
e lanciate lo script con --force: verrà usato quello invece di scaricarlo.
"""
import io
import json
import pathlib
import sys
import urllib.request

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "assets" / "img" / "photos"
ORIGINALS = ROOT / "tools" / "originals"
CREDITS = PHOTOS / "credits.json"
WIDTHS = (640, 1024, 1600)


def fetch(item):
    local = ORIGINALS / f"{item['slug']}.jpg"
    if local.exists():
        return Image.open(local)
    url = f"https://images.unsplash.com/{item['image_id']}?w=2400&q=85&fm=jpg"
    with urllib.request.urlopen(url, timeout=60) as r:
        return Image.open(io.BytesIO(r.read()))


def dominant(im):
    small = im.convert("RGB").resize((1, 1), Image.LANCZOS)
    return "#%02x%02x%02x" % small.getpixel((0, 0))


def main():
    force = "--force" in sys.argv
    items = json.loads(CREDITS.read_text(encoding="utf-8"))
    for item in items:
        slug = item["slug"]
        widths = WIDTHS + ((2400,) if item.get("hero") else ())
        targets = [PHOTOS / f"{slug}-{w}.webp" for w in widths]
        if not force and all(t.exists() for t in targets):
            continue
        if not item.get("image_id") and not (ORIGINALS / f"{slug}.jpg").exists():
            print(f"· {slug}: nessuna sorgente, salto")
            continue
        im = ImageOps.exif_transpose(fetch(item)).convert("RGB")
        if item.get("crop"):  # [x0, y0, x1, y1] in frazioni dell'immagine
            x0, y0, x1, y1 = item["crop"]
            W, H = im.size
            im = im.crop((round(x0 * W), round(y0 * H), round(x1 * W), round(y1 * H)))
        for w, target in zip(widths, targets):
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(target, "WEBP", quality=80 if w < 2400 else 76, method=6)
        item["width_1600"] = 1600
        item["height_1600"] = round(im.height * 1600 / im.width)
        item["dominant"] = dominant(im)
        print(f"✓ {slug}  {item['width_1600']}×{item['height_1600']}  {item['dominant']}")
    CREDITS.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
