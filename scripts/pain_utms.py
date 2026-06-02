"""
UTM URL builder for pain landing pages.

Reads data/pains.json so it can validate slugs and tell you which pains exist.
Prints ready-to-paste share URLs for every supported platform — same landing
page, different attribution.

Usage:
  python scripts/pain_utms.py parent-stuck
  python scripts/pain_utms.py parent-stuck v2
  python scripts/pain_utms.py parent-stuck v1 --env staging
  python scripts/pain_utms.py --list
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "pains.json"

SITES = {
    "production": "https://www.mitratutor.com",
    "staging": "https://staging-mitra-website.georgeneal.workers.dev",
}

# (source, medium) pairs. Source = where the click came from (utm_source);
# medium = the bucket Plausible/GA4 group it into (utm_medium).
PLATFORMS = [
    ("facebook", "social"),
    ("instagram", "social"),
    ("linkedin", "social"),
    ("threads", "social"),
    ("x", "social"),
    ("youtube", "social"),
    ("kakao", "messenger"),
    ("whatsapp", "messenger"),
    ("telegram", "messenger"),
    ("email", "email"),
]


def build_url(site: str, slug: str, source: str, medium: str, creative: str) -> str:
    params = {
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": f"pain-{slug}",
        "utm_content": creative,
    }
    return f"{site}/en/pain-{slug}?{urlencode(params)}"


def main():
    parser = argparse.ArgumentParser(description="Build UTM share URLs for a pain landing page")
    parser.add_argument("slug", nargs="?", help="Pain slug (e.g. parent-stuck)")
    parser.add_argument("creative", nargs="?", default="v1",
                        help="Creative variant id (utm_content) — default 'v1'. Use this to A/B "
                             "the same pain on the same platform with different copy or art.")
    parser.add_argument("--env", choices=("production", "staging"), default="production",
                        help="Which site base to point at — default production")
    parser.add_argument("--list", action="store_true", help="List slugs in the manifest and exit")
    args = parser.parse_args()

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    pains = data["pains"]
    slugs = {p["slug"] for p in pains}

    if args.list or not args.slug:
        print(f"{len(pains)} pain(s) in manifest:")
        for p in pains:
            print(f"  {p['slug']:<24}  {p['meta']['title']}")
        if not args.slug:
            print("\nusage: python scripts/pain_utms.py <slug> [creative-id] [--env staging|production]")
        return

    if args.slug not in slugs:
        print(f"ERROR: slug '{args.slug}' not in manifest. Run with --list to see options.", file=sys.stderr)
        sys.exit(1)

    site = SITES[args.env]
    print(f"# Pain landing UTMs — slug='{args.slug}' creative='{args.creative}' env={args.env}")
    print(f"# Base: {site}/en/pain-{args.slug}")
    print()
    for source, medium in PLATFORMS:
        url = build_url(site, args.slug, source, medium, args.creative)
        print(f"  {source:<10} ({medium:<9})  {url}")


if __name__ == "__main__":
    main()
