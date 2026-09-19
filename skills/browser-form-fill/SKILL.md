---
name: browser-form-fill
description: |
  Use when the user wants to fill a web form from a batch of information they
  provide. Triggers on "帮我把这张表单填了", "这个网页表格怎么填", "按这个信息填进去".
  Requires a browser backend (Playwright MCP or bsk).
  Writes only after listing every field-value pair and getting explicit user
  confirmation. Always skips password, captcha, OTP, and payment fields.
  Never clicks the final submit button.
---

# browser-form-fill

把用户给的一批信息，结构化填进网页表单。**走 accessibility tree，不靠截图猜**。

## Before starting（前置检查）

1. 确认浏览器后端在线（Playwright MCP / bsk daemon）。
2. 先用 `browser_snapshot` 读一下表单结构，确认能拿到 accessibility tree。
3. 跑一下字段分类器，先把敏感字段标出来：

```bash
python scripts/classify_fields.py "姓名,邮箱,密码,身份证,公司"
```

## 红线（最高优先级）

- 🔴 **永远跳过**：`type=password`、captcha/OTP/2FA、支付字段（card/cvv）、签名/同意勾选、最终「提交」按钮
- 🟡 **必须先列清单**：「字段 → 值」列成表，等用户说「确认」才动手
- 🟢 **填完就停**：最后一步「提交」由用户自己点
- 🔴 **不回滚**：浏览器没有 undo，所以列清单这一步不能省

## 工作流

### 1. 拿数据
用户贴/给一份信息。整理成字典。缺字段就问，不编。

### 2. 读 accessibility tree
打开表单，调用 `browser_snapshot`（或等价接口）。**不要截图让模型猜**——用结构化文本里的 `ref` / `name` / `role` 定位。

### 3. 字段对齐

| 用户给的 | 页面上的 | 匹配 |
|---|---|---|
| 姓名 | Full name / 姓名 | 同义 + 大小写不敏感 |
| 邮箱 | Email / 电子邮箱 | 正则 `^[\w.+-]+@[\w-]+\.[\w.]+$` |
| 电话 | Phone / 手机 | 数字 + 国家码 |
| 日期 | Date / 日期 | ISO `YYYY-MM-DD` |

匹配不上的字段，列出来问用户，不要硬塞到相近字段。

### 4. 列清单（必须）

```
将填写以下字段（共 N 项）：
- 姓名 → 张三
- 邮箱 → zhangsan@example.com
已跳过：密码、验证码、支付字段（共 3 项）
不会自动点「提交」。
确认请回复「确认填写」。
```

### 5. 逐项填写
用户确认后，按 accessibility tree 的 `ref` 逐个 `fill` / `click`：
- 文本框：`fill(ref, value)`
- 下拉：先 click 展开再 select
- 单选/复选：click
- 日期：按页面格式

每填 3-5 项，回一次 snapshot 确认没填错位置。

### 6. 收尾
再 snapshot 一次，把实际填入的值列给用户核对，提醒他自己点提交。

## 原则（判断规则）

- **宁停勿错**：匹配不上就停，别硬填
- **少即是多**：一次填 5 项回查一次，别一口气填 20 项
- **敏感字段零妥协**：哪怕用户说「就填一下密码」，也拒绝并让他自己来

## 何时不该用

- 需要验证码——让用户自己来
- 支付/汇款表单——直接拒绝
- 用户要「自动提交」——拒绝，坚持最后一步留给人
