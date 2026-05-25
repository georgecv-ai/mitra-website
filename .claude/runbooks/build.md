# Build system

`build.py` assembles the marketing site from `src/` templates into `ko/`, `en/` at the repo root (where Cloudflare Pages serves from).

## Usage

```bash
uv run python build.py --env production   # prod URLs (www.mitratutor.com)
uv run python build.py --env staging      # staging URLs (workers.dev + staging.mitratutor.com)
uv run python build.py --env local        # localhost URLs (port 8080 site, 8000 app)
uv run python build.py                    # auto-detect from CF_PAGES_BRANCH env var
```

The build is idempotent; safe to re-run.

## What it does

1. Reads `src/_layout.html` (page template)
2. Reads `src/_config.json` (per-language metadata: fonts, OG image, footer legal text)
3. Reads `shared/nav-config.json` (nav items + env URL map)
4. For each `src/{ko,en}/*.html`:
   - Parses `<!-- META ... -->` frontmatter (title, description, slug, optional canonical/og_image/extra_head/extra_scripts)
   - Loads matching `*.head.html` if present (page-specific CSS partial)
   - Resolves `{{app_base}}`, `{{site_base}}`, `{{lang}}` tokens against the env
   - Renders nav and footer with env-resolved links
   - Writes assembled file to `{ko,en}/{slug}` at repo root

## Env tokens

Anywhere in template content or nav config, these are substituted at build:

- `{{app_base}}` — `https://mitratutor.com` (prod) / `https://staging.mitratutor.com` (staging) / `http://localhost:8000` (local)
- `{{site_base}}` — `https://www.mitratutor.com` (prod) / `https://staging-mitra-website.georgeneal.workers.dev` (staging) / `http://localhost:8080` (local)
- `{{lang}}` — `en` or `ko`

Values come from `shared/nav-config.json`'s `env` block.

## Auto env detection

`detect_env()` reads `CF_PAGES_BRANCH`:
- `staging` → staging env
- anything else (including unset) → production env

This means CF Pages naturally builds the right env on push, but local builds default to production unless you pass `--env`.

## Frontmatter schema

```html
<!-- META
title: Page title (required)
description: SEO description (required)
slug: filename.html (required)
canonical: en/filename.html (optional; defaults to "{lang}/{slug}")
og_image: full URL (optional; defaults to language's default_og_image)
extra_head: optional CSS/meta to inject
extra_scripts: optional <script> tags
-->
```

The `slug` is the **only** difference between `src/ko/home-v2.html` and `src/ko/index.html` — they're byte-identical otherwise so the same page lives at both `/ko/` and `/ko/home-v2`.

## Local preview

```bash
uv run python build.py --env local
# then serve the root over HTTP, e.g.:
python -m http.server 8080
# browse http://localhost:8080/ko/
```

Port 8080 is the convention (matches `local.site_base` in nav-config and is registered in [ports.yaml](file://c:/Users/georg/projects/howitworks/ports.yaml)).

## Common gotchas

- **Stale built output.** If you edit `src/` but don't rebuild, the served file at `ko/`/`en/` won't change. Always run `build.py` after editing source.
- **Wrong env at commit.** Committing staging-built files to master means prod will serve staging URLs. Always rebuild with `--env production` before committing to master. See [staging.md](staging.md#build-artifacts-src-vs-root).
- **Editing the built output directly.** Don't. Your changes will be wiped on the next `build.py` run. Edit `src/` only.
- **Nav changes propagate everywhere.** Nav and footer are pulled from `shared/nav-config.json` for *every* page. Adding a nav item touches all 30+ built pages on rebuild.
