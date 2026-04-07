# -*- coding: utf-8 -*-
"""
自定义全部替换按钮组件
"""
from PySide6 import QtCore
from PySide6.QtGui import QIcon
from qfluentwidgets import TransparentToolButton


class CustomReplaceAllToolButton(TransparentToolButton):
    """
    自定义全部替换按钮
    普通状态显示白色图标，hover/按下显示黑色图标
    """

    def __init__(self, icon_size=QtCore.QSize(16, 16), parent=None):
        """
        初始化自定义全部替换按钮

        Args:
            icon_size: 图标大小，默认16x16
            parent: 父控件
        """
        super().__init__(parent)

        # 图标路径
        self._icon_white = QIcon("icons/替换全部_白色.svg")

        # 设置图标大小
        self.setIconSize(icon_size)

        # 默认显示白色图标
        self.setIcon(self._icon_white)

        # 设置提示
        self.setToolTip("替换全部")

