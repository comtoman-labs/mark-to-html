"""
MarkToHTML - Style Configuration Manager
Manages style_config.json for customizing Markdown text colors and font sizes.
Applies clean CSS overrides on top of any selected theme without breaking base layout.
"""

import os
import sys
import json

CONFIG_FILENAME = "style_config.json"


def get_config_dir() -> str:
    """Returns the base directory where style_config.json is located."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_config_path() -> str:
    """Returns the full path to style_config.json."""
    return os.path.join(get_config_dir(), CONFIG_FILENAME)


DEFAULT_STYLE_CONFIG = {
    "_description": "MarkToHTML 텍스트 스타일 설정 파일입니다. 마크다운 문법별 글자 크기(font_size)와 색상(color)을 설정할 수 있습니다. 값을 비워두면(\"\") 선택한 테마의 기본 스타일이 유지됩니다.",
    "headings": {
        "h1": {
            "font_size": "",
            "color": "",
            "font_weight": "",
            "border_bottom": ""
        },
        "h2": {
            "font_size": "",
            "color": "",
            "font_weight": "",
            "border_bottom": ""
        },
        "h3": {
            "font_size": "",
            "color": "",
            "font_weight": ""
        },
        "h4": {
            "font_size": "",
            "color": "",
            "font_weight": ""
        },
        "h5": {
            "font_size": "",
            "color": "",
            "font_weight": ""
        },
        "h6": {
            "font_size": "",
            "color": "",
            "font_weight": ""
        }
    },
    "text_formatting": {
        "bold": {
            "color": "",
            "font_weight": ""
        },
        "italic": {
            "color": "",
            "font_style": ""
        },
        "inline_code": {
            "color": "",
            "background_color": "",
            "border_color": "",
            "font_size": ""
        },
        "link": {
            "color": "",
            "hover_color": ""
        }
    },
    "blocks": {
        "blockquote": {
            "text_color": "",
            "border_color": "",
            "background_color": ""
        },
        "table": {
            "header_background": "",
            "header_color": "",
            "border_color": ""
        }
    }
}


def load_style_config() -> dict:
    """Loads style_config.json. If it does not exist, creates it with default template."""
    config_path = get_config_path()
    if not os.path.exists(config_path):
        save_style_config(DEFAULT_STYLE_CONFIG)
        return DEFAULT_STYLE_CONFIG

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"[Warning] Failed to load {config_path}: {e}")
        return DEFAULT_STYLE_CONFIG


def save_style_config(config_data: dict) -> bool:
    """Saves style configuration data to style_config.json."""
    config_path = get_config_path()
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[Error] Failed to write {config_path}: {e}")
        return False


def build_css_from_config(config: dict) -> str:
    """
    Generates CSS overrides from style_config.json for non-empty properties only.
    Preserves theme layout, centering, and untouched element styles completely.
    """
    if not config or not isinstance(config, dict):
        return ""

    rules = []

    # Headings (h1 - h6)
    headings = config.get("headings", {})
    for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        h_data = headings.get(tag, {})
        if not isinstance(h_data, dict):
            continue
        props = []
        if h_data.get("font_size"):
            props.append(f"font-size: {h_data['font_size']} !important;")
        if h_data.get("color"):
            props.append(f"color: {h_data['color']} !important;")
        if h_data.get("font_weight"):
            props.append(f"font-weight: {h_data['font_weight']} !important;")
        if h_data.get("border_bottom"):
            props.append(f"border-bottom: {h_data['border_bottom']} !important;")
        if props:
            rules.append(f".markdown-body {tag} {{ {' '.join(props)} }}")

    # Text formatting
    fmt = config.get("text_formatting", {})
    if isinstance(fmt, dict):
        # Bold
        bold = fmt.get("bold", {})
        if isinstance(bold, dict):
            b_props = []
            if bold.get("color"):
                b_props.append(f"color: {bold['color']} !important;")
            if bold.get("font_weight"):
                b_props.append(f"font-weight: {bold['font_weight']} !important;")
            if b_props:
                rules.append(f".markdown-body strong, .markdown-body b {{ {' '.join(b_props)} }}")

        # Italic
        italic = fmt.get("italic", {})
        if isinstance(italic, dict):
            i_props = []
            if italic.get("color"):
                i_props.append(f"color: {italic['color']} !important;")
            if italic.get("font_style"):
                i_props.append(f"font-style: {italic['font_style']} !important;")
            if i_props:
                rules.append(f".markdown-body em, .markdown-body i {{ {' '.join(i_props)} }}")

        # Inline Code (exclude pre > code)
        code = fmt.get("inline_code", {})
        if isinstance(code, dict):
            c_props = []
            if code.get("color"):
                c_props.append(f"color: {code['color']} !important;")
            if code.get("background_color"):
                c_props.append(f"background-color: {code['background_color']} !important;")
            if code.get("border_color"):
                c_props.append(f"border: 1px solid {code['border_color']} !important;")
            if code.get("font_size"):
                c_props.append(f"font-size: {code['font_size']} !important;")
            if c_props:
                rules.append(f".markdown-body :not(pre) > code {{ {' '.join(c_props)} }}")

        # Links
        link = fmt.get("link", {})
        if isinstance(link, dict):
            if link.get("color"):
                rules.append(f".markdown-body a {{ color: {link['color']} !important; }}")
            if link.get("hover_color"):
                rules.append(f".markdown-body a:hover {{ color: {link['hover_color']} !important; }}")

    # Blocks
    blocks = config.get("blocks", {})
    if isinstance(blocks, dict):
        bq = blocks.get("blockquote", {})
        if isinstance(bq, dict):
            bq_props = []
            if bq.get("text_color"):
                bq_props.append(f"color: {bq['text_color']} !important;")
            if bq.get("border_color"):
                bq_props.append(f"border-left-color: {bq['border_color']} !important;")
            if bq.get("background_color"):
                bq_props.append(f"background-color: {bq['background_color']} !important;")
            if bq_props:
                rules.append(f".markdown-body blockquote {{ {' '.join(bq_props)} }}")

        tbl = blocks.get("table", {})
        if isinstance(tbl, dict):
            th_props = []
            if tbl.get("header_background"):
                th_props.append(f"background-color: {tbl['header_background']} !important;")
            if tbl.get("header_color"):
                th_props.append(f"color: {tbl['header_color']} !important;")
            if th_props:
                rules.append(f".markdown-body table th {{ {' '.join(th_props)} }}")
            if tbl.get("border_color"):
                rules.append(f".markdown-body table th, .markdown-body table td {{ border-color: {tbl['border_color']} !important; }}")

    if not rules:
        return ""

    return "/* style_config.json overrides */\n" + "\n".join(rules)
