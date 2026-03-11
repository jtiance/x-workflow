# -*- coding: utf-8 -*-
"""
流程对话框模块
包含保存和加载流程的对话框
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QListWidget, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, Signal


class SaveWorkflowDialog(QDialog):
    """
    保存流程对话框
    """
    
    # 定义信号：当用户确认保存时发出
    save_confirmed = Signal(str)  # 流程名称
    
    def __init__(self, existing_names, current_name="[未命名]", parent=None):
        """
        初始化保存对话框
        
        Args:
            existing_names: 已存在的流程名称列表
            current_name: 当前标签的名称
            parent: 父控件
        """
        super().__init__(parent)
        
        self.existing_names = existing_names
        self.current_name = current_name
        
        # 设置对话框属性
        self.setWindowTitle("保存流程")
        self.setMinimumSize(400, 150)
        self.setObjectName("SaveWorkflowDialog")
        
        # 初始化 UI
        self._init_ui()
        
    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 输入标签
        if self.current_name != "[未命名]":
            label = QLabel(f"更新流程 '{self.current_name}':")
        else:
            label = QLabel("请输入流程名称:")
        label.setObjectName("SaveDialogLabel")
        
        # 名称输入框
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入流程名称...")
        self.name_input.setObjectName("WorkflowNameInput")
        self.name_input.textChanged.connect(self._on_text_changed)
        
        # 如果当前标签名不是"[未命名]"，则自动填充
        if self.current_name != "[未命名]":
            self.name_input.setText(self.current_name)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 确定按钮
        self.ok_button = QPushButton("确定")
        self.ok_button.setObjectName("SaveOkButton")
        self.ok_button.clicked.connect(self._on_ok_clicked)
        self.ok_button.setEnabled(False)  # 初始禁用
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("SaveCancelButton")
        self.cancel_button.clicked.connect(self.reject)
        
        # 添加按钮
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        # 将所有组件添加到主布局
        main_layout.addWidget(label)
        main_layout.addWidget(self.name_input)
        main_layout.addLayout(button_layout)
        
    def _on_text_changed(self, text):
        """
        当输入框内容改变时调用
        """
        # 检查 ok_button 是否已经创建
        if not hasattr(self, 'ok_button'):
            return
            
        name = text.strip()
        
        # 检查是否有内容
        has_content = bool(name)
        
        # 检查是否重复（如果当前标签名不是"[未命名]"，且输入的是当前名称，则允许）
        is_duplicate = name in self.existing_names
        is_updating_current = (self.current_name != "[未命名]") and (name == self.current_name)
        
        # 启用/禁用确定按钮
        self.ok_button.setEnabled(has_content and (not is_duplicate or is_updating_current))
        
    def _on_ok_clicked(self):
        """
        当点击确定按钮时调用
        """
        name = self.name_input.text().strip()
        
        # 再次验证
        if not name:
            QMessageBox.warning(self, "警告", "流程名称不能为空！")
            return
            
        # 检查是否重复（如果当前标签名不是"[未命名]"，且输入的是当前名称，则允许）
        is_duplicate = name in self.existing_names
        is_updating_current = (self.current_name != "[未命名]") and (name == self.current_name)
        
        if is_duplicate and not is_updating_current:
            QMessageBox.warning(self, "警告", "该流程名称已存在！")
            return
            
        # 发出信号并关闭
        self.save_confirmed.emit(name)
        self.accept()


class WorkflowManagerDialog(QDialog):
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
        super().__init__(parent)
        
        self.workflow_names = workflow_names
        
        # 设置对话框属性
        self.setWindowTitle("流程管理器")
        self.setMinimumSize(500, 450)
        self.setObjectName("WorkflowManagerDialog")
        
        # 初始化 UI
        self._init_ui()
        
    def _init_ui(self):
        """
        初始化用户界面
        """
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # ============= 工具栏 =============
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(2)
        
        # 重命名按钮
        self.rename_button = QPushButton("📝")
        self.rename_button.setToolTip("重命名")
        self.rename_button.setMinimumSize(50, 40)
        self.rename_button.setMaximumSize(50, 40)
        self.rename_button.setObjectName("RenameButton")
        self.rename_button.setStyleSheet("QPushButton { font-size: 20px; border: none; background: transparent; } QPushButton:hover { background: rgba(0, 0, 0, 0.1); border-radius: 4px; }")
        self.rename_button.clicked.connect(self._on_rename_clicked)
        self.rename_button.setEnabled(False)  # 初始禁用
        
        # 删除按钮
        self.delete_button = QPushButton("🗑️")
        self.delete_button.setToolTip("删除")
        self.delete_button.setMinimumSize(50, 40)
        self.delete_button.setMaximumSize(50, 40)
        self.delete_button.setObjectName("DeleteButton")
        self.delete_button.setStyleSheet("QPushButton { font-size: 20px; border: none; background: transparent; } QPushButton:hover { background: rgba(0, 0, 0, 0.1); border-radius: 4px; }")
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.delete_button.setEnabled(False)  # 初始禁用
        
        toolbar_layout.addWidget(self.rename_button)
        toolbar_layout.addWidget(self.delete_button)
        toolbar_layout.addStretch()
        
        # ============= 列表区域 =============
        # 列表标签
        label = QLabel("流程列表:")
        label.setObjectName("LoadDialogLabel")
        
        # 流程列表
        self.workflow_list = QListWidget()
        self.workflow_list.setObjectName("WorkflowList")
        self.workflow_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # 填充列表
        for name in self.workflow_names:
            self.workflow_list.addItem(name)
            
        # ============= 底部按钮区域 =============
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 使用按钮
        self.use_button = QPushButton("使用")
        self.use_button.setObjectName("UseButton")
        self.use_button.clicked.connect(self._on_use_clicked)
        self.use_button.setEnabled(False)  # 初始禁用
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.clicked.connect(self.reject)
        
        # 添加按钮
        button_layout.addWidget(self.use_button)
        button_layout.addWidget(self.cancel_button)
        
        # 将所有组件添加到主布局
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(label)
        main_layout.addWidget(self.workflow_list, 1)  # 让列表占更多空间
        main_layout.addLayout(button_layout)
        
        # 连接列表选择信号
        self.workflow_list.currentItemChanged.connect(self._on_selection_changed)
        
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
            self.accept()
            
    def _on_delete_clicked(self):
        """
        当点击删除按钮时调用
        """
        current_item = self.workflow_list.currentItem()
        if current_item:
            name = current_item.text()
            
            # 显示确认对话框
            from PySide6.QtWidgets import QMessageBox, QPushButton
            
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("确认删除")
            msg_box.setText(f"确定要删除流程 '{name}' 吗？")
            msg_box.setIcon(QMessageBox.Question)
            
            # 添加中文按钮
            no_button = msg_box.addButton("取消", QMessageBox.NoRole)
            yes_button = msg_box.addButton("确定", QMessageBox.YesRole)
            
            msg_box.exec()
            
            if msg_box.clickedButton() == yes_button:
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
        dialog = QDialog(self)
        dialog.setWindowTitle("重命名流程")
        dialog.setMinimumSize(400, 150)
        
        # 创建布局
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标签
        label = QLabel(f"请输入新的流程名称 (原名称: {old_name}):")
        layout.addWidget(label)
        
        # 输入框
        name_input = QLineEdit()
        name_input.setText(old_name)
        name_input.setPlaceholderText("输入新的流程名称...")
        layout.addWidget(name_input)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.setEnabled(False)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
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
        
        # 确定按钮点击
        def on_ok_clicked():
            new_name = name_input.text().strip()
            
            # 再次验证
            if not new_name:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(dialog, "警告", "流程名称不能为空！")
                return
                
            if new_name in self.workflow_names and new_name != old_name:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(dialog, "警告", "该流程名称已存在！")
                return
            
            # 更新列表
            current_item.setText(new_name)
            
            # 更新流程名称列表
            self.workflow_names.remove(old_name)
            self.workflow_names.append(new_name)
            
            # 发出重命名信号
            self.rename_confirmed.emit(old_name, new_name)
            
            dialog.accept()
        
        ok_button.clicked.connect(on_ok_clicked)
        
        # 显示对话框
        dialog.exec()
