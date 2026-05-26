# Staging + Prod Deploy Workflow

Mitra marketing website (`mitra-website` repo, Cloudflare Pages). This runbook covers the full path from a content edit to live production.

## URLs

| Env | Site | App (for cross-links) |
|-----|------|------------------------|
| **Production** | https://www.mitratutor.com | https://mitratutor.com |
| **Staging** | https://staging-mitra-website.georgeneal.workers.dev | https://staging.mitratutor.com |
| **Local** | http://localhost:8080 | http://localhost:8000 |

URLs are defined in `shared/nav-config.json` under the `env` block. `build.py` substitutes `{{app_base}}`, `{{site_base}}`, `{{lang}}` tokens at build time. See [build.md](build.md) for build internals.

## Branch model

- **`master`** = production. Auto-deploys to https://www.mitratutor.com on push.
- **`staging`** = staging preview. Auto-deploys to https://staging-mitra-website.georgeneal.workers.dev on push. Cloudflare sets `CF_PAGES_BRANCH=staging`, `build.py` auto-detects and uses staging URLs.
- **`feat/*`** = working branches.

## CRITICAL: mitra-website is NOT tutor

The `tutor/.claude/runbooks/staging.md` rule **"never merge staging into master"** does NOT apply here.

- **Why it applies to tutor:** the tutor app has staging-only commits (seed scripts, demo fixtures, fake-data dashboards) that must never reach production. There's even a `pre-merge-commit` hook enforcing it.
- **Why it does NOT apply to mitra-website:** the marketing site is pure static content. There are no "staging-only" commits in the structural sense — every commit aims at production eventually.

The mitra-website pattern across master's history is direct merges: `Merge staging into master: KO homepage rebuild`, `Merge staging into master: NE Georgia partner program`, etc. That's the established convention here.

That said, **don't merge wholesale by default**. See the next section.

## Standard workflow: feature branch off master

For small content edits where master is current:

```bash
# 1. Branch off master
git checkout master && git pull
git checkout -b feat/ko-some-edit

# 2. Edit src/{ko,en}/*.html (NOT the root /ko/, /en/ files — those are built outputs)

# 3. Build for staging and commit src/ AND built output together
uv run python build.py --env staging
git add src/ko/some-file.html ko/some-file.html
git commit -m "ko/some-file: short description"

# 4. Merge feature into staging, push to deploy staging preview
git checkout staging && git pull
git merge --no-ff feat/ko-some-edit
git push origin staging
# Verify at https://staging-mitra-website.georgeneal.workers.dev/...

# 5. After approval: cherry-pick onto a fresh branch off master, rebuild for prod, merge
git checkout master && git pull
git checkout -b feat/ko-some-edit-prod
git cherry-pick <feat-commit-shas>
uv run python build.py --env production   # swaps staging URLs in built files back to prod
git add -u
git commit -m "Rebuild for production env"  # only if rebuild produced changes
git checkout master
git merge --no-ff feat/ko-some-edit-prod -m "Merge feat/ko-some-edit-prod"
git push origin master
```

## When staging has accumulated commits you don't want in prod

This is the trap. Staging can carry months of in-progress work (English drafts, layout iterations, prototypes) that aren't approved for prod. **In that case, do NOT `git merge staging` into master** — even though the commit history shows past bulk merges.

The signal: run `git log master..staging --oneline` and look at what's there. If you see anything you can't explain or anything George hasn't explicitly approved for prod, use the cherry-pick path:

```bash
git checkout master && git pull
git checkout -b feat/prod-promote-XYZ
git cherry-pick <only-the-approved-commits>
uv run python build.py --env production
# only commit if rebuild changed anything
git checkout master
git merge --no-ff feat/prod-promote-XYZ
git push origin master
```

**2026-05-25 incident:** Tried `git merge staging` into master after George approved KO popup changes. Conflict resolution would have dragged unrelated English `for-parents-v2` drafts and English `home-v2` translation into prod. George caught it: "DO NOT push the english changes into production." Cherry-pick approach used instead. The lesson: never assume staging is shippable end-to-end just because *some* of staging is shippable.

## Build artifacts: src/ vs root

The repo commits **both** the source (`src/ko/*.html`, `src/en/*.html`) **and** the built output (`ko/*.html`, `en/*.html`). Cloudflare Pages serves the root files directly.

- **Always rebuild before committing.** Stale built files are the #1 source of "I edited the page but nothing changed" confusion.
- **Build env matters.** `--env staging` writes staging URLs (`staging.mitratutor.com`, `workers.dev`) into the output. `--env production` writes prod URLs. If you commit staging-built files to master, prod will have staging URLs.
- **After cherry-picking commits from staging onto master, always run `python build.py --env production` and check `git status`.** Even if the cherry-pick auto-resolved cleanly, the built files may contain staging URLs that need a prod rebuild.

## File pair: home-v2.html and index.html

On both master and staging, `src/ko/home-v2.html` and `src/ko/index.html` are byte-identical except for the `slug:` line. The `home-v2.html` preview path is kept alive intentionally — when editing the homepage, edit both files in lockstep. Same applies to `src/ko/home-v2.head.html` and `src/ko/index.head.html`.

```bash
# Quick check they're in sync (modulo slug line):
diff <(grep -v '^slug:' src/ko/home-v2.html) <(grep -v '^slug:' src/ko/index.html)
```

## Cloudflare Pages auto-deploy

CF Pages watches the GitHub repo and rebuilds on every push.

- Push to `master` → builds + deploys to `www.mitratutor.com`
- Push to `staging` → builds + deploys to `staging-mitra-website.georgeneal.workers.dev`
- Build command in CF dashboard runs `python build.py` (env auto-detected from `CF_PAGES_BRANCH`)
- Deploy typically completes in 1-2 minutes

## Verification checklist after prod push

- [ ] `https://www.mitratutor.com/ko/` loads and shows your changes
- [ ] No staging URLs in the page source (`view-source:` and search for `workers.dev` / `staging.mitratutor`)
- [ ] If you changed the homepage, verify both `/ko/` and `/ko/home-v2` look right (the byte-identical pair)
- [ ] If you changed nav/footer, verify on at least 3 different pages

## History

- **2026-05-25:** Runbook created after George corrected the assistant on a staging→master merge attempt that would have dragged English drafts into prod. Cherry-pick + rebuild for prod env established as the safe pattern when staging has unrelated WIP.
