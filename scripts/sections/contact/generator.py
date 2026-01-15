#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contact 联系方式模块生成器
生成主页联系方式预览
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json

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

def get_contact_icon(contact_type):
    """获取联系方式图标"""
    icon_map = {
        'phone': 'fas fa-phone',
        'email': 'fas fa-envelope',
        'github': 'fab fa-github',
        'wechat': 'fab fa-weixin',
        'qq': 'fab fa-qq',
        'douyin': 'fab fa-tiktok',
        'linkedin': 'fab fa-linkedin',
        'twitter': 'fab fa-twitter',
        'weibo': 'fab fa-weibo',
        'website': 'fas fa-globe',
        'location': 'fas fa-map-marker-alt'
    }

    return icon_map.get(contact_type.lower(), 'fas fa-address-card')

def generate_contact_preview_html():
    """生成联系方式预览区域HTML"""
    # 设置模板环境
    env = setup_template_env()

    # 读取配置
    root_dir = Path(__file__).parent.parent.parent.parent
    title_file = root_dir / "data" / "contact" / "title.json"
    contact_file = root_dir / "data" / "contact" / "contact.json"

    title_config = load_json_file(title_file)
    contact_data = load_json_file(contact_file)

    if not title_config or not contact_data:
        print("无法加载contact配置")
        return ""

    # 处理联系方式数据
    processed_contacts = []
    for contact_type, value in contact_data.items():
        if value and str(value).strip():  # 只处理非空值
            processed_contacts.append({
                'type': contact_type,
                'value': value,
                'icon': get_contact_icon(contact_type),
                'display_name': get_display_name(contact_type)
            })

    template = env.get_template('home/contact_preview.html')
    return template.render(
        title=title_config.get('title', '联系方式'),
        subtitle=title_config.get('subtitle', '联系方式介绍'),
        contacts=processed_contacts
    )

def get_display_name(contact_type):
    """获取联系方式的显示名称"""
    name_map = {
        'phone': '电话',
        'email': '邮箱',
        'github': 'GitHub',
        'wechat': '微信',
        'qq': 'QQ',
        'douyin': '抖音',
        'linkedin': '领英',
        'twitter': '推特',
        'weibo': '微博',
        'website': '网站',
        'location': '地址'
    }

    return name_map.get(contact_type.lower(), contact_type)

def generate_contact_page_and_home():
    """生成contact预览并更新主页"""
    # 复制资源文件
    copy_contact_assets()

    # 更新主页预览
    try:
        from scripts.home.generator import generate_home_html
        generate_home_html()
        print("✅ 主页预览已更新")
    except Exception as e:
        print(f"⚠️ 更新主页预览失败: {e}")

def copy_contact_assets():
    """复制contact相关的资源文件到html目录"""
    root_dir = Path(__file__).parent.parent.parent.parent
    contact_data_dir = root_dir / "data" / "contact"
    contact_html_dir = root_dir / "html" / "contact"

    if not contact_data_dir.exists():
        return

    # 读取contact数据，找出需要复制的文件
    contact_file = contact_data_dir / "contact.json"
    contact_data = load_json_file(contact_file)

    if not contact_data:
        return

    copied_files = 0

    # 检查每个联系方式的值是否是文件路径
    for contact_type, value in contact_data.items():
        if value and isinstance(value, str):
            # 如果值看起来是文件路径（包含图片扩展名）
            if any(value.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']):
                src_file = contact_data_dir / value
                if src_file.exists():
                    # 创建目标目录
                    contact_html_dir.mkdir(parents=True, exist_ok=True)
                    dst_file = contact_html_dir / value

                    # 复制文件
                    import shutil
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1
                    print(f"✅ 复制contact资源: {src_file} → {dst_file}")

    if copied_files > 0:
        print(f"📄 复制contact资源文件: {copied_files}个")

if __name__ == "__main__":
    html_content = generate_contact_preview_html()
    print("联系方式预览HTML已生成")
    print(html_content[:300] + "..." if len(html_content) > 300 else html_content)
