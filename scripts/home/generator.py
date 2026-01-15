#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Home 页面生成器
生成完整的首页 HTML
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

def generate_nav_html(env, config):
    """生成导航栏HTML"""
    template = env.get_template('nav.html')
    return template.render(
        nav_logo=config['nav_logo'],
        nav_items=config['nav_items']
    )

def generate_hero_html(env, config):
    """生成Hero区域HTML"""
    template = env.get_template('hero.html')
    return template.render(
        hero_title=config['hero_title'],
        hero_subtitle=config['hero_subtitle'],
        hero_button_text=config['hero_button_text'],
        hero_button_link=config['hero_button_link']
    )

def generate_footer_html(env, config):
    """生成页脚HTML"""
    template = env.get_template('footer.html')
    return template.render(
        footer_text=config['footer_text'],
        footer_tagline=config['footer_tagline']
    )

def generate_home_html():
    """生成完整的首页 HTML"""
    # 设置模板环境
    env = setup_template_env()

    # 导入配置
    import sys
    root_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(root_dir))
    from scripts.common.config import load_config

    # 加载配置
    config = load_config()
    if not config:
        return

    # 获取输出路径
    output_file = root_dir / "html" / "home.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 生成各部分HTML
    nav_html = generate_nav_html(env, config)
    hero_html = generate_hero_html(env, config)

    # 调用简历预览模块
    from .resume_preview import generate_resume_preview_html
    resume_preview_html = generate_resume_preview_html()

    footer_html = generate_footer_html(env, config)

    # 组合内容HTML
    content_html = hero_html + resume_preview_html

    # 渲染完整页面
    base_template = env.get_template('base.html')
    html_content = base_template.render(
        site_title=config['site_title'],
        nav_html=nav_html,
        content_html=content_html,
        footer_html=footer_html
    )

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Home 页面 HTML 已生成: {output_file}")

if __name__ == "__main__":
    generate_home_html()
