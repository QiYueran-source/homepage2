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

    # 处理图片路径 - 指向复制后的图片位置
    if card.get('image'):
        if card['image'].startswith('http'):
            # 如果是URL，直接使用
            card['image'] = card['image']
        else:
            # 如果是本地文件，指向复制后的位置
            card['image'] = f"blog/{article_path}/{card['image']}"

    # 生成内容页面URL
    card['url'] = f"blog/{article_path}/content.html"

    # 设置卡片类型
    card['type'] = 'blog'

    return card


def get_all_cards_for_category(category_id, limit=3):
    """自动扫描并获取指定分类下的文章卡片（限制数量用于预览）"""
    root_dir = Path(__file__).parent.parent.parent
    blog_dir = root_dir / "data" / "blog" / category_id

    cards = []

    if blog_dir.exists():
        # 扫描所有子目录（文章）
        for article_dir in blog_dir.iterdir():
            if article_dir.is_dir():
                card_file = article_dir / "card.json"
                if card_file.exists():
                    card_data = load_json_file(card_file)
                    if card_data and card_data.get('status') == 'published':
                        # 构建文章路径
                        article_path = f"{category_id}/{article_dir.name}"
                        # 准备卡片数据
                        prepared_card = prepare_card_data(card_data, article_path)
                        cards.append(prepared_card)

    # 按日期排序，最新的在前
    cards.sort(key=lambda x: x.get('date', ''), reverse=True)

    # 返回限制数量的文章和统计信息
    return {
        'cards': cards[:limit],
        'total': len(cards),
        'has_more': len(cards) > limit,
        'all_cards': cards  # 保留所有文章用于其他用途
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

    # 自动扫描所有分类的文章（限制数量用于预览）
    all_featured_cards = {}
    for category in blog_config.get('categories', []):
        result = get_all_cards_for_category(category['id'])
        cards = result['cards']  # 获取实际的卡片列表

        # 为主页预览调整图片路径
        for card in cards:
            if card.get('image') and not card['image'].startswith('http'):
                if card['image'].startswith('./'):
                    image_name = card['image'][2:]  # 移除 ./
                    card['image'] = f"blog/{category['id']}/{card['article_name']}/{image_name}"

        # 保存完整的返回结果（包含统计信息）
        all_featured_cards[category['id']] = {
            'cards': cards,
            'total': result['total'],
            'has_more': result['has_more']
        }

    # 默认显示第一个分类的卡片
    first_category_id = blog_config.get('categories', [{}])[0].get('id')
    first_category_data = all_featured_cards.get(first_category_id, {})
    featured_cards = first_category_data.get('cards', []) if isinstance(first_category_data, dict) else []

    template = env.get_template('home/blog_preview.html')
    return template.render(
        title=blog_config.get('title', '个人博客'),
        subtitle=blog_config.get('subtitle', ''),
        categories=blog_config.get('categories', []),
        featured_cards=featured_cards,
        all_featured_cards=all_featured_cards
    )

if __name__ == "__main__":
    html_content = generate_blog_preview_html()
    print("博客预览区域HTML已生成")
    print(html_content[:200] + "..." if len(html_content) > 200 else html_content)
