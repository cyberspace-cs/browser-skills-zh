---
name: github-pr-review
description: |
  Use when the user asks to review a pull request, audit a diff, or check whether
  a PR is safe to merge. Triggers on phrases like "审一下这个 PR", "看看 #123",
  "帮我 review", "PR 改了什么", "is this PR good to merge".
  Requires a browser backend (Playwright MCP or bsk) OR GITHUB_TOKEN env var for
  the API script. Read-only: never merge, approve, or comment without explicit
  user confirmation.
---

# github-pr-review

对一个 GitHub Pull Request 做**严格但建设性**的中文代码审查。目标是帮用户在合并前发现问题，不是替用户做决定。

## Before starting（前置检查，必做）

在开始前先确认你有两种路径之一可用：

1. **API 路径（推荐，无需浏览器）**：检查环境变量 `GITHUB_TOKEN`。有就用 `scripts/review_pr.py` 拉结构化数据。
2. **浏览器路径**：确认浏览器后端在线（Playwright MCP / bsk daemon）。用 `browser_snapshot` 试一下能不能拿到 PR 页。

两条都不可用，**直接告诉用户**「需要 GITHUB_TOKEN 或浏览器后端」，不要硬猜 PR 内容。

## 红线（永远不做）

- ❌ 不点击 Merge / Approve / Request changes
- ❌ 不替用户在 PR 里写评论
- ❌ 不读 PR diff 之外的私有内容（密钥、env、cookies）
- ❌ 用户要「帮我 merge」——把要做的操作写出来给他自己点

## 工作流

### 1. 定位 PR
用户给链接或 `owner/repo#123`。
- 链接 → 提取 owner/repo/number
- 只给 `#123` 且在 git 仓库里 → `git remote get-url origin` 推断

### 2. 拉数据

```bash
python scripts/review_pr.py owner repo 123 --out pr-123.json
```

输出：标题、作者、+/- 行数、文件列表、每个文件 patch、CI 状态、关联 issue。

### 3. 审查四栏

| 栏 | 看什么 | 例子 |
|---|---|---|
| 架构 | 分层对不对、有没有重复造轮子 | 「新工具函数放进了 HTTP handler 里」 |
| 代码质量 | 边界条件、错误处理、死代码、测试 | 「空 list 没处理」 |
| 安全 | 注入、路径穿越、密钥、shell=True | 「`subprocess.run(shell=True)`」 |
| 改进 | 小建议，标注「非阻塞」 | 「可以用 dataclass 替换 dict」 |

每条意见必须指向 **文件:行号或函数名**，禁止「整体不错」这种废话。

### 4. 输出格式

```
## PR #123 — <标题>
- 作者 / +N/-M / CI 状态
- 一句话总评：<建议合并 / 建议修改后合并 / 建议打回>

### 🔴 必须改（阻塞）
- file.py:42 — 问题 + 为什么 + 怎么改

### 🟡 建议改（非阻塞）
- file.py:88 — 建议…

### 🟢 写得好的地方
- …

### 结论
<一段话：剩余风险>
```

## 原则（判断规则）

- **新测试只看断言真不真**：别花时间夸测试写得漂亮，看它有没有真的断言行为、有没有 mock 过度到没意义。
- **文档 PR 看事实**：查链接死没死、术语一不一致，别评文风。
- **大 PR 先归类**：>500 行先按模块分组，挑重点文件看，不逐行纠缠。
- **看不懂就说不懂**：业务上下文缺的时候，明说「这部分需要业务背景」，不要硬编。
- **CI 失败先看 flaky**：别一见红就说代码有问题，先看是不是已知 flaky test。

## 何时不该用这个 skill

- 用户要「写 PR 描述」「改 PR 标题」——写作任务，不是审查
- 用户要「合并到生产」——提醒你不是 approver
- 用户要「给作者打分」——这不是代码评审
