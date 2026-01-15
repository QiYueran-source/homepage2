#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成简历预览区域的脚本
供 gen_home.py 调用
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json

def setup_template_env():
    """设置 Jinja2 模板环境"""
    template_dir = Path(__file__).parent.parent.parent / "templates"
    return Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )

def load_json_file(file_path):
    """加载 JSON 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载 {file_path} 失败: {e}")
        return None

def generate_resume_preview_html():
    """生成简历预览区域HTML - 供外部调用的接口"""
    # 设置模板环境
    env = setup_template_env()

    # 读取简历配置数据
    root_dir = Path(__file__).parent.parent.parent
    resume_config_file = root_dir / "data" / "resume" / "title.json"
    resume_config = load_json_file(resume_config_file)

    if not resume_config:
        print("无法加载简历配置数据")
        return ""

    template = env.get_template('resume_preview.html')
    return template.render(**resume_config)

if __name__ == "__main__":
    html_content = generate_resume_preview_html()
    print("简历预览区域HTML已生成")
    print(html_content[:200] + "..." if len(html_content) > 200 else html_content)
