# -*- coding: utf-8 -*-
"""
X-Workflow 主程序入口
一个基于 PySide6 和 qt-material 的可视化流程编辑器
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from qt_material import apply_stylesheet

from widgets.main_window import MainWindow


def main():
    """
    主函数
    程序的入口点
    """
    # 启用高 DPI 支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序名称
    app.setApplicationName("X-Workflow")
    
    # 应用 qt-material 样式
    # 可选主题: 'dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml',
    #           'dark_pink.xml', 'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml',
    #           'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml', 'light_cyan.xml',
    #           'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml', 'light_purple.xml',
    #           'light_red.xml', 'light_teal.xml', 'light_yellow.xml'
    apply_stylesheet(app, theme='dark_lightgreen.xml')
    
    # 创建并显示主窗口（MainWindow 中已设置最大化）
    window = MainWindow()
    
    # 运行应用程序主循环
    sys.exit(app.exec())


# 程序入口
if __name__ == "__main__":
    main()
