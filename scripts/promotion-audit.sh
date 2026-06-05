#!/bin/sh
# Print what's on `staging` that hasn't reached `master` yet.
#
# Use this BEFORE any staging->master promotion to see the full landscape:
#   - commits already promoted via cherry-pick (annotated)
#   - commits that touch only known-WIP paths (probably stay on staging)
#   - everything else (promotion candidates — needs your eyes)
#
# Why this exists: legitimate features have gotten stuck on staging for
# weeks because the operator wasn't sure if a wholesale merge would drag
# WIP along. Example: WhatsApp callouts shipped to staging mid-May, didn't
# reach prod until 2026-05-26 because nothing flagged them as stale. This
# script makes that visibility cheap.
#
# Usage:  sh scripts/promotion-audit.sh
#         (run from anywhere in the repo)

set -e

# Make sure we have current refs
git fetch --quiet origin master staging 2>/dev/null || true

# Paths that are intentionally staging-only (drafts, prototypes). Update
# this list when WIP areas change.
WIP_PATTERNS="src/en/home-v2 src/en/for-parents-v2 en/home-v2 en/for-parents-v2 en/static/images/home-v2 HOME-V2-KO-NOTES.md src/ko/for-parents-wip ko/for-parents-wip ko/static/images/parents-wip"

# How many master..staging commits are there?
total=$(git log master..staging --oneline | wc -l | tr -d ' ')
already_pickedup=$(git cherry master staging | grep -c '^- ' || true)
pending=$((total - already_pickedup))

cat <<EOF
======================================================================
  PROMOTION AUDIT  (mitra-website)
======================================================================
  Total commits on staging not on master:  $total
  Already cherry-picked into master:       $already_pickedup
  Genuinely pending:                       $pending
======================================================================

EOF

if [ "$pending" = "0" ]; then
    echo "  Nothing to promote. master and staging are content-equivalent."
    echo "  (any remaining delta is just build-artifact URL rewriting.)"
    echo ""
    exit 0
fi

echo "PENDING COMMITS (master..staging, not yet on master):"
echo "----------------------------------------------------------------------"
git cherry -v master staging | grep '^+ ' | while read marker sha rest; do
    # Show commit + the files it touched, tagged with [WIP] if all files are
    # staging-only paths.
    files=$(git show --stat --format='' "$sha" | head -n -1 | awk '{print $1}')
    tag=""
    if [ -n "$files" ]; then
        all_wip=1
        for f in $files; do
            is_wip=0
            for pat in $WIP_PATTERNS; do
                case "$f" in *"$pat"*) is_wip=1; break;; esac
            done
            if [ "$is_wip" = "0" ]; then
                all_wip=0; break
            fi
        done
        if [ "$all_wip" = "1" ]; then tag=" [WIP-only]"; fi
    fi
    printf "  %s%s\n     %s\n\n" "$sha" "$tag" "$rest"
done

cat <<EOF
----------------------------------------------------------------------
LEGEND
  [WIP-only]   Commit touches only known-WIP paths (see WIP_PATTERNS in
               this script). Probably stays on staging until the WIP work
               is approved. If you don't see this tag, the commit touches
               files that DO ship to prod and is a promotion candidate.

NEXT STEP
  For the candidates without [WIP-only], decide one at a time:
    git checkout -b feat/promote-XYZ master
    git cherry-pick <sha>
    python build.py --env production
    git checkout master && git merge --no-ff feat/promote-XYZ
    git push origin master

EOF
