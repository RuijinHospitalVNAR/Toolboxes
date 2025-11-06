# CountAPI 连接问题解决方案

## 问题说明

如果遇到 `ERR_TUNNEL_CONNECTION_FAILED` 或类似的网络连接错误，说明您的网络环境无法访问 CountAPI 服务。这通常是由于：

1. **防火墙限制**：阻止了对 `api.countapi.xyz` 的访问
2. **网络代理**：代理配置导致连接失败
3. **地区限制**：某些网络环境可能限制访问外部 API

## 智能禁用机制

代码已实现**智能禁用机制**：

### 工作原理

1. **首次访问**：尝试连接 CountAPI
2. **连接失败**：自动禁用 CountAPI，切换到本地存储
3. **后续访问**：跳过 CountAPI 请求，直接使用本地存储
4. **网络恢复**：如果网络恢复，会重新尝试并自动启用

### 禁用状态存储

当 API 连接失败时，会在 `localStorage` 中设置标记：
- `vlpim_api_disabled = 'true'` - VLPIM 的 API 已禁用
- `circular_contact_map_api_disabled = 'true'` - Circular Contact Map 的 API 已禁用

### 自动恢复

如果网络恢复，代码会在后台自动重试：
- 成功连接后，自动清除禁用标记
- 恢复使用 CountAPI 进行全局统计

## 手动重新启用 API

如果需要手动重新启用 API（例如网络问题已解决），可以在浏览器控制台执行：

```javascript
// 清除禁用标记，重新启用 API
localStorage.removeItem('vlpim_api_disabled');
localStorage.removeItem('circular_contact_map_api_disabled');

// 刷新页面
location.reload();
```

## 当前行为

### API 可用时
- ✅ 使用 CountAPI 进行全局统计
- ✅ 所有用户的访问都会被统计
- ✅ 数据持久化存储在 CountAPI 服务器

### API 不可用时（自动切换）
- ✅ 自动禁用 CountAPI 请求
- ✅ 使用本地存储进行统计
- ✅ 不会显示错误信息
- ✅ 页面正常使用

## 统计方式说明

### 本地存储模式（API 禁用时）
- 仅统计当前浏览器/设备的访问
- 数据存储在浏览器本地
- 清除浏览器数据会重置计数
- 不同设备/浏览器数据不共享

### CountAPI 模式（API 可用时）
- 统计所有用户的访问
- 数据存储在 CountAPI 服务器
- 跨设备、跨浏览器共享
- 全局统一的访问统计

## 网络诊断

### 检查 CountAPI 是否可访问

在浏览器控制台执行：

```javascript
fetch('https://api.countapi.xyz/get/toolboxes/vlpim')
  .then(r => r.json())
  .then(data => console.log('CountAPI 可用:', data))
  .catch(err => console.log('CountAPI 不可用:', err));
```

### 如果返回错误

- **ERR_TUNNEL_CONNECTION_FAILED**：网络/代理问题
- **ERR_CONNECTION_REFUSED**：防火墙阻止
- **ERR_NAME_NOT_RESOLVED**：DNS 解析失败

## 解决方案

### 方案 1: 使用本地存储（当前默认）

如果网络环境无法访问 CountAPI，代码会自动切换到本地存储模式，无需任何操作。

### 方案 2: 配置网络代理

如果您的网络环境需要通过代理访问外网：

1. 检查浏览器代理设置
2. 配置系统代理（如果需要）
3. 确保代理允许访问 `api.countapi.xyz`

### 方案 3: 使用 VPN

如果网络环境限制访问，可以使用 VPN 服务。

### 方案 4: 清除禁用标记

如果网络问题已解决，手动清除禁用标记：

```javascript
localStorage.removeItem('vlpim_api_disabled');
localStorage.removeItem('circular_contact_map_api_disabled');
location.reload();
```

## 总结

**当前实现**：
- ✅ 自动检测网络可用性
- ✅ 失败时自动禁用，避免重复错误
- ✅ 静默降级到本地存储
- ✅ 网络恢复时自动重试

**用户体验**：
- ✅ 不会看到错误信息
- ✅ 页面正常使用
- ✅ 统计功能仍然工作（本地模式）

即使网络环境限制访问 CountAPI，页面也能正常工作，只是统计范围变为本地浏览器。

