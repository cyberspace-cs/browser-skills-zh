# Trending 分类规则

快速参考：GitHub Trending 周报怎么分类。配合 `github-trending-digest` skill 使用。

## 分类方向（默认）

| 方向 | 典型项目特征 |
|---|---|
| **Agent / Coding Agent** | 描述里有 "agent"、"coding"、"assistant"、"AI pair" |
| **Agent OS / 沙箱** | 描述里有 "sandbox"、"isolated"、"microVM"、"security" |
| **浏览器自动化** | 描述里有 "browser"、"playwright"、"MCP"、"automation" |
| **AI 写作 / 去 AI 味** | 描述里有 "humanize"、"writing"、"AI detection" |
| **基础设施 / 工具链** | CLI、Rust、DevTools、构建工具 |
| **其他** | 游戏、设计、趣味项目 |

## 存疑信号（单独放「存疑」区）

描述里出现以下词的，标注存疑：

- "bypass"、"circumvent"（绕过 X）
- "10x"、"100x"、"amazing"、"revolutionary"（夸张）
- "AGI"、"sentient"、"conscious"（噱头）
- "replaces X"（替代整个 X）

## 系列识别

- 同前缀项目（如 `jev-*`）：明说「这是一个系列」
- 同作者项目：标注「连续 N 周在榜」

## 数据准确性

- star 数以脚本抓到的为准
- 不要凭印象写「大概 5k stars」
- 今天新增 star ≠ 总 star，别混
