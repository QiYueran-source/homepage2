#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公共配置和工具模块
"""

import json
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

def load_json_file(file_path):
    """加载 JSON 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载 {file_path} 失败: {e}")
        return None

def load_frame_config(page_name='home'):
    """加载页面框架配置"""
    root_dir = Path(__file__).parent.parent.parent
    data_dir = root_dir / "data"

    # 加载全局框架配置
    global_frame_file = data_dir / "frame.json"
    global_frame = load_json_file(global_frame_file) or {}

    # 加载页面特定框架配置
    page_frame_file = data_dir / page_name / "frame.json"
    page_frame = load_json_file(page_frame_file) or {}

    # 合并配置（页面特定配置覆盖全局配置）
    frame_config = global_frame.copy()
    frame_config.update(page_frame)

    return frame_config

def load_config():
    """加载全局配置（主要用于首页）"""
    root_dir = Path(__file__).parent.parent.parent
    data_dir = root_dir / "data"

    # 加载框架配置（首页）
    frame_config = load_frame_config('home')

    # 读取首页内容配置
    title_file = data_dir / "title.json"
    title_data = load_json_file(title_file)

    config = {
        'site_title': frame_config.get('site_title', '个人主页'),
        'nav_logo': frame_config.get('nav_logo', '个人主页'),
        'hero_title': '欢迎访问',
        'hero_subtitle': '这里是我的个人主页',
        'hero_button_text': '了解更多',
        'hero_button_link': '#resume',
        'footer_text': frame_config.get('footer_text', '© 2025 个人主页'),
        'footer_tagline': frame_config.get('footer_tagline', ''),
        'icp_number': frame_config.get('icp_number', ''),
        'nav_items': []
    }

    # 应用首页内容配置
    if title_data:
        config.update({
            'hero_title': title_data.get("hero_title", config['hero_title']),
            'hero_subtitle': title_data.get("hero_subtitle", config['hero_subtitle']),
            'hero_button_text': title_data.get("hero_button_text", config['hero_button_text']),
            'hero_button_link': title_data.get("hero_button_link", config['hero_button_link'])
        })

    # 读取 order.json 获取导航顺序
    order_file = data_dir / "order.json"
    order_data = load_json_file(order_file)

    # 构建导航项 - 从各个页面的frame.json中收集
    nav_items = []
    if order_data:
        for section in order_data:
            if section == "home":
                nav_items.append({
                    "id": "home",
                    "title": config['nav_logo'],
                    "href": "#home"
                })
            else:
                # 从对应页面的frame.json中读取导航标题
                section_frame = load_frame_config(section)
                nav_title = section_frame.get('nav_title')
                if nav_title:
                    # 为不同页面设置正确的路径
                    if section == "resume":
                        # 简历指向主页的简历预览部分
                        href = "#resume"
                    elif section == "blog":
                        # 博客指向主页的博客预览部分
                        href = "#blog-preview"
                    elif section == "project":
                        # 项目指向主页的项目预览部分
                        href = "#projects"
                    else:
                        href = f"#{section}"
                    nav_items.append({
                        "id": section,
                        "title": nav_title,
                        "href": href
                    })
                # 如果没有配置，暂时跳过（只处理当前实现的页面）

    config['nav_items'] = nav_items
    return config
