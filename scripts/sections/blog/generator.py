#!/usr/bin/env python3
"""
博客生成器
基于项目生成器的方式生成博客列表
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json
from scripts.common.mdconfig import markdown_to_html

def setup_template_env():
    """设置 Jinja2 模板环境"""
    template_dir = Path(__file__).parent.parent.parent.parent / "templates"
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

def prepare_card_data(card_data, category_id, article_name):
    """准备卡片数据，处理路径和URL"""
    card = card_data.copy()

    # 处理图片路径
    if card.get('image'):
        if card['image'].startswith('http'):
            # 如果是URL，直接使用
            card['image'] = card['image']
        else:
            # 如果是本地文件，确保是正确的相对路径
            if not card['image'].startswith('./'):
                card['image'] = f"./{card['image']}"

    # 生成内容页面URL
    card['content_url'] = f"content.html"
    card['url'] = f"blog/{article_name}/content.html"

    # 设置卡片类型
    card['type'] = 'blog'

    return card

def generate_card_html(card_data):
    """生成博客卡片HTML片段"""
    env = setup_template_env()
    template = env.get_template('components/card.html')
    return template.render(card=card_data)

def generate_blog_html(card_data, md_html_content):
    """生成完整博客HTML页面"""
    env = setup_template_env()
    template = env.get_template('components/article.html')
    return template.render(
        card=card_data,
        content_html=md_html_content,
        site_title="个人博客"
    )

def get_all_blogs():
    """自动扫描并获取所有博客"""
    root_dir = Path(__file__).parent.parent.parent.parent
    blog_dir = root_dir / "data" / "blog"

    blogs = []

    if blog_dir.exists():
        # 扫描所有子目录（博客）
        for blog_dir_item in blog_dir.iterdir():
            if blog_dir_item.is_dir() and blog_dir_item.name != "__pycache__":
                card_file = blog_dir_item / "card.json"
                content_file = blog_dir_item / "content.md"
                if card_file.exists():
                    card_data = load_json_file(card_file)
                    if card_data and card_data.get('status') == 'published':
                        # 读取博客详细内容
                        description = ""
                        if content_file.exists():
                            try:
                                with open(content_file, 'r', encoding='utf-8') as f:
                                    description = f.read()
                            except Exception as e:
                                print(f"读取博客内容失败 {content_file}: {e}")

                        card_data['description'] = description
                        card_data['blog_path'] = blog_dir_item.name

                        # 准备卡片数据（保持原始图片路径）
                        prepared_card = prepare_card_data(card_data, 'blog', blog_dir_item.name)
                        blogs.append(prepared_card)

    # 按日期排序，最新的在前
    blogs.sort(key=lambda x: x.get('date', ''), reverse=True)

    return blogs

def generate_blog_detail_page(blog):
    """生成单个博客详细页面"""
    env = setup_template_env()
    template = env.get_template('components/article.html')

    # 准备文章数据
    article_data = {
        'title': blog['title'],
        'summary': blog['summary'],
        'date': blog['date'],
        'category': blog.get('category', ''),
        'type': 'blog',
        'tags': blog.get('tags', []),
        'status': blog.get('status', 'published')
    }

    # 处理内容
    html_content = markdown_to_html(blog.get('description', ''))

    html_output = template.render(
        card=article_data,
        content=html_content
    )

    # 保存文件
    output_dir = Path(__file__).parent.parent.parent.parent / "html" / "blog" / blog['blog_path']
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "index.html"
    output_file.write_text(html_output, encoding='utf-8')

    print(f"✅ 生成博客详情页: {blog['title']}")

def scan_and_generate_blogs():
    """扫描博客目录并生成所有文件"""
    print("🔍 开始扫描博客文章...")

    # 设置路径
    data_root = Path(__file__).parent.parent.parent.parent / "data" / "blog"
    output_root = Path(__file__).parent.parent.parent.parent / "html" / "blog"

    if not data_root.exists():
        print("❌ 博客数据目录不存在")
        return

    # 统计信息
    total_blogs = 0
    generated_cards = 0
    generated_blogs = 0

    # 扫描博客目录
    for blog_dir in data_root.iterdir():
        if not blog_dir.is_dir() or blog_dir.name == "__pycache__":
            continue

        total_blogs += 1
        print(f"📁 处理博客: {blog_dir.name}")

        # 检查必需文件
        card_file = blog_dir / "card.json"
        content_file = blog_dir / "content.md"

        if not card_file.exists():
            print(f"⚠️ 跳过 {blog_dir.name}: 缺少 card.json")
            continue

        # 加载卡片数据
        card_data = load_json_file(card_file)
        if not card_data:
            print(f"⚠️ 跳过 {blog_dir.name}: card.json 无效")
            continue

        # 准备卡片数据
        prepared_card = prepare_card_data(card_data, 'blog', blog_dir.name)

        # 创建输出目录
        output_dir = output_root / blog_dir.name
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            # 生成卡片HTML
            card_html = generate_card_html(prepared_card)
            card_output = output_dir / "card.html"
            with open(card_output, 'w', encoding='utf-8') as f:
                f.write(card_html)
            generated_cards += 1
            print(f"✅ 生成卡片: {card_output}")

            # 处理内容文件
            if content_file.exists():
                # 读取并转换Markdown
                with open(content_file, 'r', encoding='utf-8') as f:
                    md_content = f.read()

                html_content = markdown_to_html(md_content)

                # 检测同目录下背景图（background.png/jpg/webp），供正文页使用
                for ext in ('png', 'jpg', 'webp'):
                    bg = blog_dir / f'background.{ext}'
                    if bg.exists():
                        prepared_card['background_url'] = f'background.{ext}'
                        break

                # 生成博客HTML
                blog_html = generate_blog_html(prepared_card, html_content)
                blog_output = output_dir / "content.html"
                with open(blog_output, 'w', encoding='utf-8') as f:
                    f.write(blog_html)
                generated_blogs += 1
                print(f"✅ 生成博客: {blog_output}")

                # 复制博客目录
                import shutil
                try:
                    # 复制整个博客目录，但排除md文件
                    for item in blog_dir.iterdir():
                        if item.is_file() and item.name != 'content.md':
                            shutil.copy2(item, output_dir)
                        elif item.is_dir():
                            shutil.copytree(item, output_dir / item.name, dirs_exist_ok=True)
                    print(f"✅ 复制博客目录: {blog_dir} → {output_dir}")
                except Exception as e:
                    print(f"⚠️ 复制博客目录失败: {e}")
            else:
                print(f"⚠️ {blog_dir.name} 缺少 content.md 文件")

        except Exception as e:
            print(f"❌ 生成失败: {e}")

    # 生成博客列表页面
    if total_blogs > 0:
        try:
            generate_blog_list_page()
        except Exception as e:
            print(f"❌ 生成博客列表页面失败: {e}")

    # 输出统计信息
    print("📊 生成统计:")
    print(f"   发现博客: {total_blogs}")
    print(f"   生成卡片: {generated_cards}")
    print(f"   生成博客: {generated_blogs}")
    print("🎉 博客生成完成！")

def generate_all_blog_pages():
    """生成所有博客详细页面（兼容旧接口）"""
    return scan_and_generate_blogs()

def generate_blog_list_page():
    """生成博客列表页面（显示所有博客）"""
    print("🏗️ 开始生成博客列表页面...")

    # 设置模板环境
    env = setup_template_env()

    # 加载框架配置
    root_dir = Path(__file__).parent.parent.parent.parent
    frame_file = root_dir / "data" / "blog" / "frame.json"
    frame_config = load_json_file(frame_file)

    if not frame_config:
        print("❌ 无法加载博客框架配置")
        return

    # 获取所有博客
    blogs = get_all_blogs()

    # 为博客列表页面调整图片路径（移除./前缀）
    for blog in blogs:
        if blog.get('image') and not blog['image'].startswith('http'):
            if blog['image'].startswith('./'):
                blog['image'] = blog['image'][2:]  # 移除 ./

    if not blogs:
        print("⚠️ 没有博客数据")
        return

    template = env.get_template('sections/blog/all_content_page.html')

    # 生成HTML
    html_content = template.render(
        frame=frame_config,
        blogs=blogs,
        total_blogs=len(blogs)
    )

    # 保存文件
    output_dir = root_dir / "html" / "blog"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "index.html"
    output_file.write_text(html_content, encoding='utf-8')

    print(f"✅ 生成博客列表页面: {output_file} ({len(blogs)}篇文章)")
    print("📊 博客列表页面生成完成！")

def generate_blogs_preview_html():
    """生成博客预览区域HTML - 供外部调用的接口"""
    # 设置模板环境
    env = setup_template_env()

    # 读取博客配置数据
    root_dir = Path(__file__).parent.parent.parent.parent
    title_file = root_dir / "data" / "blog" / "title.json"
    title_data = load_json_file(title_file)

    # 获取所有博客
    all_blogs = get_all_blogs()

    # 限制预览数量（类似项目的3篇）
    preview_blogs = all_blogs[:3]

    # 为主页预览调整图片路径
    for blog in preview_blogs:
        if blog.get('image') and not blog['image'].startswith('http'):
            if blog['image'].startswith('./'):
                image_name = blog['image'][2:]  # 移除 ./
                blog['image'] = f"blog/{blog['blog_path']}/{image_name}"

    template = env.get_template('home/blog_preview.html')
    return template.render(
        title=title_data.get('title', '个人博客') if title_data else '个人博客',
        blogs=preview_blogs,
        total_count=len(all_blogs),
        has_more=len(all_blogs) > 3
    )

def scan_and_generate_blogs_and_home():
    """生成博客页面并更新主页预览"""
    # 先生成博客页面
    scan_and_generate_blogs()

    # 再更新主页预览
    try:
        from scripts.home.generator import generate_home_html
        generate_home_html()
        print("✅ 主页预览已更新")
    except Exception as e:
        print(f"⚠️ 更新主页预览失败: {e}")

if __name__ == "__main__":
    html_content = generate_blogs_preview_html()
    print("博客预览HTML已生成")
    print(html_content[:300] + "..." if len(html_content) > 300 else html_content)

