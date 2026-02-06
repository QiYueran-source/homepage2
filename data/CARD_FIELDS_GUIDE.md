# 博客和项目卡片字段说明文档

本文档详细说明博客和项目卡片的各个字段及其取值范围，用于指导内容创建和维护。

## 博客卡片字段

### 必填字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `title` | string | 文章标题，显示在卡片和文章页面的标题位置 | `"外汇交易基础知识与入门指南"` |
| `summary` | string | 文章摘要，简要描述文章内容，用于卡片展示和SEO | `"了解外汇市场的基本概念，掌握货币对交易原理..."` |
| `date` | string | 发布日期，格式为 `YYYY-MM-DD` | `"2025-01-19"` |
| `status` | string | 文章状态，决定是否在网站上显示 | `"published"` |

### 可选字段

| 字段名 | 类型 | 说明 | 示例 | 默认值 |
|--------|------|------|------|-------|
| `id` | string | 文章唯一标识符，用于URL生成 | `"forex-trading-basics"` | 自动生成 |
| `image` | string | 封面图片路径，支持相对路径和URL | `"https://picsum.photos/seed/forex/800/500"` 或 `"cover.png"` | 无 |
| `category` | string | 文章分类，必须与目录结构一致 | `"经济与金融"` | 从目录结构获取 |
| `tags` | array | 标签数组，用于分类和搜索 | `["外汇交易", "货币对", "汇率"]` | `[]` |

### status 字段取值

| 取值 | 说明 | 是否显示 |
|------|------|----------|
| `"published"` | 已发布文章 | ✅ 显示 |
| 其他值 | 未发布或草稿 | ❌ 不显示 |

## 项目卡片字段

### 必填字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `title` | string | 项目标题 | `"预期协同效应分析工具"` |
| `summary` | string | 项目简介 | `"基于多agent强化学习的预期协同效应分析研究..."` |
| `date` | string | 项目开始或完成日期，格式为 `YYYY-MM` | `"2024-12"` |
| `status` | string | 项目状态 | `"completed"` |

### 可选字段

| 字段名 | 类型 | 说明 | 示例 | 默认值 |
|--------|------|------|------|-------|
| `id` | string | 项目唯一标识符 | `"expected-synergy"` | 自动生成 |
| `technologies` | array | 使用的技术栈 | `["Python", "PyTorch", "SB3"]` | `[]` |
| `image` | string | 项目封面图片，支持相对路径和URL | `"./封面.png"` 或 `"https://..."` | 无 |
| `github_url` | string | GitHub仓库地址 | `"https://github.com/user/repo.git"` | 无 |
| `demo_url` | string | 演示地址 | `"https://demo.example.com"` | 无 |
| `category` | string | 项目分类 | `"金融深度学习"` | 无 |

### status 字段取值

| 取值 | 说明 | 是否显示 |
|------|------|----------|
| `"published"` | 已发布项目 | ✅ 显示 |
| `"completed"` | 已完成项目 | ✅ 显示 |
| `"in-development"` | 开发中项目 | ✅ 显示 |
| 其他值 | 未完成或私有项目 | ❌ 不显示 |

## 字段使用建议

### 标题 (title)
- 简洁明了，突出核心内容
- 长度建议：20-50字符
- 避免使用特殊字符

### 摘要 (summary)
- 100-200字符为宜
- 突出项目/文章的核心价值
- 用于SEO优化

### 日期 (date)
- 博客：精确到日 `YYYY-MM-DD`
- 项目：精确到月 `YYYY-MM`

### 图片 (image)
- 支持格式：JPG, PNG, WebP
- 建议尺寸：800x500 或 1200x800
- 相对路径：`"./image.jpg"`
- 网络URL：`"https://example.com/image.jpg"`

### 标签 (tags)
- 2-5个相关标签
- 使用常用关键词
- 有利于SEO和内容发现

### 技术栈 (technologies)
- 列出核心技术
- 按重要性排序
- 标准命名（如 "Python", "JavaScript"）

## 目录结构要求

### 博客目录结构
```
data/blog/
├── 分类目录1/
│   ├── 文章目录1/
│   │   ├── card.json    # 文章配置
│   │   └── content.md   # 文章内容
│   └── 文章目录2/
│       ├── card.json
│       └── content.md
└── 分类目录2/
    └── ...
```

### 项目目录结构
```
data/project/
├── 项目目录1/
│   ├── card.json        # 项目配置
│   ├── content.md       # 项目详情
│   └── 其他资源文件...  # 图片、文档等
└── 项目目录2/
    └── ...
```

## 配置示例

### 博客卡片示例
```json
{
    "title": "数据总线架构设计与实践",
    "summary": "深入探讨数据总线架构的核心设计原则，实现高可用、高性能的数据流转系统",
    "date": "2025-01-15",
    "image": "cover.png",
    "category": "技术分享",
    "tags": ["架构设计", "数据总线", "微服务", "高可用"],
    "status": "published"
}
```

### 项目卡片示例
```json
{
    "id": "expected-synergy",
    "title": "预期协同效应分析工具",
    "summary": "基于多agent强化学习的预期协同效应分析研究，以及相应研究系统",
    "technologies": ["Python", "PyTorch", "SB3", "Docker", "数据流水线"],
    "image": "./封面.png",
    "github_url": "https://github.com/xxx/repo.git",
    "demo_url": "https://github.com/xxx/repo.git",
    "status": "completed",
    "date": "2024-12",
    "category": "金融深度学习"
}
```

## 注意事项

1. **文件编码**：所有JSON文件必须使用UTF-8编码
2. **路径分隔符**：使用正斜杠 `/`，避免反斜杠 `\`
3. **必填字段**：确保所有必填字段都存在且有效
4. **状态管理**：合理使用status字段控制内容可见性
5. **命名规范**：目录和文件名避免特殊字符，使用英文或拼音

## 常见问题

### Q: 为什么我的博客/项目没有显示在首页？
A: 检查 `status` 字段是否设置为正确的发布状态。

### Q: 图片路径应该怎么写？
A: 相对路径使用 `./filename.jpg`，网络图片直接使用完整URL。

### Q: ID字段是必须的吗？
A: 不是必须的，但建议设置，有助于URL美化和SEO。

### Q: 如何添加新的技术标签？
A: 在 `technologies` 数组中添加技术名称，系统会自动处理。

---

*最后更新：2025年1月*
