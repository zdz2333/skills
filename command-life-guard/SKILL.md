---
name: command-life-guard
description: 终端命令急救工具 — 当 terminal 命令失败、超时、报 "BLOCKED"、退出码非零、或者命令执行后完全没反应时使用。自动诊断错误类型（超时/权限/网络/路径/资源），智能重试（指数退避），输出人类可读的错误报告和修复建议。触发场景：命令超时了、命令报了 BLOCKED、命令报 permission denied、命令报 connection refused、命令报 ENOENT 或 No such file、命令报 too many open files、命令卡死了不知道怎么停、命令失败了想知道原因、想对一个不可靠的命令加速重试。不要忽略任何可疑的错误输出，哪怕只是 warning — Command Life Guard 会帮你判断要不要处理。
trigger: "命令超时了"、"命令失败了"、"blocked"、"connection refused"、"重试一下"、"命令报错了"、"permission denied"、"No such file"、"too many open files"、"命令卡住了"
---

# Command Life Guard

> 终端命令失败了吗？别急着重输，让我来救。

## 使用示例

```
用户：git push 超时了，报 BLOCKED: Command timed out
助手：→ 触发 command-life-guard
     → 诊断：网络/认证/大文件三选一
     → 输出诊断报告 + 具体修复命令
     → 用户执行后恢复正常

用户：pip install 报 too many open files
助手：→ 触发 command-life-guard
     → 诊断：资源耗尽
     → 执行 ulimit -n 65536
     → 重新执行 pip install

用户：npm install 一直卡着不动
助手：→ 触发 command-life-guard
     → 诊断：网络/registry/权限
     → 给出 Ctrl+C + 换镜像方案
```

---

## 核心能力

### 1. 智能错误诊断

用 `scripts/diagnose.py` 分析错误输出，自动分类：

| 错误类型 | 典型关键词 | 解决方案 |
|---------|-----------|---------|
| **超时** | `timed out`, `BLOCKED`, `Timeout` | 增加 timeout，或拆分命令 |
| **权限不足** | `permission denied`, `EACCES`, `sudo` | 检查用户权限，或加 `sudo` |
| **路径错误** | `No such file`, `not found`, `ENOENT` | 检查路径拼写和目录是否存在 |
| **网络问题** | `connection refused`, `ConnectionReset`, `ECONNREFUSED` | 检查目标服务状态、端口、防火墙 |
| **资源耗尽** | `too many open files`, `out of memory`, `ENOSPC`, `disk full` | 清理资源或增加系统限制 |
| **进程僵死** | 命令执行后完全无输出、无法 Ctrl+C | 找到进程 PID，SIGTERM→SIGKILL |

```bash
# 诊断命令（直接运行）
python3 ~/.hermes/skills/command-life-guard/scripts/diagnose.py "错误信息"

# 或传入完整命令 + 输出
python3 ~/.hermes/skills/command-life-guard/scripts/diagnose.py "git push" "BLOCKED: Command timed out"
```

### 2. 智能重试（指数退避）

遇到以下错误自动重试（不用你手动重输）：
- 超时错误（`timed out`、`BLOCKED`）
- 临时网络错误（`Connection refused` 可能是服务刚启动）
- 暂时性资源满（`too many open files`）

重试策略：
```
第 1 次：立刻重试
第 2 次：等 2 秒
第 3 次：等 4 秒
第 4 次：等 8 秒
第 5 次：放弃，输出诊断报告
```

⚠️ **有副作用的命令不重试**：删除（`rm -rf`）、覆写、格式化类命令先确认。

### 3. 超时保护

遇到超慢命令，先用 `SIGTERM` 优雅终止，不是直接 `SIGKILL` 强制杀死。

---

## 标准诊断流程

### Step 1：收集信息

先不要重试，收集这些信息：

```bash
# 是什么命令？
echo "上一条命令：$(history | tail -1 | sed 's/ *[0-9]* *//')"

# 退出码是多少？（0 = 成功，非0 = 失败）
echo "退出码：$?"

# 网络通不通？
curl -s --connect-timeout 5 https://github.com > /dev/null && echo "网络 OK" || echo "网络问题"

# 目标服务在不在？
nc -zv github.com 443 -w 5
```

### Step 2：运行诊断脚本

```bash
python3 ~/.hermes/skills/command-life-guard/scripts/diagnose.py "错误信息"
```

脚本会输出：
- 错误类型判断
- 置信度（高/中/低）
- 具体修复命令（可以直接复制）

### Step 3：根据诊断结果行动

按照脚本输出的修复命令执行。如果置信度是"低"，说明可能是复合错误，手动检查：

```bash
# 检查命令本身是否有问题
<command> --help

# 检查依赖是否存在
which <command>   # 路径对不对
<command> -v      # 版本

# 检查权限
ls -la <path>     # 文件存在吗，权限够吗

# 检查系统资源
ulimit -n         # 打开文件数上限
df -h             # 磁盘空间
free -m           # 内存（Linux）
```

---

## 常见场景急救手册

### 场景 1：git push 超时

```bash
# 诊断
git status
git remote -v

# 如果是 HTTPS 认证问题
git config --get credential.helper

# 解决方案 A：增加 SSH timeout
GIT_SSH_COMMAND="ssh -o ConnectTimeout=15 -o ServerAliveInterval=60" git push

# 解决方案 B：换成 HTTPS 方式（如果 SSH 不通）
git remote set-url origin https://github.com/USER/REPO.git
git push
```

### 场景 2：pip / npm 安装超时

```bash
# 诊断
pip install --timeout=10 <package>
curl -s --connect-timeout 5 pypi.org

# 解决方案：换国内镜像
pip install -i https://mirrors.aliyun.com/pypi/simple/ <package>
npm install --registry=https://registry.npmmirror.com
```

### 场景 3：curl 请求挂住

```bash
# 诊断：加 timeout 和 verbose
curl -v --max-time 10 https://example.com

# 常见卡住原因和对策
# - DNS 解析慢 → 加 --dns-timeout
# - 连接建立慢 → 加 --connect-timeout
# - 传输慢 → 加 --max-time
curl --max-time 15 --dns-timeout 5 --connect-timeout 10 https://example.com
```

### 场景 4：进程僵死（命令执行后完全没反应）

```bash
# 在另一个 terminal 找到僵死进程
ps aux | grep <命令关键词>

# 优雅终止（先 SIGTERM，等 5 秒）
kill -15 <PID>

# 如果还在，等更久再强制
sleep 5 && kill -9 <PID>
```

### 场景 5：too many open files

```bash
# 诊断
ulimit -n
lsof | wc -l

# 临时增加 limit
ulimit -n 65536

# 永久方案（macOS）
echo "ulimit -n 65536" >> ~/.zshrc

# 永久方案（Linux）
sudo bash -c 'echo "* soft nofile 65536" >> /etc/security/limits.conf'
sudo bash -c 'echo "* hard nofile 65536" >> /etc/security/limits.conf'
```

---

## 快速命令参考

```bash
# 查看网络连通性（5秒超时）
curl -s --connect-timeout 5 https://github.com > /dev/null && echo "OK" || echo "网络问题"

# 测试端口连通性
nc -zv host port -w 5

# 诊断超时原因（macOS）
/usr/bin/time -l <command>

# 优雅终止所有 node 进程
pkill -15 -f "node"

# 查看最耗资源的进程
top -l 1 | head -20
```

---

## 注意事项

- **不要对有副作用的命令盲目重试**（删除、覆写类命令先确认）
- **重试间隔递增**（指数退避），避免雪崩
- **网络命令优先**检查防火墙和代理设置
- **权限问题**先确认是用户权限还是系统保护（SIP）
- **复合错误**（多个问题同时出现）先修复最上层的问题，再重新诊断
