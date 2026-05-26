# mitra-website Runbooks

Operational breadcrumbs for the Mitra marketing website (separate repo from `tutor`). Read the relevant topic file before touching prod or accessing CF Pages.

| Topic | File | When to read |
|-------|------|--------------|
| Staging + prod deploy workflow | [staging.md](staging.md) | Before pushing any KO/EN content change |
| Build system + env handling | [build.md](build.md) | When `build.py` behavior is unclear, or env URL tokens look wrong |

## Operator tools

- `scripts/promotion-audit.sh` — list what's on staging but not master, with `[WIP-only]` tagging. Run before any promotion work.
- `scripts/pre-merge-commit` — blocks `git merge staging` while on master (escape with `--no-verify`, but run the audit first). Active per-clone when `core.hooksPath=scripts/` and `branch.master.mergeOptions=--no-ff` are set.

Per-clone setup (each developer once):

```bash
git config core.hooksPath scripts/
git config branch.master.mergeOptions --no-ff
```

## Repo orientation

- **Repo:** `georgecv-ai/mitra-website` at `c:\Users\georg\projects\mitra-website`
- **Hosting:** Cloudflare Pages (static), built from `build.py` (Jinja-ish template assembly)
- **Sister repo:** `georgecv-ai/mitra` at `c:\Users\georg\projects\tutor` — FastAPI app on Railway. Different deploy model, different staging conventions. Don't confuse the two: `tutor/.claude/runbooks/staging.md` is about the *app*, not this site.
