#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
Article Poster Generator v2
将 JSON 数据生成多张信息图海报（2400x3600 竖版 PNG）

Usage:
    python3 generate_posters.py --input posters.json --style dark-tech --output ~/Desktop/posters/

Styles: dark-tech | cyberpunk | minimal-biz | guochao | dark-green
"""

import argparse
import json
import os
import sys
import asyncio
import shutil
from datetime import datetime
from pathlib import Path
from string import Template

# ============================================================
# Style Definitions
# ============================================================

STYLES = {
    "dark-tech": {
        "name": "暗夜科技",
        "bg": "#1a1a1a",
        "bg_gradient": "linear-gradient(180deg, #1e1e1e 0%, #141414 100%)",
        "card_bg": "#242424",
        "card_bg_alt": "#1f1f1f",
        "card_border": "#333333",
        "text_primary": "#ffffff",
        "text_secondary": "#b8b8b8",
        "text_muted": "#666666",
        "accent": "#cc4444",
        "accent2": "#e87a7a",
        "accent3": "#8a2b2b",
        "accent_gradient": "linear-gradient(135deg, #cc4444, #e85d5d)",
        "tag_bg": "rgba(204,68,68,0.12)",
        "tag_border": "#cc4444",
        "highlight_bg": "rgba(204,68,68,0.08)",
        "divider": "#333333",
        "number_color": "rgba(204,68,68,0.25)",
        "dot_color": "rgba(204,68,68,0.08)",
        "border_colors": {
            "red": "#cc4444", "yellow": "#cc4444", "green": "#cc4444",
            "cyan": "#a0a0a0", "orange": "#e87a7a", "purple": "#8a2b2b"
        },
        "border_colors_list": ["#cc4444", "#e87a7a", "#a0a0a0", "#cc4444", "#8a2b2b", "#e87a7a"],
    },
    "cyberpunk": {
        "name": "赛博朋克",
        "bg": "#0a0a1a",
        "bg_gradient": "linear-gradient(180deg, #0a0a1a 0%, #0d0d2b 50%, #0a0a1a 100%)",
        "card_bg": "#10102a",
        "card_bg_alt": "#0d0d24",
        "card_border": "#1a1a40",
        "text_primary": "#F0F4F6",
        "text_secondary": "#9999cc",
        "text_muted": "#7a7ab8",
        "accent": "#00d4ff",
        "accent2": "#b347d9",
        "accent3": "#ff007c",
        "accent_gradient": "linear-gradient(135deg, #00d4ff, #b347d9)",
        "tag_bg": "rgba(0,212,255,0.10)",
        "tag_border": "#00d4ff",
        "highlight_bg": "rgba(0,212,255,0.06)",
        "divider": "#1a1a40",
        "number_color": "rgba(0,212,255,0.18)",
        "dot_color": "rgba(0,212,255,0.06)",
        "border_colors": {
            "red": "#ff007c", "yellow": "#00d4ff", "green": "#00d4ff",
            "cyan": "#00d4ff", "orange": "#b347d9", "purple": "#b347d9"
        },
        "border_colors_list": ["#00d4ff", "#b347d9", "#ff007c", "#00d4ff", "#b347d9", "#00d4ff"],
    },
    "minimal-biz": {
        "name": "极简清新",
        "bg": "#F0F7F7",
        "bg_gradient": "linear-gradient(180deg, #F0F7F7 0%, #E4F0EF 100%)",
        "card_bg": "#ffffff",
        "card_bg_alt": "#f8fafc",
        "card_border": "#e2e8f0",
        "text_primary": "#1C2226",
        "text_secondary": "#5E6A72",
        "text_muted": "#94a3b8",
        "accent": "#1A7D7D",
        "accent2": "#158073",
        "accent3": "#2BA8A0",
        "accent_gradient": "linear-gradient(135deg, #1A7D7D, #158073)",
        "tag_bg": "rgba(26,125,125,0.08)",
        "tag_border": "#1A7D7D",
        "highlight_bg": "rgba(26,125,125,0.06)",
        "divider": "#e2e8f0",
        "number_color": "rgba(26,125,125,0.10)",
        "dot_color": "rgba(26,125,125,0.04)",
        "border_colors": {
            "red": "#1A7D7D", "yellow": "#1A7D7D", "green": "#1A7D7D",
            "cyan": "#1A7D7D", "orange": "#1A7D7D", "purple": "#1A7D7D"
        },
        "border_colors_list": ["#1A7D7D", "#1A7D7D", "#1A7D7D", "#1A7D7D", "#1A7D7D", "#1A7D7D"],
    },
    "guochao": {
        "name": "黑金奢华",
        "bg": "#1a0a0a",
        "bg_gradient": "linear-gradient(180deg, #1a0a0a 0%, #1a0f0a 50%, #1a0a0a 100%)",
        "card_bg": "#2a1515",
        "card_bg_alt": "#241212",
        "card_border": "#3a2020",
        "text_primary": "#F0F4F6",
        "text_secondary": "#A0AAB2",
        "text_muted": "#7a7a82",
        "accent": "#d4a853",
        "accent2": "#c43a31",
        "accent3": "#a8a8b0",
        "accent_gradient": "linear-gradient(135deg, #d4a853, #c43a31)",
        "tag_bg": "rgba(212,168,83,0.10)",
        "tag_border": "#d4a853",
        "highlight_bg": "rgba(212,168,83,0.08)",
        "divider": "#3a2020",
        "number_color": "rgba(212,168,83,0.18)",
        "dot_color": "rgba(212,168,83,0.05)",
        "border_colors": {
            "red": "#c43a31", "yellow": "#d4a853", "green": "#d4a853",
            "cyan": "#a8a8b0", "orange": "#c43a31", "purple": "#d4a853"
        },
        "border_colors_list": ["#d4a853", "#c43a31", "#a8a8b0", "#d4a853", "#c43a31", "#a8a8b0"],
    },
    "dark-green": {
        "name": "暗夜青绿",
        "bg": "#0C1316",
        "bg_gradient": "linear-gradient(180deg, #0C1316 0%, #0a1012 100%)",
        "card_bg": "#172228",
        "card_bg_alt": "#121B20",
        "card_border": "#1C2A31",
        "text_primary": "#F0F4F6",
        "text_secondary": "#8A96A0",
        "text_muted": "#788691",
        "accent": "#3DB8B0",
        "accent2": "#2BA8A0",
        "accent3": "#1A7D7D",
        "accent_gradient": "linear-gradient(135deg, #3DB8B0, #2BA8A0)",
        "tag_bg": "rgba(61,184,176,0.10)",
        "tag_border": "#3DB8B0",
        "highlight_bg": "rgba(61,184,176,0.07)",
        "divider": "#1C2A31",
        "number_color": "rgba(61,184,176,0.18)",
        "dot_color": "rgba(61,184,176,0.05)",
        "border_colors": {
            "red": "#4F8AFF", "yellow": "#F5B041", "green": "#3DB8B0",
            "cyan": "#00E5FF", "orange": "#F5B041", "purple": "#4F8AFF"
        },
        "border_colors_list": ["#3DB8B0", "#00E5FF", "#4F8AFF", "#F5B041", "#2BA8A0", "#1A7D7D"],
    },
}

# ============================================================
# HTML Template Parts
# ============================================================

BASE_CSS = Template("""
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
    width: 2400px; height: 3600px;
    font-family: system-ui, "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
    background: ${bg};
    background: ${bg_gradient};
    color: ${text_primary};
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
}

.poster {
    width: 2400px; height: 3600px;
    padding: 100px 120px 90px;
    display: flex; flex-direction: column;
    position: relative;
    overflow: hidden;
}
.slide-num-bg {
    position: absolute; top: 20px; right: 40px;
    font-size: 520px; font-weight: 900;
    color: ${number_color};
    line-height: 1; letter-spacing: -14px;
    user-select: none; pointer-events: none;
}
.dot-grid {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    background-image: radial-gradient(${dot_color} 1.5px, transparent 1.5px);
    background-size: 48px 48px;
    opacity: 0.5;
}

/* ── header ── */
.header-row {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 40px; position: relative; z-index: 2;
}
.tag {
    display: inline-flex; align-items: center; gap: 18px;
    padding: 22px 44px;
    background: ${tag_bg}; border: 1.5px solid ${tag_border};
    border-radius: 60px; font-size: 52px; font-weight: 600;
    color: ${accent}; width: fit-content;
}
.tag-icon { font-size: 52px; }
.header-decoration {
    font-size: 38px; color: ${text_muted}; letter-spacing: 4px; opacity: 0.7;
}

.accent-bar {
    width: 140px; height: 12px;
    background: ${accent_gradient}; border-radius: 6px;
    margin-bottom: 40px;
}

/* ── titles (大幅增大) ── */
.main-title {
    font-size: 160px; font-weight: 900;
    line-height: 1.2; margin-bottom: 28px;
    letter-spacing: 2px; color: ${text_primary};
    position: relative; z-index: 2;
}
.subtitle {
    font-size: 68px; font-weight: 400;
    color: ${text_secondary};
    margin-bottom: 48px; line-height: 1.5;
    position: relative; z-index: 2;
}
.divider-line {
    width: 100%; height: 0;
    border-top: 2px dashed ${divider};
    margin: 36px 0; position: relative; z-index: 2;
}

/* ── cards (content) ── */
.cards-area {
    flex: 1; display: flex; flex-direction: column;
    justify-content: space-evenly;
    position: relative; z-index: 2;
}
.card {
    background: ${card_bg}; border: 1.5px solid ${card_border};
    border-radius: 28px; padding: 60px 68px;
    position: relative; overflow: hidden; z-index: 2;
}
.card-border-left {
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 8px; border-radius: 28px 0 0 28px;
}
.card-title {
    font-size: 120px; font-weight: 800;
    margin-bottom: 28px; line-height: 1.3; color: ${text_primary};
}
.card-content {
    font-size: 64px; font-weight: 400;
    line-height: 1.75; color: ${text_secondary};
}
.card-highlight {
    display: block; margin-top: 28px;
    padding: 28px 40px;
    background: ${highlight_bg};
    border-left: 7px solid ${accent};
    border-radius: 0 18px 18px 0;
    font-size: 64px; font-weight: 600;
    color: ${accent}; line-height: 1.55;
}
.card-meta {
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 18px; font-size: 42px; color: ${text_muted};
}
.card-meta-dot {
    width: 8px; height: 8px; border-radius: 50%; background: ${text_muted};
}

/* ── highlight list (cover) ── */
.highlights-area {
    flex: 1; display: flex; flex-direction: column;
    justify-content: space-evenly;
    position: relative; z-index: 2;
}
.highlight-list {
    list-style: none; padding: 0;
    flex: 1; display: flex; flex-direction: column;
    justify-content: space-evenly;
    position: relative; z-index: 2;
}
.highlight-list li {
    display: flex; align-items: center; gap: 32px;
    padding: 48px 56px;
    background: ${card_bg}; border: 1.5px solid ${card_border};
    border-left: 8px solid ${accent};
    border-radius: 24px;
    font-size: 76px; line-height: 1.55; color: ${text_secondary};
}
.highlight-num {
    flex-shrink: 0; width: 88px; height: 88px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 22px;
    background: ${tag_bg}; border: 1.5px solid ${tag_border};
    color: ${accent}; font-size: 42px; font-weight: 800;
}

/* ── cover ── */
.cover-title {
    font-size: 240px; font-weight: 900;
    line-height: 1.15; margin-bottom: 40px;
    letter-spacing: 4px; color: ${text_primary};
    position: relative; z-index: 2;
}
.cover-subtitle {
    font-size: 76px; color: ${accent};
    font-weight: 500; margin-bottom: 56px;
    line-height: 1.45; position: relative; z-index: 2;
}
.cover-section {
    flex: 1; display: flex; flex-direction: column;
    position: relative; z-index: 2;
}

/* ── summary ── */
.summary-area {
    flex: 1; display: flex; flex-direction: column;
    position: relative; z-index: 2;
}
.summary-box {
    background: ${card_bg}; border: 1.5px solid ${card_border};
    border-radius: 28px; padding: 72px 80px;
    margin-bottom: 56px; position: relative; z-index: 2; overflow: hidden;
}
.summary-box::before {
    content: ''; position: absolute;
    left: 0; top: 0; bottom: 0; width: 8px;
    background: ${accent_gradient}; border-radius: 28px 0 0 28px;
}
.summary-text {
    font-size: 88px; line-height: 1.7;
    color: ${text_secondary}; font-weight: 400;
}
.summary-quote-icon {
    font-size: 100px; color: ${accent}; opacity: 0.4;
    margin-bottom: 24px; display: block;
}

.action-label {
    display: flex; align-items: center; gap: 18px;
    font-size: 72px; font-weight: 700;
    color: ${accent}; margin-bottom: 40px;
    letter-spacing: 2px; position: relative; z-index: 2;
}
.action-label-line { flex: 1; height: 2px; background: ${divider}; }
.action-list {
    list-style: none; padding: 0;
    flex: 1; display: flex; flex-direction: column;
    justify-content: space-evenly;
    position: relative; z-index: 2;
}
.action-item {
    display: flex; align-items: center; gap: 36px;
    padding: 52px 60px;
    background: ${card_bg}; border: 1.5px solid ${card_border};
    border-radius: 24px;
    font-size: 80px; line-height: 1.45; color: ${text_primary};
}
.action-num {
    flex-shrink: 0; width: 90px; height: 90px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 50%; background: ${accent_gradient};
    color: #fff; font-size: 44px; font-weight: 800;
}

/* ── steps layout ── */
.steps-area {
    flex: 1; display: flex; flex-direction: column;
    justify-content: space-evenly;
    position: relative; z-index: 2;
}
.step-item {
    display: flex; gap: 44px; align-items: flex-start;
}
.step-left {
    display: flex; flex-direction: column; align-items: center;
    flex-shrink: 0; width: 120px;
}
.step-num {
    width: 110px; height: 110px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 50%; background: ${accent_gradient};
    color: #fff; font-size: 52px; font-weight: 900;
}
.step-line {
    width: 4px; flex: 1; min-height: 40px;
    background: ${divider}; margin-top: 12px;
}
.step-right {
    flex: 1; padding: 40px 48px 40px 0;
    background: ${card_bg}; border: 1.5px solid ${card_border};
    border-radius: 24px; padding: 44px 48px;
}
.step-title {
    font-size: 120px; font-weight: 800;
    margin-bottom: 20px; line-height: 1.25; color: ${text_primary};
}
.step-content {
    font-size: 64px; line-height: 1.7; color: ${text_secondary};
}

/* ── grid layout (2 col) ── */
.grid-area {
    flex: 1; display: flex; flex-direction: column;
    justify-content: space-evenly;
    position: relative; z-index: 2;
}
.grid-row {
    display: flex; gap: 36px;
}
.grid-cell {
    flex: 1;
    background: ${card_bg}; border: 1.5px solid ${card_border};
    border-radius: 28px; padding: 56px 52px;
    position: relative; overflow: hidden;
    display: flex; flex-direction: column;
}
.grid-cell-border {
    position: absolute; top: 0; left: 0; right: 0;
    height: 8px; border-radius: 28px 28px 0 0;
}
.grid-cell-icon {
    font-size: 80px; margin-bottom: 24px; display: block;
}
.grid-cell-title {
    font-size: 100px; font-weight: 800;
    margin-bottom: 20px; line-height: 1.25; color: ${text_primary};
}
.grid-cell-content {
    font-size: 64px; line-height: 1.7; color: ${text_secondary};
}

/* ── quote layout ── */
.quote-area {
    flex: 1; display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    position: relative; z-index: 2;
    text-align: center;
}
.quote-mark {
    font-size: 200px; color: ${accent}; opacity: 0.15;
    line-height: 1; margin-bottom: 20px;
}
.quote-text {
    font-size: 110px; font-weight: 800;
    line-height: 1.35; color: ${text_primary};
    max-width: 1900px; margin-bottom: 48px;
}
.quote-source {
    font-size: 60px; color: ${text_muted};
    font-weight: 400; line-height: 1.5;
}
.quote-detail-cards {
    width: 100%; margin-top: 56px;
    display: flex; flex-direction: column; gap: 28px;
}
.quote-detail-card {
    display: flex; align-items: flex-start; gap: 28px;
    padding: 44px 52px;
    background: ${card_bg}; border: 1.5px solid ${card_border};
    border-left: 8px solid ${accent};
    border-radius: 24px;
    text-align: left;
}
.quote-detail-label {
    font-size: 56px; color: ${accent}; font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 14px;
}
.quote-detail-text {
    font-size: 68px; line-height: 1.6; color: ${text_secondary};
    font-weight: 500;
}

/* ── footer ── */
.footer {
    display: flex; align-items: center; justify-content: space-between;
    padding-top: 32px; border-top: 1.5px solid ${divider};
    margin-top: 48px; position: relative; z-index: 2; flex-shrink: 0;
}
.page-indicator {
    font-size: 42px; color: ${text_muted}; font-weight: 600; letter-spacing: 2px;
}
.watermark {
    font-size: 42px; color: ${text_muted}; opacity: 0.5;
    letter-spacing: 3px; font-weight: 500;
}
.footer-bar {
    position: absolute; bottom: 0; left: 0; right: 0; height: 6px;
}

/* ── stats row (cover) ── */
.stats-row {
    display: flex; gap: 24px;
    margin-bottom: 40px;
    position: relative; z-index: 2;
}
.stat-chip {
    display: flex; align-items: center; gap: 10px;
    padding: 18px 36px;
    background: ${card_bg}; border: 1.5px solid ${card_border};
    border-radius: 18px;
    font-size: 48px; color: ${text_secondary};
}
.stat-chip .stat-val {
    font-weight: 700; color: ${accent};
}

.spacer-sm { height: 20px; flex-shrink: 0; }
.spacer-md { height: 36px; flex-shrink: 0; }
.spacer-lg { height: 56px; flex-shrink: 0; }
.flex-grow { flex: 1; min-height: 20px; }
""")

# --- Cyberpunk extra CSS (glowing effects) ---
CYBERPUNK_EXTRA_CSS = """
/* ── 赛博朋克：锋利切角 + 霓虹发光 ── */
.card, .grid-cell, .action-item, .summary-box, .step-right, .highlight-list li {
    border-radius: 4px !important;
}
.tag { border-radius: 4px !important; }
.highlight-num { border-radius: 4px !important; }

/* 纯冷白标题，不用渐变 */
.cover-title { color: #F0F4F6; }
.main-title { color: #F0F4F6; }
.step-title { color: #00d4ff; }
.quote-text { color: #00d4ff; }

/* 霓虹发光 */
.card {
    box-shadow: 0 0 8px rgba(0,212,255,0.15), 0 0 24px rgba(0,212,255,0.06);
    border-top: 1px solid rgba(0,212,255,0.15);
}
.grid-cell {
    box-shadow: 0 0 8px rgba(0,212,255,0.12), 0 0 20px rgba(0,212,255,0.05);
    border-top: 1px solid rgba(0,212,255,0.15);
}
.step-right {
    box-shadow: 0 0 8px rgba(0,212,255,0.12), 0 0 20px rgba(0,212,255,0.05);
    border-top: 1px solid rgba(0,212,255,0.12);
}
.action-item {
    box-shadow: 0 0 6px rgba(0,212,255,0.10), 0 0 16px rgba(0,212,255,0.04);
    border-top: 1px solid rgba(0,212,255,0.10);
}
.summary-box {
    box-shadow: 0 0 10px rgba(0,212,255,0.12), 0 0 24px rgba(0,212,255,0.06);
}
.tag {
    box-shadow: 0 0 8px rgba(0,212,255,0.20), 0 0 16px rgba(0,212,255,0.10);
    border-color: rgba(0,212,255,0.6);
}
.highlight-list li {
    box-shadow: 0 0 6px rgba(0,212,255,0.08);
    border-top: 1px solid rgba(0,212,255,0.10);
}

/* 步骤编号发光 */
.step-num {
    box-shadow: 0 0 12px rgba(0,212,255,0.4), 0 0 24px rgba(0,212,255,0.15);
}
.action-num {
    box-shadow: 0 0 10px rgba(0,212,255,0.3), 0 0 20px rgba(0,212,255,0.12);
}

/* 顶部霓虹线 */
.poster::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #00d4ff, #b347d9, #ff007c);
    box-shadow: 0 0 12px rgba(0,212,255,0.5), 0 0 24px rgba(179,71,217,0.3);
}
.footer-bar {
    background: linear-gradient(90deg, #ff007c, #b347d9, #00d4ff);
    box-shadow: 0 4px 12px rgba(0,212,255,0.3);
}

/* HUD 装饰码 */
.poster::before {
    content: 'SYS.REQ // NEON_GRID v4.2 // LAT:35.68 LON:139.76';
    position: absolute; bottom: 100px; left: 140px;
    font-size: 22px; color: rgba(0,212,255,0.12);
    letter-spacing: 4px; font-family: monospace;
    pointer-events: none; z-index: 1;
}
"""

# --- Guochao extra CSS ---
GUOCHAO_EXTRA_CSS = """
/* ── 黑金奢华：邀请函质感 ── */
.cover-title { color: #FFFFFF; }
.main-title { color: #FFFFFF; }
.step-title { color: #d4a853; }
.quote-text { color: #d4a853; }
.card-title { color: #FFFFFF; }

/* 内框装饰（精致邀请函） */
.poster::before {
    content: ''; position: absolute;
    top: 36px; left: 36px; right: 36px; bottom: 36px;
    border: 1.5px solid rgba(212,168,83,0.12);
    border-radius: 8px; pointer-events: none; z-index: 1;
}

/* 卡片质感 */
.card, .grid-cell, .step-right {
    border-color: rgba(212,168,83,0.15);
    border-top: 1px solid rgba(212,168,83,0.25);
    box-shadow: 0 16px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(212,168,83,0.06);
}
.action-item {
    border-color: rgba(212,168,83,0.12);
    border-top: 1px solid rgba(212,168,83,0.20);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(212,168,83,0.05);
}
.summary-box {
    border-color: rgba(212,168,83,0.15);
    border-top: 1px solid rgba(212,168,83,0.25);
    box-shadow: 0 16px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(212,168,83,0.06);
}
.highlight-list li {
    border-color: rgba(212,168,83,0.12);
    border-top: 1px solid rgba(212,168,83,0.20);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(212,168,83,0.05);
}
.tag { border-color: rgba(212,168,83,0.5); color: #d4a853; }

.footer-bar { background: linear-gradient(90deg, #c43a31, #d4a853, #c43a31); }
.poster::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #c43a31, #d4a853, #c43a31);
}
"""

MINIMAL_BIZ_EXTRA_CSS = """
/* ── 极简清新：Apple/Stripe 级 SaaS 质感 ── */
.card, .grid-cell, .step-right {
    border: 1px solid rgba(26,125,125,0.15);
    box-shadow: 0 20px 40px -10px rgba(26,125,125,0.08), 0 4px 10px rgba(0,0,0,0.02);
}
.action-item {
    border: 1px solid rgba(26,125,125,0.12);
    box-shadow: 0 12px 24px -8px rgba(26,125,125,0.06), 0 2px 6px rgba(0,0,0,0.02);
}
.summary-box {
    border: 1px solid rgba(26,125,125,0.15);
    box-shadow: 0 20px 40px -10px rgba(26,125,125,0.08), 0 4px 10px rgba(0,0,0,0.02);
}
.highlight-list li {
    border: 1px solid rgba(26,125,125,0.12);
    box-shadow: 0 12px 24px -8px rgba(26,125,125,0.06), 0 2px 6px rgba(0,0,0,0.02);
}
.cover-title { color: #1A7D7D; }
.step-title { color: #1A7D7D; }
.quote-text { color: #1A7D7D; }
.poster::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #158073, #1A7D7D, #2BA8A0);
}
.footer-bar { background: linear-gradient(90deg, #158073, #1A7D7D, #2BA8A0); }
"""

DARK_TECH_EXTRA_CSS = """
/* ── 暗夜科技：CNC金属切割质感 ── */
.card, .grid-cell, .step-right {
    border: 1px solid #111111;
    border-top: 1px solid #3a3a3a;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
}
.action-item {
    border: 1px solid #111111;
    border-top: 1px solid #3a3a3a;
    box-shadow: 0 10px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
}
.summary-box {
    border: 1px solid #111111;
    border-top: 1px solid #3a3a3a;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
}
.highlight-list li {
    border: 1px solid #111111;
    border-top: 1px solid #3a3a3a;
    box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
}

/* 猩红标题 */
.cover-title { color: #ffffff; }
.step-title { color: #cc4444; }
.quote-text { color: #cc4444; }

.footer-bar { background: linear-gradient(90deg, #8a2b2b, #cc4444, #8a2b2b); }
.poster::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #8a2b2b, #cc4444, #e85d5d, #cc4444, #8a2b2b);
}
"""

DARK_GREEN_EXTRA_CSS = """
.cover-title { color: #3DB8B0; }
.card { box-shadow: 0 0 30px rgba(61,184,176,0.04); border-top: 1px solid rgba(255,255,255,0.04); }
.grid-cell { box-shadow: 0 0 30px rgba(61,184,176,0.04); border-top: 1px solid rgba(255,255,255,0.04); }
.step-right { box-shadow: 0 0 20px rgba(61,184,176,0.03); border-top: 1px solid rgba(255,255,255,0.04); }
.tag { box-shadow: 0 0 12px rgba(61,184,176,0.08); }
.footer-bar { background: linear-gradient(90deg, #1A7D7D, #2BA8A0, #3DB8B0); }
.poster::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #1A7D7D, #2BA8A0, #3DB8B0);
}
.step-title { color: #3DB8B0; }
.quote-text { color: #3DB8B0; }
"""


def get_extra_css(style_id):
    if style_id == "cyberpunk":
        return CYBERPUNK_EXTRA_CSS
    elif style_id == "guochao":
        return GUOCHAO_EXTRA_CSS
    elif style_id == "minimal-biz":
        return MINIMAL_BIZ_EXTRA_CSS
    elif style_id == "dark-tech":
        return DARK_TECH_EXTRA_CSS
    elif style_id == "dark-green":
        return DARK_GREEN_EXTRA_CSS
    return ""


# ============================================================
# HTML Generators
# ============================================================

HTML_WRAPPER = Template("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=2400, initial-scale=1.0">
<style>
${css}
${extra_css}
${svg_css}
</style>
</head>
<body>
${body}
</body>
</html>""")


def escape_html(text):
    if not text:
        return ""
    return (text.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


# ── SVG Icon Library (Lucide-style monochrome line icons) ──
_S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'

SVG_ICONS = {
    # 通用
    "⚡": f'<svg {_S}><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "💡": f'<svg {_S}><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2v1"/><path d="M12 7a4 4 0 0 0-4 4c0 1.5.8 2.8 2 3.5V18h4v-3.5c1.2-.7 2-2 2-3.5a4 4 0 0 0-4-4z"/></svg>',
    "📊": f'<svg {_S}><rect x="3" y="12" width="4" height="9" rx="1"/><rect x="10" y="7" width="4" height="14" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>',
    "📋": f'<svg {_S}><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M9 2v2h6V2"/><path d="M9 12h6"/><path d="M9 16h4"/></svg>',
    "🛠": f'<svg {_S}><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94L6.73 20.15a2.1 2.1 0 0 1-3-3l6.78-6.78a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "🔑": f'<svg {_S}><circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.3 9.3"/><path d="m18.5 5.5 3 3"/></svg>',
    "🔍": f'<svg {_S}><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "📄": f'<svg {_S}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="13" y2="17"/></svg>',
    "🧠": f'<svg {_S}><path d="M12 2a6 6 0 0 0-6 6c0 2 1 3.5 2 4.5V18h8v-5.5c1-1 2-2.5 2-4.5a6 6 0 0 0-6-6z"/><path d="M9 18v2a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2v-2"/><path d="M12 2v4"/><path d="M8 6l2 2"/><path d="M16 6l-2 2"/></svg>',
    "💰": f'<svg {_S}><circle cx="12" cy="12" r="10"/><path d="M9 12h6"/><path d="M12 9v6"/><path d="M15 9.5c-.5-1-1.5-1.5-3-1.5s-3 1-3 2.5 1.5 2 3 2.5 3 1 3 2.5-1 2.5-3 2.5-2.5-.5-3-1.5"/></svg>',
    "💬": f'<svg {_S}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "⚠": f'<svg {_S}><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "🎨": f'<svg {_S}><circle cx="13.5" cy="6.5" r="2.5"/><path d="M22 12c0 5.5-4.5 10-10 10S2 17.5 2 12 6.5 2 12 2c1.5 0 3 .3 4.3.9"/><circle cx="8" cy="15" r="1.5" fill="currentColor"/><circle cx="12" cy="17" r="1.5" fill="currentColor"/><circle cx="16" cy="15" r="1.5" fill="currentColor"/></svg>',
    "🌍": f'<svg {_S}><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "🛡": f'<svg {_S}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "📌": f'<svg {_S}><path d="M15 4.5L7.5 12l-3-3L12 1.5z"/><path d="M9 15l-6 6"/><path d="M14.5 4L20 9.5"/></svg>',
    "🔧": f'<svg {_S}><path d="M6.3 20.3a2.4 2.4 0 0 0 3.4 0L12 18l-6-6-2.3 2.3a2.4 2.4 0 0 0 0 3.4z"/><path d="m22 2-6.3 6.3"/><path d="m18.3 6.3-4.6-4.6"/><path d="M2 22l6-6"/></svg>',
}

# CSS for inline SVG icons
SVG_ICON_CSS = """
.svg-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 1em; height: 1em; vertical-align: middle;
}
.svg-icon svg {
    width: 100%; height: 100%;
}
.tag .svg-icon { width: 0.9em; height: 0.9em; }
.grid-cell-icon .svg-icon { width: 1em; height: 1em; }
"""


def emoji_to_svg(emoji):
    """Convert emoji to inline SVG if available, otherwise return emoji as-is."""
    if emoji in SVG_ICONS:
        return f'<span class="svg-icon">{SVG_ICONS[emoji]}</span>'
    return emoji


# ── Section border color → icon mapping ──
SECTION_ICONS = {
    "red": "◆", "yellow": "◆", "green": "◆",
    "cyan": "◆", "orange": "◆", "purple": "◆",
}

CONTENT_DECORATORS = ["◆", "◇", "▸", "●", "○", "■"]


def render_cover(slide, style, style_id, total_slides):
    tag = escape_html(slide.get("tag", ""))
    tag_icon = emoji_to_svg(slide.get("tag_icon", "📌"))
    title = escape_html(slide.get("title", "")).replace("\n", "<br>")
    subtitle = escape_html(slide.get("subtitle", ""))
    highlights = slide.get("highlights", [])
    slide_num = slide.get("slide_number", "00")
    border_colors = style["border_colors_list"]

    # Build numbered highlight items with colored accent
    hl_items = ""
    for i, h in enumerate(highlights):
        color = border_colors[i % len(border_colors)]
        num_str = str(i + 1).zfill(2)
        hl_items += f'''<li style="border-left-color: {color};">
            <span class="highlight-num" style="border-color: {color}; color: {color};">{num_str}</span>
            <span>{escape_html(h)}</span>
        </li>\n'''

    # Stats chips
    stats_html = f"""
    <div class="stats-row">
        <div class="stat-chip">{emoji_to_svg("📄")} 共 <span class="stat-val">&nbsp;{total_slides}&nbsp;</span> 页</div>
        <div class="stat-chip">{emoji_to_svg("📊")} 要点 <span class="stat-val">&nbsp;{len(highlights)}&nbsp;</span> 条</div>
    </div>"""

    body = f"""
<div class="poster">
    <div class="dot-grid"></div>
    <div class="slide-num-bg">{escape_html(slide_num)}</div>
    <div class="header-row">
        <div class="tag"><span class="tag-icon">{tag_icon}</span> {tag}</div>
        <div class="header-decoration">INFOGRAPHIC</div>
    </div>
    <div class="cover-section">
        <div class="accent-bar"></div>
        <div class="cover-title">{title}</div>
        <div class="cover-subtitle">{subtitle}</div>
        {stats_html}
        <div class="divider-line"></div>
        <div class="highlights-area">
            <ul class="highlight-list">
                {hl_items}
            </ul>
        </div>
    </div>
    <div class="footer">
        <div class="page-indicator">{slide_num} / {str(total_slides - 1).zfill(2)}</div>
        <div class="watermark">INFOGRAPHIC</div>
    </div>
    <div class="footer-bar"></div>
</div>"""
    return body


def render_content(slide, style, style_id, total_slides):
    tag = escape_html(slide.get("tag", ""))
    tag_icon = emoji_to_svg(slide.get("tag_icon", "📋"))
    title = escape_html(slide.get("title", ""))
    sections = slide.get("sections", [])
    slide_num = slide.get("slide_number", "01")
    border_colors = style["border_colors_list"]

    cards_html = ""
    for idx, sec in enumerate(sections):
        sec_title = escape_html(sec.get("title", ""))
        sec_content = escape_html(sec.get("content", ""))
        sec_highlight = escape_html(sec.get("highlight", ""))
        border_color_key = sec.get("border_color", "red")
        border_color = style["border_colors"].get(border_color_key, style["accent"])

        # Icon based on border color
        icon = SECTION_ICONS.get(border_color_key, "◆")

        highlight_html = ""
        if sec_highlight:
            highlight_html = f'<span class="card-highlight">{sec_highlight}</span>'

        # Number label inside card
        card_num = str(idx + 1).zfill(2)

        cards_html += f"""
        <div class="card">
            <div class="card-border-left" style="background: {border_color};"></div>
            <div class="card-meta">
                <span style="color: {border_color}; font-weight: 700;">#{card_num}</span>
                <span class="card-meta-dot"></span>
                <span>{icon} {escape_html(sec.get("title", ""))[:8]}</span>
            </div>
            <div class="spacer-sm"></div>
            <div class="card-title">{sec_title}</div>
            <div class="card-content">{sec_content}{highlight_html}</div>
        </div>"""

    body = f"""
<div class="poster">
    <div class="dot-grid"></div>
    <div class="slide-num-bg">{escape_html(slide_num)}</div>
    <div class="header-row">
        <div class="tag"><span class="tag-icon">{tag_icon}</span> {tag}</div>
        <div class="header-decoration">PAGE {escape_html(slide_num)}</div>
    </div>
    <div class="accent-bar"></div>
    <div class="main-title">{title}</div>
    <div class="divider-line"></div>
    <div class="cards-area">
        {cards_html}
    </div>
    <div class="footer">
        <div class="page-indicator">{slide_num} / {str(total_slides - 1).zfill(2)}</div>
        <div class="watermark">INFOGRAPHIC</div>
    </div>
    <div class="footer-bar"></div>
</div>"""
    return body


def render_summary(slide, style, style_id, total_slides):
    tag = escape_html(slide.get("tag", "总结"))
    tag_icon = emoji_to_svg(slide.get("tag_icon", "💡"))
    title = escape_html(slide.get("title", "核心观点"))
    summary_text = escape_html(slide.get("summary_text", ""))
    action_items = slide.get("action_items", [])
    slide_num = slide.get("slide_number", "06")

    actions_html = ""
    for i, item in enumerate(action_items, 1):
        actions_html += f"""
        <div class="action-item">
            <span class="action-num">{i}</span>
            {escape_html(item)}
        </div>"""

    body = f"""
<div class="poster">
    <div class="dot-grid"></div>
    <div class="slide-num-bg">{escape_html(slide_num)}</div>
    <div class="header-row">
        <div class="tag"><span class="tag-icon">{tag_icon}</span> {tag}</div>
        <div class="header-decoration">SUMMARY</div>
    </div>
    <div class="accent-bar"></div>
    <div class="main-title">{title}</div>
    <div class="divider-line"></div>
    <div class="summary-area">
        <div class="summary-box">
            <span class="summary-quote-icon">❝</span>
            <div class="summary-text">{summary_text}</div>
        </div>
        <div class="action-label">
            <span>{emoji_to_svg("📋")} 行动建议</span>
            <span class="action-label-line"></span>
        </div>
        <ul class="action-list">
            {actions_html}
        </ul>
    </div>
    <div class="footer">
        <div class="page-indicator">{slide_num} / {str(total_slides - 1).zfill(2)}</div>
        <div class="watermark">INFOGRAPHIC</div>
    </div>
    <div class="footer-bar"></div>
</div>"""
    return body


def render_steps(slide, style, style_id, total_slides):
    """Render steps/timeline layout - big numbered steps with connecting line."""
    tag = escape_html(slide.get("tag", ""))
    tag_icon = emoji_to_svg(slide.get("tag_icon", "📋"))
    title = escape_html(slide.get("title", ""))
    steps = slide.get("steps", [])
    slide_num = slide.get("slide_number", "01")
    border_colors = style["border_colors_list"]

    steps_html = ""
    for idx, step in enumerate(steps):
        color = border_colors[idx % len(border_colors)]
        step_title = escape_html(step.get("title", ""))
        step_content = escape_html(step.get("content", ""))
        line_html = '<div class="step-line"></div>' if idx < len(steps) - 1 else ''

        steps_html += f"""
        <div class="step-item">
            <div class="step-left">
                <div class="step-num" style="background: {color};">{idx + 1}</div>
                {line_html}
            </div>
            <div class="step-right">
                <div class="step-title">{step_title}</div>
                <div class="step-content">{step_content}</div>
            </div>
        </div>"""

    body = f"""
<div class="poster">
    <div class="dot-grid"></div>
    <div class="slide-num-bg">{escape_html(slide_num)}</div>
    <div class="header-row">
        <div class="tag"><span class="tag-icon">{tag_icon}</span> {tag}</div>
        <div class="header-decoration">PAGE {escape_html(slide_num)}</div>
    </div>
    <div class="accent-bar"></div>
    <div class="main-title">{title}</div>
    <div class="divider-line"></div>
    <div class="steps-area">
        {steps_html}
    </div>
    <div class="footer">
        <div class="page-indicator">{slide_num} / {str(total_slides - 1).zfill(2)}</div>
        <div class="watermark">INFOGRAPHIC</div>
    </div>
    <div class="footer-bar"></div>
</div>"""
    return body


def render_grid(slide, style, style_id, total_slides):
    """Render 2-column grid layout - for tips, pitfalls, comparisons."""
    tag = escape_html(slide.get("tag", ""))
    tag_icon = emoji_to_svg(slide.get("tag_icon", "📋"))
    title = escape_html(slide.get("title", ""))
    cells = slide.get("cells", [])
    slide_num = slide.get("slide_number", "01")
    border_colors = style["border_colors_list"]

    # Build rows of 2
    rows_html = ""
    for i in range(0, len(cells), 2):
        cells_html = ""
        for j in range(2):
            if i + j < len(cells):
                cell = cells[i + j]
                color = border_colors[(i + j) % len(border_colors)]
                icon = emoji_to_svg(cell.get("icon", "◆"))
                c_title = escape_html(cell.get("title", ""))
                c_content = escape_html(cell.get("content", ""))
                cells_html += f"""
                <div class="grid-cell">
                    <div class="grid-cell-border" style="background: {color};"></div>
                    <div class="grid-cell-icon">{icon}</div>
                    <div class="grid-cell-title">{c_title}</div>
                    <div class="grid-cell-content">{c_content}</div>
                </div>"""
        rows_html += f'<div class="grid-row">{cells_html}</div>'

    body = f"""
<div class="poster">
    <div class="dot-grid"></div>
    <div class="slide-num-bg">{escape_html(slide_num)}</div>
    <div class="header-row">
        <div class="tag"><span class="tag-icon">{tag_icon}</span> {tag}</div>
        <div class="header-decoration">PAGE {escape_html(slide_num)}</div>
    </div>
    <div class="accent-bar"></div>
    <div class="main-title">{title}</div>
    <div class="divider-line"></div>
    <div class="grid-area">
        {rows_html}
    </div>
    <div class="footer">
        <div class="page-indicator">{slide_num} / {str(total_slides - 1).zfill(2)}</div>
        <div class="watermark">INFOGRAPHIC</div>
    </div>
    <div class="footer-bar"></div>
</div>"""
    return body


def render_quote(slide, style, style_id, total_slides):
    """Render big quote/highlight layout - single impactful statement."""
    tag = escape_html(slide.get("tag", ""))
    tag_icon = emoji_to_svg(slide.get("tag_icon", "💬"))
    quote_text = escape_html(slide.get("quote", ""))
    source = escape_html(slide.get("source", ""))
    details = slide.get("details", [])
    slide_num = slide.get("slide_number", "01")

    details_html = ""
    if details:
        detail_cards = ""
        for d in details:
            label = escape_html(d.get("label", ""))
            text = escape_html(d.get("text", ""))
            detail_cards += f"""
            <div class="quote-detail-card">
                <div>
                    <div class="quote-detail-label">{label}</div>
                    <div class="quote-detail-text">{text}</div>
                </div>
            </div>"""
        details_html = f'<div class="quote-detail-cards">{detail_cards}</div>'

    source_html = f'<div class="quote-source">— {source}</div>' if source else ''

    body = f"""
<div class="poster">
    <div class="dot-grid"></div>
    <div class="slide-num-bg">{escape_html(slide_num)}</div>
    <div class="header-row">
        <div class="tag"><span class="tag-icon">{tag_icon}</span> {tag}</div>
        <div class="header-decoration">PAGE {escape_html(slide_num)}</div>
    </div>
    <div class="quote-area">
        <div class="quote-mark">❝</div>
        <div class="quote-text">{quote_text}</div>
        {source_html}
        {details_html}
    </div>
    <div class="footer">
        <div class="page-indicator">{slide_num} / {str(total_slides - 1).zfill(2)}</div>
        <div class="watermark">INFOGRAPHIC</div>
    </div>
    <div class="footer-bar"></div>
</div>"""
    return body


def generate_html(slide, style_id, total_slides):
    style = STYLES[style_id]
    slide_type = slide.get("type", "content")

    css = BASE_CSS.substitute(**style)
    extra_css = get_extra_css(style_id)

    if slide_type == "cover":
        body = render_cover(slide, style, style_id, total_slides)
    elif slide_type == "summary":
        body = render_summary(slide, style, style_id, total_slides)
    elif slide_type == "steps":
        body = render_steps(slide, style, style_id, total_slides)
    elif slide_type == "grid":
        body = render_grid(slide, style, style_id, total_slides)
    elif slide_type == "quote":
        body = render_quote(slide, style, style_id, total_slides)
    else:
        body = render_content(slide, style, style_id, total_slides)

    return HTML_WRAPPER.substitute(css=css, extra_css=extra_css, svg_css=SVG_ICON_CSS, body=body)


# ============================================================
# Screenshot Engine
# ============================================================

async def capture_screenshots(slides_html, output_dir, data):
    from playwright.async_api import async_playwright

    output_path = Path(output_dir).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)

    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 2400, "height": 3600},
            device_scale_factor=1,
        )

        for i, (slide, html) in enumerate(zip(data["slides"], slides_html)):
            slide_num = slide.get("slide_number", str(i).zfill(2))
            slide_type = slide.get("type", "content")
            filename = f"slide_{slide_num}_{slide_type}.png"
            filepath = output_path / filename

            # Save HTML for debugging
            html_path = output_path / f"slide_{slide_num}_{slide_type}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

            # Screenshot
            page = await context.new_page()
            await page.set_content(html, wait_until="networkidle")
            await page.screenshot(path=str(filepath), full_page=False)
            await page.close()

            results.append(str(filepath))
            print(f"[OK] {filename} -> {filepath}")

        await browser.close()

    return results


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Article Poster Generator")
    parser.add_argument("--input", "-i", required=True, help="JSON input file path")
    parser.add_argument("--style", "-s", default=None,
                        choices=["dark-tech", "cyberpunk", "minimal-biz", "guochao", "dark-green"],
                        help="Style template (overrides JSON style)")
    parser.add_argument("--output", "-o", default="./posters/",
                        help="Output base directory (default: ./posters/)")
    parser.add_argument("--topic", "-t", default=None,
                        help="Topic name for folder (default: extracted from cover title)")

    args = parser.parse_args()

    # Read JSON
    input_path = Path(args.input).expanduser()
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Determine style
    style_id = args.style or data.get("style", "dark-tech")
    if style_id not in STYLES:
        print(f"[ERROR] Unknown style: {style_id}. Options: {', '.join(STYLES.keys())}")
        sys.exit(1)

    # Build output path: ./posters/YYMMDD-主题/风格/
    topic = args.topic or data.get("topic", "")
    if not topic:
        for slide in data.get("slides", []):
            if slide.get("type") == "cover":
                topic = slide.get("title", "").replace("\n", "").strip()
                break
    if not topic:
        topic = "untitled"
    # Sanitize topic for filesystem
    topic = topic.replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "")

    date_prefix = datetime.now().strftime("%y%m%d")
    topic_dir = Path(args.output).expanduser() / f"{date_prefix}-{topic}"
    style_dir = topic_dir / style_id

    topic_dir.mkdir(parents=True, exist_ok=True)
    style_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON to topic root
    json_dest = topic_dir / "poster_data.json"
    shutil.copy2(str(input_path), str(json_dest))
    print(f"[INFO] JSON saved: {json_dest}")

    print(f"[INFO] Style: {STYLES[style_id]['name']} ({style_id})")
    print(f"[INFO] Slides: {len(data['slides'])}")
    print(f"[INFO] Output: {style_dir}")
    print()

    # Generate HTML for each slide
    total_slides = len(data["slides"])
    slides_html = []
    for slide in data["slides"]:
        html = generate_html(slide, style_id, total_slides)
        slides_html.append(html)

    # Screenshot — output to style subdirectory
    results = asyncio.run(capture_screenshots(slides_html, str(style_dir), data))

    print()
    print(f"[DONE] Generated {len(results)} posters")
    print(f"[DONE] Topic dir: {topic_dir}")
    print(f"[DONE] Style dir: {style_dir}")
    for r in results:
        print(f"  {r}")


if __name__ == "__main__":
    main()
