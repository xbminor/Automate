from pathlib import Path
from PySide6.QtCore import QUrl

COLOR_BASE_BG = "#ABABAB"
COLOR_ACCENT = "#3D6480"
COLOR_ACCENT_BG = "#8D9CA8"
COLOR_VALID = "#228B22"
COLOR_INVALID = "#B22222"

COLOR_WHITE = "#FFFFFF"
COLOR_BLACK = "#000000"
FONT_FAMILY = "Segoe UI"
FONT_WEIGHT_LIGHT = "333"
FONT_WEIGHT_MEDIUM = "550"
FONT_WEIGHT_HEAVY = "1000"

pathRoot = Path(__file__).resolve().parents[2]
pathAssets = pathRoot / "assets"



LABEL_DEFAULT = f"""
QLabel {{
    font-size: 11pt;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_LIGHT};
    color: {COLOR_WHITE}
}}
"""

LABEL_HEADING = f"""
QLabel {{
    font-size: 13pt;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_MEDIUM};
    color: {COLOR_WHITE}
}}
"""

LABEL_TITLE = f"""
QLabel {{
    font-size: 15pt;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_HEAVY};
    color: {COLOR_WHITE}
}}
"""



LIST_DRAG_DROP = f"""
QListWidget {{
    border: 2px dashed {COLOR_ACCENT};
    border-radius: 8px;
    background-color: {COLOR_BASE_BG};
    padding: 4px 4px;
}}

QListWidget::item {{
    background-color: {COLOR_ACCENT_BG};
    border: 2px solid {COLOR_ACCENT};
    border-radius: 4px;
    margin-bottom: 4px;
    margin-right: 4px;
    padding: 4px 4px;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_LIGHT};
    font-size: 13px;
    color: {COLOR_BLACK};
}}

QListWidget QScrollBar:vertical {{
    background-color: {COLOR_BLACK};
}}

QListWidget QScrollBar::handle:vertical {{
    background-color: {COLOR_ACCENT_BG};
    border: 2px solid {COLOR_ACCENT};
    border-radius: 4px;
}}
"""



INPUT_DEFAULT = f"""
QLineEdit {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    padding: 4px 4px;
    border: 2px solid {COLOR_ACCENT};
    border-radius: 4px;
    background-color: {COLOR_BASE_BG};
    color: {COLOR_BLACK};
}}
"""

INPUT_VALID = f"""
QLineEdit {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    padding: 4px 4px;
    border: 2px solid {COLOR_VALID};
    border-radius: 4px;
    background-color: {COLOR_BASE_BG};
    color: {COLOR_BLACK};
}}
"""

INPUT_INVALID = f"""
QLineEdit {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    padding: 4px 4px;
    border: 2px solid {COLOR_INVALID};
    border-radius: 4px;
    background-color: {COLOR_BASE_BG};
    color: {COLOR_BLACK};
}}
"""



BUTTON_DEFAULT = f"""
QPushButton {{
    font-size: 11pt;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_MEDIUM};
    padding: 4px 8px;
    border: 2px solid {COLOR_ACCENT};
    border-radius: 4px;
    background-color: {COLOR_ACCENT_BG};
    color: {COLOR_BLACK};
}}

QPushButton:hover {{
    background-color: {COLOR_BASE_BG};
}}

QPushButton:pressed {{
    background-color: {COLOR_ACCENT};
    color: {COLOR_WHITE};
}}
"""



COMBOX_DEFAULT = f"""
QComboBox {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    font-weight: {FONT_WEIGHT_MEDIUM};
    border: 2px solid {COLOR_ACCENT};
    border-radius: 4px;
    background-color: {COLOR_BASE_BG};
    color: {COLOR_BLACK};
    padding-right: 30px;
}}

QComboBox::drop-down {{
    subcontrol-position: top right;
    width: 20px;
    border-left: 2px solid {COLOR_ACCENT};
    background-color: {COLOR_ACCENT_BG};
}}

QComboBox::drop-down:hover {{
    background-color: {COLOR_ACCENT};
}}

QComboBox QAbstractItemView {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    font-weight: {FONT_WEIGHT_MEDIUM};
    background-color: {COLOR_ACCENT_BG};
    border: 2px solid {COLOR_ACCENT};
    color: {COLOR_BLACK};
    outline: none;
}}

QComboBox QAbstractItemView::item::hover {{
    background-color: {COLOR_BASE_BG};
    color: {COLOR_BLACK};
}}

QComboBox QAbstractItemView::item::selected {{
   border-left: 6px solid {COLOR_ACCENT};
   border-bottom: 2px solid {COLOR_ACCENT};
   background-color: {COLOR_BASE_BG};
   color: {COLOR_BLACK};
}}
"""





