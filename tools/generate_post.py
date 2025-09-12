#!/usr/bin/env python3
import os, json, random, datetime, pathlib, re

TOPICS = {
  "hydroponie": [
    "Guide complet pour demarrer avec la NFT (Nutrient Film Technique)",
    "Comparatif substrats: billes d'argile vs laine de roche vs coco",
    "Cycle lumiere: optimiser la croissance des salades"
  ]
}

def slugify(s):
    s = s.lower(); s = re.sub(r'[^a-z0-9]+','-',s).strip('-'); return s[:80]

def ensure_assets(root: pathlib.Path):
    (root/"assets").mkdir(exist_ok=True)
    ph = root/"assets"/"placeholder.jpg"
    if not ph.exists():
        try:
            from PIL import Image, ImageDraw
            img = Image.new("RGB",(1200,630),(20,28,38))
            d = ImageDraw.Draw(img)
            d.rectangle([60,60,1140,570], outline=(124,196,255), width=6)
            d.text((100,280),"NovaGrow", fill=(124,196,255))
            img.save(ph, "JPEG", quality=88)
        except Exception:
            ph.write_bytes(b"")  # fallback
    return str(ph.relative_to(root))

def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    posts = root/"posts"; posts.mkdir(exist_ok=True)
    cover = ensure_assets(root)

    today = datetime.date.today().isoformat()
    title = random.choice(TOPICS["hydroponie"])
    slug = slugify(title)

    md = f"""---
title: "{title}"
date: "{today}"
image: "{cover}"
---

(Cet article a ete genere automatiquement, sans aucune donnee personnelle.)

## {title}

Introduction SEO sur le theme hydroponie.

- Point 1
- Point 2
- Point 3

> Lien vers NovaGrow.
"""
    (posts/f"{today}-{slug}.md").write_text(md, encoding="utf-8")

    idx = root/"posts.json"
    items = []
    if idx.exists():
        try: items = json.loads(idx.read_text(encoding="utf-8"))
        except Exception: items = []
    items = [i for i in items if i.get("file") != f"{today}-{slug}.md"]
    items.append({"file": f"{today}-{slug}.md", "title": title, "date": today, "image": cover})
    idx.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    import pathlib
    main()
