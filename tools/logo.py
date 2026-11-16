#!/usr/bin/env python3
"""Vettorializza il logo di Horses of Florence (da assets/img/brand/logo-source.jpg).

    pip install pillow numpy potracer
    python3 tools/logo.py

Il logo è arrivato come PDF con dentro un'immagine JPEG piccola (491×624 px),
girata di 90° per stare in verticale nella pagina A4. Lo script la riporta
nel verso giusto (90° in senso orario: cavallo a testa china, giglio dritto,
scritta orizzontale sotto), poi separa l'inchiostro nero (cavallo e scritta) da quello rosso (giglio),
li ingrandisce, li ammorbidisce e li ricalca in curve vettoriali con potrace.
Crea in assets/img/brand/:
  logo.svg         logo completo, colori originali (nero e rosso), scritta sotto
  mark.svg         solo cavallo e giglio, colori originali
  mark-navy.svg    cavallo blu notte e giglio rosso (per fondi chiari)
  mark-ivory.svg   cavallo avorio e giglio rosso (per fondi scuri)
  favicon.svg      marchio avorio su quadrato blu (icona del sito)
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
TEXT_Y = 436         # sotto questa riga c'è la scritta


def trace(mask_float, y0, y1, size):
    """Ricalca un livello (0..1) limitato alle righe [y0, y1) e restituisce il path SVG."""
    W, H = size
    m = mask_float.copy()
    m[:y0, :] = 0
    m[y1:, :] = 0
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


def bbox(mask, y0, y1):
    m = mask.copy()
    m[:y0, :] = False
    m[y1:, :] = False
    ys, xs = np.where(m)
    return xs.min(), ys.min(), xs.max(), ys.max()


def svg(viewbox, paths, title):
    body = "\n".join(f'<path fill="{fill}"{rule} d="{d}"/>' for fill, rule, d in paths)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-labelledby="t">'
        f'<title id="t">{title}</title>\n{body}\n</svg>\n'
    )


def main():
    # il file estratto dal PDF è girato: 90° in senso orario lo riporta nel verso giusto
    im = Image.open(SRC).convert("RGB").transpose(Image.Transpose.ROTATE_270)
    a = np.asarray(im).astype(float) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    black = 1 - a.max(axis=2)
    red = np.clip((r - np.maximum(g, b)) * 1.25, 0, 1)
    W, H = im.size

    horse = trace(black, 0, TEXT_Y, im.size)
    lily = trace(red, 0, TEXT_Y, im.size)
    text = trace(black, TEXT_Y, H, im.size)

    pad = 6
    ink_mask = (black > 0.5) | (red > 0.5)
    x0, y0, x1, y1 = bbox(ink_mask, 0, H)
    full_vb = f"{x0 - pad} {y0 - pad} {x1 - x0 + 2 * pad} {y1 - y0 + 2 * pad}"
    x0, y0, x1, y1 = bbox(ink_mask, 0, TEXT_Y)
    mark_vb = f"{x0 - pad} {y0 - pad} {x1 - x0 + 2 * pad} {y1 - y0 + 2 * pad}"

    ev = ' fill-rule="evenodd"'
    files = {
        "logo.svg": svg(full_vb, [(RED, "", lily), (INK, ev, horse), (INK, ev, text)], "Horses of Florence"),
        "mark.svg": svg(mark_vb, [(RED, "", lily), (INK, ev, horse)], "Horses of Florence"),
        "mark-navy.svg": svg(mark_vb, [(RED, "", lily), (NAVY, ev, horse)], "Horses of Florence"),
        "mark-ivory.svg": svg(mark_vb, [(RED, "", lily), (IVORY, ev, horse)], "Horses of Florence"),
    }
    # favicon: marchio avorio su quadrato blu con angoli arrotondati
    vx, vy, vw, vh = map(float, mark_vb.split())
    side = max(vw, vh) * 1.18
    fx, fy = vx + vw / 2 - side / 2, vy + vh / 2 - side / 2
    files["favicon.svg"] = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fx:.1f} {fy:.1f} {side:.1f} {side:.1f}">'
        f'<rect x="{fx:.1f}" y="{fy:.1f}" width="{side:.1f}" height="{side:.1f}" rx="{side * 0.2:.1f}" fill="{NAVY}"/>'
        f'<path fill="{RED}" d="{lily}"/><path fill="{IVORY}" fill-rule="evenodd" d="{horse}"/></svg>\n'
    )
    for name, content in files.items():
        (BRAND / name).write_text(content, encoding="utf-8")
        print(f"✓ assets/img/brand/{name}  ({len(content) / 1024:.1f} KB)  viewBox {full_vb if name == 'logo.svg' else mark_vb}")


if __name__ == "__main__":
    main()
