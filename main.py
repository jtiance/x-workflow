# -*- coding: utf-8 -*-
"""
X-Workflow 主程序入口
一个基于 PySide6 和 PySide6-Fluent-Widgets 的可视化流程编辑器
"""

import shutil
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme

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
    # 在创建任何Qt对象之前设置默认字体，解决Segoe UI缺失警告
    import os
    os.environ["QT_FONT_FAMILY"] = ".AppleSystemUIFont"

    # 初始化配置文件
    initialize_config()

    # Qt 6 已默认启用高DPI支持，无需手动设置
    # 以下属性在Qt 6中已废弃
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序名称
    app.setApplicationName("X-Workflow")

    # 设置默认字体
    from PySide6.QtGui import QFont
    font = QFont(".AppleSystemUIFont", 13)
    app.setFont(font)
    
    # 设置应用程序图标
    from PySide6.QtGui import QIcon
    import platform
    
    # 根据操作系统选择图标格式
    if platform.system() == 'Darwin':  # macOS
        icon_path = get_resource_path("X-Workflow.icns")
    else:  # Windows 或其他系统
        icon_path = get_resource_path("X-Workflow.png")
    
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # 应用 Fluent Design 主题 - 必须在创建任何窗口之前调用
    # 可选主题: Theme.LIGHT, Theme.DARK, Theme.AUTO
    setTheme(Theme.DARK)
    
    # 创建主窗口
    window = MainWindow()
    
    # 手动设置深色背景（确保 qfluentwidgets 组件外的区域也是深色）
    window.setStyleSheet("""
        QMainWindow {
            background-color: #272727;
        }
        QWidget {
            background-color: #272727;
            color: #ffffff;
        }
        QLabel {
            color: #ffffff;
        }
    """)
    
    # 运行应用程序主循环
    sys.exit(app.exec())


# 程序入口
if __name__ == "__main__":
    main()
