# Google Analytics 设置指南

## 概述

已将所有页面的访问统计从 CountAPI 切换到 **Google Analytics 4 (GA4)**。Google Analytics 提供更稳定、更可靠的访问统计服务。

## 设置步骤

### 1. 创建 Google Analytics 账户

1. 访问 [Google Analytics](https://analytics.google.com/)
2. 使用您的 Google 账户登录
3. 点击"开始测量"（Start measuring）

### 2. 创建媒体资源（Property）

1. 在 Google Analytics 中，点击"管理"（Admin）
2. 在"媒体资源"列中，点击"创建媒体资源"（Create Property）
3. 填写信息：
   - 媒体资源名称：`Toolboxes`（或您喜欢的名称）
   - 报告时区：选择您的时区
   - 货币：选择您的货币
4. 点击"下一步"

### 3. 配置业务信息（可选）

1. 选择业务规模和类别
2. 点击"创建"

### 4. 获取 Measurement ID

1. 创建媒体资源后，系统会显示"数据流"（Data Streams）页面
2. 点击"添加数据流" > "网站"（Web）
3. 填写网站信息：
   - 网站 URL：例如 `https://ruijinhospitalvnar.github.io`
   - 流名称：例如 `Toolboxes Website`
4. 点击"创建流"
5. **复制 Measurement ID**（格式：`G-XXXXXXXXXX`）

### 5. 更新代码中的 Measurement ID

在所有 HTML 文件中，将 `G-XXXXXXXXXX` 替换为您实际的 Measurement ID：

#### 需要更新的文件：

1. **`VLPIM_Web_services/index.html`** (第 24 和 30 行)
2. **`Circular_Contact_Map/index.html`** (第 28 和 34 行)
3. **`index.html`** (第 10 和 16 行)

查找并替换：
```javascript
// 将这行
gtag('config', 'G-XXXXXXXXXX');

// 替换为您的实际 ID
gtag('config', 'G-您的实际ID');
```

例如：
```javascript
gtag('config', 'G-ABC123XYZ789');
```

## 验证安装

### 方法 1: Google Analytics 实时报告

1. 登录 Google Analytics
2. 进入"报告" > "实时"（Reports > Realtime）
3. 访问您的网站
4. 在实时报告中应该能看到您的访问

### 方法 2: 浏览器开发者工具

1. 打开浏览器开发者工具（F12）
2. 切换到"网络"（Network）标签
3. 刷新页面
4. 查找 `collect` 请求（应该发送到 `google-analytics.com`）
5. 如果看到这个请求，说明跟踪代码正常工作

### 方法 3: Google Tag Assistant

1. 安装 [Google Tag Assistant](https://chrome.google.com/webstore/detail/tag-assistant-legacy-by-g/kejbdjndbnbjgmefkgdddjlbokphdefk) 浏览器扩展
2. 访问您的网站
3. 点击扩展图标，查看跟踪状态

## 功能说明

### 页面访问追踪

- ✅ **自动追踪**：Google Analytics 自动追踪页面访问
- ✅ **会话管理**：自动识别新会话和重复访问
- ✅ **详细报告**：在 GA Dashboard 中查看详细统计

### 本地存储（显示用）

- 页面上的访问数显示使用本地存储（localStorage）
- 作为简单的显示计数器
- 不影响 Google Analytics 的追踪

### 数据查看

访问统计数据在 Google Analytics Dashboard 中查看：
- **实时报告**：当前在线的用户
- **概览报告**：访问量、用户数、会话数等
- **页面报告**：各个页面的访问统计
- **地理位置**：用户来源地区
- **设备信息**：用户使用的设备类型

## 优势

### 相比 CountAPI

- ✅ **更稳定**：Google 服务，全球可用
- ✅ **更可靠**：不会出现连接失败问题
- ✅ **更详细**：提供丰富的分析报告
- ✅ **更专业**：行业标准分析工具

### 功能特性

- 📊 **实时统计**：实时查看访问情况
- 📈 **历史数据**：保存历史访问记录
- 🌍 **地理位置**：查看用户来源地区
- 📱 **设备分析**：分析用户使用的设备
- 🔍 **用户行为**：追踪用户行为路径
- 📉 **趋势分析**：查看访问趋势变化

## 注意事项

1. **Measurement ID 格式**：确保使用正确的格式（`G-` 开头，后面是字母数字组合）
2. **所有页面**：确保所有 HTML 文件都更新了 Measurement ID
3. **数据延迟**：Google Analytics 数据可能有 24-48 小时的延迟
4. **实时数据**：实时报告可以立即看到访问，但详细报告可能需要一些时间

## 隐私政策

使用 Google Analytics 需要：
- 在网站中添加隐私政策说明
- 告知用户使用了 Google Analytics
- 遵守 GDPR 等隐私法规（如果适用）

## 常见问题

### Q: 如何查看访问统计？

A: 登录 Google Analytics，在 Dashboard 中查看各种报告。

### Q: 数据更新频率？

A: 实时报告可以立即看到，标准报告可能需要 24-48 小时。

### Q: 需要后端服务器吗？

A: 不需要。Google Analytics 完全通过前端 JavaScript 追踪。

### Q: 可以追踪多个网站吗？

A: 可以。可以在同一个 GA 账户中创建多个媒体资源。

### Q: 如何停止追踪？

A: 删除或注释掉 Google Analytics 代码即可。

## 总结

Google Analytics 提供了专业、稳定的访问统计服务，比 CountAPI 更适合生产环境使用。配置完成后，您就可以在 Google Analytics Dashboard 中查看详细的访问统计报告。

