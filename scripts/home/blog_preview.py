#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成博客预览区域的脚本
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

def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载 {file_path} 失败: {e}")
        return None

def get_latest_blog_cards(limit=3):
    """获取最新的博客文章卡片（用于主页预览）"""
    root_dir = Path(__file__).parent.parent.parent
    blog_dir = root_dir / "data" / "blog"

    cards = []

    if blog_dir.exists():
        # 直接扫描所有文章目录（扁平结构）
        for article_dir in blog_dir.iterdir():
            if article_dir.is_dir() and not article_dir.name.startswith('.'):
                card_file = article_dir / "card.json"
                if card_file.exists():
                    card_data = load_json_file(card_file)
                    if card_data and card_data.get('status') == 'published':
                        # 复制原始数据并添加文章路径信息
                        card = card_data.copy()
                        card['article_path'] = article_dir.name
                        card['url'] = f"blog/{article_dir.name}/content.html"
                        card['type'] = 'blog'
                        cards.append(card)

    # 按日期排序，最新的在前
    cards.sort(key=lambda x: x.get('date', ''), reverse=True)

    # 返回最新的文章
    return {
        'cards': cards[:limit],
        'total': len(cards),
        'has_more': len(cards) > limit
    }

def generate_blog_preview_html():
    """生成博客预览区域HTML - 供外部调用的接口"""
    # 设置模板环境
    env = setup_template_env()

    # 读取博客配置数据
    root_dir = Path(__file__).parent.parent.parent
    blog_config_file = root_dir / "data" / "blog" / "title.json"
    blog_config = load_json_file(blog_config_file)

    if not blog_config:
        print("无法加载博客配置数据")
        return ""

    # 获取最新的博客文章
    latest_blogs = get_latest_blog_cards()

    # 为主页预览调整图片路径
    for card in latest_blogs['cards']:
        if card.get('image') and not card['image'].startswith('http'):
            # 处理本地图片路径
            if card['image'].startswith('./'):
                image_name = card['image'][2:]  # 移除 ./
            else:
                image_name = card['image']  # 直接使用文件名
            card['image'] = f"blog/{card['article_path']}/{image_name}"

    template = env.get_template('home/blog_preview.html')
    return template.render(
        title=blog_config.get('title', '个人博客'),
        subtitle=blog_config.get('subtitle', ''),
        blogs=latest_blogs['cards'],
        total_count=latest_blogs['total'],
        has_more=latest_blogs['has_more']
    )

if __name__ == "__main__":
    html_content = generate_blog_preview_html()
    print("博客预览区域HTML已生成")
    print(html_content[:200] + "..." if len(html_content) > 200 else html_content)
