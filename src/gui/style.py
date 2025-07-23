from pathlib import Path
from PySide6.QtCore import QUrl

COLOR_BASE_BG = "#8D9CA8"
COLOR_BASE_PRESSED = "#6B8FA2"
COLOR_BASE_HIGHLIGHT = "#B0BCC6"
COLOR_BASE_SHADOW = "#5F6B75"
COLOR_WIDGET_BG = "#ABABAB"
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
    color: {COLOR_BLACK}
}}
"""

LABEL_HEADING = f"""
QLabel {{
    font-size: 13pt;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_MEDIUM};
    color: {COLOR_BLACK}
}}
"""

LABEL_TITLE = f"""
QLabel {{
    font-size: 15pt;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_HEAVY};
    color: {COLOR_BLACK}
}}
"""



LIST_DRAG_DROP = f"""
QListWidget {{
    border-top: 4px solid {COLOR_BASE_SHADOW};
    border-left: 4px solid {COLOR_BASE_SHADOW};
    border-bottom: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 4px solid {COLOR_BASE_HIGHLIGHT};
    background-color: {COLOR_WIDGET_BG};
    padding: 4px 4px;
}}

QListWidget::item {{
    background-color: {COLOR_BASE_BG};
    border-top: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 2px solid {COLOR_BASE_SHADOW};
    border-right: 2px solid {COLOR_BASE_SHADOW};
    margin-bottom: 2px;
    margin-right: 4px;
    padding: 4px 4px;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_LIGHT};
    font-size: 13px;
    color: {COLOR_BLACK};
    outline: none;
}}


QListWidget QScrollBar:vertical {{
    background-color: {COLOR_WIDGET_BG};
    width: 15px;

}}

QListWidget QScrollBar::handle:vertical {{
    background-color: {COLOR_BASE_BG};
    border-top: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 2px solid {COLOR_BASE_SHADOW};
    border-right: 2px solid {COLOR_BASE_SHADOW};
    
}}

QListWidget QScrollBar::handle:vertical:hover {{
    background-color: {COLOR_BASE_BG};
    border-top: 2px solid {COLOR_BASE_SHADOW};
    border-left: 2px solid {COLOR_BASE_SHADOW};
    border-bottom: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 2px solid {COLOR_BASE_HIGHLIGHT};
}}

QListWidget QScrollBar::handle:vertical:pressed {{
    background-color: {COLOR_BASE_PRESSED};
    border-top: 2px solid {COLOR_BASE_SHADOW};
    border-left: 2px solid {COLOR_BASE_SHADOW};
    border-bottom: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 2px solid {COLOR_BASE_HIGHLIGHT};
    
}}
"""



BUTTON_DEFAULT = f"""
QPushButton {{
    font-size: 11pt;
    font-family: {FONT_FAMILY};
    font-weight: {FONT_WEIGHT_MEDIUM};

    border-top: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 4px solid {COLOR_BASE_SHADOW};
    border-right: 4px solid {COLOR_BASE_SHADOW};

    background-color: {COLOR_BASE_BG};
    color: {COLOR_BLACK};
    padding: 4px 8px;
}}

QPushButton:hover {{
    border-top: 4px solid {COLOR_BASE_SHADOW};
    border-left: 4px solid {COLOR_BASE_SHADOW};
    border-bottom: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 4px solid {COLOR_BASE_HIGHLIGHT};
}}

QPushButton:pressed {{
    border-top: 4px solid {COLOR_BASE_SHADOW};
    border-left: 4px solid {COLOR_BASE_SHADOW};
    border-bottom: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 4px solid {COLOR_BASE_HIGHLIGHT};
    background-color: {COLOR_BASE_PRESSED};
    color: {COLOR_WHITE}
}}
"""


FRAME_PANEL = f"""
QFrame#Panel {{
    background-color: {COLOR_BASE_BG};
    border-top: 6px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 6px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 6px solid {COLOR_BASE_SHADOW};
    border-right: 6px solid {COLOR_BASE_SHADOW};
    padding: 6px;

}}
"""


FRAME_INPUT = f"""
QFrame#InputField {{
    background-color: {COLOR_BASE_BG};
    border-top: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 4px solid {COLOR_BASE_SHADOW};
    border-right: 4px solid {COLOR_BASE_SHADOW};
    padding: 4px;
}}
"""

INPUT_DEFAULT = f"""
QLineEdit {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    padding: 4px 4px;

    border-top: 2px solid {COLOR_BASE_SHADOW};
    border-left: 2px solid {COLOR_BASE_SHADOW};
    border-bottom: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 2px solid {COLOR_BASE_HIGHLIGHT};

    background-color: {COLOR_WIDGET_BG};
    color: {COLOR_BLACK};
}}
"""

FRAME_COMBOX = f"""
QFrame#Combox {{
    background-color: {COLOR_BASE_BG};
    border-top: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 4px solid {COLOR_BASE_SHADOW};
    border-right: 4px solid {COLOR_BASE_SHADOW};
    padding: 4px;
}}
"""

COMBOX_DEFAULT = f"""
QComboBox {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    font-weight: {FONT_WEIGHT_MEDIUM};

    border-top: 2px solid {COLOR_BASE_SHADOW};
    border-left: 2px solid {COLOR_BASE_SHADOW};
    border-bottom: 2Px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 2Px solid {COLOR_BASE_HIGHLIGHT};

    background-color: {COLOR_WIDGET_BG};
    color: {COLOR_BLACK};
    padding-right: 30px;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;

    border-top: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 2px solid {COLOR_BASE_SHADOW};
    border-right: 2px solid {COLOR_BASE_SHADOW};

    background-color: {COLOR_BASE_BG};
}}

QComboBox::drop-down:hover {{
    border-top: 2px solid {COLOR_BASE_SHADOW};
    border-left: 2px solid {COLOR_BASE_SHADOW};
    border-bottom: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 2px solid {COLOR_BASE_HIGHLIGHT};

    background-color: {COLOR_BASE_BG};
}}

QComboBox::drop-down:pressed,
QComboBox::drop-down:on {{
    border-top: 2px solid {COLOR_BASE_SHADOW};
    border-left: 2px solid {COLOR_BASE_SHADOW};
    border-bottom: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 2px solid {COLOR_BASE_HIGHLIGHT};

    background-color: {COLOR_BASE_PRESSED};
}}

QComboBox QAbstractItemView {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    font-weight: {FONT_WEIGHT_MEDIUM};

    
    border-left: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 2px solid {COLOR_BASE_SHADOW};
    border-right: 2px solid {COLOR_BASE_SHADOW};

    background-color: {COLOR_WIDGET_BG};
    color: {COLOR_BLACK};
    outline: none;
}}

QComboBox QAbstractItemView::item {{
    border-top: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 2px solid {COLOR_BASE_SHADOW};
    border-right: 2px solid {COLOR_BASE_SHADOW};
    background-color: {COLOR_WIDGET_BG};
    padding: 4px 8px;
    margin-bottom: -1px;
}}


QComboBox QAbstractItemView::item::selected {{
    border-top: 2px solid {COLOR_BASE_SHADOW};
    border-left: 2px solid {COLOR_BASE_SHADOW};
    border-bottom: 2px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 2px solid {COLOR_BASE_HIGHLIGHT};
    background-color: {COLOR_BASE_PRESSED};
    color: {COLOR_WHITE};
}}
"""




FRAME_TABS = f"""
QFrame#TabWrapper {{ 
    background-color:{COLOR_BASE_BG};
}}
"""


TABS_DEFAULT = f"""
QTabWidget::pane {{
    border: 2px solid {COLOR_BASE_BG};
    background-color: {COLOR_BASE_BG};
    
}}

QTabBar::tab {{
    font-family: {FONT_FAMILY};
    font-size: 11pt;
    font-weight: {FONT_WEIGHT_MEDIUM};
    color: {COLOR_BLACK};

    border-top: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-left: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-bottom: 4px solid {COLOR_BASE_SHADOW};
    border-right: 4px solid {COLOR_BASE_SHADOW};

    background-color: {COLOR_BASE_BG};
    padding: 6px 12px;

}}

QTabBar::tab:selected {{
    border-top: 4px solid {COLOR_BASE_SHADOW};
    border-left: 4px solid {COLOR_BASE_SHADOW};
    border-bottom: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 4px solid {COLOR_BASE_HIGHLIGHT};
    background-color: {COLOR_BASE_BG};
}}

QTabBar::tab:hover {{
    border-top: 4px solid {COLOR_BASE_SHADOW};
    border-left: 4px solid {COLOR_BASE_SHADOW};
    border-bottom: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 4px solid {COLOR_BASE_HIGHLIGHT};
    background-color: {COLOR_BASE_BG};
}}

QTabBar::tab:pressed {{
    border-top: 4px solid {COLOR_BASE_SHADOW};
    border-left: 4px solid {COLOR_BASE_SHADOW};
    border-bottom: 4px solid {COLOR_BASE_HIGHLIGHT};
    border-right: 4px solid {COLOR_BASE_HIGHLIGHT};
    background-color: {COLOR_BASE_PRESSED};
    color: {COLOR_WHITE};
}}

"""
