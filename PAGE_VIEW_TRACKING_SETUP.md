# 页面访问统计配置指南

## 概述

本指南将帮助您将页面访问统计从**本地浏览器统计**改为**统计所有用户的数据**。

## 方案对比

### 方案 1: Cloudflare Workers + KV（推荐）

**优点**:
- ✅ 完全免费（每日 100,000 次请求）
- ✅ 数据完全控制
- ✅ 无需数据库
- ✅ 快速部署

**缺点**:
- ⚠️ 需要 Cloudflare 账户
- ⚠️ 需要配置 KV 存储

### 方案 2: 第三方统计服务（最简单）

**优点**:
- ✅ 无需后端开发
- ✅ 专业统计功能
- ✅ 图表和可视化

**缺点**:
- ⚠️ 可能需要付费（部分服务有免费版）
- ⚠️ 数据在第三方服务

---

## 方案 1: Cloudflare Workers 部署步骤

### 步骤 1: 创建 Cloudflare 账户

1. 访问 https://dash.cloudflare.com/
2. 注册或登录账户（免费）

### 步骤 2: 创建 KV Namespace

1. 在 Dashboard 中，进入 **Workers & Pages**
2. 点击 **KV** 标签
3. 点击 **Create a namespace**
4. 名称：`PAGE_STATS`
5. 复制 **Namespace ID**（格式：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

### 步骤 3: 创建 Worker

1. 在 **Workers & Pages** 中，点击 **Create application** > **Create Worker**
2. 名称：`vlpim-page-stats`
3. 点击 **Deploy**

### 步骤 4: 配置 KV Binding

1. 在 Worker 页面，点击 **Settings** > **Variables**
2. 在 **KV Namespace Bindings** 部分，点击 **Add binding**
3. Variable name: `PAGE_STATS`
4. KV namespace: 选择 `PAGE_STATS`
5. 点击 **Save**

### 步骤 5: 部署代码

#### 方法 A: 使用 Dashboard（简单）

1. 在 Worker 页面，点击 **Quick edit**
2. 复制 `workers/page-stats.js` 的内容
3. 粘贴到编辑器，替换默认代码
4. 点击 **Save and deploy**

#### 方法 B: 使用 Wrangler CLI（推荐）

```bash
# 1. 安装 Wrangler
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 创建 KV namespace（如果还没有）
wrangler kv:namespace create "PAGE_STATS"
# 输出类似：{ binding = "PAGE_STATS", id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" }

# 4. 编辑 wrangler.toml，填入 KV namespace ID
# 将 YOUR_KV_NAMESPACE_ID 替换为上面输出的 id

# 5. 部署
cd workers
wrangler publish
```

### 步骤 6: 获取 Worker URL

部署后，Cloudflare 会提供 URL，格式如：
```
https://vlpim-page-stats.YOUR_SUBDOMAIN.workers.dev
```

### 步骤 7: 更新前端代码

在以下文件中，将 `YOUR_SUBDOMAIN.workers.dev` 替换为您的实际 Worker URL：

1. `VLPIM_Web_services/index.html` (第 1378 行)
2. `Circular_Contact_Map/index.html` (第 188 行)
3. `index.html` (第 153 行)

**示例**:
```javascript
// 替换前
const API_ENDPOINT = 'https://vlpim-page-stats.YOUR_SUBDOMAIN.workers.dev';

// 替换后（使用您的实际 URL）
const API_ENDPOINT = 'https://vlpim-page-stats.abc123.workers.dev';
```

---

## 方案 2: 使用 Plausible Analytics（最简单）

### 步骤 1: 注册 Plausible 账户

1. 访问 https://plausible.io/
2. 注册账户（免费试用 30 天，之后 $9/月）

### 步骤 2: 添加网站

1. 在 Dashboard 中，点击 **Add website**
2. 域名填写：`ruijinhospitalvnar.github.io`
3. 复制提供的脚本代码

### 步骤 3: 在前端代码中添加脚本

在 `index.html` 的 `<head>` 部分添加：

```html
<script defer data-domain="ruijinhospitalvnar.github.io" 
        src="https://plausible.io/js/script.js"></script>
```

### 步骤 4: 显示统计数据

Plausible 会在 Dashboard 中显示详细统计，包括：
- 页面访问量
- 独立访客
- 访问来源
- 地理位置等

**注意**: Plausible 不提供公开的 API 来显示访问数量，需要在 Dashboard 查看。

---

## 方案 3: 使用 Google Analytics（免费）

### 步骤 1: 创建 Google Analytics 账户

1. 访问 https://analytics.google.com/
2. 创建账户和属性（免费）

### 步骤 2: 获取跟踪 ID

1. 在属性设置中，找到 **Measurement ID**（格式：`G-XXXXXXXXXX`）

### 步骤 3: 在前端代码中添加脚本

在 `index.html` 的 `<head>` 部分添加：

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### 步骤 4: 显示统计数据

使用 Google Analytics API 获取统计数据并在页面显示。

---

## API 使用说明

### 记录访问（POST）

```javascript
POST https://your-worker.workers.dev/track
Content-Type: application/json

{
  "tool": "vlpim",
  "sessionId": "unique-session-id-12345"
}
```

### 获取统计（GET）

```javascript
// 获取所有工具的统计
GET https://your-worker.workers.dev/stats

// 响应:
{
  "vlpim": 1234,
  "ccm": 567,
  "total": 1801
}

// 获取特定工具的统计
GET https://your-worker.workers.dev/stats?tool=vlpim

// 响应:
{
  "tool": "vlpim",
  "views": 1234
}
```

---

## 测试

### 1. 测试 API 端点

```bash
# 测试记录访问
curl -X POST https://your-worker.workers.dev/track \
  -H "Content-Type: application/json" \
  -d '{"tool":"vlpim","sessionId":"test123"}'

# 测试获取统计
curl https://your-worker.workers.dev/stats
```

### 2. 测试前端集成

1. 打开浏览器开发者工具（F12）
2. 访问页面
3. 查看 Network 标签，确认 API 请求成功
4. 检查 Console 是否有错误

---

## 故障排除

### 问题 1: CORS 错误

**解决方案**: 确保 Worker 代码中设置了正确的 CORS 头：
```javascript
'Access-Control-Allow-Origin': '*'
```

### 问题 2: KV 绑定失败

**解决方案**: 
1. 检查 KV namespace 是否创建
2. 检查 Worker 设置中的 KV binding 是否正确配置
3. 确保 binding 名称与代码中的变量名一致

### 问题 3: API 请求失败

**解决方案**:
- 检查 Worker URL 是否正确
- 检查网络连接
- 查看浏览器控制台错误信息
- 代码会自动降级到 localStorage（如果 API 失败）

---

## 免费额度

### Cloudflare Workers
- ✅ 每天 100,000 次请求（免费）
- ✅ KV Storage: 每天 100,000 次读取，1,000 次写入（免费）
- ✅ 完全免费，无需信用卡

### Plausible Analytics
- ⚠️ 免费试用 30 天
- ⚠️ 之后 $9/月（或自托管）

### Google Analytics
- ✅ 完全免费
- ✅ 无限制使用

---

## 推荐方案

**如果您的访问量不大（< 100,000/天）**:
- 推荐使用 **Cloudflare Workers**（方案 1）
- 完全免费，数据控制

**如果您需要详细的统计和分析**:
- 推荐使用 **Google Analytics**（方案 3）
- 免费，功能强大

**如果您需要隐私友好的统计**:
- 推荐使用 **Plausible Analytics**（方案 2）
- 符合 GDPR，无 Cookie

---

## 下一步

1. 选择一个方案
2. 按照步骤部署
3. 更新前端代码中的 API 端点
4. 测试功能
5. 提交代码到 GitHub

---

## 技术支持

如有问题，请：
1. 查看 Cloudflare Workers 文档：https://developers.cloudflare.com/workers/
2. 查看 Plausible 文档：https://plausible.io/docs
3. 查看 Google Analytics 文档：https://developers.google.com/analytics

