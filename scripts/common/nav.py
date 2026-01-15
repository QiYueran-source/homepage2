#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导航栏生成器
"""

from .config import setup_template_env

def generate_nav(config, current_page='home'):
    """生成导航栏HTML"""
    env = setup_template_env()

    # 为导航项添加active状态
    nav_items = []
    for item in config['nav_items']:
        nav_item = item.copy()
        nav_item['is_active'] = (item['id'] == current_page)
        nav_items.append(nav_item)

    template = env.get_template('nav.html')
    return template.render(
        nav_logo=config['nav_logo'],
        nav_items=nav_items,
        current_page=current_page
    )
