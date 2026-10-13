"""
MarkToHTML - Core Converter Engine
Converts Markdown to standalone, styled HTML with syntax highlighting.
"""

import os
import re
import markdown
from pygments.formatters import HtmlFormatter

from config_manager import load_style_config, build_css_from_config

# CSS Themes
GITHUB_LIGHT_CSS = """
:root {
    --color-canvas-default: #ffffff;
    --color-canvas-subtle: #f6f8fa;
    --color-fg-default: #1f2328;
    --color-fg-muted: #656d76;
    --color-border-default: #d0d7de;
    --color-border-muted: #hsla(210,18%,87%,1);
    --color-accent-fg: #0969da;
    --color-accent-emphasis: #0969da;
    --code-bg: #f6f8fa;
}
"""

MODERN_CHARCOAL_CSS = """
:root {
    --color-canvas-default: #1e1e20;
    --color-canvas-subtle: #26262a;
    --color-fg-default: #e4e4e7;
    --color-fg-muted: #a1a1aa;
    --color-border-default: #38383e;
    --color-border-muted: #27272b;
    --color-accent-fg: #38bdf8;
    --color-accent-emphasis: #0284c7;
    --code-bg: #27272b;
}
"""

GITHUB_DARK_CSS = """
:root {
    --color-canvas-default: #0d1117;
    --color-canvas-subtle: #161b22;
    --color-fg-default: #e6edf3;
    --color-fg-muted: #848d97;
    --color-border-default: #30363d;
    --color-border-muted: #21262d;
    --color-accent-fg: #2f81f7;
    --color-accent-emphasis: #1f6feb;
    --code-bg: #161b22;
}
"""

NOTION_CSS = """
:root {
    --color-canvas-default: #fbfbfa;
    --color-canvas-subtle: #f1f1ef;
    --color-fg-default: #37352f;
    --color-fg-muted: #787774;
    --color-border-default: #e9e9e8;
    --color-border-muted: #eeeeec;
    --color-accent-fg: #0b6e99;
    --color-accent-emphasis: #0b6e99;
    --code-bg: #f7f6f3;
}
"""

LIGHT_MODERN_CSS = """
:root {
    --color-canvas-default: #ffffff;
    --color-canvas-subtle: #f8f8f8;
    --color-fg-default: #1f1f1f;
    --color-fg-muted: #616161;
    --color-border-default: #e5e5e5;
    --color-border-muted: #eeeeee;
    --color-accent-fg: #005fb8;
    --color-accent-emphasis: #004e96;
    --code-bg: #f8f8f8;
}
"""

DRACULA_CSS = """
:root {
    --color-canvas-default: #282a36;
    --color-canvas-subtle: #21222c;
    --color-fg-default: #f8f8f2;
    --color-fg-muted: #6272a4;
    --color-border-default: #44475a;
    --color-border-muted: #343746;
    --color-accent-fg: #bd93f9;
    --color-accent-emphasis: #ff79c6;
    --code-bg: #1e1f29;
}
"""

NORD_CSS = """
:root {
    --color-canvas-default: #2e3440;
    --color-canvas-subtle: #242933;
    --color-fg-default: #d8dee9;
    --color-fg-muted: #7b88a1;
    --color-border-default: #434c5e;
    --color-border-muted: #3b4252;
    --color-accent-fg: #88c0d0;
    --color-accent-emphasis: #81a1c1;
    --code-bg: #242933;
}
"""

SOLARIZED_LIGHT_CSS = """
:root {
    --color-canvas-default: #fdf6e3;
    --color-canvas-subtle: #eee8d5;
    --color-fg-default: #586e75;
    --color-fg-muted: #93a1a1;
    --color-border-default: #e0d7c3;
    --color-border-muted: #eee8d5;
    --color-accent-fg: #268bd2;
    --color-accent-emphasis: #2aa198;
    --code-bg: #eee8d5;
}
"""

BASE_MARKDOWN_CSS = """
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Pretendard", Roboto, Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.65;
    background-color: var(--color-canvas-default);
    color: var(--color-fg-default);
    transition: background-color 0.2s ease, color 0.2s ease;
    word-wrap: break-word;
}

.markdown-body {
    max-width: 920px;
    margin: 0 auto;
    padding: 40px 32px;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
    color: var(--color-fg-default);
}

h1 {
    font-size: 2em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid var(--color-border-default);
}

h2 {
    font-size: 1.5em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid var(--color-border-default);
}

h3 { font-size: 1.25em; }
h4 { font-size: 1em; }

p, blockquote, ul, ol, dl, table, pre, details {
    margin-top: 0;
    margin-bottom: 16px;
}

hr {
    height: 0.25em;
    padding: 0;
    margin: 24px 0;
    background-color: var(--color-border-default);
    border: 0;
}

blockquote {
    padding: 8px 16px;
    color: var(--color-fg-muted);
    border-left: 3px solid var(--color-accent-fg);
    background-color: var(--color-canvas-subtle);
    border-radius: 0 6px 6px 0;
    margin: 16px 0;
}

ul, ol {
    padding-left: 2em;
}

li + li {
    margin-top: 0.25em;
}

a {
    color: var(--color-accent-fg);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

code {
    padding: 0.2em 0.45em;
    margin: 0 0.15em;
    font-size: 85%;
    white-space: break-spaces;
    background-color: var(--code-bg);
    border: 1px solid var(--color-border-default);
    border-radius: 6px;
    font-family: ui-monospace, SFMono-Regular, "Cascadia Code", "Fira Code", Consolas, monospace;
}

pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: var(--code-bg);
    border-radius: 8px;
    border: 1px solid var(--color-border-default);
}

pre code {
    padding: 0;
    margin: 0;
    font-size: 100%;
    word-break: normal;
    white-space: pre;
    background: transparent;
    border: 0;
}

.codehilite {
    border-radius: 8px;
    background-color: var(--code-bg) !important;
    border: 1px solid var(--color-border-default);
    margin-bottom: 16px;
    overflow: auto;
}

.codehilite pre {
    border: none;
    margin: 0;
}

table {
    border-spacing: 0;
    border-collapse: collapse;
    display: block;
    width: max-content;
    max-width: 100%;
    overflow: auto;
    margin-bottom: 16px;
}

table th, table td {
    padding: 8px 14px;
    border: 1px solid var(--color-border-default);
}

table th {
    font-weight: 600;
    background-color: var(--color-canvas-subtle);
}

table tr:nth-child(2n) {
    background-color: var(--color-canvas-subtle);
}

img {
    max-width: 100%;
    box-sizing: content-box;
    border-radius: 6px;
}

/* Checkbox / Task lists */
input[type="checkbox"] {
    margin-right: 0.4em;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: var(--color-border-default);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--color-fg-muted);
}
"""

THEMES = {
    "Modern Charcoal (모던 차콜)": {
        "theme_css": MODERN_CHARCOAL_CSS,
        "pygments_style": "one-dark"
    },
    "Light Modern (라이트 모던)": {
        "theme_css": LIGHT_MODERN_CSS,
        "pygments_style": "vs"
    },
    "Dracula (드라큘라)": {
        "theme_css": DRACULA_CSS,
        "pygments_style": "dracula"
    },
    "Nord (노르드)": {
        "theme_css": NORD_CSS,
        "pygments_style": "nord"
    },
    "Solarized Light (솔라라이즈드)": {
        "theme_css": SOLARIZED_LIGHT_CSS,
        "pygments_style": "solarized-light"
    },
    "GitHub Dark": {
        "theme_css": GITHUB_DARK_CSS,
        "pygments_style": "monokai"
    },
    "GitHub Light": {
        "theme_css": GITHUB_LIGHT_CSS,
        "pygments_style": "default"
    },
    "Notion Style": {
        "theme_css": NOTION_CSS,
        "pygments_style": "friendly"
    }
}


def get_empty_placeholder_html(theme_name: str = "Modern Charcoal (모던 차콜)") -> str:
    """Returns a welcome / placeholder HTML when no file is selected."""
    theme_info = THEMES.get(theme_name, THEMES["Modern Charcoal (모던 차콜)"])
    pygments_css = HtmlFormatter(style=theme_info["pygments_style"]).get_style_defs('.codehilite')
    theme_and_base_css = f"{theme_info['theme_css']}\n{BASE_MARKDOWN_CSS}"
    
    cfg = load_style_config()
    config_override_css = build_css_from_config(cfg)
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MarkToHTML</title>
<style>
{theme_and_base_css}
{pygments_css}
{config_override_css}
.welcome-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    text-align: center;
    color: var(--color-fg-muted);
}}
.welcome-icon {{
    font-size: 64px;
    margin-bottom: 20px;
}}
.welcome-title {{
    font-size: 24px;
    font-weight: 600;
    color: var(--color-fg-default);
    margin-bottom: 12px;
}}
.welcome-desc {{
    font-size: 15px;
    max-width: 480px;
    line-height: 1.6;
    margin-bottom: 24px;
}}
.feature-box {{
    background: var(--color-canvas-subtle);
    border: 1px solid var(--color-border-default);
    border-radius: 10px;
    padding: 16px 24px;
    text-align: left;
    display: inline-block;
    max-width: 440px;
    width: 100%;
}}
.feature-box ul {{
    margin: 0;
    padding-left: 20px;
    color: var(--color-fg-default);
}}
.feature-box li {{
    margin: 6px 0;
    font-size: 14px;
}}
</style>
</head>
<body>
<div class="welcome-container">
    <div class="welcome-icon">📄 ➔ 🌐</div>
    <div class="welcome-title">MarkToHTML 프리뷰어</div>
    <div class="welcome-desc">
        좌측 파일 탐색창에서 마크다운(<code>.md</code>) 파일을 클릭하면<br>
        실시간으로 변환된 웹페이지가 이곳에 표시됩니다.
    </div>
    <div class="feature-box">
        <ul>
            <li>👈 <b>좌측 탐색기</b>: 폴더 변경 및 MD 파일 선택</li>
            <li>💾 <b>HTML로 저장</b>: 완결형 독립 HTML 파일로 내보내기</li>
            <li>🌐 <b>브라우저 보기</b>: 크롬/엣지 브라우저에서 바로 열기</li>
            <li>🎨 <b>테마 변경</b>: GitHub 다크, 라이트, Notion 스타일 지원</li>
        </ul>
    </div>
</div>
</body>
</html>
"""
    return html


def convert_markdown_to_html(md_text: str, title: str = "MarkToHTML Document", theme_name: str = "Modern Charcoal (모던 차콜)") -> str:
    """
    Converts markdown text to a full, self-contained standalone HTML page.
    Includes embedded CSS for layout and syntax highlighting, plus style_config.json overrides.
    """
    theme_info = THEMES.get(theme_name, THEMES["Modern Charcoal (모던 차콜)"])
    pygments_css = HtmlFormatter(style=theme_info["pygments_style"]).get_style_defs('.codehilite')

    # 1. Base Theme CSS + BASE_MARKDOWN_CSS (centered layout: margin: 0 auto; max-width: 920px; padding: 40px 32px)
    theme_and_base_css = f"{theme_info['theme_css']}\n{BASE_MARKDOWN_CSS}"

    # 2. Layer style_config.json text overrides on top for any selected theme
    cfg = load_style_config()
    config_override_css = build_css_from_config(cfg)

    # Convert Markdown to HTML body
    md_extensions = [
        'extra',           # Tables, attr_list, def_list, fenced_code, etc.
        'codehilite',      # Code syntax highlighting via Pygments
        'toc',             # Table of contents support
        'sane_lists',      # Clean lists
        'nl2br'            # Newlines to break (optional user friendly)
    ]
    
    extension_configs = {
        'codehilite': {
            'linenums': False,
            'guess_lang': True,
            'css_class': 'codehilite'
        }
    }

    html_body = markdown.markdown(
        md_text,
        extensions=md_extensions,
        extension_configs=extension_configs
    )

    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{theme_and_base_css}
{pygments_css}
{config_override_css}
</style>
</head>
<body>
<div class="markdown-body">
{html_body}
</div>
</body>
</html>
"""
    return full_html


def convert_file(file_path: str, theme_name: str = "Modern Charcoal (모던 차콜)") -> str:
    """Reads a markdown file from disk and converts it to HTML."""
    if not os.path.exists(file_path):
        return get_empty_placeholder_html(theme_name)
    
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        md_text = f.read()
        
    title = os.path.splitext(os.path.basename(file_path))[0]
    return convert_markdown_to_html(md_text, title=title, theme_name=theme_name)
