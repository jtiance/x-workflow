# -*- coding: utf-8 -*-
"""
FluentIcon 图标预览工具
展示所有FluentIcon枚举值在ToggleToolButton中的显示效果
"""
import sys

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt
from qfluentwidgets import TransparentToggleToolButton, FluentIcon


class IconPreviewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FluentIcon 预览")
        self.resize(1200, 800)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # 获取所有FluentIcon枚举值
        icon_enums = [attr for attr in dir(FluentIcon) if not attr.startswith('_') and attr.isupper()]
        print(f"共找到 {len(icon_enums)} 个FluentIcon图标")

        # 每行显示6个图标（带标签）
        columns = 6
        for i, icon_name in enumerate(icon_enums):
            row = i // columns
            col = i % columns

            try:
                # 创建水平布局容器，包含图标和标签
                item_layout = QHBoxLayout()
                item_layout.setSpacing(8)
                item_layout.setContentsMargins(5, 5, 5, 5)

                # 获取图标
                icon = getattr(FluentIcon, icon_name)

                # 创建按钮
                btn = TransparentToggleToolButton()
                btn.setIcon(icon)
                btn.setIconSize(QtCore.QSize(20, 20))
                btn.setFixedSize(40, 40)
                btn.setToolTip(icon_name)
                item_layout.addWidget(btn)

                # 添加图标名称标签，放在右侧
                label = QLabel(icon_name)
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                label.setStyleSheet("font-size: 12px; color: #666;")
                item_layout.addWidget(label)

                # 添加弹性填充，让布局更紧凑
                item_layout.addStretch()

                # 添加到网格布局
                layout.addLayout(item_layout, row, col)

            except Exception as e:
                print(f"加载图标 {icon_name} 失败: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IconPreviewWindow()
    window.show()
    sys.exit(app.exec())
