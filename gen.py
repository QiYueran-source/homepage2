#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一生成脚本入口
用于管理所有页面生成任务
"""

import argparse
import subprocess
import sys
from pathlib import Path

def run_script(script_name, *args):
    """运行指定的生成脚本或模块"""
    try:
        if "." in script_name:
            # 模块形式：scripts.home.generator
            module_parts = script_name.split(".")
            module_name = ".".join(module_parts[:-1])
            func_name = module_parts[-1]

            # 动态导入模块
            module = __import__(module_name, fromlist=[func_name])
            func = getattr(module, func_name)
            # 调用生成函数
            func(*args)
        else:
            # 传统脚本形式
            script_path = Path(__file__).parent / "scripts" / f"{script_name}.py"
            if not script_path.exists():
                print(f"错误：脚本 {script_name}.py 不存在")
                return False

            cmd = [sys.executable, str(script_path)] + list(args)
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        print(f"✅ {script_name} 生成完成")
        return True
    except Exception as e:
        print(f"❌ {script_name} 生成失败：{e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="统一页面生成器")
    parser.add_argument(
        "targets",
        nargs="*",
        help="要生成的页面（默认：all）"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细输出"
    )

    args = parser.parse_args()

    # 定义生成任务映射
    tasks = {
        "home": "scripts.home.generator.generate_home_html",
        "resume": "scripts.sections.resume.generator.generate_resume_page",
        "blog": "scripts.blog.generator.scan_and_generate_blog",
    }

    # 处理默认值和验证
    targets = args.targets if args.targets else ["all"]

    # 验证参数
    valid_targets = ["home", "resume", "all"]
    for target in targets:
        if target not in valid_targets:
            parser.error(f"无效选择: '{target}' (选择: {', '.join(valid_targets)})")

    # 执行生成任务
    success_count = 0
    total_count = 0

    if "all" in targets:
        targets = list(tasks.keys())
    
    for target in targets:
        if target in tasks:
            total_count += 1
            # 直接运行对应的脚本或模块
            if run_script(tasks[target]):
                success_count += 1
        else:
            print(f"警告：未知目标 '{target}'")
    
    # 输出结果统计
    if total_count > 0:
        print(f"\n📊 生成统计：{success_count}/{total_count} 成功")
        if success_count == total_count:
            print("🎉 所有页面生成完成！")
            return 0
        else:
            print("⚠️ 部分页面生成失败")
            return 1
    else:
        print("ℹ️ 没有执行任何生成任务")
        return 0

if __name__ == "__main__":
    sys.exit(main())