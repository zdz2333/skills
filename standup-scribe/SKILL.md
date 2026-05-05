---
name: standup-scribe
description: 每日站会助手 — 自动生成结构化 standup 更新，从 Linear/Git 提取昨日工作。触发场景：写 standup 无从下笔、不知道昨天干了什么、需要汇报工作进度。当用户说"站会怎么写"、"standup"、"昨天干了什么"、"standup 更新"、"daily update"、"工作进展"时调用。
trigger: 当用户说"站会怎么写"、"standup"、"昨天干了什么"、"standup 更新"、"daily update"、"工作进展"、"晨会说什么"、"同步一下进度"时调用
---

# Standup Scribe — 站会更新生成器

> 30 秒生成清晰的 standup 更新，不用再凑字数

## 🎯 解决什么问题

每天站会前临时想"昨天干了什么"？写 standup 更新总要比划半天才想起来？

**Standup Scribe** 从 Linear Issues 和 Git Commits 自动提取你昨天的工作，生成结构清晰的 standup 更新。

---

## 📖 使用方法

### Step 1：描述大致工作内容

```
用户：帮我写今天的 standup
助手：→ 触发 standup-scribe
```

系统会自动尝试从以下来源提取：
- Linear：分配给你且最近完成的 Issues
- Git：昨天的 commits

### Step 2：补充 blockers（如果有）

```
用户：有个 blocker，是后端 API 还没好
助手：→ 记录 blocker
```

### Step 3：输出格式化 standup

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Standup 更新 — @DATE@
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 昨日完成
  • [ENG-XXX] 任务标题
  • [ENG-XXX] 任务标题

🚧 今日计划
  • [ENG-XXX] 任务标题

🚫 Blockers
  • 后端 API 依赖未完成，阻塞首页开发

💭 备注
  • ...
```

---

## 🔌 数据源集成

### Linear（可选）

```bash
# 获取昨天完成的 issues
LINEAR_API_KEY="your-key"
START=$(date -v-1d +%Y-%m-%d)
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"query { viewer { assignedIssues(filter: {completedAt: {gte: \"$START\"} } ) { nodes { identifier title completedAt } } }\"}"
```

### Git（自动）

```bash
# 昨天的所有 commits
git log --since="yesterday" --until="today" --format="• %s" --author="$(git config user.email)"

# 统计昨天代码量
git log --since="yesterday" --until="today" --stat | tail -1
```

---

## 💡 手动模式（无 API 时）

如果无法访问 Linear/Git，直接描述：

```
用户：我昨天做了首页的响应式布局，修了三个 bug，还开了两个会
助手：→ 格式化输出 standup
```

---

## ⚠️ 注意事项

- Blockers 优先显示，站会最重要的信息
- 如果 Linear/Git 都查不到，会提示用户手动描述
- 输出格式兼容 Slack/Teams/飞书

---

## 📝 示例对话

```
用户：standup 怎么写
助手：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Standup 更新 — 2026-05-03
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 昨日完成
  • [ENG-234] 首页响应式布局完成
  • [ENG-238] 修复导航栏在移动端错位问题
  • [ENG-239] 修复搜索结果页分页 bug

🚧 今日计划
  • [ENG-240] 用户设置页面开发
  • [ENG-241] 集成测试编写

🚫 Blockers
  • 无

💭 备注
  • 下午 3 点设计评审会议
```

---

*最后更新：2026-05-03*
