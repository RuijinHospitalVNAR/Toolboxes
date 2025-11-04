# 快速开始指南

## 一键部署脚本

如果您已经配置好 Git 和 GitHub，可以使用以下命令快速部署：

### Windows PowerShell

```powershell
# 1. 确保在项目根目录
cd "F:\文章投递内容\2025\VLPIM\脚本"

# 2. 运行部署脚本（如果需要重新准备文件）
# .\deploy.ps1

# 3. 初始化 Git（如果还没有）
git init

# 4. 添加远程仓库
git remote add origin https://github.com/RuijinHospitalVNAR/Toolboxes.git
# 如果已存在，使用：git remote set-url origin https://github.com/RuijinHospitalVNAR/Toolboxes.git

# 5. 添加所有文件
git add .

# 6. 提交
git commit -m "Initial commit: Add VLPIM Web Services"

# 7. 推送到 GitHub
git branch -M main
git push -u origin main
```

### 后续更新

```powershell
# 更新文件后
git add .
git commit -m "Update: 描述更改内容"
git push origin main
```

## 手动部署步骤

如果自动脚本不可用，请参考 [GIT_DEPLOY.md](GIT_DEPLOY.md) 中的详细步骤。

## 验证部署

1. 推送成功后，访问 https://github.com/RuijinHospitalVNAR/Toolboxes
2. 进入 Settings → Pages
3. 确认 "Source" 设置为 `main` 分支
4. 等待几分钟后访问：https://ruijinhospitalvnar.github.io/Toolboxes/

## 常见问题

**Q: 推送时要求输入用户名和密码？**  
A: 使用 GitHub Personal Access Token 作为密码。创建方法：GitHub Settings → Developer settings → Personal access tokens

**Q: Pages 不显示？**  
A: 检查仓库是否为 Public，并查看 Actions 标签页是否有构建错误

**Q: 如何更新网站？**  
A: 修改文件后，执行 `git add .`, `git commit -m "message"`, `git push`

