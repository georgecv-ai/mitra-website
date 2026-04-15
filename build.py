"""
Marketing site build script.

Reads `src/_layout.html`, `src/_config.json`, and content fragments from
`src/en/*.html` and `src/ko/*.html`. Writes assembled standalone HTML to
`en/*.html` and `ko/*.html` at the repo root (where Cloudflare Pages serves
from).

Each content fragment may have an HTML comment "frontmatter" at the top:

    <!-- META
    title: Mitra — About
    description: Mitra AI Tutor was built for students who learn differently.
    slug: about.html
    canonical: en/about.html
    -->
    <div class="about-page">
      ...
    </div>

Required keys: title, description, slug.
canonical defaults to "{lang}/{slug}".
og_image defaults to the language's default_og_image.
extra_head and extra_scripts are optional.

Run:  python build.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
LAYOUT_PATH = SRC / "_layout.html"
CONFIG_PATH = SRC / "_config.json"


META_BLOCK_RE = re.compile(
    r"^\s*<!--\s*META\s*\n(.*?)\n\s*-->\s*\n", re.DOTALL
)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_layout() -> str:
    return LAYOUT_PATH.read_text(encoding="utf-8")


def parse_fragment(text: str) -> tuple[dict, str]:
    """Split a content file into (metadata dict, body html)."""
    meta = {}
    m = META_BLOCK_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        body = text[m.end():]
    else:
        body = text
    return meta, body


def render_nav_items(nav_items: list[dict], current_href: str) -> str:
    out = []
    for item in nav_items:
        active = ' active' if current_href == item["href"] else ''
        out.append(
            f'        <li class="nav-item">'
            f'<a class="nav-link{active}" href="{item["href"]}">'
            f'{item["label"]}</a></li>'
        )
    return "\n".join(out)


def render_footer_links(footer_links: list[dict]) -> str:
    out = []
    for link in footer_links:
        cls = ' class="text-muted"' if link.get("muted") else ''
        out.append(f'        <a href="{link["href"]}"{cls}>{link["label"]}</a>')
    return "\n".join(out)


def assemble_page(layout: str, lang_cfg: dict, lang: str, meta: dict, body: str) -> str:
    slug = meta.get("slug", "")
    # slug_clean strips the trailing .html so canonical/hreflang use the
    # CF-Pages-friendly clean URL form (e.g. /en/about not /en/about.html).
    slug_clean = slug[:-5] if slug.endswith(".html") else slug
    if slug_clean == "index":
        slug_clean = ""  # /en/ not /en/index
    title = meta.get("title", "Mitra")
    description = meta.get("description", lang_cfg.get("default_description", ""))
    og_description = meta.get("og_description", description)
    twitter_description = meta.get("twitter_description", description)
    og_image = meta.get("og_image", lang_cfg.get("default_og_image", ""))

    current_href = f"/{lang}/{slug}" if slug else f"/{lang}/"
    nav_items_html = render_nav_items(lang_cfg["nav_items"], current_href)
    footer_links_html = render_footer_links(lang_cfg["footer_links"])

    en_active = "active" if lang == "en" else ""
    ko_active = "active" if lang == "ko" else ""

    toggle = lang_cfg["lang_toggle"]

    # Normal pages get wrapped in <main class="container py-4">.
    # Pages with `raw: true` in META supply their own structure between nav
    # and footer (e.g. a hero banner before <main>, or a custom main_class).
    if meta.get("raw", "").lower() == "true":
        content_block = body.rstrip()
    else:
        main_class = meta.get("main_class", "container py-4")
        content_block = (
            f'<main class="{main_class}">\n{body.rstrip()}\n</main>'
        )

    replacements = {
        "{{ html_lang }}": lang_cfg["html_lang"],
        "{{ fonts_url }}": lang_cfg.get("fonts_url", ""),
        "{{ title }}": title,
        "{{ description }}": description,
        "{{ og_description }}": og_description,
        "{{ twitter_description }}": twitter_description,
        "{{ og_image }}": og_image,
        "{{ slug }}": slug,
        "{{ slug_clean }}": slug_clean,
        "{{ extra_head }}": meta.get("extra_head", ""),
        "{{ extra_scripts }}": meta.get("extra_scripts", ""),
        "{{ nav_items_html }}": nav_items_html,
        "{{ footer_links_html }}": footer_links_html,
        "{{ footer_copyright }}": lang_cfg["footer_copyright"],
        "{{ footer_legal_html }}": lang_cfg["footer_legal_html"],
        "{{ lang_toggle_current_flag }}": toggle["current_flag"],
        "{{ lang_toggle_current_alt }}": toggle["current_alt"],
        "{{ en_active_class }}": en_active,
        "{{ ko_active_class }}": ko_active,
        "{{ content_block }}": content_block,
    }

    out = layout
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def build():
    if not SRC.exists():
        print(f"ERROR: {SRC} does not exist", file=sys.stderr)
        sys.exit(1)
    config = load_config()
    layout = load_layout()

    total = 0
    for lang in ("en", "ko"):
        lang_cfg = config.get(lang)
        if not lang_cfg:
            print(f"WARNING: no config for lang={lang}, skipping")
            continue
        src_dir = SRC / lang
        if not src_dir.exists():
            print(f"WARNING: {src_dir} does not exist, skipping")
            continue
        out_dir = ROOT / lang
        out_dir.mkdir(parents=True, exist_ok=True)
        for src_file in sorted(src_dir.glob("*.html")):
            # Skip sidecar .head.html files
            if src_file.name.endswith(".head.html"):
                continue
            text = src_file.read_text(encoding="utf-8")
            meta, body = parse_fragment(text)
            if not meta.get("slug"):
                meta["slug"] = src_file.name
            # Look for sidecar extra_head file alongside the fragment
            sidecar = src_file.with_suffix(".head.html")
            if sidecar.exists():
                meta["extra_head"] = sidecar.read_text(encoding="utf-8").rstrip()
            assembled = assemble_page(layout, lang_cfg, lang, meta, body)
            out_file = out_dir / src_file.name
            out_file.write_text(assembled, encoding="utf-8")
            total += 1
            print(f"  wrote {out_file.relative_to(ROOT)}")
    print(f"Built {total} pages.")


if __name__ == "__main__":
    build()
