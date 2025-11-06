# 修复 "Script function not found: doGet" 错误

## 问题诊断

如果访问 URL 仍然显示 "Script function not found: doGet"，请按照以下步骤逐一检查：

## 步骤 1: 使用最简单的测试代码

### 1.1 复制测试代码

复制以下**最简单的代码**到 Google Apps Script：

```javascript
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    success: true,
    message: "doGet function is working!",
    tool: e.parameter.tool || 'all'
  }))
  .setMimeType(ContentService.MimeType.JSON);
}
```

### 1.2 在 Google Apps Script 中操作

1. **打开 Google Apps Script**：https://script.google.com/
2. **找到您的项目**（包含部署 ID `AKfycbzQ6qwA0NqrIYUgnwJnvep2QB2nRYmU6LI8KB8wwtp3QKi6ORqscPjF3Vv2VQ-6SPi6` 的项目）
3. **检查文件列表**：
   - 左侧应该有一个文件（通常是 `Code.gs`）
   - 如果文件名不是 `Code.gs`，**重命名为 `Code.gs`**
4. **删除所有现有代码**，粘贴上面的测试代码
5. **保存**（Ctrl+S 或 Cmd+S）
6. **检查是否有错误**：
   - 代码中不应该有红色下划线
   - 如果有错误，修复后再保存

## 步骤 2: 重新部署（关键步骤）

### 2.1 删除旧部署（推荐）

1. 点击 **"部署"** > **"管理部署"**
2. 找到现有的部署
3. 点击右侧的 **"删除"**（垃圾桶图标）
4. 确认删除

### 2.2 创建新部署

1. 点击 **"部署"** > **"新建部署"**
2. 点击 **"选择类型"** 旁边的齿轮图标
3. 选择 **"Web 应用"**
4. 配置设置：
   - **说明**：GA Stats API（可选）
   - **执行身份**：**我**（重要！）
   - **具有访问权限的用户**：**任何人**（重要！）
5. **不要点击"部署"**，先继续下一步

### 2.3 选择版本（非常重要！）

1. 在部署对话框中，找到 **"版本"** 下拉菜单
2. **必须选择 "新版本"**（不要选择 "Head"）
3. 点击 **"部署"**
4. **复制新的 Web App URL**（格式：`https://script.google.com/macros/s/.../exec`）

## 步骤 3: 测试

### 3.1 测试基本功能

访问新的 Web App URL（不带参数）：
```
https://script.google.com/macros/s/YOUR_NEW_DEPLOYMENT_ID/exec
```

应该返回：
```json
{
  "success": true,
  "message": "doGet function is working!",
  "tool": "all"
}
```

### 3.2 测试带参数

访问：
```
https://script.google.com/macros/s/YOUR_NEW_DEPLOYMENT_ID/exec?tool=vlpim
```

应该返回：
```json
{
  "success": true,
  "message": "doGet function is working!",
  "tool": "vlpim"
}
```

## 步骤 4: 如果测试成功，替换为完整代码

如果测试代码工作正常，说明 `doGet` 函数可以被识别。然后：

1. 将测试代码替换为 `ga-stats-complete.gs` 中的完整代码
2. 保存
3. 再次部署（选择"新版本"）
4. 测试完整功能

## 常见错误和解决方案

### 错误 1: 文件名称不是 Code.gs

**症状**：代码在其他文件中（如 `ga-stats-complete.gs`）

**解决**：
- 重命名文件为 `Code.gs`
- 或者删除旧文件，创建新文件 `Code.gs`

### 错误 2: 部署时选择了 "Head" 而不是 "新版本"

**症状**：代码已保存，但部署后仍然找不到函数

**解决**：
- 删除旧部署
- 创建新部署
- **必须选择 "新版本"**

### 错误 3: 代码中有语法错误

**症状**：代码有红色下划线

**解决**：
- 修复所有语法错误
- 确保代码可以保存
- 点击"运行"测试代码

### 错误 4: 使用了错误的部署 URL

**症状**：使用了旧的部署 URL

**解决**：
- 每次部署后，都会生成新的 URL
- 使用最新的部署 URL
- 更新前端代码中的 URL

## 验证清单

在部署前，请确认：

- [ ] 代码在 `Code.gs` 文件中
- [ ] 代码已保存（没有未保存的更改）
- [ ] 代码中没有语法错误（没有红色下划线）
- [ ] 函数名称是 `doGet`（大小写正确）
- [ ] 部署时选择了 **"新版本"**（不是 "Head"）
- [ ] 执行身份设置为 **"我"**
- [ ] 访问权限设置为 **"任何人"**

## 如果仍然无法解决

1. **创建全新的项目**：
   - 在 Google Apps Script 中创建新项目
   - 复制代码到新项目
   - 重新部署

2. **检查项目设置**：
   - 确保项目没有被禁用
   - 检查是否有配额限制

3. **联系支持**：
   - 如果以上步骤都无法解决，可能是 Google Apps Script 的问题
   - 可以尝试等待一段时间后重试

