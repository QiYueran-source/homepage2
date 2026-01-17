#!/usr/bin/env python3
"""
项目预览生成器
参考博客预览的方式生成项目列表
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
    card['url'] = f"project/{article_name}/content.html"

    # 设置卡片类型
    card['type'] = 'project'

    return card

def generate_card_html(card_data):
    """生成项目卡片HTML片段"""
    env = setup_template_env()
    template = env.get_template('components/card.html')
    return template.render(card=card_data)

def generate_project_html(card_data, md_html_content):
    """生成完整项目HTML页面"""
    env = setup_template_env()
    template = env.get_template('components/article.html')
    return template.render(
        card=card_data,
        content_html=md_html_content,
        site_title="项目经历"
    )

def get_all_projects():
    """自动扫描并获取所有项目"""
    root_dir = Path(__file__).parent.parent.parent.parent
    project_dir = root_dir / "data" / "project"

    projects = []

    if project_dir.exists():
        # 扫描所有子目录（项目）
        for project_dir_item in project_dir.iterdir():
            if project_dir_item.is_dir() and project_dir_item.name != "__pycache__":
                card_file = project_dir_item / "card.json"
                content_file = project_dir_item / "content.md"
                if card_file.exists():
                    card_data = load_json_file(card_file)
                    if card_data and card_data.get('status') in ['published', 'completed', 'in-development']:
                        # 读取项目详细内容
                        description = ""
                        if content_file.exists():
                            try:
                                with open(content_file, 'r', encoding='utf-8') as f:
                                    description = f.read()
                            except Exception as e:
                                print(f"读取项目内容失败 {content_file}: {e}")

                        card_data['description'] = description
                        card_data['project_path'] = project_dir_item.name

                        # 准备卡片数据（保持原始图片路径）
                        prepared_card = prepare_card_data(card_data, 'project', project_dir_item.name)
                        projects.append(prepared_card)

    # 按日期排序，最新的在前
    projects.sort(key=lambda x: x.get('date', ''), reverse=True)

    return projects

def generate_project_detail_page(project):
    """生成单个项目详细页面"""
    env = setup_template_env()
    template = env.get_template('components/article.html')

    # 准备文章数据
    article_data = {
        'title': project['title'],
        'summary': project['summary'],
        'date': project['date'],
        'category': project['category'],
        'type': 'project',
        'technologies': project.get('technologies', []),
        'demo_url': project.get('demo_url'),
        'github_url': project.get('github_url'),
        'status': project.get('status', 'completed')
    }

    # 处理内容
    html_content = markdown_to_html(project.get('description', ''))

    html_output = template.render(
        card=article_data,
        content=html_content
    )

    # 保存文件
    output_dir = Path(__file__).parent.parent.parent.parent / "html" / "project" / project['project_path']
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "index.html"
    output_file.write_text(html_output, encoding='utf-8')

    print(f"✅ 生成项目详情页: {project['title']}")

def scan_and_generate_projects():
    """扫描项目目录并生成所有文件"""
    print("🔍 开始扫描项目...")

    # 设置路径
    data_root = Path(__file__).parent.parent.parent.parent / "data" / "project"
    output_root = Path(__file__).parent.parent.parent.parent / "html" / "project"

    if not data_root.exists():
        print("❌ 项目数据目录不存在")
        return

    # 统计信息
    total_projects = 0
    generated_cards = 0
    generated_projects = 0

    # 扫描项目目录
    for project_dir in data_root.iterdir():
        if not project_dir.is_dir() or project_dir.name == "__pycache__":
            continue

        total_projects += 1
        print(f"📁 处理项目: {project_dir.name}")

        # 检查必需文件
        card_file = project_dir / "card.json"
        content_file = project_dir / "content.md"

        if not card_file.exists():
            print(f"⚠️ 跳过 {project_dir.name}: 缺少 card.json")
            continue

        # 加载卡片数据
        card_data = load_json_file(card_file)
        if not card_data:
            print(f"⚠️ 跳过 {project_dir.name}: card.json 无效")
            continue

        # 准备卡片数据
        prepared_card = prepare_card_data(card_data, 'project', project_dir.name)

        # 创建输出目录
        output_dir = output_root / project_dir.name
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

                # 生成项目HTML
                project_html = generate_project_html(prepared_card, html_content)
                project_output = output_dir / "content.html"
                with open(project_output, 'w', encoding='utf-8') as f:
                    f.write(project_html)
                generated_projects += 1
                print(f"✅ 生成项目: {project_output}")

                # 复制项目目录
                import shutil
                try:
                    # 复制整个项目目录，但排除md文件
                    for item in project_dir.iterdir():
                        if item.is_file() and item.name != 'content.md':
                            shutil.copy2(item, output_dir)
                        elif item.is_dir():
                            shutil.copytree(item, output_dir / item.name, dirs_exist_ok=True)
                    print(f"✅ 复制项目目录: {project_dir} → {output_dir}")
                except Exception as e:
                    print(f"⚠️ 复制项目目录失败: {e}")
            else:
                print(f"⚠️ {project_dir.name} 缺少 content.md 文件")

        except Exception as e:
            print(f"❌ 生成失败: {e}")

    # 生成项目列表页面
    if total_projects > 0:
        try:
            generate_project_list_page()
        except Exception as e:
            print(f"❌ 生成项目列表页面失败: {e}")

    # 输出统计信息
    print("📊 生成统计:")
    print(f"   发现项目: {total_projects}")
    print(f"   生成卡片: {generated_cards}")
    print(f"   生成项目: {generated_projects}")
    print("🎉 项目生成完成！")

def generate_all_project_pages():
    """生成所有项目详细页面（兼容旧接口）"""
    return scan_and_generate_projects()

def generate_project_list_page():
    """生成项目列表页面（显示所有项目）"""
    print("🏗️ 开始生成项目列表页面...")

    # 设置模板环境
    env = setup_template_env()

    # 加载框架配置
    root_dir = Path(__file__).parent.parent.parent.parent
    frame_file = root_dir / "data" / "project" / "frame.json"
    frame_config = load_json_file(frame_file)

    if not frame_config:
        print("❌ 无法加载项目框架配置")
        return

    # 获取所有项目
    projects = get_all_projects()

    # 为项目列表页面调整图片路径（移除./前缀）
    for project in projects:
        if project.get('image') and not project['image'].startswith('http'):
            if project['image'].startswith('./'):
                project['image'] = project['image'][2:]  # 移除 ./

    if not projects:
        print("⚠️ 没有项目数据")
        return

    template = env.get_template('sections/project/all_project_page.html')

    # 生成HTML
    html_content = template.render(
        frame=frame_config,
        projects=projects,
        total_projects=len(projects)
    )

    # 保存文件
    output_dir = root_dir / "html" / "project"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "index.html"
    output_file.write_text(html_content, encoding='utf-8')

    print(f"✅ 生成项目列表页面: {output_file} ({len(projects)}个项目)")
    print("📊 项目列表页面生成完成！")

def generate_projects_preview_html():
    """生成项目预览区域HTML - 供外部调用的接口"""
    # 设置模板环境
    env = setup_template_env()

    # 读取项目配置数据
    root_dir = Path(__file__).parent.parent.parent.parent
    title_file = root_dir / "data" / "project" / "title.json"
    title_data = load_json_file(title_file)

    # 获取所有项目
    all_projects = get_all_projects()

    # 限制预览数量（类似博客的3篇）
    preview_projects = all_projects[:3]

    # 为主页预览调整图片路径
    for project in preview_projects:
        if project.get('image') and not project['image'].startswith('http'):
            if project['image'].startswith('./'):
                image_name = project['image'][2:]  # 移除 ./
                project['image'] = f"project/{project['project_path']}/{image_name}"

    template = env.get_template('home/project_preview.html')
    return template.render(
        title=title_data.get('title', '项目经历') if title_data else '项目经历',
        projects=preview_projects,
        total_count=len(all_projects),
        has_more=len(all_projects) > 3
    )

def scan_and_generate_projects_and_home():
    """生成项目页面并更新主页预览"""
    # 先生成项目页面
    scan_and_generate_projects()

    # 再更新主页预览
    try:
        from scripts.home.generator import generate_home_html
        generate_home_html()
        print("✅ 主页预览已更新")
    except Exception as e:
        print(f"⚠️ 更新主页预览失败: {e}")

if __name__ == "__main__":
    html_content = generate_projects_preview_html()
    print("项目预览HTML已生成")
    print(html_content[:300] + "..." if len(html_content) > 300 else html_content)