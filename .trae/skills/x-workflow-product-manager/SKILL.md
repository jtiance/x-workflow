---
name: x-workflow-product-manager
description: X-Workflow 产品经理技能，用于理解用户需求并转化为产品 PRD。专门针对 x-workflow 可视化流程编辑器项目，包含控件设计、布局规范、集成流程等方面的产品知识。使用场景：(1) 用户提出新的控件需求时，(2) 需要优化现有控件布局时，(3) 需要添加新功能到 x-workflow 时，(4) 需要编写产品需求文档时。
---

# X-Workflow 产品经理 SKILL

## 项目概述

X-Workflow 是一个基于 PySide6 和 qt-material 的可视化流程编辑器，用于通过拖拽和配置控件来构建文本处理工作流。

## 核心产品原则

### 1. 控件设计规范

#### 控件基类 (BaseControl)
所有控件必须继承自 `BaseControl`，并实现以下方法：
- `_init_content()` - 初始化控件 UI（替代旧的 `_setup_ui()`）
- `execute(text)` - 执行控件的核心逻辑
- `get_config()` - 获取控件配置
- `load_config(config)` - 加载控件配置
- `get_control_type()` - 返回控件类型标识
- `reset_parameters()` - 重置参数到默认值

#### 布局规范
- **必须使用 GridLayout** - 确保所有控件的 label 右对齐，右侧组件对齐
- **Label 宽度统一** - 所有 label 最小宽度设为 70px
- **右侧组件自动填充** - 使用 `QSizePolicy.Expanding` 和 `setColumnStretch(1, 1)`
- **间距统一** - 使用 `setSpacing(10)` 设置行间距
- **CheckBox 跨两列** - 对于单选选项，使用 `addWidget(widget, row, 0, 1, 2)` 跨两列显示

#### 控件集成流程
新控件添加需要完成以下步骤：

1. **创建控件文件** - 在 `controls/` 目录下创建 `<control_name>.py`
2. **更新 `__init__.py`** - 添加导入语句和 `__all__` 列表
3. **更新 `control_dialog.py`** - 在 `_populate_control_list()` 中添加控件
4. **更新 `control_dialog.py`** - 在 `_update_preview()` 中添加预览逻辑
5. **更新 `main_window.py`** - 在 `_on_control_selected()` 中添加创建逻辑

### 2. 历史需求回顾

#### 已实现的需求
1. **控件加载问题** (2026-03-12)
   - 问题：新增控件未在选择器中展示
   - 解决方案：更新三个文件（`__init__.py`、`control_dialog.py`、`main_window.py`）

2. **控件布局优化** (2026-03-12)
   - 问题：使用 HBoxLayout 导致 label 不对齐
   - 解决方案：统一改为 GridLayout

3. **控件合并** (2026-03-12)
   - 需求：将 add_prefix 和 add_suffix 合并为 add_text
   - 功能：支持增加前缀、增加后缀、增加前后缀三种模式

4. **大小写转换控件优化** (2026-03-12)
   - 需求：重新设计界面，下拉菜单填充空白区域
   - 增加功能：全部大写、全部小写、首字母大写、每个单词首字母大写

### 3. PRD 模板

当需要编写产品需求文档时，使用以下结构：

```markdown
# X-Workflow 产品需求文档 (PRD)

## 1. 需求概述
- 需求来源：
- 优先级：[高/中/低]
- 预计开发时间：

## 2. 功能描述
详细描述需要实现的功能。

## 3. 用户故事
作为 [用户角色]，我想要 [功能]，以便 [价值]。

## 4. 验收标准
- [ ] 标准 1
- [ ] 标准 2

## 5. 技术实现要点
- 需要修改的文件列表
- 关键实现细节

## 6. 测试要点
- 测试场景 1
- 测试场景 2
```

### 4. 需求分析工作流

当用户提出新需求时，按以下步骤处理：

1. **理解需求**
   - 明确用户想要解决的问题
   - 识别是新增功能还是优化现有功能
   - 确认优先级和时间要求

2. **评估影响**
   - 确定需要修改哪些文件
   - 评估是否影响现有功能
   - 考虑是否需要更新文档

3. **制定方案**
   - 如果是新控件：按照"控件集成流程"执行
   - 如果是布局优化：确保使用 GridLayout 规范
   - 如果是功能优化：评估对现有配置的兼容性

4. **编写 PRD**（如需要）
   - 使用上述 PRD 模板
   - 包含验收标准和测试要点

### 5. 控件类型列表

当前已有的控件：
- `text_replace` - 文本替换
- `json_format` - JSON 格式化
- `add_text` - 增加文本（前缀/后缀/前后缀）
- `case_convert` - 大小写转换
- `text_split` - 文本分割
- `text_merge` - 文本合并
- `text_search_delete` - 文本搜索删除

### 6. 常见问题处理

#### Q: 新增控件后在选择器中看不到？
A: 检查三个文件是否都更新了：
1. `controls/__init__.py` - 是否添加了导入
2. `widgets/control_dialog.py` - `_populate_control_list()` 是否添加
3. `widgets/main_window.py` - `_on_control_selected()` 是否添加

#### Q: 控件应该使用什么布局？
A: 必须使用 GridLayout，确保：
- Label 宽度 70px
- 右侧组件使用 Expanding 策略
- 设置 `setColumnStretch(1, 1)`

#### Q: 如何处理配置兼容性？
A: 在 `load_config()` 中提供默认值，确保旧配置也能正常加载。