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

## Guardrails (active as of 2026-05-26)

The same `pre-merge-commit` hook that tutor uses is now active here. **`git merge staging` while on master is blocked** with an explanatory message. The escape hatch is `--no-verify`, but pause first and run the audit script (below).

The reasoning behind the block: even though mitra-website is "pure static content" without structural staging-only commits like tutor's seed scripts, staging in practice accumulates in-progress drafts (English v2 pages, layout iterations, prototypes) that aren't approved for prod. A wholesale staging→master merge drags them. The hook makes that impossible by accident.

**Per-clone setup** (each developer must run on their own clone — git config is per-clone, not committed):

```bash
git config core.hooksPath scripts/
git config branch.master.mergeOptions --no-ff
```

Verify after every clone, and at session start:

```bash
git config core.hooksPath              # -> scripts/
git config branch.master.mergeOptions  # -> --no-ff
```

Both must be set. Without `branch.master.mergeOptions --no-ff`, a fast-forward `git merge staging` skips the hook entirely (no merge commit gets created, so pre-merge-commit never fires).

### `scripts/promotion-audit.sh`

Run this before any promotion work to see what's actually on staging:

```bash
sh scripts/promotion-audit.sh
```

Output:
- Total commits on staging not on master
- `[WIP-only]` tag on commits whose touched files all match known staging-only paths (see `WIP_PATTERNS` in the script — update the list when WIP areas change)
- Untagged commits = promotion candidates that touch files that DO ship to prod

The original failure mode this exists to prevent: WhatsApp callouts sat on staging from mid-May to 2026-05-26 because no one had visibility into "legitimate work stuck on staging." Now there's a one-line audit.

## History note: why the convention changed

Pre-2026-05-26, the mitra-website convention was direct staging→master merges (`Merge staging into master: KO homepage rebuild`, `Merge staging into master: NE Georgia partner program`). That worked when staging was kept clean. By mid-May 2026, staging had ~50 commits of mixed-state work, and a wholesale merge would have shipped unapproved English drafts. The new hook + audit script reflect that reality: feature branches off master are now the standard unit of promotion, same as tutor.

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
- **2026-05-26:** Staging cleanup pass + guardrails landed. Bucket A (WhatsApp callouts), Bucket A-2 (EN homepage + faq), Bucket D (free-trial WhatsApp option) all promoted to master via individual feature branches. Bucket B/C (English `home-v2` + `for-parents-v2` drafts) explicitly held on staging. Bucket E backfilled master into staging. Then: `scripts/pre-merge-commit` hook copied from tutor, `scripts/promotion-audit.sh` added, per-clone git config documented. Trigger was George's observation that the staging→master gap was costing legitimate work (the WhatsApp callouts had been stuck since mid-May).
