# CountAPI 页面访问统计配置

## 概述

使用 **CountAPI** 实现全局页面访问统计，**无需创建后端服务器**，直接在前端调用即可。

## CountAPI 简介

CountAPI 是一个免费的计数器服务，提供简单的 RESTful API：
- ✅ **完全免费**，无需注册
- ✅ **无需后端**，直接在前端调用
- ✅ **数据持久化**，存储在 CountAPI 服务器
- ✅ **全局统计**，所有用户访问都会被统计

## API 端点

### 1. 增加计数（Hit）
```
GET https://api.countapi.xyz/hit/{namespace}/{key}
```
- 每次调用计数器 +1
- 自动创建计数器（如果不存在）

### 2. 获取计数（Get）
```
GET https://api.countapi.xyz/get/{namespace}/{key}
```
- 返回当前计数值
- 响应格式：`{"value": 123}`

## 配置说明

### 命名空间（Namespace）
- **Namespace**: `toolboxes`
- 用于组织多个计数器

### 计数器键名（Keys）
- `vlpim` - VLPIM Web Services 访问统计
- `circular_contact_map` - Circular Contact Map 访问统计

## 代码实现

### VLPIM Web Services

```javascript
// 记录访问
await fetch(`https://api.countapi.xyz/hit/toolboxes/vlpim`);

// 获取统计
const response = await fetch(`https://api.countapi.xyz/get/toolboxes/vlpim`);
const data = await response.json();
const views = data.value || 0;
```

### Circular Contact Map

```javascript
// 记录访问
await fetch(`https://api.countapi.xyz/hit/toolboxes/circular_contact_map`);

// 获取统计
const response = await fetch(`https://api.countapi.xyz/get/toolboxes/circular_contact_map`);
const data = await response.json();
const views = data.value || 0;
```

### 根目录聚合

```javascript
// 同时获取两个工具的统计
const [vlpimResponse, ccmResponse] = await Promise.all([
    fetch(`https://api.countapi.xyz/get/toolboxes/vlpim`),
    fetch(`https://api.countapi.xyz/get/toolboxes/circular_contact_map`)
]);

const vlpimData = await vlpimResponse.json();
const ccmData = await ccmResponse.json();
const total = (vlpimData.value || 0) + (ccmData.value || 0);
```

## 防重复计数机制

代码中已实现防重复计数：
- 使用 `sessionStorage` 存储会话 ID
- 每个会话只计数一次（刷新页面不重复计数）
- 新标签页或新访问会重新计数

## 自动降级机制

如果 CountAPI 不可用，代码会自动降级到 `localStorage`：
- API 失败时使用本地存储
- 保证功能可用性
- 控制台会显示警告信息

## 测试

### 1. 测试 API 端点

在浏览器控制台或使用 curl：

```bash
# 测试增加计数
curl https://api.countapi.xyz/hit/toolboxes/vlpim

# 测试获取计数
curl https://api.countapi.xyz/get/toolboxes/vlpim
```

### 2. 测试前端集成

1. 打开浏览器开发者工具（F12）
2. 访问页面
3. 查看 Network 标签，确认 API 请求成功
4. 检查 Console 是否有错误

## 优势

### 相比自建后端
- ✅ **零配置**：无需服务器、数据库
- ✅ **零维护**：无需维护后端代码
- ✅ **零成本**：完全免费
- ✅ **快速部署**：代码更新即可使用

### 相比 Cloudflare Workers
- ✅ **更简单**：无需创建账户和配置
- ✅ **更快速**：无需部署步骤
- ✅ **更直接**：代码中直接使用

## 注意事项

1. **计数器创建**：首次访问时 CountAPI 会自动创建计数器
2. **命名空间**：使用 `toolboxes` 作为命名空间，便于管理
3. **键名规范**：使用小写字母和下划线（如 `circular_contact_map`）
4. **API 限制**：CountAPI 可能有请求频率限制，但通常足够使用

## 自定义命名空间

如果需要使用自定义命名空间，修改代码中的 `namespace` 变量：

```javascript
// 将 'toolboxes' 改为您的命名空间
const namespace = 'your-namespace';
```

**建议命名空间格式**：
- 使用小写字母
- 可以使用连字符或下划线
- 保持唯一性（避免冲突）

## 故障排除

### 问题 1: API 请求失败

**可能原因**：
- 网络连接问题
- CountAPI 服务暂时不可用

**解决方案**：
- 代码已实现自动降级到 localStorage
- 检查浏览器控制台错误信息

### 问题 2: 计数不准确

**可能原因**：
- 同一会话多次刷新被计数

**解决方案**：
- 代码已实现会话管理，同一会话只计数一次
- 检查 `sessionStorage` 是否正常工作

### 问题 3: CORS 错误

**可能原因**：
- CountAPI 应支持 CORS，但可能有限制

**解决方案**：
- CountAPI 通常支持 CORS
- 如有问题，检查浏览器控制台错误

## API 响应格式

### 成功响应（Get）
```json
{
  "value": 123,
  "status": 200
}
```

### 成功响应（Hit）
```json
{
  "value": 124,
  "status": 200
}
```

## 免费额度

CountAPI 是免费服务，但可能有以下限制：
- 请求频率限制（通常足够使用）
- 无 SLA 保证（依赖服务可用性）

## 总结

CountAPI 是实现全局页面访问统计的**最简单方案**：
- ✅ 无需后端开发
- ✅ 无需服务器部署
- ✅ 无需配置数据库
- ✅ 直接在前端使用
- ✅ 完全免费

代码已更新，**可以直接使用**！

