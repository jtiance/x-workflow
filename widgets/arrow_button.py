# -*- coding: utf-8 -*-
"""
五边形箭头按钮模块
提供带有右指向箭头的五边形按钮
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QPainterPath, QColor, QBrush, QPen


class ArrowButton(QPushButton):
    """
    五边形箭头按钮
    左边是矩形，右边是箭头，形成五边形结构
    """
    
    def __init__(self, text="", parent=None):
        """
        初始化箭头按钮
        
        Args:
            text: 按钮文字
            parent: 父控件
        """
        super().__init__(text, parent)
        
        # 设置按钮属性
        self.setMinimumHeight(30)
        self.setCursor(Qt.PointingHandCursor)
        
        # 颜色配置
        self._normal_bg_color = QColor("#4a5568")  # 默认灰色
        self._hover_bg_color = QColor("#718096")   # 悬停时稍亮
        self._pressed_bg_color = QColor("#2d3748") # 按下时稍暗
        self._selected_bg_color = QColor("#3182ce") # 选中时蓝色
        self._text_color = QColor("#ffffff")
        self._border_color = QColor("#2d3748")
        
        self._is_selected = False
        self._is_hovered = False
        
        # 设置样式
        self._update_style()
        
    def set_selected(self, selected):
        """
        设置按钮选中状态
        
        Args:
            selected: 是否选中
        """
        self._is_selected = selected
        self._update_style()
        
    def is_selected(self):
        """
        获取按钮选中状态
        
        Returns:
            bool: 是否选中
        """
        return self._is_selected
        
    def _update_style(self):
        """
        更新样式
        """
        if self._is_selected:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {self._text_color.name()};
                    border: none;
                    padding: 5px 10px;
                }}
            """)
        elif self._is_hovered:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {self._text_color.name()};
                    border: none;
                    padding: 5px 10px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {self._text_color.name()};
                    border: none;
                    padding: 5px 10px;
                }}
            """)
        
    def enterEvent(self, event):
        """
        鼠标进入事件
        """
        self._is_hovered = True
        self._update_style()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """
        鼠标离开事件
        """
        self._is_hovered = False
        self._update_style()
        super().leaveEvent(event)
        
    def paintEvent(self, event):
        """
        绘制按钮
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 获取按钮区域
        rect = QRectF(0, 0, self.width(), self.height())
        
        # 计算箭头的宽度（按钮宽度的15%）
        arrow_width = self.width() * 0.15
        if arrow_width < 10:
            arrow_width = 10
        if arrow_width > 30:
            arrow_width = 30
            
        # 计算矩形部分的宽度
        rect_width = self.width() - arrow_width
        
        # 圆角半径
        corner_radius = 3
        
        # 创建五边形路径
        path = QPainterPath()
        
        # 1. 左上角 - 圆角
        path.moveTo(corner_radius, 0)
        path.arcTo(0, 0, corner_radius * 2, corner_radius * 2, 90, 90)
        
        # 2. 左下角 - 圆角
        path.lineTo(0, self.height() - corner_radius)
        path.arcTo(0, self.height() - corner_radius * 2, corner_radius * 2, corner_radius * 2, 180, 90)
        
        # 3. 右下角 - 圆角
        path.lineTo(rect_width - corner_radius, self.height())
        path.arcTo(rect_width - corner_radius * 2, self.height() - corner_radius * 2, corner_radius * 2, corner_radius * 2, 270, 90)
        
        # 4. 到箭头尖端 - 保持尖角
        tip_x = self.width() - 2
        tip_y = self.height() / 2
        path.lineTo(tip_x, tip_y)
        
        # 5. 右上角 - 圆角
        path.lineTo(rect_width, corner_radius)
        path.arcTo(rect_width - corner_radius * 2, 0, corner_radius * 2, corner_radius * 2, 0, 90)
        
        # 闭合路径
        path.closeSubpath()
        
        # 确定背景颜色
        if self._is_selected:
            bg_color = self._selected_bg_color
        elif self._is_hovered:
            bg_color = self._hover_bg_color
        elif self.isDown():
            bg_color = self._pressed_bg_color
        else:
            bg_color = self._normal_bg_color
            
        # 绘制填充
        painter.fillPath(path, QBrush(bg_color))
        
        # 绘制边框
        pen = QPen(self._border_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # 绘制文字
        # 计算文字位置（放在矩形区域内，居中对齐）
        text_rect = QRectF(5, 0, rect_width - 5, self.height())
        painter.setPen(self._text_color)
        
        # 设置文字对齐方式
        from PySide6.QtGui import QFont
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        
        # 绘制文字，使用省略号如果文字太长
        from PySide6.QtCore import Qt
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignHCenter, self.text())
