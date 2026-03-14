# -*- coding: utf-8 -*-
"""
X-Workflow 主程序入口
一个基于 PySide6 和 qt-material 的可视化流程编辑器
"""

import sys
import os
import shutil
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from qt_material import apply_stylesheet

from widgets.main_window import MainWindow


def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径，兼容开发环境和 PyInstaller 打包环境
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的环境
        base_path = Path(sys._MEIPASS)
    else:
        # 开发环境
        base_path = Path(__file__).parent
    return base_path / relative_path


def initialize_config():
    """
    初始化配置文件：如果 ~/.x-workflow 目录或配置文件不存在，则创建并复制默认配置
    """
    # 用户配置目录
    user_config_dir = Path.home() / ".x-workflow"
    # 用户配置文件路径
    user_config_file = user_config_dir / "workflow-config.json"
    # 默认配置文件路径（从资源中获取）
    default_config_file = get_resource_path("workflow-config.json")
    
    # 创建用户配置目录（如果不存在）
    if not user_config_dir.exists():
        user_config_dir.mkdir(parents=True, exist_ok=True)
    
    # 如果用户配置文件不存在，复制默认配置
    if not user_config_file.exists() and default_config_file.exists():
        shutil.copy2(default_config_file, user_config_file)


def main():
    """
    主函数
    程序的入口点
    """
    # 初始化配置文件
    initialize_config()
    
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
