@echo off
REM Windows 打包脚本

echo 开始打包 deep-search (Windows)...

REM 清理之前的构建
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM 打包为单个可执行文件
pyinstaller --onefile ^
    --name deep-search ^
    --add-data "requirements.txt;." ^
    --hidden-import colorama ^
    --hidden-import tqdm ^
    --hidden-import orjson ^
    --console ^
    app.py

echo.
echo 打包完成！
echo 可执行文件位置: dist\deep-search.exe
echo.
echo 使用方法：
echo   dist\deep-search.exe
echo   dist\deep-search.exe C:\path\to\scan
echo   dist\deep-search.exe --help
