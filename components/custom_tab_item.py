# -*- coding: utf-8 -*-
"""
自定义标签页组件模块
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPainterPath, QColor
from qfluentwidgets import TabItem


class CustomTabItem(TabItem):
    """自定义标签页，添加灰色边框"""

    def _drawSelectedBackground(self, painter: QPainter):
        """绘制选中的背景，覆盖父类方法以添加边框"""
        w, h = self.width(), self.height()
        r = self.borderRadius
        d = 2 * r

        isDark = True  # 假设深色主题，根据需要调整

        # 绘制灰色边框
        painter.setPen(QColor(169, 169, 169, 100))  # 灰色半透明边框
        painter.setBrush(self.lightSelectedBackgroundColor if not isDark else self.darkSelectedBackgroundColor)

        # 绘制圆角矩形背景和边框
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, r, r)
        painter.drawPath(path)

        # 绘制底部边框加粗效果
        painter.setPen(QColor(169, 169, 169, 150))
        painter.drawLine(0, h - 1, w, h - 1)

    def _drawNotSelectedBackground(self, painter: QPainter):
        """绘制未选中的背景，覆盖父类方法以添加边框"""
        w, h = self.width(), self.height()
        r = self.borderRadius

        isDark = True  # 假设深色主题

        # 绘制灰色边框（更淡）
        painter.setPen(QColor(169, 169, 169, 50))  # 淡灰色边框
        painter.setBrush(Qt.NoBrush)  # 无背景

        # 绘制圆角矩形边框
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, r, r)
        painter.drawPath(path)
