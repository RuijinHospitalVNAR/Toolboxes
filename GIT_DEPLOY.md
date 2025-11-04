# GitHub Pages 部署指南

本指南将帮助您将 VLPIM Web Services 部署到 GitHub Pages。

## 步骤 1: 在 GitHub 上创建仓库

1. 访问 https://github.com/RuijinHospitalVNAR
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 仓库名称填写：`Toolboxes`
4. 设置为 **Public**（GitHub Pages 需要公开仓库）
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

## 步骤 2: 初始化本地 Git 仓库

在项目根目录（`F:\文章投递内容\2025\VLPIM\脚本`）打开 PowerShell 或 Git Bash，执行以下命令：

```powershell
# 初始化 Git 仓库（如果还没有）
git init

# 添加远程仓库
git remote add origin https://github.com/RuijinHospitalVNAR/Toolboxes.git

# 如果已经添加过，可以更新：
# git remote set-url origin https://github.com/RuijinHospitalVNAR/Toolboxes.git
```

## 步骤 3: 准备文件并提交

```powershell
# 查看当前状态
git status

# 添加所有文件（除了 .gitignore 中排除的）
git add README.md
git add index.html
git add VLPIM_Web_services/
git add .github/
git add .gitignore
git add DEPLOY.md
git add GIT_DEPLOY.md

# 或者一次性添加所有文件
# git add .

# 提交更改
git commit -m "Initial commit: Add VLPIM Web Services tool to Toolboxes repository"
```

## 步骤 4: 推送到 GitHub

```powershell
# 设置主分支为 main（GitHub Pages 推荐）
git branch -M main

# 推送到 GitHub
git push -u origin main
```

如果遇到认证问题，您可能需要：
- 使用 GitHub Personal Access Token（推荐）
- 或配置 SSH 密钥

### 使用 Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 生成新 token，勾选 `repo` 权限
3. 推送时使用 token 作为密码

## 步骤 5: 启用 GitHub Pages

1. 访问仓库设置：https://github.com/RuijinHospitalVNAR/Toolboxes/settings
2. 在左侧菜单中找到 "Pages"
3. 在 "Source" 部分：
   - Branch: 选择 `main`
   - Folder: 选择 `/ (root)`
4. 点击 "Save"
5. 等待几分钟让 GitHub 构建和部署

## 步骤 6: 访问您的网站

部署成功后，您的网站将在以下地址可用：

- **主页**: https://ruijinhospitalvnar.github.io/Toolboxes/
- **VLPIM Web Services**: https://ruijinhospitalvnar.github.io/Toolboxes/VLPIM_Web_services/

注意：首次部署可能需要几分钟时间。您可以在仓库的 "Actions" 标签页查看部署进度。

## 后续更新

当您需要更新网站时：

```powershell
# 1. 更新文件
# （例如：修改 static_example.html 后，重新复制到 VLPIM_Web_services/index.html）

# 2. 添加更改
git add .

# 3. 提交
git commit -m "Update: 描述您的更改"

# 4. 推送
git push origin main
```

GitHub Pages 会自动重新构建和部署（通常需要 1-2 分钟）。

## 添加更多工具

当您需要添加新工具时：

1. 创建新目录：`NewToolName/`
2. 在该目录中放置 `index.html`
3. 更新根目录的 `index.html`，添加新工具的链接
4. 更新根目录的 `README.md`
5. 提交并推送更改

## 文件结构

最终的仓库结构应该是：

```
Toolboxes/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml
├── VLPIM_Web_services/
│   ├── index.html          # 主页面（从 static_example.html 复制）
│   ├── readme.html         # 说明文档
│   ├── toolset.html        # 工具集页面
│   ├── README.md           # VLPIM 说明
│   ├── DP_P03146_NetMHCIIpan.xls  # 示例数据
│   └── 6htx.pdb            # 示例结构文件
├── index.html              # 仓库主页
├── README.md               # 仓库说明
├── .gitignore              # Git 忽略文件
├── DEPLOY.md               # 部署说明
└── GIT_DEPLOY.md           # Git 部署指南（本文件）
```

## 故障排除

### 问题：Pages 不显示
- 检查 GitHub Actions 是否有错误
- 确保仓库是 Public
- 检查文件路径是否正确（区分大小写）

### 问题：CSS/JS 不加载
- 检查 CDN 链接是否可访问
- 查看浏览器控制台的错误信息

### 问题：404 错误
- 确保文件路径正确
- 检查 `index.html` 中的链接路径

### 问题：大文件上传失败
- GitHub 限制单个文件 100MB
- 考虑使用 Git LFS 处理大文件

## 联系与支持

如有问题，请访问：
- GitHub Issues: https://github.com/RuijinHospitalVNAR/Toolboxes/issues
- 作者：Dr. Chufan Wang
- 邮箱：wcf231229@163.com

