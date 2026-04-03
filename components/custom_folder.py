# -*- coding: utf-8 -*-
"""
自定义文件夹选择组件
类似 SearchLineEdit，但使用文件夹图标用于选择目录
"""

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFileDialog
from qfluentwidgets import LineEdit
from qfluentwidgets.common.icon import FluentIcon as FIF
from qfluentwidgets.components.widgets.line_edit import LineEditButton


class CustomFolder(LineEdit):
    """文件夹选择输入框"""

    folder_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.folderButton = LineEditButton(FIF.FOLDER, self)

        self.hBoxLayout.addWidget(self.folderButton, 0, Qt.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)

        self.folderButton.clicked.connect(self._open_folder_dialog)
        self.clearButton.clicked.connect(self.clear)

    def _open_folder_dialog(self):
        """打开文件夹选择对话框"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择导出目录",
            self.text() or ""
        )
        if folder:
            self.setText(folder)
            self.folder_selected.emit(folder)

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        self.setTextMargins(0, 0, 28 * enable + 30, 0)
