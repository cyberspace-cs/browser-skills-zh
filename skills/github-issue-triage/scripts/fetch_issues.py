#!/usr/bin/env python3
"""拉取 GitHub 仓库的 open issues，输出 JSON。

用法:
    python fetch_issues.py owner repo [--out issues.json] [--limit 50]

需要 GITHUB_TOKEN 环境变量。
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
    ap.add_argument("--out", default="-")
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("error: set GITHUB_TOKEN first", file=sys.stderr)
        return 2

    base = f"https://api.github.com/repos/{args.owner}/{args.repo}"
    issues = api_get(
        f"{base}/issues?state=open&per_page={args.limit}", token
    )

    # 过滤掉 PR（GitHub API 把 PR 也混在 issues 里）
    real_issues = [i for i in issues if "pull_request" not in i]

    result = {
        "repo": f"{args.owner}/{args.repo}",
        "open_issues": len(real_issues),
        "issues": [
            {
                "number": i["number"],
                "title": i["title"],
                "author": i["user"]["login"],
                "labels": [l["name"] for l in i.get("labels", [])],
                "comments": i["comments"],
                "created_at": i["created_at"],
                "body": (i.get("body") or "")[:500],
            }
            for i in real_issues
        ],
    }

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out == "-":
        print(text)
    else:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {args.out}: {len(real_issues)} open issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
