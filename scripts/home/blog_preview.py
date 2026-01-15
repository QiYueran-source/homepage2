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

def prepare_card_data(card_data, article_path):
    """准备卡片数据，处理路径"""
    card = card_data.copy()

    # 处理图片路径
    if card.get('image'):
        card['image'] = f"data/blog/{article_path}/{card['image']}"

    # 生成内容页面URL
    card['url'] = f"blog/{article_path}/content.html"

    # 设置卡片类型
    card['type'] = 'blog'

    return card

def get_featured_cards_for_category(blog_config, category_id):
    """获取指定分类的代表性文章卡片"""
    represent = blog_config.get('represent', {})
    featured_articles = represent.get(category_id, [])

    cards = []
    for article_name in featured_articles[:3]:  # 最多3个
        # 构建文章路径
        article_path = f"{category_id}/{article_name}"
        card_file = Path(__file__).parent.parent.parent / "data" / "blog" / category_id / article_name / "card.json"

        if card_file.exists():
            card_data = load_json_file(card_file)
            if card_data:
                # 准备卡片数据
                prepared_card = prepare_card_data(card_data, article_path)
                cards.append(prepared_card)

    return cards

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

    # 获取技术分享分类的代表性卡片（默认显示）
    featured_cards = get_featured_cards_for_category(blog_config, "技术分享")

    template = env.get_template('home/blog_preview.html')
    return template.render(
        title=blog_config.get('title', '个人博客'),
        subtitle=blog_config.get('subtitle', ''),
        categories=blog_config.get('categories', []),
        featured_cards=featured_cards
    )

if __name__ == "__main__":
    html_content = generate_blog_preview_html()
    print("博客预览区域HTML已生成")
    print(html_content[:200] + "..." if len(html_content) > 200 else html_content)
