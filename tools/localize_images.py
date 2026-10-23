#!/usr/bin/env python3
"""Downloads the photos the pages load from the old WordPress site and points
the pages at local copies, so the deployed site doesn't depend on WordPress.

Usage: python3 tools/localize_images.py <site-dir>

Only src="..." attributes are rewritten (social-share meta tags keep absolute
URLs). If a download fails, that image keeps its remote URL and a warning is
printed; the build does not fail.
"""
import hashlib
import os
import pathlib
import re
import sys
import urllib.request

REMOTE = re.compile(r'src="(https://i0\.wp\.com/www\.dareministries\.com/wp-content/uploads/[^"]+)"')


def main(site):
    site = pathlib.Path(site).resolve()
    out_dir = site / "assets" / "img" / "photos"
    out_dir.mkdir(parents=True, exist_ok=True)
    cache = {}

    def fetch(url):
        if url in cache:
            return cache[url]
        path = url.split("?")[0]
        ext = os.path.splitext(path)[1].lower() or ".jpg"
        name = hashlib.sha1(url.encode()).hexdigest()[:12] + ext
        dest = out_dir / name
        try:
            req = urllib.request.Request(url.replace("&amp;", "&"), headers={"User-Agent": "Mozilla/5.0 (site build)"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            if len(data) < 200:
                raise ValueError("response too small")
            dest.write_bytes(data)
            cache[url] = dest
            print(f"ok    {name}  {url}")
        except Exception as exc:  # keep the remote URL
            cache[url] = None
            print(f"WARN  could not download {url}: {exc}")
        return cache[url]

    for html in site.rglob("*.html"):
        text = html.read_text(encoding="utf-8")

        def swap(match):
            local = fetch(match.group(1))
            if not local:
                return match.group(0)
            rel = os.path.relpath(local, html.parent).replace(os.sep, "/")
            return f'src="{rel}"'

        new = REMOTE.sub(swap, text)
        if new != text:
            html.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
