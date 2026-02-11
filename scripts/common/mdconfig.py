#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 渲染统一配置
支持数学公式、Mermaid 图表等扩展功能
"""

import markdown
from pymdownx.superfences import fence_div_format


def get_markdown_config():
    """
    获取 Markdown 渲染配置
    
    Returns:
        tuple: (extensions, extension_configs)
            - extensions: 扩展列表
            - extension_configs: 扩展配置字典
    """
    extensions = [
        'pymdownx.superfences', # 增强代码块（支持 Mermaid）- 必须在最前面
        'pymdownx.highlight',   # 代码高亮（与 superfences 兼容）
        'markdown.extensions.tables',  # 表格支持（从 extra 中单独提取）
        'toc',            # 目录生成
        'pymdownx.arithmatex',  # 数学公式支持
        'pymdownx.magiclink',   # 自动链接
        'pymdownx.tasklist',   # 任务列表
        'pymdownx.tilde'       # 删除线增强
    ]
    
    extension_configs = {
        'pymdownx.arithmatex': {
            'generic': True  # 使用通用模式，支持 MathJax 和 KaTeX
        },
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'mermaid',
                    'class': 'mermaid',
                    'format': fence_div_format
                }
            ],
            'disable_indented_code_blocks': True  # 禁用缩进代码块，避免冲突
        },
        'pymdownx.highlight': {
            'use_pygments': True,
            'noclasses': False,
            'pygments_style': 'monokai',
            'css_class': 'highlight'
        }
    }
    
    return extensions, extension_configs


def markdown_to_html(md_content):
    """
    将 Markdown 内容转换为 HTML
    
    Args:
        md_content (str): Markdown 格式的内容
        
    Returns:
        str: 转换后的 HTML 内容
    """
    extensions, extension_configs = get_markdown_config()
    
    html_content = markdown.markdown(
        md_content,
        extensions=extensions,
        extension_configs=extension_configs
    )
    
    return html_content
