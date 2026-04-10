# -*- coding: utf-8 -*-
"""
资源文件工具类
统一处理资源文件路径，兼容开发环境和 PyInstaller 打包环境
"""
import sys
from pathlib import Path


def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径，兼容开发环境和 PyInstaller 打包环境

    Args:
        relative_path: 相对于项目根目录的资源文件路径

    Returns:
        资源文件的绝对路径 Path 对象
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的环境
        base_path = Path(sys._MEIPASS)
    else:
        # 开发环境：当前文件在 utils 目录，所以需要返回上一级到项目根目录
        base_path = Path(__file__).parent.parent
    return base_path / relative_path
