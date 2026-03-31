# -*- coding: utf-8 -*-
"""
自定义编辑层 - 始终显示底部边框效果
"""

from PySide6.QtCore import Qt, QEvent, QRectF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPainterPath
from qfluentwidgets.common.style_sheet import themeColor


class CustomEditLayer(QWidget):
    """自定义编辑层 - 始终显示边框效果"""

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        parent.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.parent() and e.type() == QEvent.Resize:
            self.resize(e.size())
        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        # 不绘制任何内容，永远不显示蓝色边条
        pass
