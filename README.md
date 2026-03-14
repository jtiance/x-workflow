# X-Workflow

一个基于 PySide6 和 qt-material 的可视化工作流编辑器，支持文本处理流程的可视化编排、保存和管理。

## 环境要求

- Python 3.10+
- Poetry（包管理工具）

## 安装依赖

如果还没有安装 Poetry，可以使用以下方式安装：

> 官方网站：<https://python-poetry.org/>

### macOS (Homebrew)

```bash
brew install poetry
```

### Linux/macOS (curl)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Windows (PowerShell)

在 PowerShell 中运行：

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

或者使用 winget：

```powershell
winget install Poetry.Poetry
```

### 其他方式

```bash
pip install poetry
```

然后在项目目录下安装依赖：

```bash
poetry install
```

## 运行项目

1. 使用 Poetry 运行程序：

```bash
poetry run python main.py
```

或者先进入虚拟环境：

```bash
poetry shell
python main.py
```

<br />

## 打包发布

使用 PyInstaller 打包成可执行文件：

```bash
poetry run pyinstaller --name X-Workflow --windowed --add-data "workflow-config.json:." main.py
```

打包完成后，可执行文件位于 `dist/X-Workflow` 目录下。

<br />

## 项目结构

```
x-workflow/
├── main.py                      # 程序入口
├── workflow_manager.py          # 工作流配置管理器
├── widgets/                     # GUI 组件
│   ├── __init__.py
│   ├── main_window.py          # 主窗口
│   ├── tab_widget.py           # 标签页组件
│   ├── control_panel.py        # 左侧控制面板
│   ├── text_editor.py          # 右侧文本编辑器
│   ├── control_dialog.py       # 控件选择对话框
│   ├── workflow_dialogs.py     # 工作流保存/加载/管理对话框
│   └── arrow_button.py         # 箭头按钮组件
├── controls/                    # 流程控件
│   ├── __init__.py
│   ├── base_control.py         # 控件基类
│   ├── text_replace.py         # 文本替换控件
│   ├── text_search_delete.py   # 文本搜索删除控件
│   ├── json_format.py          # JSON格式化控件
│   ├── json_compress.py        # JSON压缩控件
│   ├── add_text.py             # 增加文本控件
│   ├── add_prefix.py           # 增加前缀控件
│   ├── add_suffix.py           # 增加后缀控件
│   ├── case_convert.py         # 大小写转换控件
│   ├── text_split.py           # 文本分割控件
│   ├── text_merge.py           # 文本合并控件
│   └── remove_duplicate.py     # 移除重复行控件
└── README.md
```

## 核心功能

### 1. 多标签页工作区

- 支持同时打开多个标签页，每个标签页独立工作
- 新建标签页默认命名为"\[未命名]"
- 标签页可关闭（至少保留一个）
- 快捷键支持：
  - `Ctrl+T`：新建标签页
  - `Ctrl+W`：关闭当前标签页
  - `Ctrl+Q`：退出程序
  - `Ctrl+=`：放大文本字号
  - `Ctrl+-`：缩小文本字号

### 2. 可视化控件编排

- 左侧控制面板：添加、配置和管理处理控件
- 右侧文本编辑器：输入和显示文本内容
- 支持添加多个控件，按顺序执行
- 上一个控件的输出作为下一个控件的输入

### 3. 菜单栏

- **文件菜单**：新建标签页、关闭标签页、退出程序
- **查看菜单 → 字体子菜单**：
  - 放大文本字号（Ctrl+=）
  - 缩小文本字号（Ctrl+-）
- **帮助菜单**：关于

### 4. 工作流保存与管理

- 工作目录：`~/.x-workflow/`
- 配置文件：`workflow-config.json`
- 支持工作流的保存、加载、重命名和删除

### 5. 智能保存机制

- **Save 按钮**：新建工作流时显示，弹出输入对话框
- **UPDATE 按钮**：已保存的工作流显示，弹出确认对话框直接更新
- 自动更新标签页名称为工作流名称

### 6. 流程管理器

- 点击 MANAGE 按钮打开流程管理器
- 工具栏包含：
  - 📝 **重命名**：修改工作流名称
  - 🗑️ **删除**：删除工作流（带确认）
- 底部按钮：
  - **使用**：在新标签页中加载选中的工作流
  - **取消**：关闭流程管理器
- 支持双击列表项快速使用工作流

## 控件说明

### 文本替换 (text\_replace)

- **功能**：在文本中查找并替换指定内容
- **参数**：查找文本、替换文本

### 文本搜索删除 (text\_search\_delete)

- **功能**：查找包含或不含特定文本的行并删除
- **参数**：查询文本、匹配模式、删除模式、区分大小写、是否使用正则表达式

### JSON格式化 (json\_format)

- **功能**：格式化 JSON 文本
- **参数**：缩进空格数、是否按键名排序、确保ASCII

### JSON压缩 (json\_compress)

- **功能**：压缩 JSON 文本（移除空白）
- **参数**：是否按键名排序

### 增加文本 (add\_text)

- **功能**：在文本指定位置增加内容
- **参数**：操作类型（增加前缀/后缀/指定位置）、增加的文本

### 增加前缀 (add\_prefix)

- **功能**：在每行开头增加指定文本
- **参数**：前缀文本

### 增加后缀 (add\_suffix)

- **功能**：在每行末尾增加指定文本
- **参数**：后缀文本

### 大小写转换 (case\_convert)

- **功能**：转换文本的大小写
- **参数**：转换类型（大写、小写、首字母大写、句首大写、切换大小写）

### 文本分割 (text\_split)

- **功能**：按分隔符或长度分割文本
- **参数**：分割模式、分隔符、字符数

### 文本合并 (text\_merge)

- **功能**：合并多行文本
- **参数**：合并方式（用分隔符连接、去重后合并）、分隔符

### 移除重复行 (remove\_duplicate)

- **功能**：移除文本中的重复行
- **参数**：模式（保留首次出现/保留最后一次出现）、忽略大小写、忽略空行

## 配置文件格式

工作流配置保存在 `~/.x-workflow/workflow-config.json` 中，格式如下：

```json
{
  "工作流名称1": {
    "name": "工作流名称1",
    "controls": [
      {
        "type": "text_replace",
        "find_text": "查找内容",
        "replace_text": "替换内容"
      },
      {
        "type": "json_format",
        "indent": 4,
        "sort_keys": false,
        "ensure_ascii": false
      }
    ]
  },
  "工作流名称2": {
    "name": "工作流名称2",
    "controls": [...]
  }
}
```

## 技术特点

- **基于 PySide6**：跨平台 GUI 框架
- **qt-material**：Material Design 风格主题
- **JSON 配置**：易于理解和编辑的配置格式
- **多标签页**：支持并行处理多个任务
- **可视化编排**：直观的点击添加式工作流设计

<br />

## 版本历史

### v1.2.0

- 新增"移除重复行"控件
- 新增"增加前缀"控件
- 新增"增加后缀"控件

### v1.1.0

- 新增流程管理器（MANAGE 按钮）
- 新增工作流重命名功能
- 新增工作流删除功能
- 优化按钮布局和样式
- 工具栏图标按钮（📝 重命名、🗑️ 删除）
- 双击列表项快速使用工作流

### v1.0.0

- 初始版本发布
- 支持文本替换和 JSON 格式化控件
- 工作流保存和加载功能
- 多标签页支持
- 快捷键支持

