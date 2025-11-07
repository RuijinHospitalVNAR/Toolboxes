# JSONP 加载失败故障排除指南

## 问题：Script.onerror - Failed to fetch GA stats from API

如果看到这个错误，请按照以下步骤排查：

## 步骤 1: 检查 Google Apps Script 部署

### 1.1 验证 Web App 是否可访问

在浏览器中直接访问以下 URL（替换 `YOUR_CALLBACK` 为任意名称）：

```
https://script.google.com/macros/s/AKfycbzQ6qwA0NqrIYUgnwJnvep2QB2nRYmU6LI8KB8wwtp3QKi6ORqscPjF3Vv2VQ-6SPi6/exec?tool=vlpim&callback=test
```

**预期结果**：
- 应该返回：`test({"views":0});`
- 或者返回 JSON：`{"views":0}`

**如果返回 404 或错误**：
- Web App 可能未正确部署
- URL 可能已更改
- 需要重新部署

### 1.2 检查部署设置

1. 打开 [Google Apps Script](https://script.google.com/)
2. 找到您的项目
3. 点击"部署" > "管理部署"
4. 检查部署设置：
   - **执行身份**：必须是"我"
   - **具有访问权限的用户**：必须是"任何人"（包括匿名用户）
   - **版本**：确保使用"新版本"或"最新版本"

### 1.3 重新部署

如果设置不正确：

1. 点击"编辑"（铅笔图标）
2. 修改设置：
   - 执行身份：我
   - 访问权限：任何人
   - 版本：新版本
3. 点击"部署"
4. **复制新的 Web App URL**
5. 更新前端代码中的 URL

## 步骤 2: 检查浏览器控制台

打开浏览器开发者工具（F12），查看控制台输出：

### 2.1 查看调试日志

应该看到类似以下日志：
```
Loading GA stats from: https://script.google.com/macros/s/.../exec?tool=vlpim&callback=gaStatsCallback_...
```

### 2.2 查看错误详情

如果看到错误，检查：
- **错误类型**：网络错误、404、500 等
- **URL**：确认 URL 是否正确
- **错误消息**：查看具体错误信息

## 步骤 3: 测试 JSONP 回调

### 3.1 手动测试

在浏览器控制台中运行：

```javascript
// 测试回调函数
window.testCallback = function(data) {
    console.log('Received data:', data);
};

// 创建脚本标签
const script = document.createElement('script');
script.src = 'https://script.google.com/macros/s/AKfycbzQ6qwA0NqrIYUgnwJnvep2QB2nRYmU6LI8KB8wwtp3QKi6ORqscPjF3Vv2VQ-6SPi6/exec?tool=vlpim&callback=testCallback';
script.onload = () => console.log('Script loaded');
script.onerror = (e) => console.error('Script error:', e);
document.head.appendChild(script);
```

**预期结果**：
- 应该看到 "Script loaded"
- 应该看到 "Received data: {views: 0}"

**如果失败**：
- 检查网络连接
- 检查 URL 是否正确
- 检查 Google Apps Script 是否可访问

## 步骤 4: 检查 Google Apps Script 代码

### 4.1 验证 doGet 函数

确保 `Code.gs` 文件中有 `doGet` 函数，并且：

1. 函数名称正确：`doGet`（大小写敏感）
2. 函数接受参数：`function doGet(e)`
3. 处理 callback 参数：`const callback = e.parameter.callback;`
4. 返回 JSONP 格式：`callback + '(' + jsonData + ');'`

### 4.2 检查执行日志

1. 在 Google Apps Script 编辑器中
2. 点击"执行" > "查看执行记录"
3. 查看最近的执行记录
4. 检查是否有错误

## 步骤 5: 常见问题和解决方案

### 问题 1: 404 错误

**原因**：
- Web App URL 不正确
- Web App 未部署
- 部署版本问题

**解决方案**：
- 重新部署 Web App
- 使用最新的部署 URL
- 确保选择"新版本"

### 问题 2: 网络错误

**原因**：
- 网络连接问题
- 防火墙阻止
- Google Apps Script 服务不可用

**解决方案**：
- 检查网络连接
- 尝试使用 VPN
- 稍后重试

### 问题 3: 回调函数未执行

**原因**：
- JSONP 格式不正确
- 回调函数名称不匹配
- 脚本加载但回调未调用

**解决方案**：
- 检查 Google Apps Script 返回的格式
- 确保回调函数名称正确
- 检查脚本是否成功加载

### 问题 4: CORS 错误

**原因**：
- 虽然使用 JSONP，但某些情况下仍可能出现 CORS 问题

**解决方案**：
- JSONP 应该绕过 CORS
- 如果仍有问题，检查部署设置
- 确保访问权限设置为"任何人"

## 步骤 6: 临时解决方案

如果 JSONP 仍然无法工作，可以考虑：

### 6.1 使用代理服务器

通过自己的服务器代理请求，避免 CORS 问题。

### 6.2 使用服务器端获取

在服务器端获取 Google Analytics 数据，然后通过 API 提供给前端。

### 6.3 降级到本地存储

暂时使用本地存储显示统计数据，等待问题解决。

## 调试技巧

1. **启用详细日志**：代码中已添加 `console.log`，查看浏览器控制台
2. **测试 URL**：直接在浏览器中访问 URL，查看返回内容
3. **检查网络**：在开发者工具的 Network 标签中查看请求详情
4. **逐步测试**：先测试简单的 JSONP 请求，再测试完整功能

## 需要帮助？

如果以上步骤都无法解决问题，请提供：
1. 浏览器控制台的完整错误信息
2. Network 标签中的请求详情
3. Google Apps Script 的执行日志
4. 测试 URL 的返回结果

