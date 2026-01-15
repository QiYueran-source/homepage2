#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stack 技术栈模块生成器
生成主页技术栈预览
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json

def setup_template_env():
    """设置 Jinja2 模板环境"""
    template_dir = Path(__file__).parent.parent.parent.parent / "templates"
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

def get_tech_icon(tech_name):
    """智能识别技术图标"""
    icon_map = {
        # 编程语言
        'python': 'fab fa-python',
        'javascript': 'fab fa-js',
        'typescript': 'fab fa-js-square',
        'java': 'fab fa-java',
        'cpp': 'fas fa-code',
        'c': 'fas fa-code',
        'rust': 'fab fa-rust',
        'go': 'fab fa-golang',
        'php': 'fab fa-php',
        'ruby': 'fas fa-gem',
        'swift': 'fab fa-swift',
        'kotlin': 'fas fa-code',

        # 前端框架
        'react': 'fab fa-react',
        'vue': 'fab fa-vuejs',
        'angular': 'fab fa-angular',
        'svelte': 'fas fa-code',

        # 后端框架
        'flask': 'fas fa-flask',
        'django': 'fas fa-code-branch',
        'fastapi': 'fas fa-rocket',
        'express': 'fab fa-node-js',
        'spring': 'fas fa-leaf',

        # 数据科学
        'pandas': 'fas fa-table',
        'numpy': 'fas fa-calculator',
        'scikit-learn': 'fas fa-brain',
        'tensorflow': 'fas fa-project-diagram',
        'pytorch': 'fas fa-fire',
        'plotly': 'fas fa-chart-line',
        'matplotlib': 'fas fa-chart-bar',
        'seaborn': 'fas fa-palette',

        # 数据库
        'mysql': 'fas fa-database',
        'postgresql': 'fas fa-database',
        'mongodb': 'fas fa-leaf',
        'redis': 'fas fa-server',
        'sqlite': 'fas fa-database',

        # 工具
        'docker': 'fab fa-docker',
        'kubernetes': 'fas fa-dharmachakra',
        'git': 'fab fa-git',
        'github': 'fab fa-github',
        'gitlab': 'fab fa-gitlab',
        'jenkins': 'fas fa-cogs',
        'nginx': 'fas fa-server',

        # 云服务
        'aws': 'fab fa-aws',
        'azure': 'fab fa-microsoft',
        'gcp': 'fab fa-google',

        # 其他
        'linux': 'fab fa-linux',
        'ubuntu': 'fab fa-ubuntu',
        'windows': 'fab fa-windows',
        'macos': 'fab fa-apple'
    }

    # 精确匹配
    tech_lower = tech_name.lower()
    if tech_lower in icon_map:
        return icon_map[tech_lower]

    # 模糊匹配（包含关键词）
    for key, icon in icon_map.items():
        if key in tech_lower or tech_lower in key:
            return icon

    # 默认图标
    return 'fas fa-code'

def generate_stack_preview_html():
    """生成技术栈预览区域HTML"""
    # 设置模板环境
    env = setup_template_env()

    # 读取配置
    root_dir = Path(__file__).parent.parent.parent.parent
    title_file = root_dir / "data" / "stack" / "title.json"
    stack_file = root_dir / "data" / "stack" / "stack.json"

    title_config = load_json_file(title_file)
    stack_data = load_json_file(stack_file)

    if not title_config or not stack_data:
        print("无法加载stack配置")
        return ""

    # 生成图标映射
    icon_map = {}
    for tech_name in stack_data.keys():
        icon_map[tech_name] = get_tech_icon(tech_name)

    template = env.get_template('home/stack_preview.html')
    return template.render(
        title=title_config.get('title', '技术栈'),
        subtitle=title_config.get('subtitle', '技术栈介绍'),
        stack_data=stack_data,
        icon_map=icon_map
    )

def generate_stack_page_and_home():
    """生成stack预览并更新主页"""
    # 更新主页预览
    try:
        from scripts.home.generator import generate_home_html
        generate_home_html()
        print("✅ 主页预览已更新")
    except Exception as e:
        print(f"⚠️ 更新主页预览失败: {e}")

if __name__ == "__main__":
    html_content = generate_stack_preview_html()
    print("技术栈预览HTML已生成")
    print(html_content[:300] + "..." if len(html_content) > 300 else html_content)
