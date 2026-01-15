#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简历页面生成器
生成独立的简历页面，包含PDF预览和下载功能
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def setup_template_env():
    """设置 Jinja2 模板环境"""
    template_dir = Path(__file__).parent.parent.parent.parent / "templates"
    return Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )

def load_resume_config():
    """加载简历页面配置"""
    from scripts.common.config import load_frame_config

    # 加载简历页面框架配置
    frame_config = load_frame_config('resume')

    # 确保PDF路径正确
    if 'pdf_path' not in frame_config:
        frame_config['pdf_path'] = 'data/resume/resume.pdf'

    return frame_config

def generate_resume_page_html():
    """生成简历页面HTML"""
    # 设置模板环境
    env = setup_template_env()

    # 加载配置
    config = load_resume_config()

    # 生成各部分HTML
    nav_html = generate_resume_nav_html(env, config)
    content_html = generate_resume_content_html(env, config)
    footer_html = generate_resume_footer_html(env, config)

    # 渲染完整页面
    base_template = env.get_template('base.html')
    html_content = base_template.render(
        site_title=config.get('page_title', '简历页面'),
        nav_html=nav_html,
        content_html=content_html,
        footer_html=footer_html
    )

    return html_content

def generate_resume_nav_html(env, config):
    """生成简历页面专用导航栏"""
    # 使用自定义导航栏，不使用标准导航
    nav_buttons = config.get('nav_buttons', [])
    nav_html = f'''
    <!-- 简历页面专用导航栏 -->
    <nav id="main-nav" class="fixed top-0 left-0 w-full z-50 transition-all duration-500 py-4 bg-white border-b border-gray-200">
        <div class="container mx-auto px-4 md:px-8 flex justify-between items-center">
            <h1 class="text-xl font-bold text-apple-black">{config.get('page_title', '个人简历')}</h1>
            <div class="flex space-x-4">
    '''

    for button in nav_buttons:
        nav_html += f'''
                <a href="{button['href']}"
                   class="inline-flex items-center px-3 py-2 bg-apple-hover text-apple-white rounded-lg hover:bg-[#0077ED] transition-all {button.get('class', '')}">
                    <i class="fa-solid {button['icon']} mr-2"></i>
                    {button['text']}
                </a>
        '''

    nav_html += '''
            </div>
        </div>
    </nav>
    '''

    return nav_html

def generate_resume_content_html(env, config):
    """生成简历页面内容"""
    template = env.get_template('sections/resume/page.html')
    return template.render(**config)

def generate_resume_footer_html(env, config):
    """生成简历页面页脚"""
    template = env.get_template('footer.html')
    return template.render(
        footer_text=config.get('footer_text', '© 2025 个人主页'),
        footer_tagline=config.get('footer_extra', ''),
        page_type='resume'
    )

def generate_resume_page():
    """生成简历页面并保存到文件"""
    # 生成HTML内容
    html_content = generate_resume_page_html()

    # 保存到文件 - 生成到 html/resume/index.html
    root_dir = Path(__file__).parent.parent.parent.parent
    output_dir = root_dir / "html" / "resume"
    output_file = output_dir / "index.html"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"简历页面 HTML 已生成: {output_file}")

if __name__ == "__main__":
    generate_resume_page()
