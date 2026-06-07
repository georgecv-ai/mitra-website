"""
Marketing site build script.

Reads `src/_layout.html`, `src/_config.json`, `shared/nav-config.json`, and
content fragments from `src/en/*.html` and `src/ko/*.html`. Writes assembled
standalone HTML to `en/*.html` and `ko/*.html` at the repo root (where
Cloudflare Pages serves from).

Nav and footer links come from `shared/nav-config.json` (the single source of
truth shared with the Railway app). Per-language page config (fonts, metadata,
legal text) stays in `src/_config.json`.

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

Run:  python build.py [--env production|staging|local]
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
LAYOUT_PATH = SRC / "_layout.html"
LAUNCHER_PATH = SRC / "_launcher.html"
CONFIG_PATH = SRC / "_config.json"
NAV_CONFIG_PATH = ROOT / "shared" / "nav-config.json"


META_BLOCK_RE = re.compile(
    r"^\s*<!--\s*META\s*\n(.*?)\n\s*-->\s*\n", re.DOTALL
)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_nav_config() -> dict:
    return json.loads(NAV_CONFIG_PATH.read_text(encoding="utf-8"))


def load_layout() -> str:
    return LAYOUT_PATH.read_text(encoding="utf-8")


def load_launcher() -> str:
    """Read the Mitra try-Mitra launcher snippet. Returns empty string if file
    is missing (graceful degradation — pages still build without the launcher)."""
    if not LAUNCHER_PATH.exists():
        return ""
    return LAUNCHER_PATH.read_text(encoding="utf-8")


def resolve_vars(text: str, app_base: str, site_base: str, lang: str) -> str:
    """Replace {{app_base}}, {{site_base}}, and {{lang}} in a string."""
    return (text
            .replace("{{app_base}}", app_base)
            .replace("{{site_base}}", site_base)
            .replace("{{lang}}", lang))


def _resolve_link(item: dict, lang: str, app_base: str, site_base: str) -> dict | None:
    """Resolve a single link (label + href) for a given language. Returns None if filtered out."""
    if "lang" in item and lang not in item["lang"]:
        return None
    label = item["label"].get(lang)
    if not label:
        return None
    href = resolve_vars(item["href"], app_base, site_base, lang)
    return {"label": label, "href": href}


def get_nav_items(nav_config: dict, lang: str, app_base: str, site_base: str) -> list[dict]:
    """Filter and resolve nav items for a given language. Items may have children (dropdowns)."""
    items = []
    for item in nav_config["nav_items"]:
        if "lang" in item and lang not in item["lang"]:
            continue
        label = item["label"].get(lang)
        if not label:
            continue

        if "children" in item:
            children = []
            for child in item["children"]:
                resolved = _resolve_link(child, lang, app_base, site_base)
                if resolved:
                    children.append(resolved)
            if children:
                items.append({"label": label, "children": children})
        else:
            href = resolve_vars(item["href"], app_base, site_base, lang)
            items.append({"label": label, "href": href})
    return items


def get_footer_columns(nav_config: dict, lang: str, app_base: str, site_base: str) -> list[dict]:
    """Resolve grouped footer columns for a given language."""
    columns = []
    for column in nav_config.get("footer_columns", []):
        heading = column.get("heading", {}).get(lang, "")
        links = []
        for link in column.get("links", []):
            resolved = _resolve_link(link, lang, app_base, site_base)
            if resolved:
                links.append(resolved)
        if links:
            columns.append({"heading": heading, "links": links})
    return columns


def get_footer_muted(nav_config: dict, lang: str, app_base: str, site_base: str) -> list[dict]:
    """Resolve muted footer items (e.g., Admin)."""
    items = []
    for item in nav_config.get("footer_muted", []):
        resolved = _resolve_link(item, lang, app_base, site_base)
        if resolved:
            items.append(resolved)
    return items


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
    """Render nav_items into the new wp-nav-* dropdown markup. Items with
    `style: cta` render as the pill CTA. Children with `style: sub` render
    with the .sub accent class. Top-level non-dropdown items render as plain
    wp-nav-link pills."""
    out = []
    for item in nav_items:
        if "children" in item:
            child_html = []
            for child in item["children"]:
                child_cls = ' class="sub"' if child.get("style") == "sub" else ''
                child_html.append(
                    f'          <li><a{child_cls} href="{child["href"]}">{child["label"]}</a></li>'
                )
            out.append(
                f'      <li class="wp-nav-dd" data-dd>\n'
                f'        <button class="wp-nav-link" data-dd-trigger>{item["label"]} <span class="caret">▾</span></button>\n'
                f'        <ul class="wp-nav-dd-menu">\n'
                + "\n".join(child_html) + "\n"
                f'        </ul>\n'
                f'      </li>'
            )
        else:
            cls = ' cta' if item.get("style") == "cta" else ''
            out.append(
                f'      <li><a class="wp-nav-link{cls}" href="{item["href"]}">{item["label"]}</a></li>'
            )
    return "\n".join(out)


def render_footer_columns(columns: list[dict]) -> str:
    """Render footer_columns into the new wp-footer-col markup."""
    col_html = []
    for col in columns:
        links_html = "\n".join(
            f'          <li><a href="{link["href"]}">{link["label"]}</a></li>'
            for link in col["links"]
        )
        col_html.append(
            f'      <div class="wp-footer-col">\n'
            f'        <h6>{col["heading"]}</h6>\n'
            f'        <ul>\n'
            f'{links_html}\n'
            f'        </ul>\n'
            f'      </div>'
        )
    return "\n".join(col_html)


def render_footer_admin(muted: list[dict]) -> str:
    """Render footer_muted items (Admin link) as an inline trailing element
    appended to the legal subheading. Returns " · <a>...</a>" with a leading
    separator when content exists, "" when not. The leading separator is
    intentional so the template can concatenate cleanly without producing
    a dangling middot on languages that filter out the link (e.g., KO)."""
    if not muted:
        return ""
    return " &middot; " + " &middot; ".join(
        f'<a href="{item["href"]}">{item["label"]}</a>'
        for item in muted
    )


def assemble_page(layout: str, lang_cfg: dict, lang: str, meta: dict, body: str,
                  nav_items: list[dict], footer_columns: list[dict],
                  footer_muted: list[dict],
                  app_base: str, site_base: str) -> str:
    slug = meta.get("slug", "")
    slug_clean = slug[:-5] if slug.endswith(".html") else slug
    if slug_clean == "index":
        slug_clean = ""
    title = meta.get("title", "Mitra")
    description = meta.get("description", lang_cfg.get("default_description", ""))
    og_description = meta.get("og_description", description)
    twitter_description = meta.get("twitter_description", description)
    og_image = meta.get("og_image", lang_cfg.get("default_og_image", ""))

    current_href = f"/{lang}/{slug}" if slug else f"/{lang}/"
    nav_items_html = render_nav_items(nav_items, current_href)
    footer_columns_html = render_footer_columns(footer_columns)
    footer_admin_html = render_footer_admin(footer_muted)

    en_active = "active" if lang == "en" else ""
    ko_active = "active" if lang == "ko" else ""

    # Language toggle: if a peer-language source file doesn't exist, point that
    # toggle at the peer language home (/en/ or /ko/) instead of /{peer}/{slug}
    # which would 404. Same-language link always points at the current page.
    slug_filename = slug if slug.endswith(".html") else f"{slug}.html"
    peer_en_exists = (SRC / "en" / slug_filename).exists() if slug else True
    peer_ko_exists = (SRC / "ko" / slug_filename).exists() if slug else True
    en_slug = slug if (lang == "en" or peer_en_exists) else ""
    ko_slug = slug if (lang == "ko" or peer_ko_exists) else ""

    toggle = lang_cfg["lang_toggle"]

    if meta.get("raw", "").lower() == "true":
        content_block = body.rstrip()
    else:
        main_class = meta.get("main_class", "container py-4")
        content_block = (
            f'<main class="{main_class}">\n{body.rstrip()}\n</main>'
        )

    # Resolve {{app_base}} in page content (CTA buttons, contact links, etc.)
    content_block = resolve_vars(content_block, app_base, site_base, lang)

    # Mitra launcher: the same Intercom-style try-Mitra component on every page.
    # Resolve {{app_base}} and {{lang}} so it points at the right API.
    launcher_html = resolve_vars(load_launcher(), app_base, site_base, lang)

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
        "{{ en_slug }}": en_slug,
        "{{ ko_slug }}": ko_slug,
        "{{ extra_head }}": meta.get("extra_head", ""),
        "{{ extra_scripts }}": meta.get("extra_scripts", ""),
        "{{ nav_items_html }}": nav_items_html,
        "{{ footer_columns_html }}": footer_columns_html,
        "{{ footer_admin_html }}": footer_admin_html,
        "{{ footer_copyright }}": lang_cfg["footer_copyright"],
        "{{ footer_legal_html }}": lang_cfg["footer_legal_html"],
        "{{ en_active_class }}": en_active,
        "{{ ko_active_class }}": ko_active,
        "{{ content_block }}": content_block,
        "{{ launcher_html }}": launcher_html,
    }

    out = layout
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def detect_env() -> str:
    """Auto-detect environment from CF_PAGES_BRANCH if available."""
    import os
    branch = os.environ.get("CF_PAGES_BRANCH", "")
    if branch == "staging":
        return "staging"
    return "production"


def build(env: str):
    if not SRC.exists():
        print(f"ERROR: {SRC} does not exist", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    nav_config = load_nav_config()
    layout = load_layout()

    env_vars = nav_config["env"].get(env)
    if not env_vars:
        print(f"ERROR: unknown env '{env}'. Valid: {list(nav_config['env'].keys())}", file=sys.stderr)
        sys.exit(1)
    app_base = env_vars["app_base"]
    site_base = env_vars["site_base"]

    print(f"Building for env={env}")
    print(f"  app_base = {app_base}")
    print(f"  site_base = {site_base}")

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

        # Resolve nav/footer from shared config for this language + env
        nav_items = get_nav_items(nav_config, lang, app_base, site_base)
        footer_columns = get_footer_columns(nav_config, lang, app_base, site_base)
        footer_muted = get_footer_muted(nav_config, lang, app_base, site_base)

        out_dir = ROOT / lang
        out_dir.mkdir(parents=True, exist_ok=True)
        for src_file in sorted(src_dir.glob("*.html")):
            if src_file.name.endswith(".head.html"):
                continue
            text = src_file.read_text(encoding="utf-8")
            meta, body = parse_fragment(text)
            if not meta.get("slug"):
                meta["slug"] = src_file.name
            sidecar = src_file.with_suffix(".head.html")
            if sidecar.exists():
                meta["extra_head"] = sidecar.read_text(encoding="utf-8").rstrip()
            assembled = assemble_page(layout, lang_cfg, lang, meta, body,
                                      nav_items, footer_columns, footer_muted,
                                      app_base, site_base)
            out_file = out_dir / src_file.name
            out_file.write_text(assembled, encoding="utf-8")
            total += 1
            print(f"  wrote {out_file.relative_to(ROOT)}")
    print(f"Built {total} pages.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Mitra marketing site")
    parser.add_argument("--env", default=None,
                        help="Target environment (production, staging, local). "
                             "Auto-detects from CF_PAGES_BRANCH if not set.")
    args = parser.parse_args()
    env = args.env or detect_env()
    build(env)
