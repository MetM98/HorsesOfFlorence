#!/usr/bin/env python3
"""Genera il sito statico di Horses of Florence.

    pip install jinja2      (una volta sola)
    python3 build.py

Legge  src/*.html (template) + src/site.json + src/content/<lingua>.json
       + src/content/legal/<lingua>.json + assets/img/photos/credits.json
e scrive per ogni lingua la home, la pagina privacy/ e la proposta natura/:
index.html, privacy/, natura/ (IT) · en/index.html, en/privacy/, en/natura/ (EN).
I file generati sono HTML/CSS puri: si pubblicano così come sono (GitHub Pages).
"""
import json
import pathlib
import re
import sys

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import escape

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
IMG = ROOT / "assets" / "img"

# Pagine generate per ogni lingua: (nome, sottocartella, template)
PAGES = [
    ("home", "", "home.html"),
    ("privacy", "privacy/", "legal.html"),
    # proposta alternativa della home: «una giornata nel Chianti», dall'alba alla notte
    ("natura", "natura/", "natura.html"),
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
            home = "" if page in ("home", "natura") else root + lang["path"]
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
