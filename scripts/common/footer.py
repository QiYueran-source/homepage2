#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
页脚生成器
"""

from .config import setup_template_env

def generate_footer(config, page_type='home'):
    """生成页脚HTML"""
    env = setup_template_env()

    template = env.get_template('footer.html')
    return template.render(
        footer_text=config['footer_text'],
        footer_tagline=config['footer_tagline'],
        page_type=page_type
    )
