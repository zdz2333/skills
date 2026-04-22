#!/usr/bin/env python3
"""
Codebase Inspection - 自动分析脚本
根据检测到的项目类型，自动选择最佳 --folders-to-skip 参数，
运行 pygount 并格式化输出。
"""

import subprocess
import argparse
import os
import sys


# 项目类型自动检测
PROJECT_SIGNATURES = {
    "python": {
        "files": ["setup.py", "pyproject.toml", "requirements.txt", "Pipfile", ".python-version"],
        "skip": ".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache,.pytest_cache",
    },
    "javascript": {
        "files": ["package.json", "yarn.lock", "pnpm-lock.yaml", ".npmrc"],
        "skip": ".git,node_modules,dist,build,.next,.cache,.turbo,coverage,.parcel-cache",
    },
    "typescript": {
        "files": ["tsconfig.json", "package.json"],
        "skip": ".git,node_modules,dist,build,.next,.cache,.turbo,coverage,.parcel-cache,dist",
    },
    "go": {
        "files": ["go.mod", "go.sum"],
        "skip": ".git,node_modules,venv,.cache,dist,build,__pycache__",
    },
    "rust": {
        "files": ["Cargo.toml", "Cargo.lock"],
        "skip": ".git,node_modules,venv,.cache,target,dist,build,__pycache__",
    },
    "java": {
        "files": ["pom.xml", "build.gradle", "gradlew"],
        "skip": ".git,node_modules,venv,.cache,dist,build,target,.gradle",
    },
    "ruby": {
        "files": ["Gemfile", "Gemfile.lock", "Rakefile"],
        "skip": ".git,node_modules,venv,.cache,vendor/bundle,coverage,.bundle",
    },
    "kotlin": {
        "files": ["build.gradle.kts", "settings.gradle.kts"],
        "skip": ".git,node_modules,venv,.cache,dist,build,target,.gradle",
    },
    "swift": {
        "files": ["Package.swift"],
        "skip": ".git,node_modules,venv,.cache,dist,build,.build",
    },
    "c": {
        "files": ["CMakeLists.txt", "Makefile", ".clang-format"],
        "skip": ".git,node_modules,venv,.cache,dist,build,__pycache__,vendor",
    },
}


def detect_project_type(repo_path: str) -> list:
    """检测项目类型，返回匹配的列表"""
    detected = []
    for ptype, info in PROJECT_SIGNATURES.items():
        for fname in info["files"]:
            if os.path.exists(os.path.join(repo_path, fname)):
                if ptype not in detected:
                    detected.append(ptype)
    return detected


def build_skip_arg(project_types: list) -> str:
    """根据项目类型组合 skip 参数"""
    base_skip = ".git,node_modules,venv,.venv,__pycache__,.cache,dist,build"

    specific_skips = []
    for ptype in project_types:
        specific_skips.append(PROJECT_SIGNATURES[ptype]["skip"].split(","))

    all_skips = set(base_skip.split(","))
    for skip_list in specific_skips:
        all_skips.update(skip_list)

    return ",".join(sorted(all_skips))


def run_pygmentize():
    """检查 pygount 是否可用"""
    try:
        result = subprocess.run(
            ["pygount", "--version"],
            capture_output=True, text=True
        )
        return True
    except FileNotFoundError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Codebase analysis with automatic type detection")
    parser.add_argument("path", nargs="?", default=".", help="Repository path (default: .)")
    parser.add_argument("--format", choices=["summary", "json", "detail"], default="summary",
                        help="Output format (default: summary)")
    parser.add_argument("--suffix", default=None, help="File suffixes to include (e.g. py,yaml)")
    parser.add_argument("--dry-run", action="store_true", help="Show command without running")
    args = parser.parse_args()

    # 检测项目类型
    detected = detect_project_type(args.path)
    if detected:
        print(f"🔍 检测到项目类型：{', '.join(detected)}")
    else:
        print("🔍 未识别特定项目类型，使用通用排除列表")

    skip = build_skip_arg(detected)
    print(f"📁 排除目录：{skip}\n")

    # 构建命令
    cmd = ["pygount", f"--folders-to-skip={skip}"]
    if args.format == "json":
        cmd.append("--format=json")
    elif args.format == "detail":
        pass  # 默认就是 detail 格式
    else:
        cmd.append("--format=summary")

    if args.suffix:
        cmd.append(f"--suffix={args.suffix}")

    cmd.append(args.path)

    if args.dry_run:
        print(" ".join(cmd))
        return

    # 运行
    if not run_pygmentize():
        print("❌ pygount 未安装，先运行：")
        print("  pip install pygount")
        sys.exit(1)

    print("📊 运行分析...\n")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
