# Skill Evals

衡量本仓库的 skill 是否真的能用：**该触发时触发、不该触发时不触发、按 skill 承诺的方式改变 agent 行为**。

## 三个层级

| 层级 | 检查什么 | 运行方式 | 成本 |
|---|---|---|---|
| 1. 结构 | frontmatter、命名、必填章节 | `python scripts/validate_skills.py` | 免费 |
| 2. 触发 & 路由 | 正向 prompt 能命中对应 skill，负向 prompt 不命中 | 人工/CI 检查 | 免费 |
| 3. 行为 | agent 按 skill 工作流跑完，满足 expectations[] | 在真实 agent 里跑 | 消耗 token |

## Case 格式

每个 `evals/cases/<skill-name>.json`：

- `trigger.positive`：应该触发这个 skill 的用户说法
- `trigger.negative`：不该触发、应该路由到别的 skill 的说法
- `evals[]`：具体用例，每个有 `prompt` + `expected_output` + `expectations[]`

## 跑

```bash
# 层级 1：结构校验（CI 免费）
python scripts/validate_skills.py

# 层级 2：触发路由（人工看 positive/negative 是否合理）
# 暂无自动化脚本，靠 code review

# 层级 3：行为（在 Claude Code / Cursor 里真跑）
# 把 evals/cases/*.json 里的 prompt 贴给 agent，看输出是否满足 expectations[]
```

## 当前覆盖

| skill | positive | negative | evals |
|---|---|---|---|
| github-pr-review | 3 | 2 | 1 |
| github-trending-digest | 3 | 2 | 1 |
| browser-form-fill | 3 | 2 | 1 |
