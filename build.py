#!/usr/bin/env python3
"""Genera il sito statico di Horses of Florence.

    pip install jinja2      (una volta sola)
    python3 build.py

Legge  src/*.html (template) + src/site.json + src/content/<lingua>.json
       + src/content/legal/<lingua>.json + assets/img/photos/credits.json
e scrive per ogni lingua la home e la pagina privacy/:
index.html, privacy/ (IT) · en/index.html, en/privacy/ (EN).
I file generati sono HTML/CSS puri: si pubblicano così come sono (GitHub Pages).
"""
import json
import math
import pathlib
import re
import sys

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import escape

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
IMG = ROOT / "assets" / "img"

# ---------------------------------------------------------------------------
# Disegni a inchiostro calcolati (coordinate SVG). Deterministici: stesso
# risultato a ogni build.
# ---------------------------------------------------------------------------

def _fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _smooth_closed(pts):
    """Curva chiusa e morbida (Catmull-Rom → Bézier) che passa per i punti."""
    n = len(pts)
    d = [f"M{_fmt(pts[0][0])} {_fmt(pts[0][1])}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{_fmt(c1[0])} {_fmt(c1[1])} {_fmt(c2[0])} {_fmt(c2[1])} {_fmt(p2[0])} {_fmt(p2[1])}")
    return "".join(d) + "Z"


def _smooth_open(pts):
    d = [f"M{_fmt(pts[0][0])} {_fmt(pts[0][1])}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{_fmt(c1[0])} {_fmt(c1[1])} {_fmt(c2[0])} {_fmt(c2[1])} {_fmt(p2[0])} {_fmt(p2[1])}")
    return "".join(d)


def tree_rings(n=13, size=1000):
    """Anelli di un tronco, irregolari come nel legno vero: dall'esterno verso il centro."""
    c = size / 2
    rmax, rmin = size * 0.47, size * 0.035
    rings = []
    for k in range(n):
        f = (n - 1 - k) / (n - 1)
        r = rmin + (rmax - rmin) * f ** 0.82
        ph = k * 1.73
        ox, oy = c + f * 16, c - f * 9
        pts = []
        for i in range(84):
            th = 2 * math.pi * i / 84
            w = (1 + 0.017 * math.sin(3 * th + ph) + 0.011 * math.sin(5 * th + ph * 1.3)
                 + 0.006 * math.sin(11 * th + ph * .6) + 0.022 * f * math.sin(2 * th + .5))
            pts.append((ox + r * w * math.cos(th), oy + r * w * math.sin(th)))
        rings.append(_smooth_closed(pts))
    return rings


def olive_branch():
    """Ramo d'olivo: gambo, foglie lanceolate alternate, qualche oliva. viewBox 0 0 520 300."""
    P = [(24, 262), (170, 214), (318, 128), (496, 54)]

    def bez(t):
        u = 1 - t
        return tuple(u**3 * P[0][j] + 3 * u * u * t * P[1][j] + 3 * u * t * t * P[2][j] + t**3 * P[3][j] for j in range(2))

    def tan(t):
        u = 1 - t
        v = [3 * u * u * (P[1][j] - P[0][j]) + 6 * u * t * (P[2][j] - P[1][j]) + 3 * t * t * (P[3][j] - P[2][j]) for j in range(2)]
        a = math.atan2(v[1], v[0])
        return a

    stem = f"M{P[0][0]} {P[0][1]}C{P[1][0]} {P[1][1]} {P[2][0]} {P[2][1]} {P[3][0]} {P[3][1]}"
    leaves, olives = [], []
    ts = [0.1, 0.17, 0.25, 0.32, 0.41, 0.48, 0.57, 0.64, 0.72, 0.79, 0.87, 0.93]
    for i, t in enumerate(ts):
        bx, by = bez(t)
        a = tan(t) + (0.78 if i % 2 else -0.7)
        length = 78 * (1 - 0.38 * t)
        width = length * 0.19
        tx, ty = bx + length * math.cos(a), by + length * math.sin(a)
        mx, my = (bx + tx) / 2, (by + ty) / 2
        nx, ny = -math.sin(a), math.cos(a)
        leaves.append(
            f"M{_fmt(bx)} {_fmt(by)}Q{_fmt(mx + nx * width)} {_fmt(my + ny * width)} {_fmt(tx)} {_fmt(ty)}"
            f"Q{_fmt(mx - nx * width)} {_fmt(my - ny * width)} {_fmt(bx)} {_fmt(by)}Z"
            f"M{_fmt(bx)} {_fmt(by)}L{_fmt(bx + (tx - bx) * .82)} {_fmt(by + (ty - by) * .82)}"
        )
    ex, ey = P[3]
    a = tan(1.0)
    leaves.append(
        f"M{ex} {ey}Q{_fmt(ex + 30 * math.cos(a) - 8 * math.sin(a))} {_fmt(ey + 30 * math.sin(a) + 8 * math.cos(a))} "
        f"{_fmt(ex + 58 * math.cos(a))} {_fmt(ey + 58 * math.sin(a))}"
        f"Q{_fmt(ex + 30 * math.cos(a) + 8 * math.sin(a))} {_fmt(ey + 30 * math.sin(a) - 8 * math.cos(a))} {ex} {ey}Z"
    )
    for t, dx, dy in ((0.36, 6, 30), (0.52, -4, 34), (0.68, 8, 28)):
        bx, by = bez(t)
        cx, cy = bx + dx, by + dy
        olives.append({"stalk": f"M{_fmt(bx)} {_fmt(by)}Q{_fmt(bx + dx * .2)} {_fmt(by + dy * .5)} {_fmt(cx)} {_fmt(cy - 11)}",
                       "cx": _fmt(cx), "cy": _fmt(cy), "rot": _fmt(dx * 2)})
    return {"stem": stem, "leaves": leaves, "olives": olives}


def vineyard():
    """Filari in prospettiva che salgono verso la collina. viewBox 0 0 1200 420."""
    vx, vy = 820, 96
    rows = []
    for i in range(12):
        x0 = -120 + i * 118
        # il filare si ferma sulla linea della collina
        t_end = 0.8 - abs(i - 6) * 0.018
        x1, y1 = x0 + (vx - x0) * t_end, 420 + (vy - 420) * t_end
        posts = []
        for k in range(1, 7):
            t = (k / 7) ** 1.35 * t_end
            px, py = x0 + (vx - x0) * t, 420 + (vy - 420) * t
            h = 26 * (1 - t / t_end * 0.85)
            posts.append(f"M{_fmt(px)} {_fmt(py)}v{_fmt(-h)}")
        rows.append({"line": f"M{x0} 420L{_fmt(x1)} {_fmt(y1)}", "posts": "".join(posts)})
    hill = _smooth_open([(-20, 190), (200, 160), (420, 150), (640, 128), (860, 112), (1060, 124), (1220, 140)])
    return {"rows": rows, "hill": hill}


def river(width=4200, height=220):
    """Il torrente Pesa che attraversa la striscia delle esperienze."""
    pts = []
    n = 28
    for i in range(n + 1):
        x = width * i / n
        y = height * (0.55 + 0.22 * math.sin(i * 0.9) + 0.08 * math.sin(i * 2.3 + 1))
        pts.append((x, y))
    return _smooth_open(pts)


def words(text):
    """Divide un testo in parole per le comparse legate allo scroll."""
    return text.split()


# Pagine generate per ogni lingua: (nome, sottocartella, template)
PAGES = [
    ("home", "", "home.html"),
    ("privacy", "privacy/", "legal.html"),
]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_photos():
    """Mappa slug -> metadati foto (da assets/img/photos/credits.json), solo se i file esistono."""
    path = IMG / "photos" / "credits.json"
    if not path.exists():
        return {}
    photos = {}
    for item in load(path):
        slug = item["slug"]
        if not (IMG / "photos" / f"{slug}-1024.webp").exists():
            continue
        item["has_2400"] = (IMG / "photos" / f"{slug}-2400.webp").exists()
        photos[slug] = item
    return photos


def load_sprite():
    """Mappa id -> <symbol> dallo sprite delle icone."""
    path = IMG / "icons.svg"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    return {
        m.group(1): m.group(0)
        for m in re.finditer(r"<symbol\b[^>]*\bid=\"([^\"]+)\"[^>]*>.*?</symbol>", text, re.S)
    }


def format_date(iso):
    y, m, d = iso.split("-")
    return f"{d}/{m}/{y}"


def fill_tokens(value, tokens, todo):
    """Sostituisce %%token%% nei testi legali con i dati di src/site.json (o un segnaposto evidenziato)."""
    if isinstance(value, dict):
        return {k: fill_tokens(v, tokens, todo) for k, v in value.items()}
    if isinstance(value, list):
        return [fill_tokens(v, tokens, todo) for v in value]
    if not isinstance(value, str):
        return value

    def repl(match):
        key = match.group(1)
        if key not in tokens:
            return match.group(0)
        val = tokens[key]
        return str(escape(val)) if val else f'<mark class="todo">[{escape(todo)}]</mark>'

    text = re.sub(r"%%(\w+)%%", repl, value)
    # un mailto senza indirizzo non serve: resta solo il segnaposto
    return re.sub(r'<a href="mailto:<mark class="todo">[^<]*</mark>">(<mark class="todo">[^<]*</mark>)</a>', r"\1", text)


def main():
    site = load(SRC / "site.json")
    photos = load_photos()
    sprite = load_sprite()
    env = Environment(
        loader=FileSystemLoader(str(SRC)),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    )
    env.globals.update(tree_rings=tree_rings, olive_branch=olive_branch, vineyard=vineyard, river=river)
    env.filters["words"] = words
    owner = site.get("owner", {})
    updated = format_date(site.get("legal_updated", "2026-01-01"))

    ok = True
    for lang in site["languages"]:
        code = lang["code"]
        content_path = SRC / "content" / f"{code}.json"
        legal_path = SRC / "content" / "legal" / f"{code}.json"
        if not content_path.exists() or not legal_path.exists():
            print(f"! mancano i contenuti per {code}, salto")
            continue
        t = load(content_path)
        tokens = {
            "owner_name": owner.get("name", ""),
            "owner_address": owner.get("address", ""),
            "owner_tax_id": owner.get("vat") or owner.get("tax_id", ""),
            "email": site.get("email", ""),
            "site_url": site.get("base_url", ""),
            "updated": updated,
        }
        legal = load(legal_path)
        lg = fill_tokens(legal, tokens, legal["labels"]["todo"])

        for page, page_path, template_name in PAGES:
            out_rel = lang["path"] + page_path
            root = "../" * out_rel.count("/")
            home = "" if page == "home" else root + lang["path"]
            html = env.get_template(template_name).render(
                t=t, lg=lg, site=site, lang=lang, root=root, home=home,
                page=page, page_path=page_path, photos=photos, updated=updated,
            )

            used = set(re.findall(r'href="#(i-[\w-]+)"', html))
            missing = sorted(used - sprite.keys())
            if missing:
                ok = False
                print(f"! {code}/{page}: icone mancanti nello sprite: {', '.join(missing)}")
            symbols = "".join(sprite[i] for i in sorted(used) if i in sprite)
            sprite_html = (
                '<svg xmlns="http://www.w3.org/2000/svg" class="sprite" aria-hidden="true" focusable="false">'
                f"{symbols}</svg>"
            )
            html = html.replace("<!--ICON_SPRITE-->", sprite_html)
            html = re.sub(r"\n\s*\n+", "\n", html)

            out = ROOT / out_rel / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            print(f"✓ {out.relative_to(ROOT)}  ({len(html.encode('utf-8')) / 1024:.1f} KB, {len(used)} icone)")

    if not photos:
        print("· nessuna foto trovata")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
