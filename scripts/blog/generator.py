#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客生成器
扫描 data/blog 目录，生成所有博客文章的卡片和完整页面
"""

from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader
import markdown

def setup_template_env():
    """设置 Jinja2 模板环境"""
    template_dir = Path(__file__).parent.parent.parent / "templates"
    return Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )

def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载 {file_path} 失败: {e}")
        return None

def prepare_card_data(card_data, category_name, article_name):
    """准备卡片数据，处理路径和URL"""
    card = card_data.copy()

    # 处理图片路径
    if card.get('image'):
        card['image'] = f"../../../../data/blog/{category_name}/{article_name}/{card['image']}"

    # 生成内容页面URL
    card['content_url'] = f"content.html"

    # 设置卡片类型
    card['type'] = 'blog'

    return card

def generate_card_html(card_data):
    """生成卡片HTML片段"""
    env = setup_template_env()
    template = env.get_template('components/card.html')
    return template.render(card=card_data)

def generate_article_html(card_data, md_html_content):
    """生成完整文章HTML页面"""
    env = setup_template_env()
    template = env.get_template('components/article.html')
    return template.render(
        card=card_data,
        content_html=md_html_content,
        site_title="个人博客"
    )

def scan_and_generate_blog():
    """扫描博客目录并生成所有文件"""
    print("🔍 开始扫描博客文章...")

    # 设置路径
    data_root = Path(__file__).parent.parent.parent / "data" / "blog"
    output_root = Path(__file__).parent.parent.parent / "html" / "blog"

    if not data_root.exists():
        print("❌ 博客数据目录不存在")
        return

    # 统计信息
    total_articles = 0
    generated_cards = 0
    generated_articles = 0

    # 扫描所有分类目录
    for category_dir in data_root.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue

        category_name = category_dir.name
        print(f"📂 处理分类: {category_name}")

        # 扫描分类下的文章目录
        for article_dir in category_dir.iterdir():
            if not article_dir.is_dir():
                continue

            article_name = article_dir.name
            card_file = article_dir / "card.json"
            content_file = article_dir / "content.md"

            if not card_file.exists():
                print(f"⚠️  跳过 {article_name}: 缺少 card.json")
                continue

            print(f"📝 处理文章: {article_name}")
            total_articles += 1

            # 读取卡片配置
            card_data = load_json_file(card_file)
            if not card_data:
                print(f"❌ 读取 {card_file} 失败")
                continue

            # 准备卡片数据
            prepared_card = prepare_card_data(card_data, category_name, article_name)

            # 读取并转换Markdown内容
            md_content = ""
            if content_file.exists():
                try:
                    with open(content_file, 'r', encoding='utf-8') as f:
                        md_content = f.read()
                except Exception as e:
                    print(f"⚠️ 读取 {content_file} 失败: {e}")

            # 转换Markdown为HTML
            html_content = markdown.markdown(
                md_content,
                extensions=['extra', 'codehilite', 'toc']
            )

            # 创建输出目录
            output_dir = output_root / category_name / article_name
            output_dir.mkdir(parents=True, exist_ok=True)

            try:
                # 生成卡片HTML
                card_html = generate_card_html(prepared_card)
                card_output = output_dir / "card.html"
                with open(card_output, 'w', encoding='utf-8') as f:
                    f.write(card_html)
                generated_cards += 1
                print(f"✅ 生成卡片: {card_output}")

                # 生成文章HTML
                article_html = generate_article_html(prepared_card, html_content)
                article_output = output_dir / "content.html"
                with open(article_output, 'w', encoding='utf-8') as f:
                    f.write(article_html)
                generated_articles += 1
                print(f"✅ 生成文章: {article_output}")

            except Exception as e:
                print(f"❌ 生成失败: {e}")

    # 输出统计信息
    print("📊 生成统计:")    
    print(f"   发现文章: {total_articles}")
    print(f"   生成卡片: {generated_cards}")
    print(f"   生成文章: {generated_articles}")
    print("🎉 博客生成完成！")

def generate_blog_page():
    """生成博客页面并保存（如果需要的话）"""
    # 这里可以生成博客首页或其他页面
    pass

if __name__ == "__main__":
    scan_and_generate_blog()
