# 贡献指南

欢迎给 browser-skills-zh 加新的浏览器工作流技能包。

## 加一个新 skill 的流程

1. **新建文件夹**：`skills/<kebab-case-name>/`，例如 `skills/github-issue-triage/`
2. **写 `SKILL.md`**：frontmatter + 正文，参考 `skills/github-pr-review/SKILL.md` 的结构
3. **加脚本**（可选但推荐）：复杂逻辑放 `scripts/`，用 Python 3.9+
4. **在 README.md 的「内置技能」表里加一行**
5. **提 PR**：标题格式 `feat(skills): add <skill-name>`

## SKILL.md 模板

```markdown
---
name: my-skill
description: <一句话说清做什么 + 触发场景，≤1024 字符>
---

# 标题

## 权限边界（必须先写）
- ✅ 能做什么
- ❌ 不做什么

## 工作流
1. 步骤一
2. 步骤二
3. 输出格式

## 何时不该用
- ...
```

## 原则

- **最小权限**：写操作必须先列清单等人确认。
- **只读优先**：能只读就别写。
- **不编数据**：脚本抓到什么就是什么，别凭印象写。
- **中文**：技能描述和工作流用中文写。
- **跨平台**：别绑死某一个 MCP 客户端。

## 本地校验

```bash
# 检查 frontmatter
python scripts/validate_skills.py
```

## License

贡献即代表你同意以 MIT 授权本项目。
