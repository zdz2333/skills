---
name: weekly-review
description: 周回顾生成器 — 每周五自动生成周报，回顾本周完成的任务、存在的问题、下周计划。触发场景：不知道这周干了什么、写周报无从下笔、周五不知道怎么做回顾、需要跨平台汇总一周工作。当用户说"周报怎么写"、"这周干了什么"、"帮我回顾一下"、"weekly report"、"周总结"、"周回顾"时调用。
trigger: 当用户说"周报怎么写"、"这周干了什么"、"帮我回顾一下"、"weekly report"、"周总结"、"周回顾"、"周五回顾"、"本周完成"、"下周计划"时调用
---

# Weekly Review — 周回顾生成器

> 每周五 5 分钟，搞定周报 + 下周计划

## 🎯 解决什么问题

周一不知道上周干了什么？周报凑字数？周五想做回顾但不知道怎么开始？

**Weekly Review** 从 Linear、Git commits、daily-digest 历史里提取本周工作，自动生成结构化周报。

---

## 📖 使用方法

### Step 1：收集本周数据

**Linear — 本周完成的 Issues：**

```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { viewer { assignedIssues(filter: {completedAt: {gte: \"@START_OF_WEEK@\"} } }) { nodes { identifier title completedAt } } }"}'
# @START_OF_WEEK@ 替换为本周一日期，如 2026-04-21
```

**Git — 本周提交记录：**

```bash
git log --since="@START_OF_WEEK@" --oneline --stat | head -50
# 统计本周代码量
git log --since="@START_OF_WEEK@" --format="• %s" | wc -l
```

**daily-digest — 本周任务记录（如果有保存）：**

```bash
# 如果 daily-digest 有日志文件
ls ~/.hermes/logs/daily-digest/*.md 2>/dev/null | xargs grep -l "@THIS_WEEK@"
```

### Step 2：生成周报

把上面收集的数据整理成以下格式：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 第 N 周周报 — @DATE@
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 本周完成

  1. [ENG-XXX] 任务标题
     • 完成时间：周几
     • 关键产出：...

  2. [ENG-XXX] 任务标题
     ...

📊 数据统计
  • 完成 issues：N 个
  • 代码提交：N 次
  • 主要贡献：模块 A、模块 B

🎯 问题与反思
  • 遇到的挑战：...
  • 学到的东西：...
  • 可以改进的地方：...

📅 下周计划

  P0 🔴
    • [ENG-XXX] 任务标题

  P1 🟡
    • [ENG-XXX] 任务标题

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 3：输出建议

根据本周完成情况，输出一句简短总结（15 字以内）：

```
本周亮点：@一句话总结@
```

---

## ⚡ 快速模式

如果只需要周报文字版，不用查 Git：

```
输入：帮我写周报，这周完成了 [任务描述]
期望：输出格式化周报，包含本周完成 + 下周计划
```

---

## 💡 配合使用的 Skill

- [daily-digest](../daily-digest/SKILL.md) — 每日任务追踪
- [linear](../linear/SKILL.md) — Linear Issue 管理
- [github](../github/SKILL.md) — Git commit 历史

---

## 🔍 验证步骤

```bash
# 验证 Linear API
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { viewer { name } }"}'

# 验证 Git log
git log --since="2026-04-21" --oneline | head -5
```

---

*灵感来源：GitHub Weekly Digest、Linear Cycle Report*
