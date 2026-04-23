---
name: first-commit-guide
description: Git 第一次提交指南 — 当用户第一次接触 git、不知道从哪里开始、害怕弄乱代码、想问"怎么用 git"时使用。自动诊断项目状态，生成最佳 first commit 模板，解释每一步在做什么。触发场景：第一次用 git、刚学编程不知道代码怎么管理、看了教程还是不会、第一次 push 到 GitHub、不知道 add 和 commit 区别、git init 后不知道下一步。
trigger: 当用户说"git 怎么用"、"第一次用 git"、"怎么提交代码"、"git init 之后怎么做"、"怎么 push"、"add 和 commit 是什么"、"git 教程看不懂"、"代码怎么管理"、"我想学 git"、"第一次 push 到 GitHub"、"git 怎么开始"
---

# 🚀 First Commit Guide - Git 第一次提交

> *从零到第一次 push，让 git 不再神秘*

## 🎯 解决什么问题

- 刚学编程，代码只存在本地，不知道怎么管理版本
- 看了 git 教程，概念太多，越看越懵
- `git init` 之后不知道接下来该干嘛
- 不知道 `add` 和 `commit` 有什么区别
- 想把代码 push 到 GitHub 但不知道从哪开始

**你的第一次 commit，今天搞定。**

---

## 📖 使用方法

### Step 1：诊断当前项目状态

先看看项目有没有被 git 管理：

```bash
cd 你的项目目录
git status
```

**结果 A：** 显示 `fatal: not a git repository`  
→ 项目还没初始化，需要先 `git init`

**结果 B：** 显示一堆文件名（红色或绿色）  
→ 已经有 git 仓库，跳到 Step 2

---

### Step 2：创建 .gitignore（先做这个!）

在项目根目录创建 `.gitignore` 文件，内容：

```
# macOS
.DS_Store

# Node
node_modules/
npm-debug.log*

# Python
__pycache__/
*.py[cod]
venv/

# IDE
.vscode/
.idea/

# 环境变量
.env
.env.local
```

**为什么先做这个？** 避免把不需要的文件（密码、依赖库）传上去。

---

### Step 3：添加文件并提交

```bash
# 添加所有文件（除了 .gitignore 里声明的）
git add .

# 写一条提交信息
git commit -m "first commit: initial project setup"

# 设置你的名字和邮箱（只需要做一次）
git config user.name "你的名字"
git config user.email "你的邮箱"
```

**常见错误：**
- `please tell me who you are` → 没配置 name/email，先执行上面的 config 命令
- `nothing to commit` → 所有文件都在 .gitignore 里，或者已经提交过了

---

### Step 4：连接 GitHub（可选）

```bash
# 在 GitHub 创建新仓库后，复制 SSH/HTTPS 地址
# 例如：git@github.com:username/project-name.git

# 添加远程仓库
git remote add origin git@github.com:username/project-name.git

# 第一次推送
git push -u origin master
```

**如果遇到权限错误：** 需要先配置 SSH Key，见 [github-auth skill](../github/github-auth/SKILL.md)

---

## 🎯 对话示例

```
用户: "我刚学编程，代码都是直接保存在文件夹里，想用 git 管理怎么做？"

助手: # 🚀 First Commit Guide

先看看你的项目有没有被 git 管理：
```bash
cd 你的项目目录
git status
```

**情况 1：显示 `fatal: not a git repository`**
→ 还没初始化，运行：
```bash
git init
```

**情况 2：显示文件列表**
→ 已经有 git 仓库，我们可以开始提交了！

---

告诉我你的项目在哪个目录，我来一步步带你做。
```

---

```
用户: "git init 之后我就不知道该干嘛了"

助手: 很好，你已经完成了最难的一步！接下来只有 4 步：

**Step 1：创建 .gitignore**
告诉 git 忽略哪些文件（依赖库、密码等）

**Step 2：添加文件**
```bash
git add .
```

**Step 3：写提交信息**
```bash
git commit -m "first commit"
```

**Step 4：设置你的名字（首次）**
```bash
git config user.name "你的名字"
git config user.email "你的邮箱"
```

我们来操作第一步 — 在你的项目目录里创建一个 `.gitignore` 文件。
```

---

## ⚡ 30 秒速成版

如果只需要最快速度提交：

```bash
git init                    # 初始化
git add .                   # 添加所有文件
git commit -m "first commit" # 提交
git config user.name "名字" && git config user.email "邮箱"  # 首次配置
```

**然后看你想不想 push 到 GitHub：**
- 想 → 告诉我你的 GitHub 仓库地址
- 不想 → 到这里就够了！

---

## ⚠️ 注意事项

- **第一次 commit 不用在意内容质量** —— git 的意义就是记录历史，随时可以回滚
- **提交信息要用英文还是中文？** —— 都可以，但保持一致
- **提交信息写什么？** —— `first commit` 或 `initial setup` 足够，以后用 `feat:`, `fix:` 等规范
- **不小心提交了密码？** → 立即看 [command-life-guard](../command-life-guard/SKILL.md) 的"撤销提交"部分

---

## 🔍 验证步骤

```bash
# 验证 git 是否正常工作
git status

# 期望输出：nothing to commit, working tree clean
# 或者显示已跟踪的文件

# 验证提交历史
git log --oneline

# 期望输出：你的 first commit 记录
```

---

## 📚 相关 Skill

- [github-auth](../github/github-auth/SKILL.md) — GitHub SSH Key 配置
- [github-pr-workflow](../github/github-pr-workflow/SKILL.md) — 多人协作流程
- [command-life-guard](../command-life-guard/SKILL.md) — 撤销/修复提交错误

---

*灵感来源：Git 官方文档 + 无数被 git 劝退的新手*
