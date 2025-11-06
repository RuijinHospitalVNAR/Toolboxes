# 测试 JSONP 连接

## 问题诊断

如果看到 "Failed to fetch GA stats from API" 错误，请按照以下步骤测试：

## 步骤 1: 直接在浏览器中测试 URL

在浏览器地址栏中访问以下 URL（替换 `testCallback` 为任意名称）：

```
https://script.google.com/macros/s/AKfycbxars-R7f73vTaMMGwXpuatiS9tKJpjlTSDcQpL6fp85Rovl1Nd_0ql1yocvILmwnc/exec?tool=vlpim&callback=testCallback
```

**预期结果**：
- 应该显示：`testCallback({"views":0});`
- 或者显示 JSON：`{"views":0}`

**如果显示错误或 HTML 页面**：
- Web App 可能未正确部署
- 需要检查部署设置

## 步骤 2: 在浏览器控制台中测试

打开浏览器开发者工具（F12），在控制台中运行：

```javascript
// 定义测试回调函数
window.testCallback = function(data) {
    console.log('✅ Success! Received data:', data);
};

// 创建脚本标签
const script = document.createElement('script');
script.src = 'https://script.google.com/macros/s/AKfycbxars-R7f73vTaMMGwXpuatiS9tKJpjlTSDcQpL6fp85Rovl1Nd_0ql1yocvILmwnc/exec?tool=vlpim&callback=testCallback';
script.onload = () => {
    console.log('✅ Script loaded successfully');
};
script.onerror = (e) => {
    console.error('❌ Script failed to load:', e);
};
document.head.appendChild(script);
```

**预期结果**：
- 应该看到 "✅ Script loaded successfully"
- 应该看到 "✅ Success! Received data: {views: 0}"

**如果看到错误**：
- 检查网络连接
- 检查 URL 是否正确
- 检查 Google Apps Script 是否可访问

## 步骤 3: 检查 Google Apps Script 部署

1. 打开 [Google Apps Script](https://script.google.com/)
2. 找到您的项目
3. 点击"部署" > "管理部署"
4. 检查：
   - **执行身份**：我
   - **具有访问权限的用户**：任何人（包括匿名用户）
   - **版本**：新版本

## 步骤 4: 检查 Google Apps Script 执行日志

1. 在 Google Apps Script 编辑器中
2. 点击"执行" > "查看执行记录"
3. 查看最近的执行记录
4. 检查是否有错误

## 步骤 5: 验证代码

确保 `Code.gs` 文件中有以下代码：

```javascript
function doGet(e) {
  const tool = e.parameter.tool || 'all';
  const callback = e.parameter.callback;
  
  let result = { views: 0 };
  if (tool === 'all') {
    result = {
      vlpim: 0,
      circular_contact_map: 0,
      root: 0,
      total: 0
    };
  }
  
  const jsonData = JSON.stringify(result);
  
  if (callback) {
    const safeCallback = callback.replace(/[^a-zA-Z0-9_$]/g, '');
    return ContentService.createTextOutput(safeCallback + '(' + jsonData + ');')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  } else {
    return ContentService.createTextOutput(jsonData)
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

## 常见问题

### 问题 1: 返回 HTML 错误页面

**原因**：Web App 未正确部署或访问权限设置错误

**解决方案**：
- 重新部署 Web App
- 确保访问权限设置为"任何人"

### 问题 2: 返回 404 错误

**原因**：URL 不正确或 Web App 未部署

**解决方案**：
- 检查 URL 是否正确
- 重新部署 Web App
- 使用最新的部署 URL

### 问题 3: 脚本加载但回调未执行

**原因**：返回的内容不是有效的 JavaScript

**解决方案**：
- 检查 Google Apps Script 返回的内容
- 确保返回格式为：`callbackName(data);`
- 检查 Content-Type 是否为 `application/javascript`

### 问题 4: 网络错误

**原因**：网络连接问题或防火墙阻止

**解决方案**：
- 检查网络连接
- 尝试使用 VPN
- 检查防火墙设置

## 如果仍然无法解决

请提供以下信息：
1. 直接访问 URL 的返回内容
2. 浏览器控制台的完整错误信息
3. Google Apps Script 的执行日志
4. Network 标签中的请求详情

