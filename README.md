# Deep Search - 目录扫描工具

一个强大的目录扫描工具，可以递归遍历目录并生成JSON格式的文件路径信息。

## 功能特性

- 📊 两种输出格式：树状结构和平面列表
- 🎨 彩色终端输出
- 📈 实时进度条显示
- 📝 详细日志记录
- 📉 文件类型统计
- 🚀 支持打包为独立可执行文件

## 安装

### 从源代码运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python app.py
```

### 使用打包版本

```bash
# 打包程序
chmod +x build.sh
./build.sh

# 运行打包后的程序
./dist/deep-search
```

## 使用方法

### 基本用法

```bash
# 扫描当前目录
python app.py

# 扫描指定目录
python app.py /path/to/directory

# 扫描用户主目录下的文档
python app.py ~/Documents
```

### 高级选项

```bash
# 自定义输出文件名
python app.py /some/path --output mydata

# 只生成树状结构
python app.py /some/path --tree-only

# 只生成平面列表
python app.py /some/path --list-only

# 显示详细日志
python app.py /some/path -v

# 不显示进度条（适合重定向输出）
python app.py /some/path --no-progress

# 查看完整帮助
python app.py --help
```

## 输出文件

程序会生成两个JSON文件：

1. **`{output}_tree.json`** - 树状结构，包含目录层级关系
2. **`{output}_list.json`** - 平面列表，包含所有文件的完整路径和相对路径

## 输出示例

### 树状结构示例
```json
{
  "name": "project",
  "path": "/path/to/project",
  "type": "directory",
  "children": [
    {
      "name": "app.py",
      "path": "/path/to/project/app.py",
      "type": "file",
      "size": 3191
    }
  ]
}
```

### 平面列表示例
```json
[
  {
    "name": "app.py",
    "path": "/path/to/project/app.py",
    "relative_path": "app.py",
    "size": 3191
  }
]
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `path` | 要扫描的目录路径（默认为当前目录） |
| `-o, --output` | 输出文件名前缀（默认为 "file"） |
| `--tree-only` | 只生成树状结构 |
| `--list-only` | 只生成平面列表 |
| `-v, --verbose` | 显示详细日志信息 |
| `--no-progress` | 不显示进度条 |
| `-h, --help` | 显示帮助信息 |

## 依赖

- Python 3.6+
- colorama - 彩色终端输出
- tqdm - 进度条显示
- orjson - 高性能JSON处理

## 打包说明

### 自动构建（推荐）

项目已配置 GitHub Actions，可自动为所有平台构建可执行文件：

1. **推送版本标签触发构建**：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **下载构建文件**：
   - 访问 [Actions](https://github.com/mflix-team/deep-search/actions) 页面
   - 下载对应平台的 Artifacts：
     - `deep-search-windows-latest` (Windows .exe)
     - `deep-search-macos-latest` (macOS)
     - `deep-search-ubuntu-latest` (Linux)

### 本地打包

如需在本地打包，PyInstaller 打包的可执行文件是**平台特定**的：

**macOS / Linux**:
```bash
chmod +x build.sh
./build.sh
```

**Windows**:
```cmd
build.bat
```

**手动打包**:
```bash
pyinstaller --onefile --name deep-search --console app.py
```

打包后的可执行文件位于 `dist/` 目录，可以直接运行，无需安装 Python 环境。

## 许可证

MIT License
