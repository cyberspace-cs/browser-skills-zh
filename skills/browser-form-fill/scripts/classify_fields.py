#!/usr/bin/env python3
"""把用户给的字段名映射到标准类别，标注哪些是敏感字段。

用法:
    python classify_fields.py "姓名,邮箱,密码,身份证,公司"
"""
from __future__ import annotations

import argparse
import sys

# 类别 -> 触发关键词（小写，子串匹配）
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "name": ["姓名", "name", "fullname", "full name"],
    "email": ["邮箱", "email", "e-mail", "邮件"],
    "phone": ["电话", "手机", "phone", "mobile", "tel"],
    "date": ["日期", "date", "birth", "生日"],
    "url": ["网址", "url", "website", "博客", "blog"],
    "company": ["公司", "company", "org", "组织", "单位"],
    "address": ["地址", "address", "住址"],
    "title": ["职位", "title", "job"],
}

# 敏感字段：必须跳过
SENSITIVE_KEYWORDS = [
    "password", "passwd", "pwd",
    "密码",
    "captcha", "otp", "2fa", "验证码",
    "card", "cvv", "cvc", "卡号", "信用卡", "支付",
    "ssn", "身份证", "id_card",
    "token", "secret", "api_key", "private_key",
]


def classify(field: str) -> tuple[str, str]:
    f = field.strip().lower()
    for kw in SENSITIVE_KEYWORDS:
        if kw in f:
            return "SKIP", "敏感"
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in f for kw in kws):
            return cat, "safe"
    return "unknown", "需人工确认"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fields", help="逗号分隔的字段名")
    args = ap.parse_args()

    for raw in args.fields.split(","):
        raw = raw.strip()
        if not raw:
            continue
        cat, status = classify(raw)
        print(f"{raw:20} -> {cat:10} ({status})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
