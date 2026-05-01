---
name: shell-command-builder
description: 自然语言转 Shell 命令 — 把"我想在所有 js 文件里把这个变量改名"、"批量重命名一堆文件"、"查找并删除重复照片"这种需求翻译成正确的 shell 命令。当用户说"怎么用命令做"、"shell 怎么写"、"帮我写个脚本"、"命令怎么拼"、linux 怎么查/删/改/找、mac 怎么批量操作时触发。还会解释生成的命令在做什么。
trigger: 当用户说"怎么用命令"、"shell 怎么写"、"帮我写个脚本"、"命令怎么拼"、"帮我生成一个命令"、"linux 怎么"、"mac 怎么批量"、"怎么用终端"、"bash 怎么"、"怎么在终端里"
---

# Shell Command Builder — 自然语言 → Shell 命令

> 你说想做什么，我帮你写成正确的命令

## 使用示例

```
用户：我想把所有 .js 文件里的 foo 改成 bar
助手：→ 触发 shell-command-builder
     → 生成：find . -name "*.js" -exec sed -i 's/foo/bar/g' {} +
     → 解释：find 找文件，sed 执行替换，-i 直接修改原文件

用户：怎么查找大于 100MB 的文件
助手：→ 触发 shell-command-builder
     → 生成：find . -type f -size +100M
     → 解释：-type f 只找文件，-size +100M 大于100MB

用户：批量把文件名里的空格改成下划线
助手：→ 触发 shell-command-builder
     → 生成：for f in *\ *; do mv "$f" "${f// /_}"; done
     → 解释：for 循环遍历含空格文件，${f// /_} 是 bash 参数替换
```

## 💡 常见场景 → 命令模板

### 文件查找与操作

| 需求 | 命令 | 说明 |
|------|------|------|
| 找所有 .log 文件 | `find . -name "*.log"` | -name 支持通配符 |
| 找大于 100MB 的文件 | `find . -type f -size +100M` | -type f 只选文件 |
| 找最近 7 天修改的文件 | `find . -mtime -7` | -mtime 修改时间 |
| 查找并删除空文件 | `find . -empty -delete` | 危险！先加 -print 预览 |
| 查找重复文件 | `find . -type f -exec md5sum {} + \| sort \| uniq -D -w32` | MD5 比对 |

### 批量重命名

| 需求 | 命令 |
|------|------|
| 空格改下划线 | `for f in *\ *; do mv "$f" "${f// /_}"; done` |
| 大写改小写 | `for f in *; do mv "$f" "${f,,}"; done` |
| 加前缀 | `for f in *; do mv "$f" "prefix_$f"; done` |
| 删扩展名再添新 | `for f in *.txt; do mv "$f" "${f%.txt}.md"; done` |

### 文本处理

| 需求 | 命令 |
|------|------|
| 查找含关键词的行 | `grep -r "error" .` 或 `grep -rn "error" .` |
| 统计出现次数 | `grep -ro "error" . \| wc -l` |
| 替换文本 | `sed -i 's/old/new/g' file` |
| 查看文件第 10-20 行 | `sed -n '10,20p' file` |

### 进程与服务

| 需求 | 命令 |
|------|------|
| 查看进程占用内存 | `ps aux --sort=-%mem \| head -10` |
| 强制终止进程 | `kill -9 PID` 或 `pkill -f "进程名"` |
| 查看端口占用 | `lsof -i :8080` 或 `netstat -tlnp \| grep 8080` |
| 实时查看日志 | `tail -f /var/log/syslog` |

### 网络诊断

| 需求 | 命令 |
|------|------|
| 测试端口连通 | `nc -zv host port` |
| 查看路由表 | `ip route` 或 `route -n` |
| DNS 查询 | `dig domain` 或 `nslookup domain` |
| 带宽测速 | `speedtest-cli` |

## ⚠️ 危险命令警示

| 命令 | 风险 | 安全版 |
|------|------|--------|
| `rm -rf /` | 删根目录，数据全丢 | 永远不要跑 |
| `find . -delete` | 可能误删重要文件 | 先用 `-print` 预览 |
| `> file`（无前缀） | 清空文件 | `cat file` 先确认 |
| `chmod -R 777` | 安全漏洞 | 用 `755` 或 `644` |
| `dd if=x of=y` | 硬盘直接写入 | 确认 if/of 正确 |

## 📖 使用方法

**Step 1：描述你的需求**

尽量具体：
- ✅ "把所有 .html 文件里的版权年份从 2024 改成 2025"
- ✅ "查找 /tmp 目录下超过 30 天没访问的文件"
- ❌ "帮我处理文件"

**Step 2：AI 生成命令 + 解释**

我会给你：
1. 生成的命令（可直接复制）
2. 命令各部分解释
3. 可能的副作用和注意事项

**Step 3：安全确认**

对于有风险的操作，我会标注 ⚠️，请确认后再执行。

## 🔍 验证命令正确性

```bash
# 用 echo 预览效果（不实际执行）
echo "mv old_name new_name"

# 用 -n 测试 find（不实际删除）
find . -name "*.tmp" -print

# 用 | cat 预览管道效果
cat file | sort | uniq
```

## 💡 命令速查

```
Ctrl+C      # 终止当前命令
Ctrl+Z      # 挂起后台
Ctrl+L      # 清屏
!!          # 重复上一条命令
!$          # 上一条命令的最后一个参数
```

---

*灵感来源：tldr-pages, cheat.sh, GitHub CLI*
