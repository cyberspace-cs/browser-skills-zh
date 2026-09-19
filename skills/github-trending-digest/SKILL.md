---
name: github-trending-digest
description: 抓取 GitHub Trending（今日/本周/本月），按语言和方向分类，输出一份中文日报。当用户说「这周 GitHub 有啥火的」「看看 trending」「今日热门开源」「trending 日报」时触发。只读，不自动 star/follow。
---

# GitHub Trending 日报

把 GitHub Trending 从「英文标题流」变成「中文可读、有判断、能收藏」的日报。

## 权限边界
- ✅ 只读：抓取 trending 页面 / API，不登录、不 star、不 follow、不发 issue。
- ❌ 不做任何账号操作。

## 工作流

### 1. 确认时间窗
用户没说就默认 `weekly`。可选：
- `daily`（今日）
- `weekly`（本周，默认）
- `monthly`（本月）

### 2. 抓取
优先用脚本（不依赖浏览器）：

```bash
python scripts/fetch_trending.py --since weekly --out trending.json
```

脚本直接解析 `https://github.com/trending?since=weekly` 的 HTML，提取：仓库全名、描述、语言、今日/本周新增 star、总 star。

若脚本失败（网络/页面结构变），再让浏览器后端打开 `https://github.com/trending?since=weekly` 用 accessibility tree 读列表。

### 3. 分类（这一步是这个 skill 的核心价值）
不要按语言堆列表。按**本周真正在讨论的方向**归类，例如：

- **Agent / Coding Agent**：Claude Code 插件、agent 框架、skill 包
- **Agent OS / 沙箱**：给 agent 装操作系统的项目
- **浏览器自动化**：MCP browser、browser-use 类
- **AI 写作 / 去 AI 味**：humanizer 类
- **基础设施 / 工具链**：Rust CLI、DevTools
- **其他**：游戏、设计、趣味项目

每个方向挑 2-4 个最有代表性的，写一句「它解决了什么问题」。

### 4. 输出格式

```
# GitHub Trending 周报（YYYY-MM-DD）

> 时间窗：本周 · 共抓取 N 个项目

## 🔥 本周主线
<一段话：本周在讨论什么，哪条线在升温>

## 📦 按方向

### Agent / Coding Agent
- **owner/repo** ★k — 一句话价值
- ...

### Agent OS / 沙箱
- ...

## ⭐ 本周最值得看的 3 个
1. ...
2. ...
3. ...

## 📌 值得关注但存疑
- owner/repo — 为什么存疑（营销味重 / 安全属性可疑 / 命名蹭热点）
```

### 5. 判断规则
- **不堆砌**：30 个项目全列出来没价值，挑 8-12 个真正有意思的。
- **标注存疑**：描述里出现「bypass AI detector」「10x faster」「replaces X」这类夸张词的，单独放「存疑」区。
- **关联历史**：如果某项目和上周/上月的项目是同一作者系列（如 `jev-*` 全家桶），点明「这是一个系列」。
- **不编数据**：star 数以脚本抓到的为准，不要凭印象写。

## 何时不该用
- 用户要「帮我 star 这些项目」——那是账号操作，本 skill 不做。
- 用户要「深度分析某一个项目」——用 pr-review 或单独的调研流程。
