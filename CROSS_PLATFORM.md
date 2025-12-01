# 跨平台打包说明

## 为什么不能跨平台运行？

PyInstaller 打包的可执行文件是**平台特定的**：
- macOS 打包 → macOS 可执行文件
- Windows 打包 → Windows 可执行文件 (.exe)
- Linux 打包 → Linux 可执行文件

当前的 `dist/deep-search` 只能在 macOS (ARM64) 上运行。

## 如何在 Windows 上使用

### 方法一：在 Windows 上打包（推荐）

1. 在 Windows 系统上安装 Python 3.6+
2. 安装依赖：
   ```cmd
   pip install -r requirements.txt
   ```
3. 运行 Windows 打包脚本：
   ```cmd
   build.bat
   ```
4. 可执行文件将生成在 `dist\deep-search.exe`

### 方法二：直接运行 Python 脚本（无需打包）

Windows 用户可以直接运行 Python 脚本：

1. 安装 Python 3.6+
2. 安装依赖：
   ```cmd
   pip install -r requirements.txt
   ```
3. 运行程序：
   ```cmd
   python app.py
   python app.py C:\Users\YourName\Documents
   python app.py --help
   ```

## 所有平台的打包方法

### macOS / Linux

```bash
chmod +x build.sh
./build.sh
```

生成文件：`dist/deep-search`

### Windows

```cmd
build.bat
```

生成文件：`dist\deep-search.exe`

## 使用 GitHub Actions 自动打包多平台版本

如果需要为多个平台同时打包，可以使用 CI/CD 工具（如 GitHub Actions）在不同系统上自动构建。

## 打包文件大小参考

- macOS (ARM64): ~4-5 MB
- Windows (x64): ~5-6 MB  
- Linux (x64): ~5-6 MB

## 常见问题

**Q: 可以在一个系统上为其他系统打包吗？**
A: 不可以。必须在目标系统上进行打包。

**Q: 我只有 macOS，怎么给 Windows 用户？**
A: 提供 Python 脚本和 requirements.txt，让用户自己运行或打包。

**Q: 可执行文件能在所有 Windows 版本上运行吗？**
A: 可以在 Windows 7/8/10/11 上运行（需要 64 位系统）。
