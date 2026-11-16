#!/usr/bin/env python3
"""Vettorializza il logo di Horses of Florence (da assets/img/brand/logo-source.jpg).

    pip install pillow numpy potracer
    python3 tools/logo.py

Il logo è arrivato come PDF con dentro un'immagine JPEG piccola (491×624 px).
Lo script separa l'inchiostro nero (cavallo e scritta) da quello rosso (giglio),
li ingrandisce, li ammorbidisce e li ricalca in curve vettoriali con potrace.
Crea in assets/img/brand/:
  logo.svg         logo completo, colori originali (nero e rosso), scritta verticale
  mark.svg         solo cavallo e giglio, colori originali
  mark-navy.svg    cavallo blu notte e giglio rosso (per fondi chiari)
  mark-ivory.svg   cavallo avorio e giglio rosso (per fondi scuri)
"""
import pathlib

import numpy as np
import potrace
from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets" / "img" / "brand"
SRC = BRAND / "logo-source.jpg"

INK = "#0a0a0a"      # nero del logo
RED = "#df0916"      # rosso del giglio (campionato dal file originale)
NAVY = "#14223d"     # blu del sito
IVORY = "#f7f2e8"    # avorio del sito

SCALE = 8            # ingrandimento prima del ricalco
TEXT_X = 435         # oltre questa colonna c'è la scritta verticale


def trace(mask_float, x0, x1, size):
    """Ricalca un livello (0..1) limitato alle colonne [x0, x1) e restituisce il path SVG."""
    W, H = size
    m = mask_float.copy()
    m[:, :x0] = 0
    m[:, x1:] = 0
    layer = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    layer = layer.resize((W * SCALE, H * SCALE), Image.LANCZOS).filter(ImageFilter.GaussianBlur(SCALE * 0.45))
    ink = np.asarray(layer) > 127
    # potracer considera "pieno" il valore False: va invertito
    plist = potrace.Bitmap(~ink).trace(
        turdsize=60, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
        alphamax=1.05, opticurve=True, opttolerance=0.35,
    )

    def pt(p):
        return f"{p.x / SCALE:.1f} {p.y / SCALE:.1f}"

    d = []
    for curve in plist:
        d.append("M" + pt(curve.start_point))
        for s in curve.segments:
            if s.is_corner:
                d.append("L" + pt(s.c) + "L" + pt(s.end_point))
            else:
                d.append("C" + pt(s.c1) + " " + pt(s.c2) + " " + pt(s.end_point))
        d.append("Z")
    return "".join(d)


def bbox(mask, x0, x1):
    m = mask.copy()
    m[:, :x0] = False
    m[:, x1:] = False
    ys, xs = np.where(m)
    return xs.min(), ys.min(), xs.max(), ys.max()


def svg(viewbox, paths, title):
    body = "\n".join(f'<path fill="{fill}"{rule} d="{d}"/>' for fill, rule, d in paths)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-labelledby="t">'
        f'<title id="t">{title}</title>\n{body}\n</svg>\n'
    )


def main():
    im = Image.open(SRC).convert("RGB")
    a = np.asarray(im).astype(float) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    black = 1 - a.max(axis=2)
    red = np.clip((r - np.maximum(g, b)) * 1.25, 0, 1)
    W, H = im.size

    horse = trace(black, 0, TEXT_X, im.size)
    lily = trace(red, 0, TEXT_X, im.size)
    text = trace(black, TEXT_X, W, im.size)

    pad = 6
    ink_mask = (black > 0.5) | (red > 0.5)
    x0, y0, x1, y1 = bbox(ink_mask, 0, W)
    full_vb = f"{x0 - pad} {y0 - pad} {x1 - x0 + 2 * pad} {y1 - y0 + 2 * pad}"
    x0, y0, x1, y1 = bbox(ink_mask, 0, TEXT_X)
    mark_vb = f"{x0 - pad} {y0 - pad} {x1 - x0 + 2 * pad} {y1 - y0 + 2 * pad}"

    ev = ' fill-rule="evenodd"'
    files = {
        "logo.svg": svg(full_vb, [(RED, "", lily), (INK, ev, horse), (INK, ev, text)], "Horses of Florence"),
        "mark.svg": svg(mark_vb, [(RED, "", lily), (INK, ev, horse)], "Horses of Florence"),
        "mark-navy.svg": svg(mark_vb, [(RED, "", lily), (NAVY, ev, horse)], "Horses of Florence"),
        "mark-ivory.svg": svg(mark_vb, [(RED, "", lily), (IVORY, ev, horse)], "Horses of Florence"),
    }
    for name, content in files.items():
        (BRAND / name).write_text(content, encoding="utf-8")
        print(f"✓ assets/img/brand/{name}  ({len(content) / 1024:.1f} KB)  viewBox {full_vb if name == 'logo.svg' else mark_vb}")


if __name__ == "__main__":
    main()
