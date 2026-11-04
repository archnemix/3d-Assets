"""Small command surface for humans and CI; implementation lives in task modules."""

import argparse
import json
import sys
from pathlib import Path

from .requests import describe, shards


def main() -> int:
    parser = argparse.ArgumentParser(prog="asset-library")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", help="Validate a request and print its category counts")
    plan.add_argument("request", type=Path)
    matrix = commands.add_parser("matrix", help="Emit at most five disjoint worker assignments")
    matrix.add_argument("request", type=Path)
    intake = commands.add_parser("intake", help="Download and inspect candidates into quarantine")
    intake.add_argument("request", type=Path)
    intake.add_argument("--shard", type=int, required=True)
    review = commands.add_parser("review", help="Apply explicit per-asset visual review decisions")
    review.add_argument("decisions", type=Path)
    reinspect = commands.add_parser(
        "reinspect", help="Recheck an already acquired quarantine candidate"
    )
    reinspect.add_argument("candidate", type=Path)
    for command, help_text in [
        ("refresh-plan", "Validate a quarantine refresh request"),
        ("refresh-matrix", "Emit at most five refresh worker assignments"),
        ("refresh", "Refresh inspection evidence for one worker assignment"),
    ]:
        refresh = commands.add_parser(command, help=help_text)
        refresh.add_argument("request", type=Path)
        if command == "refresh":
            refresh.add_argument("--shard", type=int, required=True)
    catalog = commands.add_parser("catalog", help="Rebuild the approved-only catalog")
    catalog.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "plan":
            describe(args.request)
        elif args.command == "matrix":
            print(json.dumps(shards(args.request)))
        elif args.command == "intake":
            from .intake import run_shard

            assignment = shards(args.request)[args.shard]
            return run_shard(
                assignment["batch_id"], json.loads(assignment["candidates"]), args.shard
            )
        elif args.command == "reinspect":
            from .inspection import reinspect

            reinspect(args.candidate.resolve())
        elif args.command in {"refresh-plan", "refresh-matrix", "refresh"}:
            from . import refresh

            if args.command == "refresh-plan":
                refresh.describe(args.request)
            elif args.command == "refresh-matrix":
                print(json.dumps(refresh.shards(args.request)))
            else:
                return refresh.run_shard(args.request, args.shard)
        elif args.command == "review":
            from .review import apply

            apply(args.decisions)
        elif args.command == "catalog":
            from .catalog import build, verify

            verify() if args.check else build()
        return 0
    except (ValueError, KeyError, IndexError, RuntimeError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
