#!/usr/bin/env bash
set -euo pipefail

batch=$1
shard=$2
kind=${3:-intake}
branch=${GITHUB_REF_NAME:?GITHUB_REF_NAME is required}
if [[ ! $batch =~ ^[a-z0-9]+(-[a-z0-9]+)*$ || ! $shard =~ ^[0-4]$ || ! $kind =~ ^(intake|refresh|animations)$ ]]; then
  echo 'Invalid batch, shard or output kind.' >&2
  exit 1
fi

# Only this invocation's output paths are staged. Never sweep unrelated edits into a bot commit.
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
if [[ $kind == animations ]]; then
  # Animation retrofit edits approved assets in place (adding an animated GLB,
  # verification frames and provenance) rather than writing to quarantine.
  git add -- assets "reports/$kind/$batch/shard-$shard.json" "reports/$kind/$batch/worker-$shard.log"
else
  git add -- "quarantine/$batch" "reports/$kind/$batch/shard-$shard.json" "reports/$kind/$batch/worker-$shard.log"
fi
if git diff --cached --quiet; then
  echo 'No shard output to publish.'
  exit 0
fi
git commit -m "assets: $kind $batch shard $shard [skip ci]"
for attempt in 1 2 3 4 5; do
  if git push origin "HEAD:$branch"; then
    exit 0
  fi
  echo "Push attempt $attempt lost a race; rebasing this shard."
  git pull --rebase origin "$branch"
  sleep "$attempt"
done
echo 'Could not publish shard after five attempts.' >&2
exit 1
