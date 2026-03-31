# -*- coding: utf-8 -*-
"""
自定义 PlainTextEdit - 始终使用焦点状态样式
"""

from qfluentwidgets import PlainTextEdit, FluentStyleSheet
from qfluentwidgets.common.style_sheet import updateDynamicStyle
from qfluentwidgets.common.font import setFont
from .custom_edit_layer import CustomEditLayer


class CustomPlainTextEdit(PlainTextEdit):
    """自定义 PlainTextEdit - 始终使用焦点状态样式"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 删除默认的 EditLayer，它会绘制蓝色边条
        if hasattr(self, 'layer') and self.layer:
            self.layer.deleteLater()
        # 替换为自定义的 EditLayer（不绘制蓝色边条）
        self.layer = CustomEditLayer(self)
        # 重新应用样式
        FluentStyleSheet.LINE_EDIT.apply(self)
        updateDynamicStyle(self)
        setFont(self)

        # 强制使用焦点状态的背景色（深色主题）
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(30, 30, 30, 0.7);
            }
        """)
