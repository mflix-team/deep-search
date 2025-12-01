# 使用 GitHub Actions 自动构建多平台版本

## 步骤 1: 在 GitHub 上创建仓库

1. 访问 [GitHub](https://github.com) 并登录
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `deep-search`
   - **Description**: `递归目录扫描工具 - 支持树状结构和平面列表输出`
   - **Public** 或 **Private**（根据需要选择）
4. 不要勾选 "Initialize this repository with a README"（我们已经有了）
5. 点击 "Create repository"

## 步骤 2: 推送代码到 GitHub

复制 GitHub 提供的命令，或使用以下命令（替换成你的仓库地址）：

```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/deep-search.git

# 推送代码
git push -u origin main
```

如果遇到分支名称问题，可能需要：
```bash
git branch -M main
git push -u origin main
```

## 步骤 3: 触发自动构建

### 方式 A: 创建版本标签（推荐）

```bash
# 创建版本标签
git tag v1.0.0

# 推送标签到 GitHub
git push origin v1.0.0
```

这会自动触发 GitHub Actions 构建所有平台的版本。

### 方式 B: 手动触发

1. 在 GitHub 仓库页面，点击 "Actions" 标签
2. 在左侧选择 "Build Executables"
3. 点击右侧的 "Run workflow" 下拉按钮
4. 点击绿色的 "Run workflow" 按钮

## 步骤 4: 下载构建的可执行文件

1. 构建完成后（大约 5-10 分钟），在 "Actions" 页面找到对应的工作流运行
2. 向下滚动到 "Artifacts" 部分
3. 下载对应平台的文件：
   - `deep-search-ubuntu-latest` - Linux 版本
   - `deep-search-windows-latest` - Windows 版本 (.exe)
   - `deep-search-macos-latest` - macOS 版本

## 步骤 5: 创建 Release（可选）

为了让用户更方便下载，可以创建 Release：

1. 在 GitHub 仓库页面，点击右侧的 "Releases"
2. 点击 "Create a new release"
3. 选择刚才创建的标签（v1.0.0）
4. 填写 Release 标题和说明
5. 将下载的可执行文件重命名并上传：
   - `deep-search-linux-x64`
   - `deep-search-windows-x64.exe`
   - `deep-search-macos-arm64` 或 `deep-search-macos-x64`
6. 点击 "Publish release"

## 工作流说明

GitHub Actions 工作流配置在 `.github/workflows/build.yml`：

- **触发条件**：
  - 推送版本标签（v*）
  - 手动触发（workflow_dispatch）

- **构建平台**：
  - Ubuntu (Linux x64)
  - Windows (Windows x64)
  - macOS (macOS ARM64/x64)

- **输出**：每个平台的独立可执行文件

## 后续更新

每次发布新版本时：

```bash
# 提交代码更改
git add .
git commit -m "描述你的更改"
git push

# 创建新版本标签
git tag v1.1.0
git push origin v1.1.0
```

GitHub Actions 会自动为新版本构建所有平台的可执行文件。

## 注意事项

1. **首次构建**可能需要 5-10 分钟
2. **私有仓库**可能有 Actions 使用限制（查看 GitHub 定价）
3. **macOS 构建**可能生成 ARM64 或 x64 版本（取决于 GitHub 提供的运行器）
4. 构建的可执行文件会作为 **Artifacts** 保存 90 天

## 故障排查

如果构建失败：

1. 检查 "Actions" 标签中的错误日志
2. 确保 `requirements.txt` 包含所有依赖
3. 确认 `app.py` 没有语法错误
4. 查看工作流配置是否正确

## 本地测试工作流

在推送前可以使用 [act](https://github.com/nektos/act) 在本地测试 GitHub Actions：

```bash
# 安装 act (macOS)
brew install act

# 测试工作流
act -j build
```
