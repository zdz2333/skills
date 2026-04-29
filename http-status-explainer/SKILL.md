---
name: http-status-explainer
description: HTTP 状态码和响应头解释器 — 把 404、500、403、301 这些天书翻译成人话。当用户发来 HTTP 状态码并问"这是什么意思"、"为什么返回 502"、"301 和 302 有什么区别"、"这个响应头是什么"、"CORS 是什么"、"retry-after 是什么意思"时触发。还能用 curl 实际测试任意 URL 的状态码和响应头。
trigger: 当用户问"404 是什么意思"、"500 是什么错"、"403 是什么"、"301 和 302 区别"、"响应头什么意思"、"header 怎么读"、"CORS 是什么意思"、"502 怎么修"、"what does this status code mean"、"HTTP status"、"这个网站返回什么状态码"
---

# HTTP Status Explainer - HTTP 状态码翻译器

> `404` → "找不到这个资源"
> `502` → "上游服务器宕了"
> `301` → "永久搬家，下次别来了"
> `302` → "临时搬家，下次还来"

## 🎯 解决什么问题

HTTP 状态码是 3 位数字的天书：
```
┌───┬─────────────┐
│ 4 │ 04          │
│   │             │
├───┴─────────────┤
│      3位数字     │
│   第一位=类别   │
└─────────────────┘
```

## 💡 第一位 = 类别（最重要）

| 第一位 | 类别 | 含义 | 例子 |
|--------|------|------|------|
| `1xx` | 信息 | 服务器收到了，等着 | 100, 102 |
| `2xx` | 成功 | 搞定了 | 200, 201, 204 |
| `3xx` | 重定向 | 换个地方再来 | 301, 302, 304 |
| `4xx` | 客户端错误 | 你搞砸了 | 400, 401, 403, 404 |
| `5xx` | 服务器错误 | 服务器搞砸了 | 500, 502, 503 |

**记法**：1xx=等，2xx=好，3xx=走，4xx=你错，5xx=我错

## 📖 常用状态码详解

### 1xx - 信息响应

| 状态码 | 含义 | 场景 |
|--------|------|------|
| `100 Continue` | 继续发请求体 | 大文件上传前先问服务器要不要 |
| `102 Processing` | 服务器在处理，别急 | 耗时操作（如 Elasticsearch） |

### 2xx - 成功

| 状态码 | 含义 | 场景 |
|--------|------|---------|
| `200 OK` | 成功（最常见） | GET/POST 正常返回 |
| `201 Created` | 创建成功 | POST 新建资源返回 |
| `204 No Content` | 成功但没内容 | DELETE 成功、empty response |
| `206 Partial Content` | 部分成功 | 断点续传、视频流 |

### 3xx - 重定向

| 状态码 | 含义 | 场景 |
|--------|------|---------|
| `301 Moved Permanently` | **永久**搬家 | 域名换了这个再也不用了 |
| `302 Found` | **临时**搬家 | 维护中、AB 测试 |
| `304 Not Modified` | 用缓存 | 浏览器缓存、CDN |
| `307 Temporary Redirect` | 临时重定向（**保留方法**） | POST 重定向 |
| `308 Permanent Redirect` | 永久重定向（**保留方法**） | 强制保留 POST |

**301 vs 302 vs 307 vs 308 区别**：
- 301/302：会把 POST 变成 GET（不安全）
- 307/308：强制保留原始方法（更安全）
- 记忆：3**0**7/3**0**8 = 保留 **O**riginal method

### 4xx - 客户端错误（你错了）

| 状态码 | 含义 | 常见原因 |
|--------|------|---------|
| `400 Bad Request` | 请求格式有问题 | JSON 语法错、参数缺失 |
| `401 Unauthorized` | 没认证 | 没登录、token 过期 |
| `403 Forbidden` | 没权限 | 登录了但没权限看这个 |
| `404 Not Found` | 找不到 | 路径错了、资源删了 |
| `405 Method Not Allowed` | 方法不支持 | 用 POST 访问只支持 GET 的接口 |
| `408 Request Timeout` | 请求超时 | 服务器等太久 |
| `409 Conflict` | 冲突 | 重复创建、资源版本冲突 |
| `410 Gone` | 永久消失 | 资源被主动删除 |
| `429 Too Many Requests` | 请求太多 | 触发了限流，需要等 |
| `431 Request Header Fields Too Large` | header 太大 | Cookie 或 JWT 太长 |
| `451 Unavailable For Legal Reasons` | 法律原因不可用 | DMCA 删除 |

### 5xx - 服务器错误（它错了）

| 状态码 | 含义 | 常见原因 |
|--------|------|---------|
| `500 Internal Server Error` | 服务器内部崩了 | 代码异常、配置错误 |
| `501 Not Implemented` | 功能没实现 | 服务器不支持这个功能 |
| `502 Bad Gateway` | **上游服务器宕了** | Nginx/代理后面的服务挂了 |
| `503 Service Unavailable` | 服务暂时不可用 | 维护中、过载 |
| `504 Gateway Timeout` | 上游服务器响应太慢 | 超时了还没返回 |
| `507 Insufficient Storage` | 服务器存储满了 | 磁盘爆了 |
| `511 Network Authentication Required` | 需要登录才能上网 | 酒店/咖啡厅 WiFi 认证页 |

## 🔧 常见组合与排查

### API 开发常见组合

| 组合 | 含义 | 排查方向 |
|------|------|---------|
| `200 + 大量 HTML` | 可能是登录页（没 token） | 检查 Authorization header |
| `401 → 302 → 200` | 先 401 重定向到登录页 | 正常 SSO 流程 |
| `301 → 302 → ... → 200` | 链式重定向 | 用 curl -L 看完整链路 |
| `429 + Retry-After: 3600` | 限流，等 1 小时 | 等着或申请更高配额 |
| `403 + X-Frame-Options` | 防止 iframe 嵌入 | 正常安全策略 |

### CORS 相关

| 状态码 | 含义 |
|--------|------|
| 请求正常但无 `Access-Control-*` 头 | CORS 配置缺失 |
| 预检请求 `OPTIONS` 返回 404 | CORS 路由没配置 |
| `Origin` 和 `Access-Control-Allow-Origin` 不匹配 | CORS 域名白名单问题 |

## 🔍 实际测试（curl）

用 curl 查看任意 URL 的状态码和响应头：

```bash
# 基础状态码检查
curl -s -o /dev/null -w "%{http_code}" https://example.com

# 带响应头的状态码
curl -sI https://example.com
# 输出：
# HTTP/2 200
# cache-control: max-age=604800
# content-type: text/html; charset=UTF-8

# 完整响应（包含头）
curl -s -i https://example.com

# 显示重定向链路
curl -sL -w "\n--- FINAL STATUS: %{http_code} ---\n" https://httpstat.us/301

# 测试特定状态码（用于调试）
curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://httpstat.us/502
```

## ⚠️ 常见误区

1. **`200 OK` 不一定表示业务成功** — API 返回 200 但 `{"success": false, "error": "余额不足"}` 才是真相
2. **`404` 不一定是你的错** — 可能是服务器配置了错误的重定向
3. **`502` 不是你的 API 有问题** — 是你调用的第三方服务挂了
4. **`301` 和 `302` 对 SEO 影响不同** — 301 告诉搜索引擎"永久移走了"，权重传递；302 不传递
5. **`499` 不是标准码** — 是 Nginx 特有的：客户端在服务器响应前断开了

## ✅ 验证方法

```bash
# 测试常见状态码
curl -s -o /dev/null -w "%{http_code}" https://httpstat.us/200   # 200
curl -s -o /dev/null -w "%{http_code}" https://httpstat.us/404   # 404
curl -s -o /dev/null -w "%{http_code}" https://httpstat.us/500   # 500
curl -s -o /dev/null -w "%{http_code}" https://httpstat.us/502   # 502

# 完整重定向链路
curl -sL -v https://httpstat.us/302 2>&1 | grep -E "< HTTP|< Location"
```

## 💡 快速查询表

```
当你不确定时：
1. 2xx = 成功（你的代码正常工作）
2. 4xx = 你的请求有问题（检查参数/权限/路径）
3. 5xx = 服务器有问题（不是你的错，但需要报告）
4. 429 = 你请求太快了（减慢速度）
5. 任何不认识的码 = Google 一下，大多数有文档
```
