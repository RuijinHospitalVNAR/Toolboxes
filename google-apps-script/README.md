# Google Apps Script - GA4 Statistics API

这个文件夹包含用于从 Google Analytics 4 获取统计数据并在网页上显示的 Google Apps Script 代码。

## 文件说明

- **`ga-stats-complete.gs`**: 完整的实现代码，支持从多个 GA4 Property 获取统计数据

## 快速设置

### 1. 创建 Apps Script 项目

1. 访问 https://script.google.com/
2. 点击"新建项目"
3. 复制 `ga-stats-complete.gs` 的内容到编辑器

### 2. 配置 Property ID

代码中已配置 Property ID（数据流 ID）：

```javascript
const PROPERTY_IDS = {
  'vlpim': '12951176208',              // VLPIM_Web_services (G-WT1MXK5JWQ)
  'circular_contact_map': '12951253362', // Circular_Contact_Map (G-H00K0HSQWN)
  'root': '12951280669'                // Toolboxes (G-F2RPLG89BD)
};
```

**已配置的 Property ID**：
- VLPIM_Web_services: `12951176208` (Measurement ID: G-WT1MXK5JWQ)
- Circular_Contact_Map: `12951253362` (Measurement ID: G-H00K0HSQWN)
- Toolboxes (root): `12951280669` (Measurement ID: G-F2RPLG89BD)

### 3. 启用 Analytics Data API

1. 在 Apps Script 编辑器中，点击左侧"服务"
2. 点击"添加服务"
3. 搜索"Analytics Data API"并添加

### 4. 部署为 Web App

1. 点击"部署" > "新建部署"
2. 选择类型："Web 应用"
3. 配置：
   - **执行身份**：我
   - **具有访问权限的用户**：任何人
4. 点击"部署"
5. **复制 Web App URL**

### 5. 更新前端代码

在以下文件中替换 `YOUR_SCRIPT_ID`：

- `index.html` (第 163 行)
- `VLPIM_Web_services/index.html` (第 1394 行)
- `Circular_Contact_Map/index.html` (第 202 行)

## API 使用

### 获取所有工具的统计数据

```
GET https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec?tool=all
```

响应：
```json
{
  "vlpim": 1234,
  "circular_contact_map": 567,
  "root": 890,
  "total": 2691
}
```

### 获取特定工具的统计数据

```
GET https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec?tool=vlpim
```

响应：
```json
{
  "views": 1234
}
```

## 支持的参数

- `tool`: 工具名称
  - `all`: 返回所有工具的统计数据
  - `vlpim`: VLPIM Web Services
  - `circular_contact_map`: Circular Contact Map
  - `root`: 根目录页面

## 注意事项

1. 首次运行需要授权 Google Analytics 访问权限
2. Google Analytics 数据可能有 24-48 小时延迟
3. API 有请求频率限制，建议缓存数据
4. 确保 Web App 部署时设置为"任何人"可访问

## 故障排除

如果遇到问题，请查看：
- Apps Script 执行日志（"执行" > "查看执行记录"）
- 浏览器控制台错误信息
- `GOOGLE_ANALYTICS_DISPLAY_STATS.md` 中的详细说明

