#!/usr/bin/env python3
"""校验所有 skills/*/SKILL.md 是否符合规范。

用法: python scripts/validate_skills.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"


def kebab_case(name: str) -> bool:
    return bool(re.fullmatch(r"[a-z][a-z0-9-]*", name)) and "--" not in name


def validate(skill_dir: Path) -> list[str]:
    errors = []
    name = skill_dir.name
    if not kebab_case(name):
        errors.append(f"文件夹名 {name!r} 不是 kebab-case")

    md = skill_dir / "SKILL.md"
    if not md.is_file():
        errors.append("缺少 SKILL.md")
        return errors

    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append("缺少 YAML frontmatter（应以 --- 开头）")
        return errors

    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("frontmatter 未闭合")
        return errors

    frontmatter = parts[1]
    m_name = re.search(r"^name:\s*(.+)$", frontmatter, re.M)
    m_desc = re.search(r"^description:\s*(.+)$", frontmatter, re.M)

    if not m_name:
        errors.append("frontmatter 缺少 name")
    elif len(m_name.group(1).strip()) > 64:
        errors.append("name 超过 64 字符")

    if not m_desc:
        errors.append("frontmatter 缺少 description")
    elif len(m_desc.group(1).strip()) > 1024:
        errors.append("description 超过 1024 字符")

    # 正文里必须有权限边界
    if "权限边界" not in text and "不做" not in text:
        errors.append("正文缺少权限边界声明")

    # 文件夹里不该有 README.md
    if (skill_dir / "README.md").is_file():
        errors.append("skill 文件夹里不该放 README.md（用 SKILL.md）")

    return errors


def main() -> int:
    if not SKILLS.is_dir():
        print("skills/ 目录不存在", file=sys.stderr)
        return 1

    failed = 0
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        errs = validate(skill_dir)
        if errs:
            failed += 1
            print(f"✗ {skill_dir.name}")
            for e in errs:
                print(f"    - {e}")
        else:
            print(f"✓ {skill_dir.name}")

    print(f"\n{failed} 个 skill 未通过校验")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
