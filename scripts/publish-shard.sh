#!/usr/bin/env bash
set -euo pipefail

batch=$1
shard=$2
branch=${GITHUB_REF_NAME:?GITHUB_REF_NAME is required}
run=${GITHUB_RUN_ID:?GITHUB_RUN_ID is required}

# Only this invocation's output paths are staged. Never sweep unrelated edits into a bot commit.
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -- "quarantine/$batch" "reports/intake/$batch/shard-$shard.json" "reports/intake/$batch/worker-$shard.log"
if git diff --cached --quiet; then
  echo 'No shard output to publish.'
  exit 0
fi
git commit -m "assets: inspect $batch shard $shard [skip ci]"
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
