"""
One-time script: adds Google Tag Manager snippet to all HTML files in the
marketing site. Idempotent — skips files that already contain the GTM ID.
Skips .bak files. Inserts <head> snippet before </head>, <body> noscript
right after <body>.

Run: python install-gtm.py
"""

from pathlib import Path

GTM_ID = "GTM-5S43DC8L"
ROOT = Path(__file__).parent

HEAD_SNIPPET = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
</head>"""

BODY_SNIPPET = f"""<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""


def process_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if GTM_ID in text:
        return "skip (already has GTM)"
    if "</head>" not in text or "<body>" not in text.lower():
        return "skip (no </head> or <body>)"

    new_text = text.replace("</head>", HEAD_SNIPPET, 1)
    # Match <body> case-insensitively by finding first occurrence
    lower = new_text.lower()
    idx = lower.find("<body>")
    if idx == -1:
        return "skip (no <body> tag after head edit)"
    new_text = new_text[:idx] + BODY_SNIPPET + new_text[idx + len("<body>"):]

    path.write_text(new_text, encoding="utf-8")
    return "updated"


def main():
    targets = []
    for html in ROOT.rglob("*.html"):
        if ".bak" in html.suffixes or html.name.endswith(".bak"):
            continue
        # Skip files in hidden dirs (.git etc)
        if any(p.startswith(".") for p in html.relative_to(ROOT).parts):
            continue
        targets.append(html)

    for path in sorted(targets):
        status = process_file(path)
        rel = path.relative_to(ROOT)
        print(f"{rel}: {status}")


if __name__ == "__main__":
    main()
