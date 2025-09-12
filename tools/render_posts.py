#!/usr/bin/env python3
# Rend chaque post Markdown (.md avec front-matter) en HTML à côté du .md
import pathlib, re

root = pathlib.Path(__file__).resolve().parents[1]
posts_dir = root / "posts"
posts_dir.mkdir(exist_ok=True)

TEMPLATE = """<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="/styles.css">
<main class="card" style="max-width:820px;margin:20px auto;padding:20px">
{cover}
<h1>{title}</h1><p><small>{date}</small></p>
{body}
</main>
"""

def render_one(md_path: pathlib.Path):
    txt = md_path.read_text(encoding="utf-8")

    # front-matter: title/date/image
    m = re.search(
        r'^---\s*title:\s*"(.*?)"\s*date:\s*"(.*?)"\s*(?:image:\s*"(.*?)")?\s*---\s*(.*)$',
        txt, re.S | re.M
    )
    if not m:
        print("Skip (no front-matter):", md_path.name)
        return

    title, date, image, body = m.groups()
    cover_html = f'<img src="/{image}" alt="cover" style="width:100%;border-radius:14px;margin-bottom:12px">' if image else ""

    # mini markdown → html (titres + listes + sauts de ligne)
    body = re.sub(r'(?m)^## (.*)$', r'<h2>\1</h2>', body)
    body = re.sub(r'(?m)^# (.*)$', r'<h1>\1</h1>', body)
    body = re.sub(r'(?m)^- (.*)$', r'<li>\1</li>', body)
    if "<li>" in body:
        body = "<ul>" + body.replace("<li>", "</ul><li>", 1).replace("</li>", "</li><ul>", 1)
        body = body.replace("</ul></ul>", "</ul>")
    body = body.replace("\n\n", "<br><br>")

    html = TEMPLATE.format(title=title, date=date, body=body, cover=cover_html)
    (posts_dir / (md_path.stem + ".html")).write_text(html, encoding="utf-8")
    print("Rendered:", md_path.name, "->", md_path.stem + ".html")

def main():
    for md in sorted(posts_dir.glob("*.md")):
        render_one(md)

if __name__ == "__main__":
    main()
