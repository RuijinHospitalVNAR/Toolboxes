/**
 * 最简单的测试版本 - 用于验证 doGet 函数是否被识别
 * 
 * 使用步骤：
 * 1. 复制这段代码到 Google Apps Script 的 Code.gs 文件中
 * 2. 保存（Ctrl+S）
 * 3. 部署 > 新建部署 > Web 应用
 * 4. 版本选择"新版本"
 * 5. 执行身份：我
 * 6. 访问权限：任何人
 * 7. 部署后测试 URL
 */

function doGet(e) {
  // Handle case when e is undefined (e.g., when running from editor)
  if (!e) {
    e = { parameter: {} };
  }
  if (!e.parameter) {
    e.parameter = {};
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    success: true,
    message: "doGet function is working!",
    tool: e.parameter.tool || 'all',
    timestamp: new Date().toISOString()
  }))
  .setMimeType(ContentService.MimeType.JSON);
}

