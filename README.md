# Article Poster Generator

**将长文章自动拆分为精美信息图海报** — 基于 Claude Code Skill 的智能内容可视化工具。

输入一篇文章，AI 自动分析结构、提取要点、匹配布局，生成 5-8 张 2400×3600 竖版高清信息图海报，适合微信公众号、小红书、朋友圈等平台分发。

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Async-green?logo=microsoft&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-blueviolet?logo=anthropic&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Demo

5 种视觉风格，适配不同内容调性：

| 暗夜科技 `dark-tech` | 赛博朋克 `cyberpunk` | 极简清新 `minimal-biz` | 黑金奢华 `guochao` | 暗夜青绿 `dark-green` |
|:---:|:---:|:---:|:---:|:---:|
| 深色底 + 猩红<br>CNC金属质感 | 深蓝紫 + 霓虹<br>4px切角机甲风 | 浅绿底 + 白卡<br>Apple级弥散阴影 | 深褐底 + 暗金<br>邀请函内框质感 | 深色底 + 青绿<br>极客气质 |

6 种页面布局，自动混搭：

| 布局 | 用途 | 适合内容 |
|------|------|----------|
| `cover` | 封面页 | 大标题 + 核心要点 |
| `content` | 卡片内容页 | 并列知识点/详细说明 |
| `steps` | 步骤流程页 | 操作教程/流程 |
| `grid` | 网格页 | 对比/技巧/避坑清单 |
| `quote` | 大字金句页 | 核心观点/名言/关键结论 |
| `summary` | 总结页 | 全文总结 + 行动建议 |

## 快速开始

### 环境要求

- Python 3.9+
- Playwright（用于 HTML → PNG 渲染）
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI（作为 Skill 使用时需要）

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/tengjun/article-poster-generator.git
cd article-poster-generator

# 2. 安装依赖
pip install playwright
playwright install chromium

# 3. (可选) 安装为 Claude Code Skill
# 将本项目复制到 ~/.claude/skills/article-poster-generator/
```

### 使用方式

#### 方式一：作为 Claude Code Skill 使用（推荐）

安装为 Skill 后，在 Claude Code 中直接对话：

```
> 帮我把这篇文章做成海报：[粘贴文章内容或链接]

> 用赛博朋克风格把这个技术博客做成信息图

> 把这篇新闻做成 6 张海报，用黑金风格
```

AI 会自动完成：分析文章 → 拆分内容 → 选择布局 → 生成 JSON → 渲染图片 → 输出海报。

#### 方式二：直接运行脚本

准备 JSON 数据文件后，直接调用生成脚本：

```bash
python scripts/generate_posters.py \
  --input poster_data.json \
  --style dark-green \
  --output ~/Desktop/posters/
```

**参数说明：**

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--input, -i` | 是 | - | JSON 数据文件路径 |
| `--style, -s` | 否 | `dark-tech` | 风格：`dark-tech` / `cyberpunk` / `minimal-biz` / `guochao` / `dark-green` |
| `--output, -o` | 否 | `./posters/` | 输出根目录 |
| `--topic, -t` | 否 | 自动提取 | 主题名（用于输出子目录命名） |

**输出目录结构：**

```
posters/
└── 260416-文章主题/
    ├── poster_data.json          # 原始数据备份
    ├── dark-green/               # 风格子目录
    │   ├── slide_00_cover.png
    │   ├── slide_01_content.png
    │   ├── slide_02_steps.png
    │   ├── slide_03_grid.png
    │   ├── slide_04_quote.png
    │   └── slide_05_summary.png
    └── copy.md                   # 配套发布文案（Skill模式生成）
```

## JSON 数据格式

输入的 JSON 文件结构如下：

```json
{
  "style": "dark-green",
  "topic": "文章主题",
  "slides": [
    {
      "type": "cover",
      "slide_number": "00",
      "tag": "今日速评",
      "tag_icon": "⚡",
      "title": "主标题",
      "subtitle": "副标题",
      "highlights": ["要点1", "要点2", "要点3"]
    },
    {
      "type": "content",
      "slide_number": "01",
      "tag": "深度解读",
      "tag_icon": "🔍",
      "title": "内容页标题",
      "sections": [
        {
          "title": "小节标题",
          "content": "正文内容（50-100字为佳）",
          "highlight": "高亮关键句（可选）",
          "border_color": "red"
        }
      ]
    },
    {
      "type": "steps",
      "slide_number": "02",
      "tag": "操作步骤",
      "tag_icon": "⚡",
      "title": "步骤标题",
      "steps": [
        { "title": "步骤一", "content": "步骤说明" }
      ]
    },
    {
      "type": "grid",
      "slide_number": "03",
      "tag": "避坑指南",
      "tag_icon": "⚠",
      "title": "网格标题",
      "cells": [
        { "icon": "❌", "title": "单元格标题", "content": "说明文字" }
      ]
    },
    {
      "type": "quote",
      "slide_number": "04",
      "tag": "核心观点",
      "tag_icon": "💬",
      "quote": "一句话核心观点",
      "source": "来源说明",
      "details": [
        { "label": "标签", "text": "详细解释" }
      ]
    },
    {
      "type": "summary",
      "slide_number": "05",
      "tag": "总结",
      "tag_icon": "💡",
      "title": "总结",
      "summary_text": "一段话总结全文",
      "action_items": ["建议1", "建议2", "建议3"]
    }
  ]
}
```

完整的布局字段说明见 [SKILL.md](./SKILL.md)。

## 设计规范

### 画布与字号

- **画布尺寸**：2400 × 3600 px（竖版 2:3）
- **内边距**：上 100px / 左右 120px / 下 90px

**字号阶梯（5级）：**

| 层级 | 用途 | 字号 |
|------|------|------|
| L1 英雄 | 封面大标题 | 240px |
| L2 页标题 | 各页标题 | 160px |
| L3 区块标题 | 卡片/步骤/金句标题 | 100-120px |
| L4 大正文 | 副标题/要点/行动建议 | 76-88px |
| L5 正文 | 所有正文内容 | 64px |
| L6 标注 | 标签/页码 | 42-52px |

### 图标系统

脚本内置 17 个常用 SVG 图标（闪电、灯泡、搜索、文件、图表等），颜色自动跟随主题 accent 色。JSON 中写 emoji 会自动映射到 SVG，确保跨设备渲染一致。

### 内容密度

- 每张海报文字总量 ≤ 200 字
- 封面标题 ≤ 10 字
- 封面要点 ≤ 4 条
- 每页内容卡片 ≤ 3 个 sections
- 金句页 details ≥ 3 条

## 方法论

Skill 内置了一套完整的文章拆分方法论，基于以下经典理论框架：

| 阶段 | 方法 | 作用 |
|------|------|------|
| **提取** | 金字塔逆向拆解 | 识别信息层级（结论→分论点→证据） |
| **提取** | 5W1H 扫描 | 确保不漏关键要素 |
| **提取** | MECE 分组检验 | 不重不漏 |
| **组织** | SCQA 叙事框架 | 决定卡片叙事顺序 |
| **组织** | LATCH 选型 | 匹配信息形状到页面布局 |
| **呈现** | 7±2 法则 / F型阅读 / 格式塔原理 | 控制认知负荷、引导视觉动线 |

详细方法论说明见 [SKILL.md](./SKILL.md)。

## 项目结构

```
article-poster-generator/
├── scripts/
│   └── generate_posters.py    # 核心渲染脚本（HTML模板 + Playwright截图）
├── SKILL.md                   # Claude Code Skill 定义（含完整方法论）
├── README.md
└── LICENSE
```

## 技术原理

```
JSON 数据 → Python 生成 HTML 页面 → Playwright 渲染截图 → 高清 PNG
```

1. **模板引擎**：使用 Python `string.Template` 将风格变量注入 CSS
2. **布局系统**：每种布局类型（cover/content/steps/grid/quote/summary）有独立的 HTML 生成函数
3. **渲染引擎**：Playwright 启动无头 Chromium，设置 2400×3600 viewport，逐页截图
4. **风格系统**：5 套完整的配色方案，通过 CSS 变量统一管理

## Contributing

欢迎贡献！你可以：

- 提交新的视觉风格
- 增加新的页面布局类型
- 改进内容拆分算法
- 提供更多语言支持

请提交 Issue 或 Pull Request。

## License

[MIT](./LICENSE)
