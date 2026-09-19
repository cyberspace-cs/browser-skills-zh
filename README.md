# browser-skills-zh

> 让 AI agent 学会用浏览器干活的**中文技能包**
> 一次编写，Claude Code / Cursor / GitHub Copilot / Codex / VS Code 直接加载

[![Agent Skills Standard](https://img.shields.io/badge/standard-Agent%20Skills%20(2025-12)-9cf?style=flat-square)](https://github.com/agentskills/agentskills)
[![MCP](https://img.shields.io/badge/runtime-MCP%20or%20CLI-orange?style=flat-square)](#接入)
[![Python](https://img.shields.io/badge/scripts-Python%203.9+-blue?style=flat-square)](#内置技能)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](#license)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](#贡献)

---

## 这是什么

主流 AI 编程助手（Claude Code、Cursor、Copilot、Codex CLI）已经能读写你的代码，但它们**不会用浏览器**——每次开网页都要你重新贴一遍操作说明。

**browser-skills-zh** 把高频浏览器工作流封装成符合 [Agent Skills 开放标准](https://github.com/agentskills/agentskills) 的 `SKILL.md`：

- 🇨🇳 **中文技能**：触发词、工作流、输出格式都按中文开发者习惯写
- 🔌 **跨平台**：一个仓库，33+ 个 agent 产品直接加载（Claude Code / Cursor / Copilot / Codex / VS Code / Gemini CLI…）
- 🧩 **结构化驱动**：底层走 accessibility tree / MCP，不依赖截图，省 token、更稳
- 🛡️ **默认只读 + 最小权限**：每个 skill 开头就写清「能做什么、不能做什么」
- 🧪 **带可运行脚本**：复杂逻辑抽到 `scripts/`，不把 token 浪费在重复劳动上

```
你（说中文）
    │
    ▼
Claude Code / Cursor / Copilot / Codex
    │ 命中触发词，自动加载对应 SKILL.md
    ▼
skills/github-pr-review/SKILL.md
    │ 调用 scripts/ 里的辅助脚本 + 浏览器后端
    ▼
Playwright MCP / Tencent BrowserSkill（复用你已登录的 Chrome）
    │
    ▼
打开 PR → 读 diff → 四栏中文审查意见
```

---

## 为什么需要它

| 现状 | browser-skills-zh |
|---|---|
| 每次开网页都要重贴操作说明 | 触发一次，自动加载技能 |
| 浏览器能力被各家私有封装锁定 | 开放标准，换平台不丢技能 |
| 截图式操作贵、慢、易抖 | accessibility tree 结构化操作 |
| 英文 skill 对中文网站/流程水土不服 | 面向中文工作流（GitHub PR、Trending 日报…） |
| agent 在浏览器里乱点一气 | 默认只读，写操作必须人工确认 |

---

## 30 秒接入

### 第 1 步：装一个浏览器后端（任选其一）

```bash
# 选项 A：Microsoft Playwright MCP（推荐，无需视觉模型）
npx @playwright/mcp@latest

# 选项 B：腾讯 BrowserSkill（复用本地 Chrome 登录态）
bsk daemon start
```

### 第 2 步：把技能软链到 agent 目录

```bash
git clone https://github.com/yourname/browser-skills-zh.git

# Claude Code / 通用 Agent Skills 目录
mkdir -p ~/.agents/skills
ln -s "$(pwd)/browser-skills-zh/skills/github-pr-review"      ~/.agents/skills/
ln -s "$(pwd)/browser-skills-zh/skills/github-trending-digest" ~/.agents/skills/
ln -s "$(pwd)/browser-skills-zh/skills/browser-form-fill"     ~/.agents/skills/
```

Windows（PowerShell）：

```powershell
New-Item -ItemType Junction -Target "$pwd\browser-skills-zh\skills\github-pr-review" `
  -Value "$HOME\.agents\skills\github-pr-review"
```

### 第 3 步：在 MCP 客户端挂浏览器后端

`~/.claude.json`（Claude Desktop 为例）：

```json
{
  "mcpServers": {
    "playwright": { "command": "npx", "args": ["@playwright/mcp@latest"] }
  }
}
```

完事。下次你说「帮我看看这个 PR」，agent 会自动加载 `github-pr-review` 技能。

---

## 内置技能

| 技能 | 触发词示例 | 它会做什么 | 写操作？ |
|---|---|---|---|
| [`github-pr-review`](skills/github-pr-review/) | 「审一下这个 PR」「看看 #123」 | 打开 PR → 读 diff → 按架构/质量/安全/改进四栏出中文意见 | ❌ 只读 |
| [`github-trending-digest`](skills/github-trending-digest/) | 「这周 GitHub 有啥火的」 | 抓 Trending → 按方向分类 → 出中文周报 | ❌ 只读 |
| [`browser-form-fill`](skills/browser-form-fill/) | 「帮我把这张表单填了」 | 读 accessibility tree → 字段对齐 → 列清单 → 等你确认 → 填写 | ✅ 需确认，不自动提交 |

### 示例：`github-pr-review` 的输出长这样

```
## PR #123 — feat: add remote gateway

- 作者：octocat · +259/-12 · CI: ✅ 3 passed / ❌ 1 failed

### 🔴 必须改（阻塞合并）
- server.rs:42 — 未认证请求直接读了 header，建议先查 Authorization

### 🟡 建议改（非阻塞）
- server.rs:88 — 错误信息泄露了内部路径

### 结论
建议修改后合并，CI 那个失败先看是不是 flaky。
```

---

## 权限与安全（请务必读）

浏览器技能 = agent 可以在你**已登录的网站**上操作。本仓库遵循最小权限：

- 🔴 **默认只读**：`github-pr-review`、`github-trending-digest` 完全不写任何网站。
- 🟡 **写操作先列清单**：`browser-form-fill` 必须把「字段 → 值」列出来，你说「确认」才动手。
- 🔴 **永远跳过**：密码、验证码、支付字段、最终提交按钮。
- 🟢 **生产环境建议跑在沙箱里**：把 agent 关进 microVM / Seatbelt / Landlock，浏览器操作不波及主机（参考 [OpenFang](https://github.com/)、E2B、Docker Sandboxes）。

---

## 目录结构

```
browser-skills-zh/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── skills/
    ├── github-pr-review/
    │   ├── SKILL.md
    │   └── scripts/review_pr.py      # 用 GitHub API 拉 PR diff
    ├── github-trending-digest/
    │   ├── SKILL.md
    │   └── scripts/fetch_trending.py # 解析 trending 页
    └── browser-form-fill/
        ├── SKILL.md
        └── scripts/classify_fields.py # 字段敏感分类
```

---

## SKILL.md 规范速查（贡献前必读）

| 规则 | 要求 |
|---|---|
| 文件名 | 必须 `SKILL.md`（大小写敏感） |
| 文件夹名 | kebab-case，如 `github-pr-review`，无空格/下划线/大写 |
| frontmatter 必填 | `name`（≤64 字符）、`description`（≤1024，写清触发场景） |
| 禁止 | 文件夹里放 `README.md`、写成 `SKILL.MD` |
| 权限边界 | 每个 skill 开头必须写「能做什么 / 不能做什么」 |
| 复杂逻辑 | 抽到 `scripts/`，别把几十行代码塞进 prompt |

---

## 路线图

- [x] v0.1：3 个核心 skill + README + 脚本
- [ ] v0.2：`github-issue-triage`（批量给 issue 分类打标签）
- [ ] v0.3：`feishu-doc-export`（飞书文档批量导出 Markdown）
- [ ] v0.4：一键安装脚本 + SKILL.md schema 校验
- [ ] v1.0：发布到 Agent Skills 市场

## 贡献

欢迎按「规范速查」提交新的浏览器工作流技能包——一个 PR 加一个 skill 文件夹即可。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

MIT © yourname
