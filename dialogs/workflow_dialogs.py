# -*- coding: utf-8 -*-
"""
流程对话框模块
包含保存和加载流程的对话框
"""

from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QLineEdit, QWidget, QVBoxLayout
)
from PySide6.QtCore import Signal
from qfluentwidgets import PushButton, ListWidget, LineEdit

from .custom_dialog import CustomDialog


class SaveWorkflowDialog(CustomDialog):
    """
    保存流程对话框
    """

    # 定义信号：当用户确认保存时发出
    save_confirmed = Signal(str)  # 流程名称

    def __init__(self, existing_names, current_name="未命名", parent=None):
        """
        初始化保存对话框

        Args:
            existing_names: 已存在的流程名称列表
            current_name: 当前标签的名称
            parent: 父控件
        """
        super().__init__(title="保存流程", parent=parent)

        self.existing_names = existing_names
        self.current_name = current_name
        self.is_updating = current_name != "未命名"

        # 设置对话框属性
        self.setMinimumSize(400, 180)

        # 初始化 UI
        self._init_ui()

    def _init_ui(self):
        """
        初始化用户界面
        """
        if self.is_updating:
            # 更新模式：只显示确认界面
            label = QLabel(f"确定要更新流程 '{self.current_name}' 吗？")
            self.add_content_widget(label)

            # 按钮区域
            self.add_button("取消", is_reject=True)
            self.add_button("覆盖", callback=self._on_ok_clicked, is_accept=True)
            self.save_as_button = self.add_button("另存为", callback=self._on_save_as_clicked)
        else:
            # 保存模式：显示输入框
            label = QLabel("流程名称:")
            self.add_content_widget(label)

            # 名称输入框
            self.name_input = LineEdit()
            self.name_input.setPlaceholderText("输入流程名称...")
            self.name_input.textChanged.connect(self._on_text_changed)
            self.add_content_widget(self.name_input)

            # 错误提示 label
            self.error_label = QLabel()
            self.error_label.setMinimumHeight(20)
            self.error_label.setText("")
            self.add_content_widget(self.error_label)

            # 按钮区域
            self.add_button("取消", is_reject=True)
            self.ok_button = self.add_button("确定", callback=self._on_ok_clicked, is_accept=True)
            self.ok_button.setEnabled(False)

    def _on_text_changed(self, text):
        """
        当输入框内容改变时调用
        """
        # 只在保存模式下处理
        if self.is_updating:
            return

        # 检查 ok_button 是否已经创建
        if not hasattr(self, 'ok_button'):
            return

        name = text.strip()

        # 检查是否有内容
        has_content = bool(name)

        # 检查是否重复
        is_duplicate = name in self.existing_names

        # 显示/隐藏错误提示
        if has_content and is_duplicate:
            self.error_label.setText("流程名称已经存在，请换一个名称重试")
        else:
            self.error_label.setText("")

        # 启用/禁用确定按钮
        self.ok_button.setEnabled(has_content and not is_duplicate)

    def _on_ok_clicked(self):
        """
        当点击确定/覆盖按钮时调用
        """
        if self.is_updating:
            # 更新模式：直接用当前名称
            name = self.current_name
        else:
            # 保存模式：从输入框获取
            name = self.name_input.text().strip()

            # 验证
            if not name:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "警告", "流程名称不能为空！")
                return

            # 检查是否重复
            is_duplicate = name in self.existing_names

            if is_duplicate:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "警告", "该流程名称已存在！")
                return

        # 发出信号
        self.save_confirmed.emit(name)

    def _on_save_as_clicked(self):
        """
        当点击另存为按钮时调用
        """
        # 关闭当前对话框
        self.reject()

        # 在当前名称后加"_1"，并确保不重复
        base_name = self.current_name
        new_name = f"{base_name}_1"
        counter = 2
        while new_name in self.existing_names:
            new_name = f"{base_name}_{counter}"
            counter += 1

        # 创建新的保存对话框（非更新模式）
        dialog = SaveWorkflowDialog(self.existing_names, "未命名", self.parent())

        # 自动填充建议的新名称
        if hasattr(dialog, 'name_input'):
            dialog.name_input.setText(new_name)

        dialog.save_confirmed.connect(self.save_confirmed.emit)
        dialog.exec()


class WorkflowManagerDialog(CustomDialog):
    """
    流程管理器对话框
    """

    # 定义信号：当用户选择使用时发出
    use_confirmed = Signal(str)  # 流程名称
    # 定义信号：当用户删除流程时发出
    delete_confirmed = Signal(str)  # 流程名称
    # 定义信号：当用户重命名流程时发出
    rename_confirmed = Signal(str, str)  # 旧名称, 新名称

    def __init__(self, workflow_names, parent=None):
        """
        初始化流程管理器对话框

        Args:
            workflow_names: 流程名称列表
            parent: 父控件
        """
        super().__init__(title="流程管理器", parent=parent)

        self.workflow_names = workflow_names

        # 设置对话框属性
        self.setMinimumSize(500, 450)

        # 初始化 UI
        self._init_ui()

    def _init_ui(self):
        """
        初始化用户界面
        """
        # ============= 工具栏 =============
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(2)

        # 重命名按钮
        self.rename_button = PushButton("📝")
        self.rename_button.setToolTip("重命名")
        self.rename_button.setMinimumSize(50, 40)
        self.rename_button.setMaximumSize(50, 40)
        self.rename_button.clicked.connect(self._on_rename_clicked)
        self.rename_button.setEnabled(False)  # 初始禁用

        # 删除按钮
        self.delete_button = PushButton("🗑️")
        self.delete_button.setToolTip("删除")
        self.delete_button.setMinimumSize(50, 40)
        self.delete_button.setMaximumSize(50, 40)
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.delete_button.setEnabled(False)  # 初始禁用

        toolbar_layout.addWidget(self.rename_button)
        toolbar_layout.addWidget(self.delete_button)
        toolbar_layout.addStretch()

        # 工具栏容器
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        self.add_content_widget(toolbar_widget)

        # ============= 列表区域 =============
        # 列表标签
        label = QLabel("流程列表:")
        self.add_content_widget(label)

        # 流程列表
        self.workflow_list = ListWidget()
        self.workflow_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        # 使用 !important 强制覆盖背景色
        self.workflow_list.setStyleSheet("""
            ListWidget {
                border: 1px solid #4a4a4a;
                border-radius: 4px;
            }
            ListWidget::item {
                min-height: 30px;
            }
            ListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
        """)

        # ============= 底部按钮区域 =============
        # 取消按钮
        self.add_button("取消", is_reject=True)
        # 使用按钮（主按钮蓝色）
        self.use_button = self.add_button("使用", callback=self._on_use_clicked, is_primary=True, is_accept=True)
        self.use_button.setEnabled(False)  # 初始禁用

        # 连接列表选择信号
        self.workflow_list.currentItemChanged.connect(self._on_selection_changed)

        # 填充列表
        for name in self.workflow_names:
            self.workflow_list.addItem(name)

        # 默认选中第一个选项
        if self.workflow_list.count() > 0:
            self.workflow_list.setCurrentRow(0)

        self.add_content_widget(self.workflow_list, 1)  # 让列表占更多空间

    def _on_selection_changed(self, current, previous):
        """
        当列表选择改变时调用
        """
        has_selection = current is not None
        self.use_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.rename_button.setEnabled(has_selection)

    def _on_item_double_clicked(self, item):
        """
        当双击列表项时调用
        """
        if item:
            name = item.text()
            self.use_confirmed.emit(name)
            self.accept()

    def _on_use_clicked(self):
        """
        当点击使用按钮时调用
        """
        current_item = self.workflow_list.currentItem()
        if current_item:
            name = current_item.text()
            self.use_confirmed.emit(name)

    def _on_delete_clicked(self):
        """
        当点击删除按钮时调用
        """
        current_item = self.workflow_list.currentItem()
        if current_item:
            name = current_item.text()

            # 显示自定义确认对话框
            dialog = DeleteConfirmDialog(name, self)

            if dialog.exec() == CustomDialog.Accepted:
                # 发出删除信号
                self.delete_confirmed.emit(name)
                # 从列表中移除
                row = self.workflow_list.row(current_item)
                self.workflow_list.takeItem(row)
                # 更新流程名称列表
                self.workflow_names.remove(name)
                # 如果列表为空，禁用按钮
                if self.workflow_list.count() == 0:
                    self.use_button.setEnabled(False)
                    self.delete_button.setEnabled(False)
                    self.rename_button.setEnabled(False)

    def _on_rename_clicked(self):
        """
        当点击重命名按钮时调用
        """
        current_item = self.workflow_list.currentItem()
        if not current_item:
            return

        old_name = current_item.text()

        # 创建重命名对话框
        dialog = CustomDialog(title="重命名流程", parent=self)
        dialog.setMinimumSize(400, 150)

        # 标签
        label = QLabel(f"请输入新的流程名称 (原名称: {old_name}):")
        dialog.add_content_widget(label)

        # 输入框
        name_input = LineEdit()
        name_input.setText(old_name)
        name_input.setPlaceholderText("输入新的流程名称...")
        dialog.add_content_widget(name_input)

        # 按钮
        dialog.add_button("取消", is_reject=True)
        ok_button = dialog.add_button("确定", is_accept=True)
        ok_button.setEnabled(False)

        # 验证函数
        def validate_name():
            new_name = name_input.text().strip()
            has_content = bool(new_name)
            is_duplicate = new_name in self.workflow_names and new_name != old_name
            ok_button.setEnabled(has_content and not is_duplicate)

        # 连接输入改变信号
        name_input.textChanged.connect(validate_name)

        # 初始验证
        validate_name()

        # 显示对话框
        if dialog.exec() == CustomDialog.Accepted:
            new_name = name_input.text().strip()

            # 再次验证
            if not new_name:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "警告", "流程名称不能为空！")
                return

            if new_name in self.workflow_names and new_name != old_name:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "警告", "该流程名称已存在！")
                return

            # 更新列表
            current_item.setText(new_name)

            # 更新流程名称列表
            self.workflow_names.remove(old_name)
            self.workflow_names.append(new_name)

            # 发出重命名信号
            self.rename_confirmed.emit(old_name, new_name)


class DeleteConfirmDialog(CustomDialog):
    """
    自定义删除确认对话框
    """

    def __init__(self, workflow_name, parent=None):
        """
        初始化删除确认对话框

        Args:
            workflow_name: 要删除的流程名称
            parent: 父控件
        """
        super().__init__(title="确认删除", parent=parent)

        self.workflow_name = workflow_name

        # 设置对话框属性
        self.setMinimumSize(350, 120)

        # 初始化 UI
        self._init_ui()

    def _init_ui(self):
        """
        初始化用户界面
        """
        # 提示标签
        label = QLabel(f"确定要删除流程 '{self.workflow_name}' 吗？")
        self.add_content_widget(label)

        # 按钮区域
        self.add_button("取消", is_reject=True)
        self.add_button("确定", is_accept=True)
