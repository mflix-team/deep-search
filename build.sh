#!/bin/bash
# 使用 PyInstaller 打包脚本

echo "开始打包 deep-search..."

# 清理之前的构建
rm -rf build dist *.spec

# 打包为单个可执行文件
pyinstaller --onefile \
    --name deep-search \
    --add-data "requirements.txt:." \
    --hidden-import colorama \
    --hidden-import tqdm \
    --hidden-import orjson \
    --console \
    app.py

echo ""
echo "打包完成！"
echo "可执行文件位置: dist/deep-search"
echo ""
echo "使用方法："
echo "  ./dist/deep-search"
echo "  ./dist/deep-search /path/to/scan"
echo "  ./dist/deep-search --help"
