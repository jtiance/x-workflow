# -*- coding: utf-8 -*-
"""
流程配置管理模块
负责工作目录的创建、配置的保存和加载
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class WorkflowManager:
    """
    流程管理器
    """
    
    def __init__(self):
        """
        初始化流程管理器
        """
        # 工作目录路径
        self.work_dir = Path.home() / ".x-workflow"
        
        # 配置文件路径
        self.config_file = self.work_dir / "workflow-config.json"
        
        # 内存中的配置
        self.configs: Dict[str, Dict[str, Any]] = {}
        
        # 初始化
        self._load_configs()
    def _load_configs(self):
        """
        从文件加载配置到内存
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.configs = json.load(f)
                print(f"已加载 {len(self.configs)} 个流程配置")
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                self.configs = {}
                
    def _save_configs(self):
        """
        将内存中的配置保存到文件
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.configs, f, ensure_ascii=False, indent=2)
            print(f"已保存 {len(self.configs)} 个流程配置")
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            
    def get_workflow_names(self):
        """
        获取所有流程名称列表
        
        Returns:
            list: 流程名称列表
        """
        return list(self.configs.keys())
        
    def has_workflow(self, name: str) -> bool:
        """
        检查流程名称是否已存在
        
        Args:
            name: 流程名称
            
        Returns:
            bool: 是否存在
        """
        return name in self.configs
        
    def is_valid_name(self, name: str) -> bool:
        """
        检查流程名称是否有效（不包含特殊字符）
        
        Args:
            name: 流程名称
            
        Returns:
            bool: 是否有效
        """
        if not name or not name.strip():
            return False
            
        # 允许的字符：中文、英文、数字、下划线、连字符、空格
        import re
        pattern = r'^[\u4e00-\u9fff\w\-\s]+$'
        return bool(re.match(pattern, name.strip()))
        
    def save_workflow(self, name: str, controls_config: list):
        """
        保存流程配置
        
        Args:
            name: 流程名称
            controls_config: 控件配置列表
        """
        name = name.strip()
        self.configs[name] = {
            "name": name,
            "controls": controls_config
        }
        self._save_configs()
        
    def load_workflow(self, name: str) -> Optional[list]:
        """
        加载流程配置
        
        Args:
            name: 流程名称
            
        Returns:
            list: 控件配置列表，如果不存在返回 None
        """
        if name in self.configs:
            return self.configs[name].get("controls", [])
        return None
        
    def delete_workflow(self, name: str):
        """
        删除流程配置
        
        Args:
            name: 流程名称
        """
        if name in self.configs:
            del self.configs[name]
            self._save_configs()


# 全局流程管理器实例
_workflow_manager: Optional[WorkflowManager] = None


def get_workflow_manager() -> WorkflowManager:
    """
    获取全局流程管理器实例
    
    Returns:
        WorkflowManager: 流程管理器
    """
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = WorkflowManager()
    return _workflow_manager
