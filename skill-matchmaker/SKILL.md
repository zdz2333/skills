---
name: skill-matchmaker
description: Skill 推荐助手 — 根据需求描述，推荐最合适的 Hermes Skill。当用户说"我该用哪个 skill"、"这个需求用什么"、"我不知道该用哪个"、"帮我找 xxx skill"、"哪个 skill 能做 xxx"时触发。以 76+ 个 Skill 目录为知识库，AI 理解需求后精准推荐。
trigger: 当用户说"我该用哪个 skill"、"这个需求用什么"、"我不知道该用哪个"、"帮我找 xxx"、"哪个 skill 能做 xxx"、"我没有头绪该用哪个"、"推荐个合适的 skill"、"这个情况用什么工具"、"这种情况适合什么 skill"
---

# Skill Matchmaker — 需求 → 精准推荐

> 描述你的需求，我帮你找到最合适的 Skill

## 🎯 解决什么问题

Hermes 有 76+ 个 Skill，面对具体需求时不知道该用哪个？

- "我想做 xxx，该用什么 skill？"
- "我的需求该找哪个？"
- "这种情况用什么工具？"

**Skill Matchmaker** 以完整的 Skill 目录为知识库，理解你的需求后精准推荐。

## 📖 使用方法

### Step 1：描述你的需求

```
我需要：[你的需求描述]

示例：
- "我想自动抓取某个网页的内容"
- "帮我分析一下这个代码库"
- "我需要生成一张架构图"
- "想找一个帮我写周报的工具"
- "怎么给图片去背景"
```

### Step 2：AI 精准推荐

系统会从 76+ Skill 知识库中匹配，给出：

1. **最佳匹配** — 最适合的 Skill 名称
2. **推荐理由** — 为什么这个 Skill 适合你的需求
3. **使用入口** — 怎么调用这个 Skill

### Step 3：直接使用

```
推荐：webpage-fetch（网页内容提取）

推荐理由：这个 Skill 专门处理"抓取网页内容"的需求，
         支持多种提取方式，能处理动态和静态页面。

使用方式：直接说"帮我抓取 xxx 网页的内容"
```

## 🔍 推荐逻辑

不是关键词搜索，而是 AI 理解需求本质后推荐：

| 需求 | 推荐 | 原因 |
|------|------|------|
| "抓取网页" | `dogfood` | 内置网页抓取和内容提取工具 |
| "生成图片" | `creative/pixel-art` 等 | 多个图片生成相关 Skill |
| "写代码" | `autonomous-ai-agents/*` | 各类代码生成 Agent |
| "查新闻" | `trending-briefing` | GitHub Trending + 技术新闻 |

## 💡 示例对话

```
用户：我想知道今天 GitHub 流行什么
→ 推荐：trending-briefing
  理由：专门抓取 GitHub Trending，生成每日技术简报
  触发词："今天有什么新鲜的"、"技术早餐"

用户：我的正则表达式不工作
→ 推荐：regex-explainer
  理由：解释正则含义，诊断为什么不工作
  触发词："正则怎么读"、"为什么我的正则不工作"

用户：我要写一个自动化流程
→ 推荐：software-development/plan
  理由：多步骤任务规划，帮助拆解复杂工作流
  触发词："帮我规划一下"、"怎么做这个任务"

用户：帮我写个 shell 脚本
→ 推荐：shell-command-builder
  理由：自然语言转 Shell 命令，支持批量操作
  触发词："帮我写个脚本"、"shell 怎么写"

用户：我想做一张数据图表
→ 推荐：creative/architecture-diagram 或 data-science
  理由：diagram 生成架构图，data-science 处理数据可视化
  触发词："生成图表"、"画个图"
```

## ⚠️ 限制说明

- 推荐基于 Skill 目录知识库，最新添加的 Skill 可能未收录
- 如果没有匹配到合适的 Skill，会推荐最相关的几个并说明原因

---

*Skill 知识库：76+ Hermes Skills，定期同步*
