# -*- coding: utf-8 -*-
"""
自定义正则表达式切换按钮组件
"""
from PySide6 import QtCore
from PySide6.QtGui import QIcon
from qfluentwidgets import TransparentToggleToolButton


class CustomRegexToolButton(TransparentToggleToolButton):
    """
    自定义正则表达式切换按钮
    选中时显示白色图标，未选中时显示黑色图标
    """

    def __init__(self, icon_size=QtCore.QSize(12, 12), checked=False, parent=None):
        """
        初始化自定义正则表达式按钮

        Args:
            icon_size: 图标大小，默认12x12
            checked: 是否默认选中（使用正则表达式），默认False
            parent: 父控件
        """
        super().__init__(parent)

        # 图标路径
        self._icon_white = QIcon("icons/正则表达式_白色.svg")
        self._icon_black = QIcon("icons/正则表达式_黑色.svg")

        # 设置图标大小
        self.setIconSize(icon_size)

        # 设置默认状态
        self.setChecked(checked)
        self._update_icon()

        # 连接状态变化信号
        self.toggled.connect(self._on_toggled)

        # 设置提示
        self.setToolTip("使用正则表达式")

    def _on_toggled(self, checked):
        """当按钮选中状态变化时调用"""
        self._update_icon()

    def _update_icon(self):
        """更新图标根据选中状态"""
        if self.isChecked():
            # 选中状态：使用正则表达式，显示黑色图标
            self.setIcon(self._icon_black)
        else:
            # 未选中状态：不使用正则表达式，显示白色图标
            self.setIcon(self._icon_white)
