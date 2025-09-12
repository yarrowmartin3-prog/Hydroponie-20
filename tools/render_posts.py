#!/usr/bin/env python3
import pathlib, re

root = pathlib.Path(__file__).resolve().parents[1]
posts = list((root/"posts").glob("*.md"))
out = root/"posts"

TEMPLATE = """<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="/styles.css">
<main class="card" style="max-width:820px;margin:20px auto;padding:20px">
{cover}
<h1>{title}</h1><p><small>{date}</small></p>
{body}
</main>
"""

for md in posts:
    txt = md.read_text(encoding="utf-8")
    m = re.search(r'^---\\s*title:\\s*"(.*?)"\\s*date:\\s*"(.*?)"\\s*image:\\s*"(.*?)"\\s*---\\s*(.*)$', txt, re.S|re.M)
    if not m: 
        print("Skip:", md.name); 
        continue
    title, date, image, body = m.groups()
    cover_html = f'<img src="/{image}" alt="cover" style="width:100%;border-radius:14px;margin-bottom:12px">'
    body = body.replace("\\n\\n", "<br><br>")
    html = TEMPLATE.format(title=title, date=date, body=body, cover=cover_html)
    (out/f"{md.stem}.html").write_text(html, encoding="utf-8")

print(f"Rendered {len(posts)} posts")
