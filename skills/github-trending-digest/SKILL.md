---
name: github-trending-digest
description: |
  Use when the user asks what's trending on GitHub this week, today, or this
  month. Triggers on "这周 GitHub 有啥火的", "看看 trending", "今日热门开源",
  "trending 日报", "本周新项目".
  Reads github.com/trending only; never stars, follows, or opens issues.
  Outputs a Chinese digest grouped by theme, not a raw language-sorted list.
---

# github-trending-digest

把 GitHub Trending 从「英文标题流」变成「中文可读、有判断、能收藏」的周报。

## Before starting（前置检查）

1. 确认网络能访问 github.com（本地代理 7897 已配好就直接用）。
2. 先跑脚本，脚本失败再用浏览器：

```bash
python scripts/fetch_trending.py --since weekly --out trending.json
```

脚本直接解析 HTML，不登录、不调用 API。

## 红线

- ❌ 不 star / 不 follow / 不发 issue
- ❌ 不编 star 数——以脚本抓到的为准
- ❌ 不把 30 个项目全列出来——挑 8-12 个真正有意思的

## 工作流

### 1. 确认时间窗
用户没说就默认 `weekly`。可选 `daily` / `weekly` / `monthly`。

### 2. 抓数据
脚本优先；脚本失败再让浏览器后端打开 `https://github.com/trending?since=weekly`，用 accessibility tree 读列表。

### 3. 按方向分类（核心价值）
不要按语言堆列表。按**本周真正在讨论的方向**归类：

- Agent / Coding Agent
- Agent OS / 沙箱
- 浏览器自动化 / MCP
- AI 写作 / 去 AI 味
- 基础设施 / 工具链
- 其他

每个方向挑 2-4 个，写一句「它解决了什么问题」。

### 4. 输出格式

```
# GitHub Trending 周报（YYYY-MM-DD）
> 时间窗：本周 · 共 N 个项目

## 🔥 本周主线
<一段话：本周在讨论什么，哪条线在升温>

## 📦 按方向
### Agent / Coding Agent
- owner/repo ★k — 一句话价值

## ⭐ 本周最值得看的 3 个
1. ...

## 📌 值得关注但存疑
- owner/repo — 为什么存疑
```

## 原则（判断规则）

- **存疑信号**：描述里出现「bypass AI detector」「10x faster」「replaces X」「AGI」这类夸张词的，单独放「存疑」区。
- **系列识别**：同一作者/同前缀项目（如 `jev-*` 全家桶）要明说「这是一个系列」，不要当独立项目。
- **重复出现**：上周也在榜上的项目，标注「连续 N 周在榜」。
- **不堆数量**：30 个全列出来没价值，挑 8-12 个真正有意思的。

## 何时不该用

- 用户要「帮我 star 这些」——账号操作，不做
- 用户要「深度分析某一个」——用 pr-review 或单独调研
