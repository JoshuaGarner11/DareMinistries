#!/usr/bin/env python3
"""Builds the static site.

Each file in src/pages/ starts with a JSON header comment:
    <!--{"path": "about/", "title": "About", "nav": "about", "description": "..."}-->
The rest of the file is the page body. This script wraps every body in the
shared layout (src/layout.html), replaces {{root}} with the relative path back
to the site root, and writes <path>/index.html.

Run from the repository root:  python3 tools/build.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
HEADER_RE = re.compile(r"^\s*<!--(\{.*?\})-->\s*", re.S)

NAV_KEYS = ["home", "about", "ministries", "resources", "connect", "give"]


def build_page(src_file, layout):
    text = src_file.read_text(encoding="utf-8")
    match = HEADER_RE.match(text)
    if not match:
        raise SystemExit(f"{src_file.name}: missing JSON header comment")
    meta = json.loads(match.group(1))
    body = text[match.end():]

    path = meta["path"]  # "" for home, "about/" etc. or "404.html"
    if path.endswith(".html"):
        out = ROOT / path
        depth = path.count("/")
    else:
        out = ROOT / path / "index.html"
        depth = path.count("/")
    root = meta.get("root") or ("../" * depth if depth else "./")

    title = meta["title"]
    full_title = "Dare Ministries" if meta.get("nav") == "home" else f"{title} · Dare Ministries"

    html = body.lstrip() if meta.get("standalone") else layout.replace("{{body}}", body)
    html = html.replace("{{title}}", full_title)
    html = html.replace("{{description}}", meta.get("description", ""))
    html = html.replace("{{page_class}}", meta.get("class", ""))
    html = html.replace("{{canonical_path}}", "" if path.endswith(".html") else path)
    for key in NAV_KEYS:
        current = ' aria-current="page"' if meta.get("nav") == key else ""
        html = html.replace("{{current_" + key + "}}", current)
    html = html.replace("{{root}}", root)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out.relative_to(ROOT)


def main():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    for src_file in sorted((SRC / "pages").glob("*.html")):
        print("built", build_page(src_file, layout))


if __name__ == "__main__":
    main()
