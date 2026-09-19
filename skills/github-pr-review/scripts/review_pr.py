#!/usr/bin/env python3
"""拉取 PR 元信息与 diff，输出 JSON 供审查使用。

用法:
    python review_pr.py owner repo 123 [--out pr.json]

需要环境变量 GITHUB_TOKEN（至少 public_repo 读权限）。
走 https://api.github.com，无需 git clone。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request


def api_get(url: str, token: str) -> dict | list:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "browser-skills-zh",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("owner")
    ap.add_argument("repo")
    ap.add_argument("number", type=int)
    ap.add_argument("--out", default="-")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("error: set GITHUB_TOKEN first", file=sys.stderr)
        return 2

    base = f"https://api.github.com/repos/{args.owner}/{args.repo}"
    pr = api_get(f"{base}/pulls/{args.number}", token)
    files = api_get(f"{base}/pulls/{args.number}/files?per_page=100", token)
    checks = api_get(
        f"{base}/commits/{pr['head']['sha']}/check-runs?per_page=100", token
    )

    ci_summary = {}
    for run in checks.get("check_runs", []):
        ci_summary[run["name"]] = {
            "status": run["status"],
            "conclusion": run["conclusion"],
        }

    result = {
        "number": pr["number"],
        "title": pr["title"],
        "author": pr["user"]["login"],
        "state": pr["state"],
        "additions": pr["additions"],
        "deletions": pr["deletions"],
        "changed_files": pr["changed_files"],
        "base": pr["base"]["ref"],
        "head": pr["head"]["ref"],
        "body": (pr.get("body") or "")[:2000],
        "ci": ci_summary,
        "files": [
            {
                "filename": f["filename"],
                "status": f["status"],
                "additions": f["additions"],
                "deletions": f["deletions"],
                "patch": f.get("patch", ""),
            }
            for f in files
        ],
    }

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out == "-":
        print(text)
    else:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {args.out} ({result['changed_files']} files, "
              f"+{result['additions']}/-{result['deletions']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
