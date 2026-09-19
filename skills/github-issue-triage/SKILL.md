---
name: github-issue-triage
description: |
  Use when the user asks to triage, label, or summarize a batch of GitHub issues.
  Triggers on "给这些 issue 打标签", "issue 分类", "看看 open issues", "triage this repo".
  Reads issues via API (GITHUB_TOKEN) or browser; proposes labels/comments but
  never applies them without explicit user confirmation.
---

# github-issue-triage

批量给 GitHub issue 分类、打标签、出摘要。**只建议，不操作**。

## Before starting（前置检查）

1. 确认 `GITHUB_TOKEN` 环境变量可用（推荐）。
2. 确认仓库 owner/repo（用户给链接或本地 git remote）。
3. 先跑脚本拉 open issues 列表：

```bash
python scripts/fetch_issues.py owner repo --out issues.json
```

## 红线

- ❌ 不自动打标签 / 关 issue / 写评论
- ❌ 不删 issue
- ✅ 把建议的标签和评论写出来，用户自己去点

## 工作流

### 1. 拉 issues
脚本拉 open issues（默认前 50 个）：标题、作者、标签、评论数、创建时间、body 摘要。

### 2. 分类
按以下维度给每个 issue 打建议标签：

| 维度 | 标签候选 |
|---|---|
| 类型 | `bug` / `feature` / `question` / `docs` / `chore` |
| 优先级 | `P0-critical` / `P1-high` / `P2-medium` / `P3-low` |
| 状态 | `needs-repro` / `needs-more-info` / `stale` / `duplicate` |
| 组件 | `frontend` / `backend` / `docs` / `ci` |

### 3. 输出格式

```
## Issue Triage 报告（共 N 个 open issues）

### 🔴 需要立即处理（P0/P1）
- #123 — 标题（bug, needs-repro）
- #456 — 标题（feature, backend）

### 🟡 可以排队（P2）
- ...

### 🟢 低优先级 / stale
- ...

### 重复问题
- #789 和 #101 是同一问题

### 建议动作
1. 给 #123 打 `bug` + `needs-repro`
2. 给 #456 打 `feature` + `backend`
3. 关闭 #789（重复 #101）
```

## 原则

- **先看有没有重复**：搜关键词找类似 issue
- **needs-more-info**：描述不清的，建议要求作者补信息，不直接关
- **stale**：>90 天没活动的，建议标记 stale
- **不替 maintainer 做决定**：只建议，标签和评论由人来打

## 何时不该用

- 用户要「帮我关了这个 issue」——让他自己来
- 用户要「批量给 issue 写评论」——把评论内容写出来给他自己发
