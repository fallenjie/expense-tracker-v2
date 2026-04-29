# 记账本 V2 - SPEC

## 1. Project Overview
- **Type**: Single-file HTML5 SPA (H5 App)
- **Storage**: Pure localStorage, multi-user support
- **Users**: et_users array, et_lastUser for auto-login
- **Encoding**: UTF-8, title: 记账本 V2

## 2. Design Direction
- **Aesthetic**: Modern warm minimalism — trustworthy, clean, tactile cards
- **Color Palette**:
  - Background: #F5F3EF (warm off-white)
  - Primary: #2D5A27 (deep forest green — money/growth association)
  - Accent: #E8A838 (warm amber for income/positive)
  - Danger: #D64545 (soft red for expense/negative)
  - Card: #FFFFFF
  - Text: #1A1A1A / #666666 / #999999
- **Typography**: System Chinese-optimized stack, clean sans-serif
- **Motion**: Page transitions (slide), card entrances (fade-up), micro-interactions on tap
- **Theme**: Light mode only

## 3. Layout & Structure
- Mobile-first, max-width: 430px centered on desktop
- Bottom tab navigation: 首页 / 账单 / 报表 / 分类 / 设置
- Each tab is a "page" shown/hidden via JS
- Auth screen (login/register) shown when no user logged in

## 4. Pages & Features

### 4.1 Auth Page (登录/注册)
- Toggle between 登录 and 注册
- 手机号 + 密码 fields
- 注册: 手机号(11位), 密码(6位以上), 自动登录
- 登录: 手机号+密码匹配 et_users
- 错误提示 inline

### 4.2 首页 (Home)
- 本月结余 (large number, green if positive, red if negative)
- 本月收入 / 本月支出 (two cards side by side)
- 最近记录 (latest 5 条, clickable to go to bills page with date filter)
- 本月预算进度条 (if set in settings)

### 4.3 账单页 (Bills)
- 月份选择器 (header)
- 搜索框 (按备注搜索)
- 日期筛选 (开始日期 ~ 结束日期)
- 账单列表 (时间倒序, 按天分组显示)
- 每条记录: 分类图标+名称, 金额(收入绿/支出红), 备注, 时间
- FAB 添加按钮 → 新增页面
- 新增/编辑页面: 类型切换(收入/支出), 金额, 分类下拉, 日期选择, 备注, 保存

### 4.4 报表页 (Report)
- Tab 切换: 日报 / 月报
- **日报**: 自然日统计, 收入/支出/结余, 支出分类饼图
- **月报**: 月份切换(上一月/下一月), 收入/支出/结余, 预算进度条, 支出分类饼图, 当月记录列表

### 4.5 分类页 (Categories)
- Segmented control: 支出 / 收入
- 预设分类列表 (不可删除, 编辑仅别名)
- 自定义分类 (可增删改)
- 新增自定义: 名称 + emoji 选择
- 24 个预设支出 + 6 个预设收入

### 4.6 设置页 (Settings)
- 月度预算设置 (输入框, 保存)
- 80% 提醒开关
- 100% 提醒开关
- 退出登录按钮

## 5. Data Models

### User
```json
{ "phone": "13800138000", "password": "hashed", "created": "ISO date" }
```

### Record
```json
{ "id": "uuid", "type": "income|expense", "amount": 100, "category": "餐饮", "categoryEmoji": "🍜", "note": "午餐", "date": "2026-04-29", "user": "13800138000", "created": "ISO" }
```

### Category
```json
{ "id": "uuid", "name": "餐饮", "emoji": "🍜", "type": "expense|income", "isCustom": false, "user": "13800138000" }
```

### Budget
```json
{ "user": "13800138000", "amount": 5000, "alert80": true, "alert100": true }
```

## 6. Technical
- Single `index.html`, CSS and JS inline
- No external CDN or SDK
- UUID via crypto.randomUUID() fallback
- All dates: ISO 8601, display as YYYY-MM-DD HH:mm
- Budget alerts: checked on each expense save
- CSS conic-gradient for pie charts
