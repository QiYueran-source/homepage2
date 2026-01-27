#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误页面生成器
生成404等错误页面
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def setup_template_env():
    """设置 Jinja2 模板环境"""
    template_dir = Path(__file__).parent.parent.parent / "templates"
    return Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )


def generate_404_page():
    """生成404错误页面"""
    # 设置模板环境
    env = setup_template_env()
    
    # 获取根目录
    root_dir = Path(__file__).parent.parent.parent
    
    # 读取404模板
    template = env.get_template('404.html')
    html_content = template.render()
    
    # 输出路径
    output_file = root_dir / "html" / "404.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"404 错误页面 HTML 已生成: {output_file}")


def generate_error_pages():
    """生成所有错误页面"""
    generate_404_page()


if __name__ == "__main__":
    generate_error_pages()
