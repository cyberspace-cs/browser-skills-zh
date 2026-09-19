# 表单填写规则

快速参考：网页表单怎么安全填写。配合 `browser-form-fill` skill 使用。

## 字段分类

| 类别 | 触发词 | 处理 |
|---|---|---|
| 姓名 | 姓名 / name / fullname | safe |
| 邮箱 | 邮箱 / email / e-mail | safe，正则校验 |
| 电话 | 电话 / 手机 / phone / mobile | safe，数字+国家码 |
| 日期 | 日期 / date / birth | safe，ISO 格式 |
| 公司 | 公司 / company / org | safe |
| 地址 | 地址 / address | safe |
| **密码** | password / pwd / 密码 | **SKIP** |
| **验证码** | captcha / otp / 2fa / 验证码 | **SKIP** |
| **支付** | card / cvv / 卡号 / 支付 | **SKIP** |
| **身份证** | 身份证 / ssn / id_card | **SKIP** |
| **密钥** | token / secret / api_key | **SKIP** |

## 填写流程

1. **读 accessibility tree**：不用截图，用结构化文本定位
2. **字段对齐**：用户给的字段 ↔ 页面上的 label
3. **列清单**：「字段 → 值」表，等用户确认
4. **逐项填**：每 3-5 项回查一次
5. **收尾**：再 snapshot 核对，提醒用户自己点提交

## 永远不做

- ❌ 不填密码、验证码、支付字段
- ❌ 不自动点「提交」按钮
- ❌ 不匹配不上的字段硬塞
- ❌ 不一口气填 20 项不检查
