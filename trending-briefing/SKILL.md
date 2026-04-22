---
name: trending-briefing
description: 每日极客情报站 — 自动抓取 GitHub Trending + 技术新闻，生成结构化日报。解决"没时间刷 GitHub 但想知道今天在流行什么"的痛点。当用户说"今天有什么新鲜的"、"帮我看看 GitHub trending"、"行业动态"、"技术早餐"、"今日速递"或任何想了解当天技术趋势的场景，都应该触发此技能。
trigger: 当用户说"今天有什么新鲜的"、"帮我看看 GitHub trending"、"行业动态"、"技术早餐"、"今日速递"、"最近流行什么"、"技术新闻"、"有什么值得关注的"、"刷一下 trending"、"今日热点"时调用
---

# 📊 Trending Briefing - 每日极客情报站

> 每天 5 分钟，搞定当天技术趋势

## 🎯 解决什么问题

- **没时间刷 GitHub Trending**，但想知道今天在流行什么
- 想快速了解 Productivity 领域的最新动态
- 刷 Twitter/Reddit 太费时间，需要有人帮你筛选

## 💡 解决方案

自动化抓取 + 整理 = 一份结构清晰的日报

## 📖 使用方法

### 触发
```
> "今天有什么新鲜的技术动态？"
> "帮我看看 GitHub trending"
> "行业动态"
> "技术早餐"
```

### 执行步骤

**Step 1: 抓取 GitHub Trending**
```bash
# 下载当天 Trending 页面
curl -s "https://github.com/trending" -o ~/.hermes/trending-briefing/trending.html

# 解析提取：repo 名、描述、语言、star 数
python3 ~/.hermes/skills/trending-briefing/scripts/parse_trending.py
```

**Step 2: 生成结构化报告**
```python
# 脚本自动整理为以下格式：

## 📅 [日期] 极客日报

### 🔥 GitHub Trending Top 5
1. **[repo名]** ⭐ [star数]
   描述...
   [语言]
2. ...

### 💡 值得关注的亮点
- [亮点1]
- [亮点2]

### 🎯 我的关注点
- 今天想深入研究：[项目名]
- 潜在机会：[应用场景]
```

**Step 3: 投递报告**
直接输出给用户，或保存到指定位置

## 🔍 验证步骤

手动测试：
```bash
# 检查脚本是否正常工作
python3 ~/.hermes/skills/trending-briefing/scripts/parse_trending.py

# 应该输出格式化的 trending 列表
```

## 📁 文件结构

```
trending-briefing/
├── SKILL.md           # 本文件
└── scripts/
    └── parse_trending.py   # 解析脚本
```

## ⚠️ 注意事项

- GitHub Trending 每天 0点（UTC）更新，数据有 24 小时延迟
- 解析依赖 HTML 结构，GitHub 改版后可能需要更新正则
- 建议配合 cronjob 每天固定时间运行

### 🎯 对话示例

```
用户: "今天 GitHub 上有什么新鲜的？"

助手:
## 📅 2026-04-22 极客日报

### 🔥 GitHub Trending Top 5
1. **thunderbolt** ⭐ 2.1k
   You Control: Choose your models. Own your data.
   TypeScript
2. **claude-context** ⭐ 1.8k
   Code search MCP for Claude Code...
   TypeScript
...

### 💡 今日亮点
- MCP 相关项目持续火热
- Agents 开发入门课程新上榜

### 🎯 建议关注
- 想快速了解 Agents → `ai-agents-for-beginners`（Jupyter Notebook）
- 想本地运行模型 → 关注 llama.cpp 相关生态
```
