#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docs 文档下载模块生成器
生成文档列表页面和主页预览
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json
import shutil

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

def get_file_info(filename):
    """获取文件信息"""
    file_path = Path(__file__).parent.parent.parent.parent / "data" / "docs" / filename

    if file_path.exists():
        # 获取文件大小
        size_bytes = file_path.stat().st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f}KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f}MB"

        # 获取文件图标
        ext = filename.split('.')[-1].lower()
        icon_map = {
            'pdf': 'fa-file-pdf',
            'docx': 'fa-file-word',
            'doc': 'fa-file-word',
            'md': 'fa-file-code',
            'txt': 'fa-file-text',
            'jpg': 'fa-file-image',
            'png': 'fa-file-image',
            'zip': 'fa-file-archive'
        }
        icon_class = icon_map.get(ext, 'fa-file')

        return {
            'size': size_str,
            'icon': icon_class,
            'exists': True
        }

    return {
        'size': '未知',
        'icon': 'fa-file',
        'exists': False
    }

def generate_docs_page():
    """生成文档下载页面"""
    print("🏗️ 开始生成文档页面...")

    # 设置模板环境
    env = setup_template_env()

    # 读取配置
    root_dir = Path(__file__).parent.parent.parent.parent
    title_file = root_dir / "data" / "docs" / "title.json"
    files_file = root_dir / "data" / "docs" / "files.json"
    frame_file = root_dir / "data" / "docs" / "frame.json"

    title_config = load_json_file(title_file)
    files_config = load_json_file(files_file)
    frame_config = load_json_file(frame_file)

    if not title_config or not files_config:
        print("❌ 无法加载docs配置")
        return

    # 处理文档信息
    processed_files = {}
    for category, docs in files_config.items():
        processed_files[category] = {}
        for filename, title in docs.items():
            file_info = get_file_info(filename)
            processed_files[category][filename] = {
                'title': title,
                'size': file_info['size'],
                'icon': file_info['icon'],
                'exists': file_info['exists']
            }

    # 生成页面
    template = env.get_template('sections/docs/page.html')
    html_content = template.render(
        frame=frame_config or {},
        title_config=title_config,
        files_config=processed_files
    )

    # 保存页面
    output_dir = root_dir / "html" / "docs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "index.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 复制文档文件
    docs_output_dir = output_dir / "files"
    docs_output_dir.mkdir(exist_ok=True)

    copied_files = 0
    for category, docs in files_config.items():
        for filename in docs.keys():
            src_file = root_dir / "data" / "docs" / filename
            if src_file.exists():
                shutil.copy2(src_file, docs_output_dir)
                copied_files += 1

    print(f"✅ 生成文档页面: {output_file}")
    print(f"📄 复制文档文件: {copied_files}个")
    print("🎉 文档页面生成完成！")

def generate_docs_preview_html():
    """生成文档预览区域HTML"""
    # 设置模板环境
    env = setup_template_env()

    # 读取配置
    root_dir = Path(__file__).parent.parent.parent.parent
    title_file = root_dir / "data" / "docs" / "title.json"
    title_config = load_json_file(title_file)

    if not title_config:
        return ""

    template = env.get_template('home/docs_preview.html')
    return template.render(
        title=title_config.get('title', '文档下载'),
        subtitle=title_config.get('subtitle', '技术文档和资料下载'),
        docs_url="docs/index.html"
    )

def generate_docs_page_and_home():
    """生成文档页面并更新主页预览"""
    generate_docs_page()

    # 更新主页预览
    try:
        from scripts.home.generator import generate_home_html
        generate_home_html()
        print("✅ 主页预览已更新")
    except Exception as e:
        print(f"⚠️ 更新主页预览失败: {e}")

if __name__ == "__main__":
    generate_docs_page()
