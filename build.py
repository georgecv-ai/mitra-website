"""
One-time build script: renders Mitra portal Jinja2 templates into static HTML.

Usage:
    python build.py

Reads templates and translations from ../tutor/portal/, writes static HTML
into en/ and ko/ directories. After running, the generated HTML files are
the source of truth -- edit them directly.
"""

import json
import os
import sys
from pathlib import Path

# Jinja2 is needed -- install with: pip install jinja2
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

PORTAL_DIR = Path(__file__).parent.parent / "tutor" / "portal"
TEMPLATES_DIR = PORTAL_DIR / "templates"
TRANSLATIONS_FILE = PORTAL_DIR / "translations.json"
OUTPUT_DIR = Path(__file__).parent

PORTAL_URL = "https://app.mitratutor.com"
WWW_URL = "https://www.mitratutor.com"

# Pages to render: (template_name, output_filename, title_key_or_literal)
PAGES = [
    ("index.html", "index.html"),
    ("for_parents.html", "for-parents.html"),
    ("for_students.html", "for-students.html"),
    ("about.html", "about.html"),
    ("privacy.html", "privacy.html"),
    ("terms.html", "terms.html"),
    ("refund.html", "refund.html"),
]

# Korean overrides (these templates exist in ko/ subdirectory)
KO_OVERRIDES = {
    "index.html",
    "for_parents.html",
    "about.html",
    "privacy.html",
    "terms.html",
    "refund.html",
}


def load_translations():
    with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def make_t(translations, lang):
    """Create a translation function for the given language."""
    def t(key):
        entry = translations.get(key, {})
        if isinstance(entry, dict):
            return entry.get(lang, entry.get("en", key))
        return entry
    return t


def build_base_html(lang, translations):
    """Build the static base HTML wrapper for the public site."""
    t = make_t(translations, lang)
    other_lang = "ko" if lang == "en" else "en"
    flag_code = "kr" if lang == "ko" else "en"
    other_flag = "en" if lang == "ko" else "kr"
    lang_label = "English" if lang == "en" else "한국어"
    other_label = "한국어" if lang == "en" else "English"

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{{{ title }}}}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link rel="stylesheet" href="/{lang}/static/style.css" />
  <link rel="icon" type="image/png" href="/{lang}/static/images/mitra-logo-icon-v2_003.png">
  <link rel="canonical" href="{WWW_URL}/{{{{ canonical_path }}}}" />
</head>
<body>

<nav class="navbar navbar-expand-lg">
  <div class="container">
    <a class="navbar-brand" href="/{lang}/"><img src="/{lang}/static/images/mitra-logo-icon-v2_003.png" alt="Mitra" class="navbar-logo">Mitra AI Tutor</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navLinks">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navLinks">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="/{lang}/">{t('home')}</a></li>
        <li class="nav-item"><a class="nav-link" href="/{lang}/for-students.html">{t('for_students')}</a></li>
        <li class="nav-item"><a class="nav-link" href="/{lang}/for-parents.html">{t('for_parents')}</a></li>
        <li class="nav-item"><a class="nav-link" href="{PORTAL_URL}/{lang}/enroll">{t('enroll')}</a></li>
        <li class="nav-item"><a class="nav-link" href="{PORTAL_URL}/{lang}/parent/login">{t('parent_login')}</a></li>
        <!-- Language toggle -->
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            <img src="/{lang}/static/images/flag-{flag_code}.png" width="24" height="16" alt="{lang.upper()}" style="border-radius:2px;">
          </a>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item {"active" if lang == "en" else ""}" href="/en/{{{{ current_page }}}}"><img src="/en/static/images/flag-en.png" width="24" height="16" alt="EN" class="me-2" style="border-radius:2px;"> English</a></li>
            <li><a class="dropdown-item {"active" if lang == "ko" else ""}" href="/ko/{{{{ current_page }}}}"><img src="/ko/static/images/flag-kr.png" width="24" height="16" alt="KR" class="me-2" style="border-radius:2px;"> 한국어</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</nav>

<main class="container py-4">
  {{{{ content }}}}
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-content">
      <div class="footer-brand">
        <img src="/{lang}/static/images/mitra-logo-icon-v2_003.png" alt="Mitra" class="footer-logo-img">
        <span class="footer-logo">Mitra AI Tutor</span>
      </div>
      <div class="footer-nav">
        <a href="/{lang}/for-parents.html">{t('for_parents')}</a>
        <a href="/{lang}/about.html">{t('about')}</a>
        <a href="{PORTAL_URL}/{lang}/enroll">{t('enroll')}</a>
        <a href="mailto:support@mitratutor.com">support@mitratutor.com</a>
        <a href="/{lang}/privacy.html">{t('footer_privacy')}</a>
        <a href="/{lang}/terms.html">{t('footer_terms')}</a>
        <a href="/{lang}/refund.html">{t('footer_refund')}</a>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="mb-1">&copy; 2026 Mitra AI &middot; 미트라 AI</div>
      <div class="small text-muted">
        상호: 미트라 AI &middot; 대표자: NEAL GEORGE CLARY &middot;
        사업자등록번호: 332-06-03605 &middot;
        서울특별시 강남구 영동대로 602, 6층 Z183호 &middot;
        전화: 010-3094-9059 &middot;
        <a href="mailto:support@mitratutor.com" class="text-muted">support@mitratutor.com</a>
      </div>
    </div>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
{{{{ scripts }}}}
</body>
</html>'''


def render_page(env, template_name, lang, translations):
    """Render a single page template, extracting just the content block."""
    t_func = make_t(translations, lang)

    # Check for Korean override
    if lang == "ko" and template_name in KO_OVERRIDES:
        tpl_path = f"ko/{template_name}"
    else:
        tpl_path = template_name

    try:
        tpl = env.get_template(tpl_path)
    except Exception:
        tpl = env.get_template(template_name)

    # Render the full template (it extends base.html, but we'll extract content)
    # Instead, let's render with a custom base that captures blocks
    context = {
        "t": t_func,
        "lang": lang,
        "request": type("Request", (), {"session": type("Session", (), {"get": lambda self, k: None})()})(),
        "flash": None,
        "csrf_token": "",
    }

    rendered = tpl.render(**context)
    return rendered


def extract_content_from_rendered(html):
    """Extract just the main content from a fully rendered page."""
    # The base template wraps content in <main class="container py-4">...</main>
    start_marker = '<main class="container py-4">'
    end_marker = '</main>'

    start = html.find(start_marker)
    if start == -1:
        return html
    start += len(start_marker)
    end = html.find(end_marker, start)
    if end == -1:
        return html[start:]
    return html[start:end].strip()


def extract_scripts_from_rendered(html):
    """Extract the scripts block content (between bootstrap and </body>)."""
    marker = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
    idx = html.find(marker)
    if idx == -1:
        return ""
    after = html[idx + len(marker):]
    end = after.find("</body>")
    if end == -1:
        return ""
    scripts = after[:end].strip()
    return scripts


def extract_title_from_rendered(html):
    """Extract the <title> content."""
    start = html.find("<title>")
    if start == -1:
        return "Mitra"
    start += len("<title>")
    end = html.find("</title>", start)
    if end == -1:
        return "Mitra"
    return html[start:end]


def build_final_page(base_html_template, title, content, scripts, canonical_path, current_page):
    """Assemble the final static HTML page."""
    return (
        base_html_template
        .replace("{{ title }}", title)
        .replace("{{ content }}", content)
        .replace("{{ scripts }}", scripts)
        .replace("{{ canonical_path }}", canonical_path)
        .replace("{{ current_page }}", current_page)
    )


def main():
    if not TEMPLATES_DIR.exists():
        print(f"Error: Templates directory not found at {TEMPLATES_DIR}")
        sys.exit(1)

    translations = load_translations()

    # Set up Jinja2 environment pointing at portal templates
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )
    # Add safe filter
    env.filters["safe"] = lambda x: Markup(x)

    for lang in ("en", "ko"):
        base_html = build_base_html(lang, translations)
        out_dir = OUTPUT_DIR / lang

        for template_name, output_name in PAGES:
            print(f"  Rendering {lang}/{output_name}...")

            rendered = render_page(env, template_name, lang, translations)
            content = extract_content_from_rendered(rendered)
            scripts = extract_scripts_from_rendered(rendered)
            title = extract_title_from_rendered(rendered)

            # Build canonical path
            if output_name == "index.html":
                canonical_path = f"{lang}/"
            else:
                canonical_path = f"{lang}/{output_name}"

            final_html = build_final_page(
                base_html, title, content, scripts, canonical_path, output_name
            )

            out_file = out_dir / output_name
            out_file.write_text(final_html, encoding="utf-8")
            print(f"    -> {out_file}")

    # Create root index.html that redirects based on browser language
    root_index = OUTPUT_DIR / "index.html"
    root_index.write_text(
        '''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Mitra AI Tutor</title>
  <script>
    var lang = (navigator.language || navigator.userLanguage || 'en').substring(0, 2);
    var dest = lang === 'ko' ? '/ko/' : '/en/';
    window.location.replace(dest);
  </script>
  <noscript>
    <meta http-equiv="refresh" content="0; url=/en/" />
  </noscript>
</head>
<body>
  <p>Redirecting... <a href="/en/">English</a> | <a href="/ko/">한국어</a></p>
</body>
</html>
''',
        encoding="utf-8",
    )
    print(f"  -> {root_index}")
    print("Done!")


if __name__ == "__main__":
    main()
