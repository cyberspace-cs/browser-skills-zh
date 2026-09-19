#!/usr/bin/env python3
"""抓取 GitHub Trending，输出 JSON。

用法:
    python fetch_trending.py [--since daily|weekly|monthly] [--out trending.json]

直接解析 https://github.com/trending?since=... 的 HTML，无需登录。
走代理时设 HTTPS_PROXY=http://127.0.0.1:7897。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser


class TrendingParser(HTMLParser):
    """极简解析：找 <article class="Box-row"> 块，提取 owner/repo/desc/lang/stars。"""

    def __init__(self) -> None:
        super().__init__()
        self.repos: list[dict] = []
        self._in_article = False
        self._depth = 0
        self._cur: dict = {}
        self._buf = ""
        self._capture = ""  # 'h2' | 'desc' | 'lang' | 'stars' | None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        if tag == "article" and "Box-row" in cls:
            self._in_article = True
            self._depth = 1
            self._cur = {}
            self._buf = ""
            return
        if not self._in_article:
            return
        self._depth += 1
        if tag == "h2":
            self._capture = "h2"
            self._buf = ""
        elif tag == "p":
            self._capture = "desc"
            self._buf = ""
        elif tag == "span" and "d-inline-block" in cls and "programming" in cls:
            self._capture = "lang"
            self._buf = ""
        elif tag == "a" and a.get("href", "").endswith("/stargazers"):
            self._capture = "stars"
            self._buf = ""

    def handle_endtag(self, tag):
        if not self._in_article:
            return
        self._depth -= 1
        if self._capture == "h2" and tag == "h2":
            text = re.sub(r"\s+", " ", self._buf).strip()
            m = re.search(r"([\w.-]+)\s*/\s*([\w.-]+)", text)
            if m:
                self._cur["full_name"] = f"{m.group(1)}/{m.group(2)}"
            self._capture = None
        elif self._capture == "desc" and tag == "p":
            self._cur["description"] = self._buf.strip()
            self._capture = None
        elif self._capture == "lang" and tag == "span":
            self._cur["language"] = self._buf.strip()
            self._capture = None
        elif self._capture == "stars" and tag == "a":
            self._cur["stars"] = self._buf.strip()
            self._capture = None
        if self._depth <= 0:
            if self._cur:
                self.repos.append(self._cur)
            self._in_article = False
            self._cur = {}

    def handle_data(self, data):
        if self._capture:
            self._buf += data


def fetch(since: str) -> str:
    url = f"https://github.com/trending?since={since}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "browser-skills-zh"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--since", choices=["daily", "weekly", "monthly"], default="weekly"
    )
    ap.add_argument("--out", default="-")
    args = ap.parse_args()

    html = fetch(args.since)
    p = TrendingParser()
    p.feed(html)

    repos = [r for r in p.repos if r.get("full_name")]
    result = {"since": args.since, "count": len(repos), "repos": repos}

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out == "-":
        print(text)
    else:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {args.out}: {len(repos)} repos ({args.since})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
