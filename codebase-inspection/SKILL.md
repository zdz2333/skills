---
name: codebase-inspection
description: 分析代码库行数、语言构成、代码/注释比例的工具。当用户问"这个项目有多少行代码"、"XX 项目多大"、"语言分布"、"各语言占比"、"统计代码行数"、"查看代码规模"时使用。通过 pygount 自动检测项目类型（Python/JS/Go/Rust等），智能选择排除目录（node_modules/venv/dist等），输出格式化的统计报告。适合在 code review、架构评估、技术选型、或者想知道一个 repo 真实规模时使用。
trigger: "有多少行代码"、"项目多大"、"语言分布"、"代码行数"、"repo 大小"、"统计代码"、"代码规模"、"各语言占比"
---

# Codebase Inspection

用 pygount 分析代码库：行数统计、语言构成、代码 vs 注释比例、文件数量。

## 使用示例

```
用户：这个项目有多少行代码？
助手：→ 触发 codebase-inspection
     → 运行 analyze.py 自动检测项目类型
     → 输出语言分布表 + 总行数
     → 如果检测到 Python 项目，排除 venv 并专注 .py 文件

用户：看看这个 repo 的语言分布
助手：→ 触发 codebase-inspection
     → python3 scripts/analyze.py <path> --format=summary
     → 输出各语言文件数、代码行数、注释行数、占比

用户：go.mod 那个项目有多大？
助手：→ 检测为 Go 项目
     → 排除 .git、vendor、node_modules
     → 输出 Go 文件统计
```

## 快速开始

```bash
# 安装（如果还没有）
pip install pygount

# 自动检测项目类型并分析（推荐）
python3 ~/.hermes/skills/github/codebase-inspection/scripts/analyze.py /path/to/repo

# 只看汇总表
python3 ~/.hermes/skills/github/codebase-inspection/scripts/analyze.py /path/to/repo --format=summary

# 指定语言（如只看 Python）
python3 ~/.hermes/skills/github/codebase-inspection/scripts/analyze.py /path/to/repo --suffix=py
```

## 脚本功能：analyze.py

`scripts/analyze.py` 自动完成：

1. **项目类型检测** — 扫描 `package.json`、`go.mod`、`Cargo.toml` 等文件，自动识别 Python/JS/Go/Rust/Java 等项目
2. **智能排除目录** — 根据检测到的类型，自动组合最佳 `--folders-to-skip` 参数：
   - Python 项目 → 排除 `venv、__pycache__、.pytest_cache、.mypy_cache`
   - JS/TS 项目 → 排除 `node_modules、dist、.next、.turbo`
   - Go 项目 → 排除 `vendor、node_modules、dist`
   - Rust 项目 → 排除 `target、.git`
3. **格式化输出** — 自动以汇总表格式展示结果

### 手动指定参数

如果脚本检测不准确，可以手动指定：

```bash
# Python 项目
pygount --format=summary \
  --folders-to-skip=".git,venv,.venv,__pycache__,dist,build,.tox,.eggs" \
  .

# JavaScript/TypeScript 项目
pygount --format=summary \
  --folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage" \
  .

# 通用（适合混杂项目）
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,dist,build,.next,.tox,vendor" \
  .
```

## 常用参数

```bash
# 只看某种语言
pygount --suffix=py --format=summary .
pygount --suffix=py,yaml,yml --format=summary .

# JSON 输出（程序调用）
pygount --format=json .

# 按代码行数排序（看最大文件）
pygount . | sort -t$'\t' -k1 -nr | head -20
```

## 结果解读

汇总表列含义：

| 列 | 含义 |
|----|------|
| **Language** | 检测到的编程语言 |
| **Files** | 该语言的文件数量 |
| **Code** | 实际代码行数 |
| **Comment** | 注释和文档行数 |
| **%** | 占总行数的百分比 |

特殊伪语言：

| 类型 | 含义 |
|------|------|
| `__empty__` | 空文件 |
| `__binary__` | 二进制文件（图片、编译文件等）|
| `__generated__` | 自动生成的文件 |
| `__unknown__` | 无法识别的文件类型 |

## 常见陷阱

1. **必须加 `--folders-to-skip`** — 不排除 `node_modules/venv` 会让 pygount 跑几分钟或卡死
2. **Markdown 显示 0 代码行** — pygount 把所有 Markdown 内容算作注释，不是代码，这是预期行为
3. **大单体仓库** — 先用 `--suffix` 指定语言，不要全量扫描
4. **JSON 文件行数偏低** — pygount 对 JSON 统计保守，精确值用 `wc -l` 直接查

## 验证步骤

1. 任意选一个项目目录
2. 运行 `python3 ~/.hermes/skills/github/codebase-inspection/scripts/analyze.py <path> --format=summary`
3. 确认输出表格有语言分布和总行数
4. 如果想看特定语言，加上 `--suffix=py`（或其他后缀）
