#!/usr/bin/env python3
"""
Command Life Guard - 错误诊断脚本
自动分析错误输出，分类为：超时/权限/路径/网络/资源/进程僵死
输出：错误类型 + 置信度 + 具体修复命令
"""

import sys
import re
import json


ERROR_PATTERNS = {
    "timeout": {
        "keywords": ["timed out", "BLOCKED", "timeout", "TIMEOUT", "TimedOut"],
        "confidence": "高",
        "solution": "增加 timeout 参数，或拆分命令为多个小命令",
        "commands": [
            "curl -v --max-time 30 <url>  # 加长超时",
            "# 如果是 git 命令：",
            "GIT_SSH_COMMAND=\"ssh -o ConnectTimeout=15\" git push",
        ],
    },
    "permission": {
        "keywords": ["permission denied", "EACCES", "sudo", "Operation not permitted", "EPERM"],
        "confidence": "高",
        "solution": "检查是否是用户权限不足，或需要 sudo",
        "commands": [
            "# 检查当前用户",
            "whoami && id",
            "# 检查文件权限",
            "ls -la <path>",
            "# 如果需要 sudo",
            "sudo <command>",
        ],
    },
    "path": {
        "keywords": ["No such file", "not found", "ENOENT", "not exist", "does not exist"],
        "confidence": "高",
        "solution": "检查路径拼写、文件名大小写、目录是否存在",
        "commands": [
            "# 确认路径存在",
            "ls -la <path>",
            "# 如果是命令找不到",
            "which <command>",
            "type <command>",
        ],
    },
    "network": {
        "keywords": ["connection refused", "ECONNREFUSED", "ConnectionReset", "connection reset", "Network is unreachable", "Name or service not known", "Could not resolve host"],
        "confidence": "高",
        "solution": "检查目标服务是否在跑、端口对不对、网络通不通、防火墙",
        "commands": [
            "# 测试网络连通性",
            "curl -v --connect-timeout 5 <url>",
            "# 测试端口",
            "nc -zv <host> <port> -w 5",
            "# 检查 DNS",
            "nslookup <host>",
            "# 如果是自建服务，检查是否在跑",
            "ps aux | grep <service>",
            "curl localhost:<port>",
        ],
    },
    "resource": {
        "keywords": ["too many open files", "out of memory", "ENOSPC", "disk full", "Cannot allocate memory", "EMFILE", "max user processes"],
        "confidence": "高",
        "solution": "清理系统资源，或增加对应的系统限制",
        "commands": [
            "# 检查打开文件数",
            "ulimit -n",
            "lsof | wc -l",
            "# 临时增加限制",
            "ulimit -n 65536",
            "# 检查磁盘空间",
            "df -h",
            "# 检查内存",
            "free -m  # Linux",
            "top -l 1 | head -10  # macOS",
        ],
    },
    "zombie": {
        "keywords": ["<stdin: is a channel>", " hangs", "无响应", "卡住", "僵死"],
        "confidence": "中",
        "solution": "进程可能僵死，找到 PID 并优雅终止",
        "commands": [
            "# 在另一个 terminal",
            "ps aux | grep <command>",
            "# 优雅终止",
            "kill -15 <PID>",
            "# 等 5 秒后强制终止",
            "sleep 5 && kill -9 <PID>",
        ],
    },
}


def classify_error(error_text: str) -> dict:
    """分析错误文本，返回错误类型和修复建议"""
    error_text = error_text.lower()

    results = []
    for error_type, info in ERROR_PATTERNS.items():
        matches = [kw for kw in info["keywords"] if kw.lower() in error_text]
        if matches:
            results.append({
                "type": error_type,
                "confidence": info["confidence"],
                "matched_keywords": matches,
                "solution": info["solution"],
                "commands": info["commands"],
            })

    # 按置信度排序
    order = {"高": 0, "中": 1, "低": 2}
    results.sort(key=lambda x: order.get(x["confidence"], 2))

    return results


def output_text(results: list) -> str:
    """输出人类可读的诊断报告"""
    if not results:
        return "❓ 无法识别错误类型。请手动检查：\n  - 命令本身是否有问题（--help）\n  - 依赖是否存在（which, type）\n  - 网络通不通（curl）\n  - 文件路径对不对（ls -la）"

    lines = []
    for i, r in enumerate(results, 1):
        emoji = "🔴" if r["confidence"] == "高" else "🟡"
        lines.append(f"{emoji} [{r['confidence']}置信度] 错误类型：{r['type']}")
        lines.append(f"   匹配关键词：{', '.join(r['matched_keywords'])}")
        lines.append(f"   建议：{r['solution']}")
        lines.append(f"   可执行命令：")
        for cmd in r["commands"]:
            lines.append(f"     {cmd}")
        lines.append("")

    return "\n".join(lines)


def output_json(results: list) -> str:
    """输出 JSON 格式（给程序用）"""
    return json.dumps(results, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 2:
        print("用法: diagnose.py <错误信息> [--json]")
        print("示例: diagnose.py 'git push 报了 BLOCKED: Command timed out'")
        sys.exit(1)

    error_text = sys.argv[1]
    use_json = "--json" in sys.argv

    results = classify_error(error_text)

    if use_json:
        print(output_json(results))
    else:
        print(output_text(results))


if __name__ == "__main__":
    main()
