# 在网页上显示 Google Analytics 统计数据

## 概述

要在网页上显示 Google Analytics 的统计数据，需要通过 Google Analytics Data API 获取数据。由于 API 需要认证，我们提供两种方案：

## 方案 1: 使用 Google Apps Script（推荐，无需后端）

### 优势
- ✅ 无需后端服务器
- ✅ 免费使用
- ✅ 相对简单
- ✅ 可以公开访问

### 设置步骤

#### 1. 创建 Google Apps Script 项目

1. 访问 [Google Apps Script](https://script.google.com/)
2. 点击"新建项目"
3. 将 `google-apps-script/ga-stats.gs` 中的代码复制到编辑器

#### 2. 获取 GA4 Property ID

1. 登录 [Google Analytics](https://analytics.google.com/)
2. 进入"管理" > "媒体资源设置"
3. 找到"媒体资源 ID"（格式：`123456789`，不是 Measurement ID `G-XXX`）
4. 复制 Property ID

#### 3. 配置代码

在 Apps Script 代码中：
```javascript
const PROPERTY_ID = '123456789'; // 替换为您的 Property ID
```

#### 4. 启用 Analytics Data API

1. 在 Apps Script 编辑器中，点击"服务" > "添加服务"
2. 搜索并添加"Analytics Data API"
3. 选择最新版本并添加

#### 5. 设置权限

1. 首次运行脚本时，会提示授权
2. 点击"授权访问"
3. 选择您的 Google 账户
4. 点击"允许"

#### 6. 部署为 Web App

1. 点击"部署" > "新建部署"
2. 选择类型："Web 应用"
3. 配置：
   - **说明**：GA Stats API
   - **执行身份**：我
   - **具有访问权限的用户**：任何人
4. 点击"部署"
5. **复制 Web App URL**（格式：`https://script.google.com/macros/s/...`）

#### 7. 更新前端代码

在 HTML 文件中添加代码来调用 Apps Script：

```javascript
// 替换为您的 Apps Script Web App URL
const GA_STATS_API = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';

// 获取统计数据
async function fetchGAStats() {
  try {
    // 获取所有工具的统计
    const response = await fetch(`${GA_STATS_API}?tool=all`);
    const data = await response.json();
    
    // 更新页面显示
    document.getElementById('viewsVlpim').textContent = (data.vlpim || 0).toLocaleString();
    document.getElementById('viewsCcm').textContent = (data.circular_contact_map || 0).toLocaleString();
    document.getElementById('viewsTotal').textContent = (data.total || 0).toLocaleString();
  } catch (error) {
    console.warn('Failed to fetch GA stats:', error);
    // 使用本地存储作为降级
  }
}

// 页面加载时获取统计
fetchGAStats();
```

## 方案 2: 使用 Google Analytics Data API（需要后端）

### 优势
- ✅ 更灵活
- ✅ 可以获取更多数据
- ✅ 性能更好

### 缺点
- ❌ 需要后端服务器
- ❌ 需要配置服务账户
- ❌ 相对复杂

### 设置步骤

#### 1. 创建 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目

#### 2. 启用 Analytics Data API

1. 进入"API 和服务" > "库"
2. 搜索"Google Analytics Data API"
3. 点击"启用"

#### 3. 创建服务账户

1. 进入"API 和服务" > "凭据"
2. 点击"创建凭据" > "服务账户"
3. 填写服务账户信息
4. 创建并下载 JSON 密钥文件

#### 4. 授权服务账户访问 GA

1. 登录 [Google Analytics](https://analytics.google.com/)
2. 进入"管理" > "媒体资源访问权限管理"
3. 添加服务账户邮箱（从 JSON 文件中获取）
4. 授予"查看者"权限

#### 5. 后端实现

使用 Python 示例：

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    Filter,
    FilterExpression
)
import os

# 设置环境变量
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-key.json'

def get_page_views(property_id, page_path):
    client = BetaAnalyticsDataClient()
    
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date="2020-01-01", end_date="today")],
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.EXACT,
                    value=page_path
                )
            )
        )
    )
    
    response = client.run_report(request)
    
    if response.rows:
        return int(response.rows[0].metric_values[0].value)
    return 0

# 使用示例
views = get_page_views('123456789', '/VLPIM_Web_services/')
```

## 方案 3: 使用 Google Analytics Embed API（嵌入报告）

### 说明
这个方案可以嵌入整个 Google Analytics 报告到网页，但不是显示简单的数字。

### 实现

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://apis.google.com/js/api.js"></script>
  <script src="https://accounts.google.com/gsi/client"></script>
  <script src="https://www.gstatic.com/charts/loader.js"></script>
</head>
<body>
  <div id="embed-api-auth-container"></div>
  <div id="chart-container"></div>
  
  <script>
    gapi.load('client', () => {
      gapi.client.init({
        apiKey: 'YOUR_API_KEY',
        clientId: 'YOUR_CLIENT_ID',
        discoveryDocs: ['https://analyticsreporting.googleapis.com/$discovery/rest']
      });
      
      // 授权和显示报告
      // ... 更多代码
    });
  </script>
</body>
</html>
```

## 推荐方案

**对于您的项目，推荐使用方案 1（Google Apps Script）**，因为：
- ✅ 无需后端服务器
- ✅ 免费使用
- ✅ 相对简单
- ✅ 可以快速实现

## 注意事项

1. **Property ID vs Measurement ID**
   - Property ID：`123456789`（用于 API）
   - Measurement ID：`G-XXXXXXXXXX`（用于前端追踪）

2. **数据延迟**
   - Google Analytics 数据可能有 24-48 小时延迟
   - 实时数据可能不准确

3. **API 限制**
   - Google Analytics Data API 有请求频率限制
   - 建议缓存数据，避免频繁请求

4. **安全性**
   - 不要在前端代码中暴露服务账户密钥
   - 使用 Apps Script 时，确保 Web App 设置为"任何人"可访问

## 快速开始

### 步骤 1: 设置 Google Apps Script

1. 访问 [Google Apps Script](https://script.google.com/)
2. 点击"新建项目"
3. 将 `google-apps-script/ga-stats-complete.gs` 中的代码复制到编辑器
4. Property ID 已配置完成：
   ```javascript
   const PROPERTY_IDS = {
     'vlpim': '12951176208',           // VLPIM_Web_services (G-WT1MXK5JWQ)
     'circular_contact_map': '12951253362', // Circular_Contact_Map (G-H00K0HSQWN)
     'root': '12951280669'              // Toolboxes (G-F2RPLG89BD)
   };
   ```

### 步骤 2: 已配置的 Property ID

代码中已包含以下 Property ID（数据流 ID）：
- **VLPIM_Web_services**: `12951176208` (Measurement ID: G-WT1MXK5JWQ)
- **Circular_Contact_Map**: `12951253362` (Measurement ID: G-H00K0HSQWN)
- **Toolboxes (root)**: `12951280669` (Measurement ID: G-F2RPLG89BD)

### 步骤 3: 启用 Analytics Data API

1. 在 Apps Script 编辑器中，点击"扩展功能" > "Apps Script API"
2. 如果看到"Analytics Data API"，点击添加
3. 如果没有，需要手动启用：
   - 在代码中添加服务：点击左侧"服务" > "添加服务"
   - 搜索"Analytics Data API"并添加

### 步骤 4: 授权和部署

1. 点击"运行"按钮测试代码（会提示授权）
2. 点击"授权访问"并选择您的 Google 账户
3. 点击"允许"授予权限
4. 点击"部署" > "新建部署"
5. 选择类型："Web 应用"
6. 配置：
   - **说明**：GA Stats API
   - **执行身份**：我
   - **具有访问权限的用户**：任何人
7. 点击"部署"
8. **复制 Web App URL**（格式：`https://script.google.com/macros/s/...`）

### 步骤 5: 更新前端代码

在以下文件中，将 `YOUR_SCRIPT_ID` 替换为您的 Apps Script Web App URL：

1. **`index.html`** (第 163 行)
   ```javascript
   const GA_STATS_API = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
   ```

2. **`VLPIM_Web_services/index.html`** (第 1394 行)
   ```javascript
   const GA_STATS_API = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
   ```

3. **`Circular_Contact_Map/index.html`** (第 202 行)
   ```javascript
   const GA_STATS_API = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
   ```

### 步骤 6: 测试

1. 打开网页，查看浏览器控制台
2. 如果 API 配置正确，统计数据会从 Google Analytics 获取
3. 如果 API 未配置或失败，会使用本地存储的值（降级方案）

## 工作原理

1. **页面加载时**：
   - 首先显示本地存储的统计数据（即时显示）
   - 然后异步从 Google Analytics API 获取真实数据
   - 如果 API 调用成功，更新显示为 GA 数据
   - 如果 API 调用失败，保持本地存储的值

2. **降级方案**：
   - 如果 API 未配置（仍为 `YOUR_SCRIPT_ID`），不会尝试调用
   - 如果 API 调用失败，静默失败，使用本地存储
   - 确保即使 API 不可用，页面也能正常显示统计数据

## 注意事项

1. **数据延迟**：Google Analytics 数据可能有 24-48 小时延迟
2. **API 限制**：Google Analytics Data API 有请求频率限制，建议缓存数据
3. **Property ID vs Measurement ID**：
   - Property ID：`123456789`（用于 API）
   - Measurement ID：`G-XXXXXXXXXX`（用于前端追踪）
4. **安全性**：Web App 设置为"任何人"可访问，但只返回统计数据，不暴露敏感信息

## 故障排除

### 问题 1: API 返回错误
- 检查 Property ID 是否正确
- 确认 Analytics Data API 已启用
- 检查服务账户权限

### 问题 2: 统计数据为 0
- 确认 Google Analytics 已开始收集数据
- 检查页面路径是否正确匹配
- 查看 Apps Script 执行日志

### 问题 3: CORS 错误
- 确保 Web App 部署时设置为"任何人"可访问
- 检查响应头是否包含 CORS 头

需要我帮您实现具体的代码吗？

