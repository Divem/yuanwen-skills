# 「种点什么」MVP 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个微信小程序「种点什么」，实现用户认养一棵菜、菜农每日拍照上传、用户查看成长时间线、收获通知的完整 MVP 链路，支持用户/菜农身份切换。

**Architecture:** 单个微信小程序，内含用户端和菜农端两个视角，通过身份切换机制共用同一套后端。后端使用微信云开发（云数据库 + 云存储），消息推送使用微信订阅消息，支付使用微信支付。

**Tech Stack:** 微信小程序原生框架（WXML/WXSS/JS）、微信云开发（云数据库、云存储、云函数）、微信支付

---

## 文件结构

```
miniprogram/
├── app.js                          # 小程序入口，全局登录、角色初始化
├── app.json                        # 全局配置，tabBar 定义
├── app.wxss                        # 全局样式，主题色变量
├── utils/
│   ├── db.js                       # 云数据库操作封装（CRUD helpers）
│   ├── auth.js                     # 登录、角色切换逻辑
│   ├── date.js                     # 日期格式化工具
│   └── subscription.js             # 订阅消息授权与发送封装
├── pages/
│   ├── user/                       # ===== 用户端页面 =====
│   │   ├── home/                   # Tab1: 首页/认养商城
│   │   │   ├── home.wxml
│   │   │   ├── home.wxss
│   │   │   ├── home.js
│   │   │   └── home.json
│   │   ├── vegDetail/              # 菜品详情页
│   │   │   ├── vegDetail.wxml
│   │   │   ├── vegDetail.wxss
│   │   │   ├── vegDetail.js
│   │   │   └── vegDetail.json
│   │   ├── adoptSuccess/           # 认养成功页
│   │   │   ├── adoptSuccess.wxml
│   │   │   ├── adoptSuccess.wxss
│   │   │   ├── adoptSuccess.js
│   │   │   └── adoptSuccess.json
│   │   ├── garden/                 # Tab2: 我的菜园
│   │   │   ├── garden.wxml
│   │   │   ├── garden.wxss
│   │   │   ├── garden.js
│   │   │   └── garden.json
│   │   ├── timeline/               # 成长时间线页
│   │   │   ├── timeline.wxml
│   │   │   ├── timeline.wxss
│   │   │   ├── timeline.js
│   │   │   └── timeline.json
│   │   ├── messages/               # Tab3: 消息
│   │   │   ├── messages.wxml
│   │   │   ├── messages.wxss
│   │   │   ├── messages.js
│   │   │   └── messages.json
│   │   └── profile/                # Tab4: 我的
│   │       ├── profile.wxml
│   │       ├── profile.wxss
│   │       ├── profile.js
│   │       └── profile.json
│   ├── farmer/                     # ===== 菜农端页面 =====
│   │   ├── workbench/              # Tab1: 工作台
│   │   │   ├── workbench.wxml
│   │   │   ├── workbench.wxss
│   │   │   ├── workbench.js
│   │   │   └── workbench.json
│   │   ├── photoUpload/            # 拍照上传页
│   │   │   ├── photoUpload.wxml
│   │   │   ├── photoUpload.wxss
│   │   │   ├── photoUpload.js
│   │   │   └── photoUpload.json
│   │   ├── fieldManage/            # Tab2: 菜地管理
│   │   │   ├── fieldManage.wxml
│   │   │   ├── fieldManage.wxss
│   │   │   ├── fieldManage.js
│   │   │   └── fieldManage.json
│   │   ├── vegEdit/                # 菜品编辑页（新增/编辑）
│   │   │   ├── vegEdit.wxml
│   │   │   ├── vegEdit.wxss
│   │   │   ├── vegEdit.js
│   │   │   └── vegEdit.json
│   │   └── farmerProfile/          # Tab3: 我的（菜农）
│   │       ├── farmerProfile.wxml
│   │       ├── farmerProfile.wxss
│   │       ├── farmerProfile.js
│   │       └── farmerProfile.json
│   └── common/                     # ===== 共用页面 =====
│       ├── orders/                 # 订单列表
│       │   ├── orders.wxml
│       │   ├── orders.wxss
│       │   ├── orders.js
│       │   └── orders.json
│       └── orderDetail/            # 订单详情
│           ├── orderDetail.wxml
│           ├── orderDetail.wxss
│           ├── orderDetail.js
│           └── orderDetail.json
├── components/
│   ├── veg-card/                   # 菜品卡片组件
│   │   ├── veg-card.wxml
│   │   ├── veg-card.wxss
│   │   ├── veg-card.js
│   │   └── veg-card.json
│   ├── adoption-card/              # 认养卡片组件（菜园概览用）
│   │   ├── adoption-card.wxml
│   │   ├── adoption-card.wxss
│   │   ├── adoption-card.js
│   │   └── adoption-card.json
│   ├── timeline-item/              # 时间线条目组件
│   │   ├── timeline-item.wxml
│   │   ├── timeline-item.wxss
│   │   ├── timeline-item.js
│   │   └── timeline-item.json
│   ├── name-plate/                 # 署名牌组件
│   │   ├── name-plate.wxml
│   │   ├── name-plate.wxss
│   │   ├── name-plate.js
│   │   └── name-plate.json
│   └── quick-phrases/              # 快捷短语组件（菜农端用）
│       ├── quick-phrases.wxml
│       ├── quick-phrases.wxss
│       ├── quick-phrases.js
│       └── quick-phrases.json
cloudfunctions/
├── login/                          # 登录云函数
│   ├── index.js
│   └── package.json
├── createOrder/                    # 创建订单 + 发起支付
│   ├── index.js
│   └── package.json
├── payCallback/                    # 支付回调处理
│   ├── index.js
│   └── package.json
├── cancelExpiredOrders/            # 定时取消超时订单
│   ├── index.js
│   └── package.json
└── sendSubscribeMsg/               # 发送订阅消息
    ├── index.js
    └── package.json
```

---

## Task 1: 项目初始化与云开发环境搭建

**Files:**
- Create: `miniprogram/app.js`
- Create: `miniprogram/app.json`
- Create: `miniprogram/app.wxss`
- Create: `project.config.json`

- [ ] **Step 1: 使用微信开发者工具创建小程序项目**

在微信开发者工具中选择「云开发」模板创建项目，AppID 使用已注册的小程序 AppID。项目名称填「种点什么」。

- [ ] **Step 2: 初始化云开发环境**

在微信开发者工具中打开云开发控制台，创建环境（如 `zhongseed-dev`）。然后在 `app.js` 中初始化：

```js
// miniprogram/app.js
App({
  onLaunch() {
    wx.cloud.init({
      env: 'zhongseed-dev', // 替换为实际环境ID
      traceUser: true
    })
  },
  globalData: {
    userInfo: null,
    currentRole: 'user' // 默认用户视角
  }
})
```

- [ ] **Step 3: 配置 app.json，定义用户端 tabBar**

```json
// miniprogram/app.json
{
  "pages": [
    "pages/user/home/home",
    "pages/user/vegDetail/vegDetail",
    "pages/user/adoptSuccess/adoptSuccess",
    "pages/user/garden/garden",
    "pages/user/timeline/timeline",
    "pages/user/messages/messages",
    "pages/user/profile/profile",
    "pages/farmer/workbench/workbench",
    "pages/farmer/photoUpload/photoUpload",
    "pages/farmer/fieldManage/fieldManage",
    "pages/farmer/vegEdit/vegEdit",
    "pages/farmer/farmerProfile/farmerProfile",
    "pages/common/orders/orders",
    "pages/common/orderDetail/orderDetail"
  ],
  "tabBar": {
    "color": "#999999",
    "selectedColor": "#4CAF50",
    "backgroundColor": "#ffffff",
    "list": [
      {
        "pagePath": "pages/user/home/home",
        "text": "首页",
        "iconPath": "images/tab/home.png",
        "selectedIconPath": "images/tab/home-active.png"
      },
      {
        "pagePath": "pages/user/garden/garden",
        "text": "我的菜园",
        "iconPath": "images/tab/garden.png",
        "selectedIconPath": "images/tab/garden-active.png"
      },
      {
        "pagePath": "pages/user/messages/messages",
        "text": "消息",
        "iconPath": "images/tab/message.png",
        "selectedIconPath": "images/tab/message-active.png"
      },
      {
        "pagePath": "pages/user/profile/profile",
        "text": "我的",
        "iconPath": "images/tab/profile.png",
        "selectedIconPath": "images/tab/profile-active.png"
      }
    ]
  },
  "window": {
    "navigationBarBackgroundColor": "#4CAF50",
    "navigationBarTitleText": "种点什么",
    "navigationBarTextStyle": "white",
    "backgroundColor": "#f5f5f5"
  },
  "sitemapLocation": "sitemap.json",
  "style": "v2"
}
```

> **注意：** 微信小程序 tabBar 不支持动态切换。身份切换后通过 `wx.reLaunch` 跳转到对应角色的首页，菜农端页面不使用 tabBar，而是使用自定义底部导航组件。详见 Task 3。

- [ ] **Step 4: 配置全局样式**

```css
/* miniprogram/app.wxss */
page {
  --color-primary: #4CAF50;
  --color-primary-light: #E8F5E9;
  --color-farmer: #E91E63;
  --color-farmer-light: #FCE4EC;
  --color-text: #333333;
  --color-text-secondary: #999999;
  --color-border: #EEEEEE;
  --color-bg: #F5F5F5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 28rpx;
  color: var(--color-text);
  background-color: var(--color-bg);
}
```

- [ ] **Step 5: 在云开发控制台创建 4 个数据库集合**

在云开发控制台 → 数据库中创建以下集合：
- `users`
- `vegetables`
- `adoptions`
- `growth_logs`

每个集合使用默认权限（仅创建者可读写），后续通过云函数操作数据时以管理端权限访问。

- [ ] **Step 6: 验证云开发连接正常**

在 `miniprogram/app.js` 的 `onLaunch` 中添加测试代码，运行确认云数据库可以正常连接：

```js
// 临时测试代码，验证后删除
const db = wx.cloud.database()
db.collection('users').count().then(res => {
  console.log('云数据库连接成功，users 集合记录数:', res.total)
})
```

在微信开发者工具模拟器中运行，控制台应输出 `云数据库连接成功，users 集合记录数: 0`。

- [ ] **Step 7: 提交初始化代码**

```bash
git init
echo "node_modules/\n.superpowers/" > .gitignore
git add -A
git commit -m "feat: 项目初始化，配置云开发环境与全局样式"
```

---

## Task 2: 工具函数与登录云函数

**Files:**
- Create: `miniprogram/utils/db.js`
- Create: `miniprogram/utils/auth.js`
- Create: `miniprogram/utils/date.js`
- Create: `cloudfunctions/login/index.js`
- Create: `cloudfunctions/login/package.json`

- [ ] **Step 1: 编写日期工具函数**

```js
// miniprogram/utils/date.js
function formatDate(date) {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function daysBetween(start, end) {
  const startDate = new Date(start)
  const endDate = new Date(end || Date.now())
  return Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24))
}

function generateAdoptionCode() {
  const now = new Date()
  const dateStr = formatDate(now).replace(/-/g, '')
  const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
  return `ZD-${dateStr}-${random}`
}

module.exports = { formatDate, daysBetween, generateAdoptionCode }
```

- [ ] **Step 2: 编写数据库操作封装**

```js
// miniprogram/utils/db.js
const db = wx.cloud.database()
const _ = db.command

function getCollection(name) {
  return db.collection(name)
}

async function getById(collection, id) {
  const res = await db.collection(collection).doc(id).get()
  return res.data
}

async function queryList(collection, where, orderBy, limit = 20, skip = 0) {
  let query = db.collection(collection).where(where)
  if (orderBy) {
    query = query.orderBy(orderBy.field, orderBy.order || 'desc')
  }
  const res = await query.skip(skip).limit(limit).get()
  return res.data
}

async function addRecord(collection, data) {
  const res = await db.collection(collection).add({ data })
  return res._id
}

async function updateRecord(collection, id, data) {
  return db.collection(collection).doc(id).update({ data })
}

module.exports = { db, _, getCollection, getById, queryList, addRecord, updateRecord }
```

- [ ] **Step 3: 编写登录云函数**

```json
// cloudfunctions/login/package.json
{
  "name": "login",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "wx-server-sdk": "~2.6.3"
  }
}
```

```js
// cloudfunctions/login/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { OPENID } = cloud.getWXContext()

  // 查找已有用户
  const userRes = await db.collection('users').where({ openId: OPENID }).get()

  if (userRes.data.length > 0) {
    return { code: 0, data: userRes.data[0] }
  }

  // 新用户自动注册
  const newUser = {
    openId: OPENID,
    nickName: '',
    phone: '',
    avatar: '',
    roles: ['user'],
    currentRole: 'user',
    createdAt: db.serverDate()
  }

  const addRes = await db.collection('users').add({ data: newUser })
  newUser._id = addRes._id
  return { code: 0, data: newUser }
}
```

- [ ] **Step 4: 编写认证与角色切换工具**

```js
// miniprogram/utils/auth.js
async function login() {
  const res = await wx.cloud.callFunction({ name: 'login' })
  const user = res.result.data
  const app = getApp()
  app.globalData.userInfo = user
  app.globalData.currentRole = user.currentRole || 'user'
  return user
}

async function switchRole(targetRole) {
  const app = getApp()
  const user = app.globalData.userInfo
  if (!user.roles.includes(targetRole)) {
    throw new Error('没有该角色权限')
  }

  const { db } = require('./db')
  await db.collection('users').doc(user._id).update({
    data: { currentRole: targetRole }
  })

  app.globalData.currentRole = targetRole
  user.currentRole = targetRole

  if (targetRole === 'farmer') {
    wx.reLaunch({ url: '/pages/farmer/workbench/workbench' })
  } else {
    wx.reLaunch({ url: '/pages/user/home/home' })
  }
}

async function activateFarmerRole(inviteCode) {
  // MVP 阶段使用固定邀请码，后续可改为动态验证
  const VALID_CODES = ['FARMER2026']
  if (!VALID_CODES.includes(inviteCode)) {
    throw new Error('邀请码无效')
  }

  const app = getApp()
  const user = app.globalData.userInfo
  const { db } = require('./db')

  await db.collection('users').doc(user._id).update({
    data: { roles: ['user', 'farmer'] }
  })
  user.roles = ['user', 'farmer']
}

module.exports = { login, switchRole, activateFarmerRole }
```

- [ ] **Step 5: 在 app.js 中集成自动登录**

更新 `miniprogram/app.js`：

```js
// miniprogram/app.js
const { login } = require('./utils/auth')

App({
  onLaunch() {
    wx.cloud.init({
      env: 'zhongseed-dev',
      traceUser: true
    })
    this.autoLogin()
  },
  async autoLogin() {
    try {
      const user = await login()
      // 如果上次是菜农身份，跳转到菜农工作台
      if (user.currentRole === 'farmer' && user.roles.includes('farmer')) {
        wx.reLaunch({ url: '/pages/farmer/workbench/workbench' })
      }
    } catch (err) {
      console.error('自动登录失败:', err)
    }
  },
  globalData: {
    userInfo: null,
    currentRole: 'user'
  }
})
```

- [ ] **Step 6: 上传登录云函数并测试**

在微信开发者工具中右键 `cloudfunctions/login` → 上传并部署（云端安装依赖）。

在模拟器中运行小程序，控制台应显示登录成功日志。在云开发控制台 → 数据库 → `users` 集合中应能看到新增的用户记录。

- [ ] **Step 7: 提交**

```bash
git add miniprogram/utils/ cloudfunctions/login/ miniprogram/app.js
git commit -m "feat: 添加工具函数、登录云函数与自动登录"
```

---

## Task 3: 菜农端自定义 TabBar 组件

由于微信小程序原生 tabBar 不支持动态切换，菜农端使用自定义底部导航。

**Files:**
- Create: `miniprogram/components/farmer-tabbar/farmer-tabbar.wxml`
- Create: `miniprogram/components/farmer-tabbar/farmer-tabbar.wxss`
- Create: `miniprogram/components/farmer-tabbar/farmer-tabbar.js`
- Create: `miniprogram/components/farmer-tabbar/farmer-tabbar.json`

- [ ] **Step 1: 编写菜农端自定义 TabBar 组件**

```json
// miniprogram/components/farmer-tabbar/farmer-tabbar.json
{
  "component": true
}
```

```js
// miniprogram/components/farmer-tabbar/farmer-tabbar.js
Component({
  properties: {
    active: { type: Number, value: 0 }
  },
  data: {
    tabs: [
      { icon: '📋', text: '工作台', url: '/pages/farmer/workbench/workbench' },
      { icon: '🌾', text: '菜地管理', url: '/pages/farmer/fieldManage/fieldManage' },
      { icon: '👤', text: '我的', url: '/pages/farmer/farmerProfile/farmerProfile' }
    ]
  },
  methods: {
    onTabTap(e) {
      const index = e.currentTarget.dataset.index
      if (index === this.data.active) return
      const url = this.data.tabs[index].url
      wx.reLaunch({ url })
    }
  }
})
```

```xml
<!-- miniprogram/components/farmer-tabbar/farmer-tabbar.wxml -->
<view class="tabbar">
  <view
    class="tabbar-item {{active === index ? 'active' : ''}}"
    wx:for="{{tabs}}"
    wx:key="index"
    data-index="{{index}}"
    bindtap="onTabTap"
  >
    <text class="tabbar-icon">{{item.icon}}</text>
    <text class="tabbar-text">{{item.text}}</text>
  </view>
</view>
```

```css
/* miniprogram/components/farmer-tabbar/farmer-tabbar.wxss */
.tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  height: 100rpx;
  background: #fff;
  border-top: 1rpx solid #eee;
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 999;
}
.tabbar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.tabbar-icon { font-size: 40rpx; }
.tabbar-text { font-size: 20rpx; color: #999; margin-top: 4rpx; }
.tabbar-item.active .tabbar-text { color: #E91E63; font-weight: bold; }
```

- [ ] **Step 2: 验证组件渲染**

临时在 `pages/farmer/workbench/workbench` 页面引用该组件，确认底部导航显示正常，点击切换高亮。

```json
// pages/farmer/workbench/workbench.json
{
  "navigationBarTitleText": "工作台",
  "navigationBarBackgroundColor": "#E91E63",
  "usingComponents": {
    "farmer-tabbar": "/components/farmer-tabbar/farmer-tabbar"
  }
}
```

```xml
<!-- pages/farmer/workbench/workbench.wxml (临时) -->
<view class="page">
  <text>工作台页面</text>
</view>
<farmer-tabbar active="{{0}}" />
```

- [ ] **Step 3: 提交**

```bash
git add miniprogram/components/farmer-tabbar/
git commit -m "feat: 添加菜农端自定义底部导航组件"
```

---

## Task 4: 菜品卡片组件与首页/认养商城

**Files:**
- Create: `miniprogram/components/veg-card/veg-card.*`
- Create: `miniprogram/pages/user/home/home.*`

- [ ] **Step 1: 编写菜品卡片组件**

```json
// miniprogram/components/veg-card/veg-card.json
{ "component": true }
```

```js
// miniprogram/components/veg-card/veg-card.js
Component({
  properties: {
    veg: { type: Object, value: {} }
  },
  methods: {
    onTap() {
      wx.navigateTo({
        url: `/pages/user/vegDetail/vegDetail?id=${this.data.veg._id}`
      })
    }
  }
})
```

```xml
<!-- miniprogram/components/veg-card/veg-card.wxml -->
<view class="veg-card" bindtap="onTap">
  <image class="veg-cover" src="{{veg.coverImage}}" mode="aspectFill" />
  <view class="veg-info">
    <text class="veg-name">{{veg.name}}</text>
    <text class="veg-cycle">生长周期 {{veg.duration.trial}} 天起</text>
    <view class="veg-bottom">
      <text class="veg-price">¥{{veg.price.trial}}起</text>
      <text class="veg-stock" wx:if="{{veg.stock > 0}}">剩余 {{veg.stock}} 棵</text>
      <text class="veg-soldout" wx:else>已认满</text>
    </view>
  </view>
</view>
```

```css
/* miniprogram/components/veg-card/veg-card.wxss */
.veg-card {
  background: #fff;
  border-radius: 16rpx;
  overflow: hidden;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06);
}
.veg-cover { width: 100%; height: 320rpx; }
.veg-info { padding: 20rpx 24rpx; }
.veg-name { font-size: 32rpx; font-weight: bold; display: block; }
.veg-cycle { font-size: 24rpx; color: #999; margin-top: 8rpx; display: block; }
.veg-bottom { display: flex; justify-content: space-between; align-items: center; margin-top: 16rpx; }
.veg-price { font-size: 32rpx; color: #E53935; font-weight: bold; }
.veg-stock { font-size: 24rpx; color: #4CAF50; }
.veg-soldout { font-size: 24rpx; color: #999; }
```

- [ ] **Step 2: 编写首页**

```json
// miniprogram/pages/user/home/home.json
{
  "navigationBarTitleText": "种点什么",
  "usingComponents": {
    "veg-card": "/components/veg-card/veg-card"
  }
}
```

```js
// miniprogram/pages/user/home/home.js
const { queryList } = require('../../../utils/db')

Page({
  data: {
    vegetables: [],
    loading: true
  },
  onLoad() {
    this.loadVegetables()
  },
  onPullDownRefresh() {
    this.loadVegetables().then(() => wx.stopPullDownRefresh())
  },
  async loadVegetables() {
    this.setData({ loading: true })
    const list = await queryList('vegetables',
      { status: 'on_sale' },
      { field: 'createdAt', order: 'desc' }
    )
    this.setData({ vegetables: list, loading: false })
  }
})
```

```xml
<!-- miniprogram/pages/user/home/home.wxml -->
<view class="home">
  <view class="banner">
    <view class="banner-text">
      <text class="banner-title">种点什么</text>
      <text class="banner-slogan">让每个城市家庭都能拥有一片属于自己的田园</text>
    </view>
  </view>

  <view class="section-title">当季可认养</view>

  <view class="veg-list" wx:if="{{!loading}}">
    <veg-card wx:for="{{vegetables}}" wx:key="_id" veg="{{item}}" />
    <view class="empty" wx:if="{{vegetables.length === 0}}">
      <text>暂无可认养的菜品，敬请期待</text>
    </view>
  </view>

  <view class="loading" wx:if="{{loading}}">
    <text>加载中...</text>
  </view>
</view>
```

```css
/* miniprogram/pages/user/home/home.wxss */
.home { padding-bottom: 20rpx; }
.banner {
  background: linear-gradient(135deg, #4CAF50, #81C784);
  padding: 60rpx 32rpx;
  color: #fff;
}
.banner-title { font-size: 48rpx; font-weight: bold; display: block; }
.banner-slogan { font-size: 26rpx; margin-top: 12rpx; display: block; opacity: 0.9; }
.section-title {
  font-size: 32rpx; font-weight: bold;
  padding: 32rpx 32rpx 16rpx;
}
.veg-list { padding: 0 32rpx; }
.empty, .loading {
  text-align: center; padding: 100rpx 0;
  color: #999; font-size: 28rpx;
}
```

- [ ] **Step 3: 在云开发控制台添加测试菜品数据**

在云开发控制台 → 数据库 → `vegetables` 集合中手动添加一条测试数据：

```json
{
  "name": "小番茄",
  "desc": "酸甜可口的有机小番茄，从播种到收获约30天，适合新手体验。",
  "coverImage": "cloud://zhongseed-dev.xxxx/vegetables/tomato.jpg",
  "price": { "trial": 39, "quarterly": 99 },
  "duration": { "trial": 30, "quarterly": 90 },
  "stock": 20,
  "status": "on_sale",
  "growthInfo": "喜温暖，日照充足，注意浇水不宜过多。",
  "createdAt": "2026-04-11T00:00:00Z"
}
```

> 注意：coverImage 需要先上传一张测试图片到云存储，或使用任意可访问的图片 URL 进行测试。

- [ ] **Step 4: 运行验证首页展示正常**

在微信开发者工具模拟器中运行，确认：
1. Banner 显示品牌 slogan
2. 菜品卡片正确渲染（封面图、名称、价格、剩余库存）
3. 下拉刷新正常工作

- [ ] **Step 5: 提交**

```bash
git add miniprogram/components/veg-card/ miniprogram/pages/user/home/
git commit -m "feat: 首页认养商城与菜品卡片组件"
```

---

## Task 5: 菜品详情页与认养下单

**Files:**
- Create: `miniprogram/pages/user/vegDetail/vegDetail.*`
- Create: `cloudfunctions/createOrder/index.js`
- Create: `cloudfunctions/createOrder/package.json`
- Create: `cloudfunctions/payCallback/index.js`
- Create: `cloudfunctions/payCallback/package.json`

- [ ] **Step 1: 编写菜品详情页**

```json
// miniprogram/pages/user/vegDetail/vegDetail.json
{ "navigationBarTitleText": "菜品详情" }
```

```js
// miniprogram/pages/user/vegDetail/vegDetail.js
const { getById } = require('../../../utils/db')

Page({
  data: {
    veg: null,
    planType: 'trial',
    ownerName: '',
    submitting: false
  },
  onLoad(options) {
    this.loadVeg(options.id)
  },
  async loadVeg(id) {
    const veg = await getById('vegetables', id)
    this.setData({ veg })
  },
  onPlanChange(e) {
    this.setData({ planType: e.currentTarget.dataset.plan })
  },
  onNameInput(e) {
    this.setData({ ownerName: e.detail.value })
  },
  async onAdopt() {
    const { veg, planType, ownerName, submitting } = this.data
    if (submitting) return
    if (!ownerName.trim()) {
      wx.showToast({ title: '请填写署名', icon: 'none' })
      return
    }
    if (veg.stock <= 0) {
      wx.showToast({ title: '该菜品已认满', icon: 'none' })
      return
    }

    this.setData({ submitting: true })
    try {
      const res = await wx.cloud.callFunction({
        name: 'createOrder',
        data: { vegId: veg._id, planType, ownerName: ownerName.trim() }
      })
      const { payment, adoptionId } = res.result.data

      // 发起微信支付
      await wx.requestPayment(payment)

      // 支付成功，跳转认养成功页
      wx.redirectTo({
        url: `/pages/user/adoptSuccess/adoptSuccess?id=${adoptionId}`
      })
    } catch (err) {
      if (err.errMsg !== 'requestPayment:fail cancel') {
        wx.showToast({ title: '下单失败，请重试', icon: 'none' })
      }
    } finally {
      this.setData({ submitting: false })
    }
  }
})
```

```xml
<!-- miniprogram/pages/user/vegDetail/vegDetail.wxml -->
<view class="detail" wx:if="{{veg}}">
  <image class="detail-cover" src="{{veg.coverImage}}" mode="aspectFill" />

  <view class="detail-body">
    <text class="detail-name">{{veg.name}}</text>
    <text class="detail-desc">{{veg.desc}}</text>

    <view class="section">
      <text class="section-label">种植说明</text>
      <text class="section-text">{{veg.growthInfo}}</text>
    </view>

    <view class="section">
      <text class="section-label">选择套餐</text>
      <view class="plan-options">
        <view
          class="plan-item {{planType === 'trial' ? 'active' : ''}}"
          data-plan="trial"
          bindtap="onPlanChange"
        >
          <text class="plan-name">尝鲜装</text>
          <text class="plan-price">¥{{veg.price.trial}}</text>
          <text class="plan-duration">{{veg.duration.trial}} 天</text>
        </view>
        <view
          class="plan-item {{planType === 'quarterly' ? 'active' : ''}}"
          data-plan="quarterly"
          bindtap="onPlanChange"
        >
          <text class="plan-name">季度装</text>
          <text class="plan-price">¥{{veg.price.quarterly}}</text>
          <text class="plan-duration">{{veg.duration.quarterly}} 天</text>
        </view>
      </view>
    </view>

    <view class="section">
      <text class="section-label">为你的菜署个名</text>
      <input
        class="name-input"
        placeholder="例如：达尔文的菜"
        value="{{ownerName}}"
        bindinput="onNameInput"
        maxlength="20"
      />
    </view>
  </view>

  <view class="bottom-bar">
    <view class="price-display">
      <text class="price-label">合计</text>
      <text class="price-value">¥{{planType === 'trial' ? veg.price.trial : veg.price.quarterly}}</text>
    </view>
    <button
      class="adopt-btn"
      disabled="{{veg.stock <= 0 || submitting}}"
      bindtap="onAdopt"
    >
      {{veg.stock <= 0 ? '已认满' : (submitting ? '下单中...' : '立即认养')}}
    </button>
  </view>
</view>
```

```css
/* miniprogram/pages/user/vegDetail/vegDetail.wxss */
.detail-cover { width: 100%; height: 400rpx; }
.detail-body { padding: 32rpx; }
.detail-name { font-size: 40rpx; font-weight: bold; display: block; }
.detail-desc { font-size: 28rpx; color: #666; margin-top: 12rpx; display: block; line-height: 1.6; }
.section { margin-top: 40rpx; }
.section-label { font-size: 28rpx; font-weight: bold; display: block; margin-bottom: 16rpx; }
.section-text { font-size: 26rpx; color: #666; line-height: 1.6; }
.plan-options { display: flex; gap: 20rpx; }
.plan-item {
  flex: 1; text-align: center; padding: 24rpx;
  border: 2rpx solid #eee; border-radius: 12rpx;
}
.plan-item.active { border-color: #4CAF50; background: #E8F5E9; }
.plan-name { font-size: 28rpx; font-weight: bold; display: block; }
.plan-price { font-size: 36rpx; color: #E53935; font-weight: bold; display: block; margin-top: 8rpx; }
.plan-duration { font-size: 22rpx; color: #999; display: block; margin-top: 4rpx; }
.name-input {
  border: 2rpx solid #eee; border-radius: 12rpx;
  padding: 20rpx 24rpx; font-size: 28rpx;
}
.bottom-bar {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; align-items: center;
  background: #fff; padding: 16rpx 32rpx;
  padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
  border-top: 1rpx solid #eee;
}
.price-display { flex: 1; }
.price-label { font-size: 24rpx; color: #999; }
.price-value { font-size: 40rpx; color: #E53935; font-weight: bold; margin-left: 8rpx; }
.adopt-btn {
  background: #4CAF50 !important; color: #fff !important;
  border-radius: 40rpx !important; padding: 0 60rpx !important;
  font-size: 30rpx !important; line-height: 80rpx !important;
}
.adopt-btn[disabled] { background: #ccc !important; }
```

- [ ] **Step 2: 编写创建订单云函数**

```json
// cloudfunctions/createOrder/package.json
{
  "name": "createOrder",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "wx-server-sdk": "~2.6.3"
  }
}
```

```js
// cloudfunctions/createOrder/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { OPENID } = cloud.getWXContext()
  const { vegId, planType, ownerName } = event

  // 获取菜品信息
  const vegRes = await db.collection('vegetables').doc(vegId).get()
  const veg = vegRes.data

  if (veg.stock <= 0) {
    return { code: -1, msg: '库存不足' }
  }

  const price = veg.price[planType]
  const duration = veg.duration[planType]

  // 生成认养编号
  const now = new Date()
  const dateStr = `${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}`
  const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
  const code = `ZD-${dateStr}-${random}`

  // 计算结束日期
  const endDate = new Date(now.getTime() + duration * 24 * 60 * 60 * 1000)

  // 创建认养记录
  const adoption = {
    userId: OPENID,
    vegId,
    code,
    ownerName,
    planType,
    status: 'pending_payment',
    startDate: db.serverDate(),
    endDate: new Date(endDate),
    orderId: '',
    createdAt: db.serverDate()
  }

  const addRes = await db.collection('adoptions').add({ data: adoption })
  const adoptionId = addRes._id

  // 扣减库存
  await db.collection('vegetables').doc(vegId).update({
    data: { stock: db.command.inc(-1) }
  })

  // 发起微信支付
  const payRes = await cloud.cloudPay.unifiedOrder({
    body: `种点什么-${veg.name}-${planType === 'trial' ? '尝鲜装' : '季度装'}`,
    outTradeNo: adoptionId,
    totalFee: price * 100, // 分为单位
    spbillCreateIp: '127.0.0.1',
    envId: cloud.DYNAMIC_CURRENT_ENV,
    functionName: 'payCallback',
    nonceStr: String(Date.now()),
    tradeType: 'JSAPI'
  })

  return {
    code: 0,
    data: {
      adoptionId,
      payment: payRes.payment
    }
  }
}
```

- [ ] **Step 3: 编写支付回调云函数**

```json
// cloudfunctions/payCallback/package.json
{
  "name": "payCallback",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "wx-server-sdk": "~2.6.3"
  }
}
```

```js
// cloudfunctions/payCallback/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { outTradeNo, resultCode, transactionId } = event

  if (resultCode !== 'SUCCESS') {
    // 支付失败，恢复库存
    const adoption = await db.collection('adoptions').doc(outTradeNo).get()
    await db.collection('vegetables').doc(adoption.data.vegId).update({
      data: { stock: db.command.inc(1) }
    })
    await db.collection('adoptions').doc(outTradeNo).update({
      data: { status: 'payment_failed' }
    })
    return { errcode: 0, errmsg: 'handled' }
  }

  // 支付成功，更新认养状态
  await db.collection('adoptions').doc(outTradeNo).update({
    data: {
      status: 'growing',
      orderId: transactionId
    }
  })

  // 创建站内消息通知
  const adoption = await db.collection('adoptions').doc(outTradeNo).get()
  const veg = await db.collection('vegetables').doc(adoption.data.vegId).get()

  // 在 growth_logs 中记录播种
  await db.collection('growth_logs').add({
    data: {
      adoptionId: outTradeNo,
      images: [],
      text: `🌱 ${veg.data.name}已播种，开始成长之旅！`,
      stage: 'seeding',
      logDate: db.serverDate(),
      farmerId: 'system',
      createdAt: db.serverDate()
    }
  })

  return { errcode: 0, errmsg: 'SUCCESS' }
}
```

- [ ] **Step 4: 上传云函数并验证下单流程**

在微信开发者工具中上传 `createOrder` 和 `payCallback` 云函数。

在模拟器中完成下单流程测试（开发环境中微信支付走模拟模式）：
1. 首页点击菜品卡片 → 进入详情页
2. 选择套餐、填写署名 → 点击立即认养
3. 完成支付 → 跳转认养成功页

- [ ] **Step 5: 提交**

```bash
git add miniprogram/pages/user/vegDetail/ cloudfunctions/createOrder/ cloudfunctions/payCallback/
git commit -m "feat: 菜品详情页与认养下单支付流程"
```

---

## Task 6: 认养成功页与署名牌组件

**Files:**
- Create: `miniprogram/pages/user/adoptSuccess/adoptSuccess.*`
- Create: `miniprogram/components/name-plate/name-plate.*`

- [ ] **Step 1: 编写署名牌组件**

```json
// miniprogram/components/name-plate/name-plate.json
{ "component": true }
```

```js
// miniprogram/components/name-plate/name-plate.js
Component({
  properties: {
    vegName: { type: String, value: '' },
    ownerName: { type: String, value: '' },
    code: { type: String, value: '' },
    startDate: { type: String, value: '' }
  }
})
```

```xml
<!-- miniprogram/components/name-plate/name-plate.wxml -->
<view class="plate">
  <view class="plate-header">
    <text class="plate-icon">🌱</text>
    <text class="plate-brand">种点什么</text>
  </view>
  <view class="plate-body">
    <text class="plate-veg">{{vegName}}</text>
    <text class="plate-owner">主人：{{ownerName}}</text>
    <text class="plate-code">编号：{{code}}</text>
    <text class="plate-date">认养日期：{{startDate}}</text>
  </view>
</view>
```

```css
/* miniprogram/components/name-plate/name-plate.wxss */
.plate {
  background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
  border-radius: 20rpx; padding: 40rpx;
  border: 2rpx solid #A5D6A7;
}
.plate-header { display: flex; align-items: center; margin-bottom: 24rpx; }
.plate-icon { font-size: 40rpx; margin-right: 12rpx; }
.plate-brand { font-size: 24rpx; color: #4CAF50; font-weight: bold; }
.plate-body { text-align: center; }
.plate-veg { font-size: 40rpx; font-weight: bold; display: block; color: #2E7D32; }
.plate-owner { font-size: 32rpx; display: block; margin-top: 16rpx; color: #333; }
.plate-code { font-size: 24rpx; display: block; margin-top: 12rpx; color: #666; }
.plate-date { font-size: 22rpx; display: block; margin-top: 8rpx; color: #999; }
```

- [ ] **Step 2: 编写认养成功页**

```json
// miniprogram/pages/user/adoptSuccess/adoptSuccess.json
{
  "navigationBarTitleText": "认养成功",
  "usingComponents": {
    "name-plate": "/components/name-plate/name-plate"
  }
}
```

```js
// miniprogram/pages/user/adoptSuccess/adoptSuccess.js
const { getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')

Page({
  data: {
    adoption: null,
    vegName: '',
    dateStr: ''
  },
  async onLoad(options) {
    const adoption = await getById('adoptions', options.id)
    const veg = await getById('vegetables', adoption.vegId)
    this.setData({
      adoption,
      vegName: veg.name,
      dateStr: formatDate(adoption.startDate)
    })
    // 引导订阅消息授权
    this.requestSubscription()
  },
  requestSubscription() {
    wx.requestSubscribeMessage({
      tmplIds: [
        // 替换为实际的模板ID
        'TEMPLATE_GROWTH_UPDATE',
        'TEMPLATE_HARVEST_NOTICE'
      ],
      success(res) {
        console.log('订阅消息授权结果:', res)
      }
    })
  },
  goToGarden() {
    wx.switchTab({ url: '/pages/user/garden/garden' })
  }
})
```

```xml
<!-- miniprogram/pages/user/adoptSuccess/adoptSuccess.wxml -->
<view class="success-page" wx:if="{{adoption}}">
  <view class="success-icon">🎉</view>
  <text class="success-title">认养成功！</text>
  <text class="success-desc">你的菜已经播种啦，每天来看看它的成长吧</text>

  <view class="plate-wrapper">
    <name-plate
      vegName="{{vegName}}"
      ownerName="{{adoption.ownerName}}"
      code="{{adoption.code}}"
      startDate="{{dateStr}}"
    />
  </view>

  <button class="go-garden-btn" bindtap="goToGarden">去我的菜园看看</button>
</view>
```

```css
/* miniprogram/pages/user/adoptSuccess/adoptSuccess.wxss */
.success-page { text-align: center; padding: 60rpx 32rpx; }
.success-icon { font-size: 100rpx; }
.success-title { font-size: 40rpx; font-weight: bold; display: block; margin-top: 20rpx; }
.success-desc { font-size: 28rpx; color: #666; display: block; margin-top: 12rpx; }
.plate-wrapper { margin: 60rpx 0; }
.go-garden-btn {
  background: #4CAF50 !important; color: #fff !important;
  border-radius: 40rpx !important; margin-top: 40rpx;
}
```

- [ ] **Step 3: 验证认养成功页展示正常**

从菜品详情页完成下单后，确认跳转到成功页，署名牌正确显示菜品名、署名、编号和日期。

- [ ] **Step 4: 提交**

```bash
git add miniprogram/pages/user/adoptSuccess/ miniprogram/components/name-plate/
git commit -m "feat: 认养成功页与署名牌组件"
```

---

## Task 7: 我的菜园与成长时间线

**Files:**
- Create: `miniprogram/components/adoption-card/adoption-card.*`
- Create: `miniprogram/components/timeline-item/timeline-item.*`
- Create: `miniprogram/pages/user/garden/garden.*`
- Create: `miniprogram/pages/user/timeline/timeline.*`

- [ ] **Step 1: 编写认养卡片组件**

```json
// miniprogram/components/adoption-card/adoption-card.json
{ "component": true }
```

```js
// miniprogram/components/adoption-card/adoption-card.js
const { daysBetween } = require('../../utils/date')

Component({
  properties: {
    adoption: { type: Object, value: {} },
    vegName: { type: String, value: '' },
    coverImage: { type: String, value: '' },
    selected: { type: Boolean, value: false }
  },
  computed: {},
  data: { growDays: 0 },
  lifetimes: {
    attached() {
      this.setData({
        growDays: daysBetween(this.data.adoption.startDate, Date.now())
      })
    }
  },
  methods: {
    onTap() {
      this.triggerEvent('select', { adoption: this.data.adoption })
    }
  }
})
```

```xml
<!-- miniprogram/components/adoption-card/adoption-card.wxml -->
<view class="adopt-card {{selected ? 'selected' : ''}}" bindtap="onTap">
  <image class="adopt-cover" src="{{coverImage}}" mode="aspectFill" />
  <view class="adopt-info">
    <text class="adopt-name">{{vegName}}</text>
    <text class="adopt-owner">{{adoption.ownerName}}</text>
    <text class="adopt-code">{{adoption.code}}</text>
    <view class="adopt-status">
      <text class="status-tag {{adoption.status === 'growing' ? 'growing' : 'harvested'}}">
        {{adoption.status === 'growing' ? '生长中' : '已收获'}}
      </text>
      <text class="grow-days">第 {{growDays}} 天</text>
    </view>
  </view>
</view>
```

```css
/* miniprogram/components/adoption-card/adoption-card.wxss */
.adopt-card {
  display: inline-block; width: 280rpx;
  background: #fff; border-radius: 16rpx;
  overflow: hidden; margin-right: 20rpx;
  border: 2rpx solid #eee; flex-shrink: 0;
}
.adopt-card.selected { border-color: #4CAF50; }
.adopt-cover { width: 280rpx; height: 180rpx; }
.adopt-info { padding: 16rpx; }
.adopt-name { font-size: 28rpx; font-weight: bold; display: block; }
.adopt-owner { font-size: 22rpx; color: #666; display: block; margin-top: 4rpx; }
.adopt-code { font-size: 20rpx; color: #999; display: block; margin-top: 4rpx; }
.adopt-status { display: flex; justify-content: space-between; align-items: center; margin-top: 8rpx; }
.status-tag { font-size: 20rpx; padding: 2rpx 12rpx; border-radius: 20rpx; }
.status-tag.growing { background: #E8F5E9; color: #4CAF50; }
.status-tag.harvested { background: #FFF3E0; color: #FF9800; }
.grow-days { font-size: 20rpx; color: #999; }
```

- [ ] **Step 2: 编写时间线条目组件**

```json
// miniprogram/components/timeline-item/timeline-item.json
{ "component": true }
```

```js
// miniprogram/components/timeline-item/timeline-item.js
Component({
  properties: {
    log: { type: Object, value: {} }
  },
  methods: {
    previewImage(e) {
      const url = e.currentTarget.dataset.url
      wx.previewImage({
        current: url,
        urls: this.data.log.images
      })
    }
  }
})
```

```xml
<!-- miniprogram/components/timeline-item/timeline-item.wxml -->
<view class="tl-item">
  <view class="tl-dot-line">
    <view class="tl-dot {{log.stage ? 'milestone' : ''}}"></view>
    <view class="tl-line"></view>
  </view>
  <view class="tl-content">
    <view class="tl-header">
      <text class="tl-date">{{log.logDateStr}}</text>
      <text class="tl-stage" wx:if="{{log.stage}}">{{log.stageLabel}}</text>
    </view>
    <view class="tl-images" wx:if="{{log.images.length > 0}}">
      <image
        wx:for="{{log.images}}" wx:key="*this"
        class="tl-img"
        src="{{item}}"
        mode="aspectFill"
        data-url="{{item}}"
        bindtap="previewImage"
      />
    </view>
    <text class="tl-text" wx:if="{{log.text}}">{{log.text}}</text>
  </view>
</view>
```

```css
/* miniprogram/components/timeline-item/timeline-item.wxss */
.tl-item { display: flex; padding-bottom: 32rpx; }
.tl-dot-line { display: flex; flex-direction: column; align-items: center; margin-right: 20rpx; }
.tl-dot { width: 20rpx; height: 20rpx; border-radius: 50%; background: #ccc; flex-shrink: 0; }
.tl-dot.milestone { background: #4CAF50; width: 24rpx; height: 24rpx; }
.tl-line { width: 2rpx; flex: 1; background: #eee; margin-top: 8rpx; }
.tl-content { flex: 1; }
.tl-header { display: flex; align-items: center; gap: 12rpx; margin-bottom: 12rpx; }
.tl-date { font-size: 26rpx; color: #999; }
.tl-stage {
  font-size: 20rpx; background: #E8F5E9; color: #4CAF50;
  padding: 2rpx 16rpx; border-radius: 20rpx;
}
.tl-images { display: flex; flex-wrap: wrap; gap: 8rpx; margin-bottom: 12rpx; }
.tl-img { width: 200rpx; height: 200rpx; border-radius: 8rpx; }
.tl-text { font-size: 28rpx; color: #333; line-height: 1.6; }
```

- [ ] **Step 3: 编写我的菜园页面**

```json
// miniprogram/pages/user/garden/garden.json
{
  "navigationBarTitleText": "我的菜园",
  "usingComponents": {
    "adoption-card": "/components/adoption-card/adoption-card"
  }
}
```

```js
// miniprogram/pages/user/garden/garden.js
const { queryList, getById } = require('../../../utils/db')

Page({
  data: {
    adoptions: [],
    selectedId: '',
    loading: true
  },
  onShow() {
    this.loadAdoptions()
  },
  async loadAdoptions() {
    this.setData({ loading: true })
    const app = getApp()
    const user = app.globalData.userInfo
    if (!user) {
      this.setData({ loading: false })
      return
    }

    const adoptions = await queryList('adoptions',
      { userId: user.openId, status: 'growing' },
      { field: 'createdAt', order: 'desc' }
    )

    // 关联菜品信息
    const enriched = await Promise.all(adoptions.map(async (a) => {
      const veg = await getById('vegetables', a.vegId)
      return { ...a, vegName: veg.name, coverImage: veg.coverImage }
    }))

    this.setData({
      adoptions: enriched,
      selectedId: enriched.length > 0 ? enriched[0]._id : '',
      loading: false
    })
  },
  onSelectAdoption(e) {
    const { adoption } = e.detail
    this.setData({ selectedId: adoption._id })
  },
  viewTimeline() {
    if (!this.data.selectedId) return
    wx.navigateTo({
      url: `/pages/user/timeline/timeline?id=${this.data.selectedId}`
    })
  },
  viewNamePlate() {
    // 后续扩展：弹出署名牌弹窗
  }
})
```

```xml
<!-- miniprogram/pages/user/garden/garden.wxml -->
<view class="garden">
  <view wx:if="{{loading}}" class="loading"><text>加载中...</text></view>

  <block wx:elif="{{adoptions.length > 0}}">
    <view class="garden-header">
      <text class="garden-title">我认养的菜</text>
      <text class="garden-count">共 {{adoptions.length}} 棵</text>
    </view>

    <scroll-view class="card-scroll" scroll-x>
      <adoption-card
        wx:for="{{adoptions}}" wx:key="_id"
        adoption="{{item}}"
        vegName="{{item.vegName}}"
        coverImage="{{item.coverImage}}"
        selected="{{item._id === selectedId}}"
        bind:select="onSelectAdoption"
      />
    </scroll-view>

    <view class="action-buttons">
      <button class="action-btn primary" bindtap="viewTimeline">查看成长记录</button>
    </view>
  </block>

  <view wx:else class="empty">
    <text class="empty-icon">🌱</text>
    <text class="empty-text">还没有认养任何菜哦</text>
    <navigator url="/pages/user/home/home" open-type="switchTab" class="empty-link">去认养一棵</navigator>
  </view>
</view>
```

```css
/* miniprogram/pages/user/garden/garden.wxss */
.garden { padding: 32rpx 0; }
.garden-header { display: flex; justify-content: space-between; align-items: center; padding: 0 32rpx; margin-bottom: 20rpx; }
.garden-title { font-size: 36rpx; font-weight: bold; }
.garden-count { font-size: 24rpx; color: #999; }
.card-scroll { white-space: nowrap; padding: 0 32rpx; }
.action-buttons { padding: 40rpx 32rpx; }
.action-btn { border-radius: 40rpx !important; font-size: 30rpx !important; }
.action-btn.primary { background: #4CAF50 !important; color: #fff !important; }
.empty { text-align: center; padding: 200rpx 0; }
.empty-icon { font-size: 80rpx; display: block; }
.empty-text { font-size: 28rpx; color: #999; display: block; margin-top: 20rpx; }
.empty-link { font-size: 28rpx; color: #4CAF50; display: block; margin-top: 20rpx; }
.loading { text-align: center; padding: 100rpx 0; color: #999; }
```

- [ ] **Step 4: 编写成长时间线页面**

```json
// miniprogram/pages/user/timeline/timeline.json
{
  "navigationBarTitleText": "成长记录",
  "usingComponents": {
    "timeline-item": "/components/timeline-item/timeline-item"
  }
}
```

```js
// miniprogram/pages/user/timeline/timeline.js
const { queryList, getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')

const STAGE_LABELS = {
  seeding: '播种',
  sprouting: '发芽',
  growing: '生长中',
  flowering: '开花',
  fruiting: '结果',
  harvested: '收获'
}

Page({
  data: {
    adoption: null,
    vegName: '',
    logs: [],
    loading: true
  },
  async onLoad(options) {
    const adoption = await getById('adoptions', options.id)
    const veg = await getById('vegetables', adoption.vegId)

    this.setData({ adoption, vegName: veg.name })
    this.loadLogs(options.id)
  },
  async loadLogs(adoptionId) {
    this.setData({ loading: true })
    const logs = await queryList('growth_logs',
      { adoptionId },
      { field: 'logDate', order: 'desc' },
      100
    )

    const enriched = logs.map(log => ({
      ...log,
      logDateStr: formatDate(log.logDate),
      stageLabel: STAGE_LABELS[log.stage] || ''
    }))

    this.setData({ logs: enriched, loading: false })
  },
  onPullDownRefresh() {
    this.loadLogs(this.data.adoption._id).then(() => wx.stopPullDownRefresh())
  }
})
```

```xml
<!-- miniprogram/pages/user/timeline/timeline.wxml -->
<view class="timeline-page">
  <view class="tl-header" wx:if="{{adoption}}">
    <text class="tl-veg-name">{{vegName}} · {{adoption.ownerName}}</text>
    <text class="tl-veg-code">{{adoption.code}}</text>
  </view>

  <view class="tl-list" wx:if="{{!loading && logs.length > 0}}">
    <timeline-item wx:for="{{logs}}" wx:key="_id" log="{{item}}" />
  </view>

  <view class="empty" wx:if="{{!loading && logs.length === 0}}">
    <text>暂无成长记录，菜农正在努力拍照中</text>
  </view>

  <view class="loading" wx:if="{{loading}}"><text>加载中...</text></view>
</view>
```

```css
/* miniprogram/pages/user/timeline/timeline.wxss */
.timeline-page { padding: 32rpx; }
.tl-header { margin-bottom: 32rpx; }
.tl-veg-name { font-size: 36rpx; font-weight: bold; display: block; }
.tl-veg-code { font-size: 24rpx; color: #999; display: block; margin-top: 4rpx; }
.empty, .loading { text-align: center; padding: 100rpx 0; color: #999; font-size: 28rpx; }
```

- [ ] **Step 5: 验证我的菜园 → 时间线完整流程**

在模拟器中：
1. 先完成一次认养下单
2. 切换到「我的菜园」Tab，确认认养卡片正确展示
3. 点击「查看成长记录」，确认时间线页面显示系统自动创建的播种记录

- [ ] **Step 6: 提交**

```bash
git add miniprogram/components/adoption-card/ miniprogram/components/timeline-item/ miniprogram/pages/user/garden/ miniprogram/pages/user/timeline/
git commit -m "feat: 我的菜园页面与成长时间线"
```

---

## Task 8: 消息页面

**Files:**
- Create: `miniprogram/pages/user/messages/messages.*`

- [ ] **Step 1: 编写消息页面**

```json
// miniprogram/pages/user/messages/messages.json
{ "navigationBarTitleText": "消息" }
```

```js
// miniprogram/pages/user/messages/messages.js
const { queryList, getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')

Page({
  data: {
    messages: [],
    loading: true
  },
  onShow() {
    this.loadMessages()
  },
  async loadMessages() {
    this.setData({ loading: true })
    const app = getApp()
    const user = app.globalData.userInfo
    if (!user) { this.setData({ loading: false }); return }

    // 从 growth_logs 获取最近的更新记录作为消息
    const { db, _ } = require('../../../utils/db')
    const adoptions = await queryList('adoptions',
      { userId: user.openId },
      { field: 'createdAt', order: 'desc' }
    )

    if (adoptions.length === 0) {
      this.setData({ messages: [], loading: false })
      return
    }

    const adoptionIds = adoptions.map(a => a._id)
    const adoptionMap = {}
    for (const a of adoptions) {
      const veg = await getById('vegetables', a.vegId)
      adoptionMap[a._id] = { ownerName: a.ownerName, vegName: veg.name, code: a.code }
    }

    const logs = await queryList('growth_logs',
      { adoptionId: _.in(adoptionIds) },
      { field: 'logDate', order: 'desc' },
      50
    )

    const messages = logs.map(log => {
      const info = adoptionMap[log.adoptionId] || {}
      return {
        ...log,
        vegName: info.vegName || '',
        ownerName: info.ownerName || '',
        dateStr: formatDate(log.logDate),
        adoptionId: log.adoptionId
      }
    })

    this.setData({ messages, loading: false })
  },
  goToTimeline(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/user/timeline/timeline?id=${id}`
    })
  }
})
```

```xml
<!-- miniprogram/pages/user/messages/messages.wxml -->
<view class="msg-page">
  <view wx:if="{{loading}}" class="loading"><text>加载中...</text></view>

  <view wx:elif="{{messages.length > 0}}" class="msg-list">
    <view
      class="msg-item"
      wx:for="{{messages}}" wx:key="_id"
      data-id="{{item.adoptionId}}"
      bindtap="goToTimeline"
    >
      <image
        class="msg-thumb"
        wx:if="{{item.images.length > 0}}"
        src="{{item.images[0]}}"
        mode="aspectFill"
      />
      <view class="msg-thumb-placeholder" wx:else>🌱</view>
      <view class="msg-content">
        <text class="msg-title">{{item.vegName}} · {{item.ownerName}}</text>
        <text class="msg-text">{{item.text}}</text>
        <text class="msg-date">{{item.dateStr}}</text>
      </view>
    </view>
  </view>

  <view wx:else class="empty">
    <text>暂无消息</text>
  </view>
</view>
```

```css
/* miniprogram/pages/user/messages/messages.wxss */
.msg-page { padding: 20rpx 0; }
.msg-item {
  display: flex; padding: 24rpx 32rpx; background: #fff;
  border-bottom: 1rpx solid #f0f0f0;
}
.msg-thumb { width: 100rpx; height: 100rpx; border-radius: 12rpx; flex-shrink: 0; }
.msg-thumb-placeholder {
  width: 100rpx; height: 100rpx; border-radius: 12rpx;
  background: #E8F5E9; display: flex; align-items: center;
  justify-content: center; font-size: 40rpx; flex-shrink: 0;
}
.msg-content { margin-left: 20rpx; flex: 1; overflow: hidden; }
.msg-title { font-size: 28rpx; font-weight: bold; display: block; }
.msg-text {
  font-size: 26rpx; color: #666; display: block; margin-top: 8rpx;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.msg-date { font-size: 22rpx; color: #999; display: block; margin-top: 8rpx; }
.empty, .loading { text-align: center; padding: 200rpx 0; color: #999; }
```

- [ ] **Step 2: 验证消息列表展示及跳转**

在模拟器中切换到消息 Tab，确认能看到成长记录消息列表，点击跳转到对应的时间线页面。

- [ ] **Step 3: 提交**

```bash
git add miniprogram/pages/user/messages/
git commit -m "feat: 用户端消息页面"
```

---

## Task 9: 用户端「我的」页面与身份切换

**Files:**
- Create: `miniprogram/pages/user/profile/profile.*`

- [ ] **Step 1: 编写「我的」页面**

```json
// miniprogram/pages/user/profile/profile.json
{ "navigationBarTitleText": "我的" }
```

```js
// miniprogram/pages/user/profile/profile.js
const { switchRole, activateFarmerRole } = require('../../../utils/auth')

Page({
  data: {
    userInfo: null,
    isFarmer: false
  },
  onShow() {
    const app = getApp()
    const user = app.globalData.userInfo
    if (user) {
      this.setData({
        userInfo: user,
        isFarmer: user.roles.includes('farmer')
      })
    }
  },
  onGetUserInfo(e) {
    if (e.detail.userInfo) {
      const app = getApp()
      const { db } = require('../../../utils/db')
      db.collection('users').doc(app.globalData.userInfo._id).update({
        data: {
          nickName: e.detail.userInfo.nickName,
          avatar: e.detail.userInfo.avatarUrl
        }
      })
      app.globalData.userInfo.nickName = e.detail.userInfo.nickName
      app.globalData.userInfo.avatar = e.detail.userInfo.avatarUrl
      this.setData({ userInfo: app.globalData.userInfo })
    }
  },
  goToOrders() {
    wx.navigateTo({ url: '/pages/common/orders/orders' })
  },
  async onSwitchToFarmer() {
    if (this.data.isFarmer) {
      await switchRole('farmer')
    } else {
      // 弹出邀请码输入
      const self = this
      wx.showModal({
        title: '激活菜农身份',
        content: '请输入邀请码',
        editable: true,
        placeholderText: '请输入邀请码',
        async success(res) {
          if (res.confirm && res.content) {
            try {
              await activateFarmerRole(res.content.trim())
              wx.showToast({ title: '激活成功', icon: 'success' })
              self.setData({ isFarmer: true })
              setTimeout(() => switchRole('farmer'), 1500)
            } catch (err) {
              wx.showToast({ title: err.message, icon: 'none' })
            }
          }
        }
      })
    }
  },
  onContactService() {
    // 微信客服由小程序后台配置，使用 button open-type="contact" 触发
  }
})
```

```xml
<!-- miniprogram/pages/user/profile/profile.wxml -->
<view class="profile">
  <view class="user-header">
    <image class="avatar" src="{{userInfo.avatar || '/images/default-avatar.png'}}" />
    <view class="user-info">
      <text class="nickname">{{userInfo.nickName || '点击登录'}}</text>
    </view>
    <button wx:if="{{!userInfo.nickName}}" class="login-btn" open-type="getUserInfo" bindgetuserinfo="onGetUserInfo">获取头像昵称</button>
  </view>

  <view class="menu-list">
    <view class="menu-item" bindtap="goToOrders">
      <text>我的订单</text>
      <text class="menu-arrow">></text>
    </view>
    <view class="menu-item" bindtap="onSwitchToFarmer">
      <text>{{isFarmer ? '切换为菜农身份' : '成为菜农（需邀请码）'}}</text>
      <text class="menu-arrow">></text>
    </view>
    <button class="menu-item contact-btn" open-type="contact">
      <text>联系客服</text>
      <text class="menu-arrow">></text>
    </button>
    <view class="menu-item">
      <text>关于我们</text>
      <text class="menu-arrow">></text>
    </view>
  </view>
</view>
```

```css
/* miniprogram/pages/user/profile/profile.wxss */
.profile { padding-top: 40rpx; }
.user-header {
  display: flex; align-items: center; padding: 32rpx;
  background: #fff; margin-bottom: 20rpx;
}
.avatar { width: 120rpx; height: 120rpx; border-radius: 50%; background: #eee; }
.user-info { margin-left: 24rpx; flex: 1; }
.nickname { font-size: 34rpx; font-weight: bold; }
.login-btn { font-size: 24rpx !important; padding: 0 20rpx !important; }
.menu-list { background: #fff; }
.menu-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 32rpx; border-bottom: 1rpx solid #f0f0f0;
  font-size: 30rpx;
}
.menu-arrow { color: #ccc; font-size: 28rpx; }
.contact-btn {
  background: transparent !important; text-align: left !important;
  border-radius: 0 !important; margin: 0 !important;
  line-height: normal !important; font-size: 30rpx !important;
}
```

- [ ] **Step 2: 验证身份切换流程**

在模拟器中：
1. 进入「我的」页面，点击「成为菜农」
2. 输入邀请码 `FARMER2026`，确认激活成功
3. 自动跳转到菜农端工作台

- [ ] **Step 3: 提交**

```bash
git add miniprogram/pages/user/profile/
git commit -m "feat: 用户端我的页面与身份切换"
```

---

## Task 10: 菜农端工作台

**Files:**
- Create: `miniprogram/pages/farmer/workbench/workbench.*`

- [ ] **Step 1: 编写工作台页面**

```json
// miniprogram/pages/farmer/workbench/workbench.json
{
  "navigationBarTitleText": "工作台",
  "navigationBarBackgroundColor": "#E91E63",
  "usingComponents": {
    "farmer-tabbar": "/components/farmer-tabbar/farmer-tabbar"
  }
}
```

```js
// miniprogram/pages/farmer/workbench/workbench.js
const { queryList, db, _ } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')

Page({
  data: {
    todayStats: { pending: 0, done: 0, newOrders: 0 },
    pendingPhotos: [],
    newOrders: [],
    loading: true
  },
  onShow() {
    this.loadWorkbench()
  },
  async loadWorkbench() {
    this.setData({ loading: true })
    const today = formatDate(new Date())

    // 获取所有 growing 状态的认养
    const adoptions = await queryList('adoptions',
      { status: 'growing' },
      { field: 'createdAt', order: 'desc' },
      100
    )

    // 获取今天已拍照的认养IDs
    const todayLogs = await queryList('growth_logs',
      { logDate: db.RegExp({ regexp: today }) },
      null, 100
    )
    const doneIds = new Set(todayLogs.map(l => l.adoptionId))

    // 关联菜品信息
    const { getById } = require('../../../utils/db')
    const enriched = await Promise.all(adoptions.map(async (a) => {
      const veg = await getById('vegetables', a.vegId)
      return { ...a, vegName: veg.name, hasTodayLog: doneIds.has(a._id) }
    }))

    const pending = enriched.filter(a => !a.hasTodayLog)
    const done = enriched.filter(a => a.hasTodayLog)

    // 新订单（paid 状态，等待确认播种）
    const newOrders = await queryList('adoptions',
      { status: 'paid' },
      { field: 'createdAt', order: 'desc' }
    )

    this.setData({
      todayStats: { pending: pending.length, done: done.length, newOrders: newOrders.length },
      pendingPhotos: pending,
      newOrders,
      loading: false
    })
  },
  goToPhoto(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/farmer/photoUpload/photoUpload?id=${id}`
    })
  },
  async confirmOrder(e) {
    const id = e.currentTarget.dataset.id
    const { updateRecord } = require('../../../utils/db')
    await updateRecord('adoptions', id, { status: 'growing' })
    wx.showToast({ title: '已确认播种', icon: 'success' })
    this.loadWorkbench()
  }
})
```

```xml
<!-- miniprogram/pages/farmer/workbench/workbench.wxml -->
<view class="workbench">
  <view class="stats-bar">
    <view class="stat-item">
      <text class="stat-num">{{todayStats.pending}}</text>
      <text class="stat-label">待拍照</text>
    </view>
    <view class="stat-item">
      <text class="stat-num done">{{todayStats.done}}</text>
      <text class="stat-label">已完成</text>
    </view>
    <view class="stat-item" wx:if="{{todayStats.newOrders > 0}}">
      <text class="stat-num warn">{{todayStats.newOrders}}</text>
      <text class="stat-label">新订单</text>
    </view>
  </view>

  <!-- 新订单提醒 -->
  <view class="section" wx:if="{{newOrders.length > 0}}">
    <text class="section-title">新订单</text>
    <view class="order-item" wx:for="{{newOrders}}" wx:key="_id">
      <view class="order-info">
        <text class="order-name">{{item.ownerName}}</text>
        <text class="order-code">{{item.code}} · {{item.planType === 'trial' ? '尝鲜装' : '季度装'}}</text>
      </view>
      <button class="confirm-btn" data-id="{{item._id}}" bindtap="confirmOrder">确认播种</button>
    </view>
  </view>

  <!-- 待拍照列表 -->
  <view class="section">
    <text class="section-title">待拍照 ({{pendingPhotos.length}})</text>
    <view class="photo-item" wx:for="{{pendingPhotos}}" wx:key="_id" data-id="{{item._id}}" bindtap="goToPhoto">
      <view class="photo-info">
        <text class="photo-veg">{{item.vegName}}</text>
        <text class="photo-owner">{{item.ownerName}} · {{item.code}}</text>
      </view>
      <text class="photo-arrow">📷</text>
    </view>
    <view class="empty-section" wx:if="{{pendingPhotos.length === 0 && !loading}}">
      <text>今天的拍照任务都完成了 👍</text>
    </view>
  </view>
</view>
<farmer-tabbar active="{{0}}" />
```

```css
/* miniprogram/pages/farmer/workbench/workbench.wxss */
.workbench { padding-bottom: 140rpx; }
.stats-bar {
  display: flex; background: linear-gradient(135deg, #E91E63, #F06292);
  padding: 40rpx; color: #fff;
}
.stat-item { flex: 1; text-align: center; }
.stat-num { font-size: 48rpx; font-weight: bold; display: block; }
.stat-num.done { color: #C8E6C9; }
.stat-num.warn { color: #FFE082; }
.stat-label { font-size: 22rpx; opacity: 0.8; display: block; margin-top: 4rpx; }
.section { padding: 24rpx 32rpx; }
.section-title { font-size: 30rpx; font-weight: bold; display: block; margin-bottom: 16rpx; }
.photo-item {
  display: flex; justify-content: space-between; align-items: center;
  background: #fff; padding: 24rpx; border-radius: 12rpx; margin-bottom: 12rpx;
}
.photo-info { flex: 1; }
.photo-veg { font-size: 30rpx; font-weight: bold; display: block; }
.photo-owner { font-size: 24rpx; color: #999; display: block; margin-top: 4rpx; }
.photo-arrow { font-size: 36rpx; }
.order-item {
  display: flex; justify-content: space-between; align-items: center;
  background: #fff; padding: 24rpx; border-radius: 12rpx; margin-bottom: 12rpx;
}
.order-info { flex: 1; }
.order-name { font-size: 30rpx; font-weight: bold; display: block; }
.order-code { font-size: 24rpx; color: #999; display: block; margin-top: 4rpx; }
.confirm-btn {
  background: #E91E63 !important; color: #fff !important;
  font-size: 24rpx !important; padding: 0 24rpx !important;
  border-radius: 20rpx !important; line-height: 60rpx !important;
}
.empty-section { text-align: center; padding: 40rpx; color: #999; font-size: 26rpx; }
```

- [ ] **Step 2: 验证工作台展示**

切换到菜农身份后，确认工作台显示：今日统计、新订单列表、待拍照列表。

- [ ] **Step 3: 提交**

```bash
git add miniprogram/pages/farmer/workbench/
git commit -m "feat: 菜农端工作台页面"
```

---

## Task 11: 菜农端拍照上传页

**Files:**
- Create: `miniprogram/pages/farmer/photoUpload/photoUpload.*`
- Create: `miniprogram/components/quick-phrases/quick-phrases.*`

- [ ] **Step 1: 编写快捷短语组件**

```json
// miniprogram/components/quick-phrases/quick-phrases.json
{ "component": true }
```

```js
// miniprogram/components/quick-phrases/quick-phrases.js
Component({
  data: {
    phrases: ['今日浇水', '长势良好', '施肥一次', '开始发芽', '阳光充足', '修剪枝叶', '病虫防治']
  },
  methods: {
    onTap(e) {
      const text = e.currentTarget.dataset.text
      this.triggerEvent('select', { text })
    }
  }
})
```

```xml
<!-- miniprogram/components/quick-phrases/quick-phrases.wxml -->
<view class="phrases">
  <view
    class="phrase-tag"
    wx:for="{{phrases}}" wx:key="*this"
    data-text="{{item}}"
    bindtap="onTap"
  >{{item}}</view>
</view>
```

```css
/* miniprogram/components/quick-phrases/quick-phrases.wxss */
.phrases { display: flex; flex-wrap: wrap; gap: 12rpx; }
.phrase-tag {
  background: #FCE4EC; color: #E91E63;
  padding: 8rpx 20rpx; border-radius: 20rpx;
  font-size: 24rpx;
}
```

- [ ] **Step 2: 编写拍照上传页**

```json
// miniprogram/pages/farmer/photoUpload/photoUpload.json
{
  "navigationBarTitleText": "拍照上传",
  "navigationBarBackgroundColor": "#E91E63",
  "usingComponents": {
    "quick-phrases": "/components/quick-phrases/quick-phrases"
  }
}
```

```js
// miniprogram/pages/farmer/photoUpload/photoUpload.js
const { getById, addRecord } = require('../../../utils/db')
const { daysBetween, formatDate } = require('../../../utils/date')

const STAGES = [
  { value: '', label: '不变更' },
  { value: 'seeding', label: '播种' },
  { value: 'sprouting', label: '发芽' },
  { value: 'growing', label: '生长中' },
  { value: 'flowering', label: '开花' },
  { value: 'fruiting', label: '结果' },
  { value: 'harvested', label: '收获' }
]

Page({
  data: {
    adoption: null,
    vegName: '',
    growDays: 0,
    images: [],
    text: '',
    stage: '',
    stages: STAGES,
    stageIndex: 0,
    submitting: false
  },
  async onLoad(options) {
    const adoption = await getById('adoptions', options.id)
    const veg = await getById('vegetables', adoption.vegId)
    this.setData({
      adoption,
      vegName: veg.name,
      growDays: daysBetween(adoption.startDate, Date.now())
    })
  },
  chooseImage() {
    const remaining = 9 - this.data.images.length
    if (remaining <= 0) {
      wx.showToast({ title: '最多9张', icon: 'none' })
      return
    }
    wx.chooseMedia({
      count: remaining,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      camera: 'back',
      success: (res) => {
        const newImages = res.tempFiles.map(f => f.tempFilePath)
        this.setData({ images: [...this.data.images, ...newImages] })
      }
    })
  },
  removeImage(e) {
    const index = e.currentTarget.dataset.index
    const images = [...this.data.images]
    images.splice(index, 1)
    this.setData({ images })
  },
  onTextInput(e) {
    this.setData({ text: e.detail.value })
  },
  onPhraseSelect(e) {
    const phrase = e.detail.text
    const current = this.data.text
    this.setData({ text: current ? `${current}，${phrase}` : phrase })
  },
  onStageChange(e) {
    const index = e.detail.value
    this.setData({ stageIndex: index, stage: STAGES[index].value })
  },
  async onSubmit() {
    const { images, text, adoption, submitting } = this.data
    if (submitting) return
    if (images.length === 0) {
      wx.showToast({ title: '请至少拍一张照片', icon: 'none' })
      return
    }

    this.setData({ submitting: true })
    try {
      // 上传图片到云存储
      const uploadedUrls = []
      for (const img of images) {
        const ext = img.split('.').pop()
        const cloudPath = `growth/${adoption._id}/${Date.now()}_${Math.random().toString(36).slice(2)}.${ext}`
        const uploadRes = await wx.cloud.uploadFile({
          cloudPath,
          filePath: img
        })
        uploadedUrls.push(uploadRes.fileID)
      }

      // 创建成长记录
      await addRecord('growth_logs', {
        adoptionId: adoption._id,
        images: uploadedUrls,
        text: text.trim(),
        stage: this.data.stage || null,
        logDate: formatDate(new Date()),
        farmerId: getApp().globalData.userInfo.openId,
        createdAt: new Date()
      })

      wx.showToast({ title: '上传成功', icon: 'success' })
      setTimeout(() => wx.navigateBack(), 1500)
    } catch (err) {
      console.error('上传失败:', err)
      wx.showToast({ title: '上传失败，请重试', icon: 'none' })
    } finally {
      this.setData({ submitting: false })
    }
  }
})
```

```xml
<!-- miniprogram/pages/farmer/photoUpload/photoUpload.wxml -->
<view class="upload-page" wx:if="{{adoption}}">
  <view class="info-bar">
    <text class="info-veg">{{vegName}}</text>
    <text class="info-detail">{{adoption.ownerName}} · {{adoption.code}} · 第{{growDays}}天</text>
  </view>

  <view class="section">
    <text class="section-label">拍照（{{images.length}}/9）</text>
    <view class="image-grid">
      <view class="img-wrapper" wx:for="{{images}}" wx:key="*this">
        <image class="img-preview" src="{{item}}" mode="aspectFill" />
        <view class="img-remove" data-index="{{index}}" bindtap="removeImage">×</view>
      </view>
      <view class="img-add" bindtap="chooseImage" wx:if="{{images.length < 9}}">
        <text class="add-icon">📷</text>
        <text class="add-text">拍照/相册</text>
      </view>
    </view>
  </view>

  <view class="section">
    <text class="section-label">写点什么</text>
    <textarea
      class="text-input"
      placeholder="记录今天的种植情况..."
      value="{{text}}"
      bindinput="onTextInput"
      maxlength="500"
    />
    <quick-phrases bind:select="onPhraseSelect" />
  </view>

  <view class="section">
    <text class="section-label">阶段变更（可选）</text>
    <picker bindchange="onStageChange" value="{{stageIndex}}" range="{{stages}}" range-key="label">
      <view class="stage-picker">
        {{stages[stageIndex].label}}
        <text class="picker-arrow">▼</text>
      </view>
    </picker>
  </view>

  <button class="submit-btn" disabled="{{submitting}}" bindtap="onSubmit">
    {{submitting ? '上传中...' : '提交'}}
  </button>
</view>
```

```css
/* miniprogram/pages/farmer/photoUpload/photoUpload.wxss */
.upload-page { padding: 0 32rpx 32rpx; }
.info-bar {
  background: linear-gradient(135deg, #E91E63, #F06292);
  margin: 0 -32rpx; padding: 32rpx;
  color: #fff;
}
.info-veg { font-size: 36rpx; font-weight: bold; display: block; }
.info-detail { font-size: 24rpx; opacity: 0.8; display: block; margin-top: 8rpx; }
.section { margin-top: 32rpx; }
.section-label { font-size: 28rpx; font-weight: bold; display: block; margin-bottom: 16rpx; }
.image-grid { display: flex; flex-wrap: wrap; gap: 12rpx; }
.img-wrapper { position: relative; width: 200rpx; height: 200rpx; }
.img-preview { width: 100%; height: 100%; border-radius: 8rpx; }
.img-remove {
  position: absolute; top: -10rpx; right: -10rpx;
  width: 40rpx; height: 40rpx; border-radius: 50%;
  background: rgba(0,0,0,0.6); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 24rpx;
}
.img-add {
  width: 200rpx; height: 200rpx; border: 2rpx dashed #ccc;
  border-radius: 8rpx; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
}
.add-icon { font-size: 48rpx; }
.add-text { font-size: 22rpx; color: #999; margin-top: 8rpx; }
.text-input {
  width: 100%; height: 200rpx; border: 2rpx solid #eee;
  border-radius: 12rpx; padding: 20rpx; font-size: 28rpx;
  margin-bottom: 16rpx; box-sizing: border-box;
}
.stage-picker {
  background: #fff; border: 2rpx solid #eee; border-radius: 12rpx;
  padding: 20rpx 24rpx; display: flex; justify-content: space-between;
}
.picker-arrow { color: #999; }
.submit-btn {
  margin-top: 40rpx; background: #E91E63 !important;
  color: #fff !important; border-radius: 40rpx !important;
}
.submit-btn[disabled] { background: #ccc !important; }
```

- [ ] **Step 3: 验证拍照上传流程**

在模拟器中：
1. 从工作台点击待拍照菜品 → 进入拍照上传页
2. 拍照/选择图片，填写日志，选择快捷短语
3. 提交成功后返回工作台，待拍照数量减 1
4. 切换到用户端查看时间线，确认新记录出现

- [ ] **Step 4: 提交**

```bash
git add miniprogram/components/quick-phrases/ miniprogram/pages/farmer/photoUpload/
git commit -m "feat: 菜农端拍照上传页面与快捷短语组件"
```

---

## Task 12: 菜农端菜地管理

**Files:**
- Create: `miniprogram/pages/farmer/fieldManage/fieldManage.*`
- Create: `miniprogram/pages/farmer/vegEdit/vegEdit.*`

- [ ] **Step 1: 编写菜地管理页面**

```json
// miniprogram/pages/farmer/fieldManage/fieldManage.json
{
  "navigationBarTitleText": "菜地管理",
  "navigationBarBackgroundColor": "#E91E63",
  "usingComponents": {
    "farmer-tabbar": "/components/farmer-tabbar/farmer-tabbar"
  }
}
```

```js
// miniprogram/pages/farmer/fieldManage/fieldManage.js
const { queryList, getById, updateRecord } = require('../../../utils/db')

Page({
  data: {
    tab: 'vegetables', // vegetables | adoptions
    vegetables: [],
    adoptions: [],
    adoptionFilter: 'all',
    loading: true
  },
  onShow() {
    this.loadData()
  },
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({ tab })
  },
  async loadData() {
    this.setData({ loading: true })

    const vegetables = await queryList('vegetables', {}, { field: 'createdAt', order: 'desc' }, 100)

    const adoptions = await queryList('adoptions',
      {},
      { field: 'createdAt', order: 'desc' },
      100
    )
    const enriched = await Promise.all(adoptions.map(async (a) => {
      const veg = await getById('vegetables', a.vegId)
      return { ...a, vegName: veg.name }
    }))

    this.setData({ vegetables, adoptions: enriched, loading: false })
  },
  goToAddVeg() {
    wx.navigateTo({ url: '/pages/farmer/vegEdit/vegEdit' })
  },
  goToEditVeg(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/farmer/vegEdit/vegEdit?id=${id}` })
  },
  filterAdoptions(e) {
    this.setData({ adoptionFilter: e.currentTarget.dataset.filter })
  },
  async markHarvested(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({
      title: '确认收获',
      content: '标记为已收获后将通知用户',
      success: async (res) => {
        if (res.confirm) {
          await updateRecord('adoptions', id, { status: 'harvested' })
          wx.showToast({ title: '已标记收获', icon: 'success' })
          this.loadData()
        }
      }
    })
  }
})
```

```xml
<!-- miniprogram/pages/farmer/fieldManage/fieldManage.wxml -->
<view class="field-manage">
  <view class="tab-bar">
    <view class="tab {{tab === 'vegetables' ? 'active' : ''}}" data-tab="vegetables" bindtap="switchTab">菜品管理</view>
    <view class="tab {{tab === 'adoptions' ? 'active' : ''}}" data-tab="adoptions" bindtap="switchTab">认养列表</view>
  </view>

  <!-- 菜品管理 -->
  <view wx:if="{{tab === 'vegetables'}}">
    <button class="add-btn" bindtap="goToAddVeg">+ 新增菜品</button>
    <view class="list">
      <view class="list-item" wx:for="{{vegetables}}" wx:key="_id" data-id="{{item._id}}" bindtap="goToEditVeg">
        <image class="list-thumb" src="{{item.coverImage}}" mode="aspectFill" />
        <view class="list-info">
          <text class="list-name">{{item.name}}</text>
          <text class="list-meta">库存: {{item.stock}} · ¥{{item.price.trial}}起</text>
          <text class="list-status {{item.status === 'on_sale' ? 'on' : 'off'}}">
            {{item.status === 'on_sale' ? '上架中' : (item.status === 'off_shelf' ? '已下架' : '已认满')}}
          </text>
        </view>
        <text class="list-arrow">></text>
      </view>
    </view>
  </view>

  <!-- 认养列表 -->
  <view wx:if="{{tab === 'adoptions'}}">
    <view class="filter-bar">
      <view class="filter {{adoptionFilter === 'all' ? 'active' : ''}}" data-filter="all" bindtap="filterAdoptions">全部</view>
      <view class="filter {{adoptionFilter === 'growing' ? 'active' : ''}}" data-filter="growing" bindtap="filterAdoptions">生长中</view>
      <view class="filter {{adoptionFilter === 'harvested' ? 'active' : ''}}" data-filter="harvested" bindtap="filterAdoptions">已收获</view>
    </view>
    <view class="list">
      <block wx:for="{{adoptions}}" wx:key="_id">
        <view class="list-item" wx:if="{{adoptionFilter === 'all' || item.status === adoptionFilter}}">
          <view class="list-info" style="flex:1">
            <text class="list-name">{{item.vegName}} · {{item.ownerName}}</text>
            <text class="list-meta">{{item.code}} · {{item.planType === 'trial' ? '尝鲜装' : '季度装'}}</text>
            <text class="list-status {{item.status === 'growing' ? 'on' : 'off'}}">
              {{item.status === 'growing' ? '生长中' : '已收获'}}
            </text>
          </view>
          <button
            wx:if="{{item.status === 'growing'}}"
            class="harvest-btn"
            data-id="{{item._id}}"
            catchtap="markHarvested"
          >标记收获</button>
        </view>
      </block>
    </view>
  </view>
</view>
<farmer-tabbar active="{{1}}" />
```

```css
/* miniprogram/pages/farmer/fieldManage/fieldManage.wxss */
.field-manage { padding-bottom: 140rpx; }
.tab-bar { display: flex; background: #fff; border-bottom: 1rpx solid #eee; }
.tab {
  flex: 1; text-align: center; padding: 24rpx; font-size: 30rpx; color: #666;
  border-bottom: 4rpx solid transparent;
}
.tab.active { color: #E91E63; border-bottom-color: #E91E63; font-weight: bold; }
.add-btn {
  margin: 20rpx 32rpx; background: #E91E63 !important; color: #fff !important;
  border-radius: 12rpx !important; font-size: 28rpx !important;
}
.list { padding: 0 32rpx; }
.list-item {
  display: flex; align-items: center; background: #fff;
  padding: 20rpx; border-radius: 12rpx; margin-top: 12rpx;
}
.list-thumb { width: 100rpx; height: 100rpx; border-radius: 8rpx; margin-right: 16rpx; flex-shrink: 0; }
.list-info { flex: 1; }
.list-name { font-size: 28rpx; font-weight: bold; display: block; }
.list-meta { font-size: 22rpx; color: #999; display: block; margin-top: 4rpx; }
.list-status { font-size: 20rpx; display: inline-block; margin-top: 4rpx; padding: 2rpx 12rpx; border-radius: 20rpx; }
.list-status.on { background: #E8F5E9; color: #4CAF50; }
.list-status.off { background: #f5f5f5; color: #999; }
.list-arrow { color: #ccc; font-size: 28rpx; }
.filter-bar { display: flex; padding: 16rpx 32rpx; gap: 16rpx; }
.filter {
  padding: 8rpx 24rpx; border-radius: 20rpx; font-size: 24rpx;
  background: #f5f5f5; color: #666;
}
.filter.active { background: #FCE4EC; color: #E91E63; }
.harvest-btn {
  background: #FF9800 !important; color: #fff !important;
  font-size: 22rpx !important; padding: 0 20rpx !important;
  border-radius: 20rpx !important; line-height: 56rpx !important;
}
```

- [ ] **Step 2: 编写菜品编辑页**

```json
// miniprogram/pages/farmer/vegEdit/vegEdit.json
{
  "navigationBarTitleText": "编辑菜品",
  "navigationBarBackgroundColor": "#E91E63"
}
```

```js
// miniprogram/pages/farmer/vegEdit/vegEdit.js
const { getById, addRecord, updateRecord } = require('../../../utils/db')

Page({
  data: {
    id: '',
    name: '',
    desc: '',
    coverImage: '',
    priceTrial: 39,
    priceQuarterly: 99,
    durationTrial: 30,
    durationQuarterly: 90,
    stock: 10,
    growthInfo: '',
    status: 'on_sale',
    submitting: false
  },
  async onLoad(options) {
    if (options.id) {
      const veg = await getById('vegetables', options.id)
      this.setData({
        id: options.id,
        name: veg.name,
        desc: veg.desc,
        coverImage: veg.coverImage,
        priceTrial: veg.price.trial,
        priceQuarterly: veg.price.quarterly,
        durationTrial: veg.duration.trial,
        durationQuarterly: veg.duration.quarterly,
        stock: veg.stock,
        growthInfo: veg.growthInfo,
        status: veg.status
      })
      wx.setNavigationBarTitle({ title: '编辑菜品' })
    } else {
      wx.setNavigationBarTitle({ title: '新增菜品' })
    }
  },
  onInput(e) {
    const field = e.currentTarget.dataset.field
    this.setData({ [field]: e.detail.value })
  },
  chooseCover() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      success: async (res) => {
        const tempPath = res.tempFiles[0].tempFilePath
        const ext = tempPath.split('.').pop()
        const cloudPath = `vegetables/${Date.now()}.${ext}`
        const uploadRes = await wx.cloud.uploadFile({ cloudPath, filePath: tempPath })
        this.setData({ coverImage: uploadRes.fileID })
      }
    })
  },
  async onSubmit() {
    const { id, name, desc, coverImage, priceTrial, priceQuarterly,
            durationTrial, durationQuarterly, stock, growthInfo, status, submitting } = this.data
    if (submitting) return
    if (!name.trim() || !coverImage) {
      wx.showToast({ title: '请填写名称和封面图', icon: 'none' })
      return
    }

    this.setData({ submitting: true })
    const vegData = {
      name: name.trim(),
      desc: desc.trim(),
      coverImage,
      price: { trial: Number(priceTrial), quarterly: Number(priceQuarterly) },
      duration: { trial: Number(durationTrial), quarterly: Number(durationQuarterly) },
      stock: Number(stock),
      growthInfo: growthInfo.trim(),
      status
    }

    try {
      if (id) {
        await updateRecord('vegetables', id, vegData)
      } else {
        vegData.createdAt = new Date()
        await addRecord('vegetables', vegData)
      }
      wx.showToast({ title: '保存成功', icon: 'success' })
      setTimeout(() => wx.navigateBack(), 1500)
    } catch (err) {
      wx.showToast({ title: '保存失败', icon: 'none' })
    } finally {
      this.setData({ submitting: false })
    }
  },
  toggleStatus() {
    this.setData({
      status: this.data.status === 'on_sale' ? 'off_shelf' : 'on_sale'
    })
  }
})
```

```xml
<!-- miniprogram/pages/farmer/vegEdit/vegEdit.wxml -->
<view class="veg-edit">
  <view class="form-item">
    <text class="form-label">菜品名称</text>
    <input class="form-input" value="{{name}}" data-field="name" bindinput="onInput" placeholder="如：小番茄" />
  </view>

  <view class="form-item">
    <text class="form-label">菜品介绍</text>
    <textarea class="form-textarea" value="{{desc}}" data-field="desc" bindinput="onInput" placeholder="简要介绍..." />
  </view>

  <view class="form-item">
    <text class="form-label">封面图</text>
    <view class="cover-picker" bindtap="chooseCover">
      <image wx:if="{{coverImage}}" class="cover-preview" src="{{coverImage}}" mode="aspectFill" />
      <view wx:else class="cover-placeholder">点击上传</view>
    </view>
  </view>

  <view class="form-item">
    <text class="form-label">种植说明</text>
    <textarea class="form-textarea" value="{{growthInfo}}" data-field="growthInfo" bindinput="onInput" placeholder="种植注意事项..." />
  </view>

  <view class="form-row">
    <view class="form-item half">
      <text class="form-label">尝鲜装价格(元)</text>
      <input class="form-input" type="digit" value="{{priceTrial}}" data-field="priceTrial" bindinput="onInput" />
    </view>
    <view class="form-item half">
      <text class="form-label">季度装价格(元)</text>
      <input class="form-input" type="digit" value="{{priceQuarterly}}" data-field="priceQuarterly" bindinput="onInput" />
    </view>
  </view>

  <view class="form-row">
    <view class="form-item half">
      <text class="form-label">尝鲜装周期(天)</text>
      <input class="form-input" type="number" value="{{durationTrial}}" data-field="durationTrial" bindinput="onInput" />
    </view>
    <view class="form-item half">
      <text class="form-label">季度装周期(天)</text>
      <input class="form-input" type="number" value="{{durationQuarterly}}" data-field="durationQuarterly" bindinput="onInput" />
    </view>
  </view>

  <view class="form-item">
    <text class="form-label">库存数量</text>
    <input class="form-input" type="number" value="{{stock}}" data-field="stock" bindinput="onInput" />
  </view>

  <view class="form-item" wx:if="{{id}}">
    <view class="status-toggle" bindtap="toggleStatus">
      <text>状态：{{status === 'on_sale' ? '上架中' : '已下架'}}</text>
      <text class="toggle-btn">切换</text>
    </view>
  </view>

  <button class="submit-btn" disabled="{{submitting}}" bindtap="onSubmit">
    {{submitting ? '保存中...' : '保存'}}
  </button>
</view>
```

```css
/* miniprogram/pages/farmer/vegEdit/vegEdit.wxss */
.veg-edit { padding: 32rpx; }
.form-item { margin-bottom: 28rpx; }
.form-label { font-size: 26rpx; font-weight: bold; display: block; margin-bottom: 8rpx; }
.form-input {
  border: 2rpx solid #eee; border-radius: 12rpx;
  padding: 16rpx 20rpx; font-size: 28rpx;
}
.form-textarea {
  border: 2rpx solid #eee; border-radius: 12rpx;
  padding: 16rpx 20rpx; font-size: 28rpx;
  width: 100%; height: 160rpx; box-sizing: border-box;
}
.form-row { display: flex; gap: 20rpx; }
.form-item.half { flex: 1; }
.cover-picker { width: 200rpx; height: 200rpx; }
.cover-preview { width: 100%; height: 100%; border-radius: 12rpx; }
.cover-placeholder {
  width: 100%; height: 100%; border: 2rpx dashed #ccc;
  border-radius: 12rpx; display: flex; align-items: center;
  justify-content: center; color: #999; font-size: 24rpx;
}
.status-toggle {
  display: flex; justify-content: space-between; align-items: center;
  background: #f5f5f5; padding: 20rpx; border-radius: 12rpx;
}
.toggle-btn { color: #E91E63; font-size: 26rpx; }
.submit-btn {
  margin-top: 40rpx; background: #E91E63 !important;
  color: #fff !important; border-radius: 40rpx !important;
}
.submit-btn[disabled] { background: #ccc !important; }
```

- [ ] **Step 3: 验证菜地管理完整流程**

1. 菜品管理：新增菜品 → 填写信息 → 保存 → 列表中出现
2. 编辑菜品：点击已有菜品 → 修改信息 → 保存
3. 认养列表：按状态筛选 → 标记收获

- [ ] **Step 4: 提交**

```bash
git add miniprogram/pages/farmer/fieldManage/ miniprogram/pages/farmer/vegEdit/
git commit -m "feat: 菜农端菜地管理与菜品编辑"
```

---

## Task 13: 菜农端「我的」页面

**Files:**
- Create: `miniprogram/pages/farmer/farmerProfile/farmerProfile.*`

- [ ] **Step 1: 编写菜农端我的页面**

```json
// miniprogram/pages/farmer/farmerProfile/farmerProfile.json
{
  "navigationBarTitleText": "我的",
  "navigationBarBackgroundColor": "#E91E63",
  "usingComponents": {
    "farmer-tabbar": "/components/farmer-tabbar/farmer-tabbar"
  }
}
```

```js
// miniprogram/pages/farmer/farmerProfile/farmerProfile.js
const { switchRole } = require('../../../utils/auth')
const { queryList } = require('../../../utils/db')

Page({
  data: {
    userInfo: null,
    stats: { photoCount: 0, vegCount: 0 }
  },
  async onShow() {
    const app = getApp()
    this.setData({ userInfo: app.globalData.userInfo })
    this.loadStats()
  },
  async loadStats() {
    const app = getApp()
    const farmerId = app.globalData.userInfo.openId

    const logs = await queryList('growth_logs', { farmerId }, null, 1)
    const { db } = require('../../../utils/db')
    const logCount = await db.collection('growth_logs').where({ farmerId }).count()
    const vegCount = await db.collection('vegetables').count()

    this.setData({
      stats: {
        photoCount: logCount.total,
        vegCount: vegCount.total
      }
    })
  },
  async onSwitchToUser() {
    await switchRole('user')
  }
})
```

```xml
<!-- miniprogram/pages/farmer/farmerProfile/farmerProfile.wxml -->
<view class="farmer-profile">
  <view class="profile-header">
    <image class="avatar" src="{{userInfo.avatar || '/images/default-avatar.png'}}" />
    <text class="nickname">{{userInfo.nickName || '菜农'}}</text>
  </view>

  <view class="stats-bar">
    <view class="stat">
      <text class="stat-num">{{stats.photoCount}}</text>
      <text class="stat-label">累计拍照</text>
    </view>
    <view class="stat">
      <text class="stat-num">{{stats.vegCount}}</text>
      <text class="stat-label">管理菜品</text>
    </view>
  </view>

  <view class="menu-list">
    <view class="menu-item" bindtap="onSwitchToUser">
      <text>切换为用户身份</text>
      <text class="menu-arrow">></text>
    </view>
    <button class="menu-item contact-btn" open-type="contact">
      <text>联系平台</text>
      <text class="menu-arrow">></text>
    </button>
  </view>
</view>
<farmer-tabbar active="{{2}}" />
```

```css
/* miniprogram/pages/farmer/farmerProfile/farmerProfile.wxss */
.farmer-profile { padding-bottom: 140rpx; }
.profile-header {
  display: flex; flex-direction: column; align-items: center;
  padding: 60rpx 32rpx; background: linear-gradient(135deg, #E91E63, #F06292);
  color: #fff;
}
.avatar { width: 140rpx; height: 140rpx; border-radius: 50%; border: 4rpx solid rgba(255,255,255,0.5); }
.nickname { font-size: 34rpx; font-weight: bold; margin-top: 16rpx; }
.stats-bar { display: flex; background: #fff; padding: 32rpx; margin-bottom: 20rpx; }
.stat { flex: 1; text-align: center; }
.stat-num { font-size: 40rpx; font-weight: bold; color: #E91E63; display: block; }
.stat-label { font-size: 22rpx; color: #999; display: block; margin-top: 4rpx; }
.menu-list { background: #fff; }
.menu-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 32rpx; border-bottom: 1rpx solid #f0f0f0; font-size: 30rpx;
}
.menu-arrow { color: #ccc; }
.contact-btn {
  background: transparent !important; text-align: left !important;
  border-radius: 0 !important; margin: 0 !important;
  line-height: normal !important; font-size: 30rpx !important;
}
```

- [ ] **Step 2: 验证菜农端 → 用户端切换**

点击「切换为用户身份」，确认跳转到用户端首页，底部 Tab 恢复为用户端导航。

- [ ] **Step 3: 提交**

```bash
git add miniprogram/pages/farmer/farmerProfile/
git commit -m "feat: 菜农端我的页面与身份切换"
```

---

## Task 14: 订单页面（用户端共用）

**Files:**
- Create: `miniprogram/pages/common/orders/orders.*`
- Create: `miniprogram/pages/common/orderDetail/orderDetail.*`

- [ ] **Step 1: 编写订单列表页面**

```json
// miniprogram/pages/common/orders/orders.json
{ "navigationBarTitleText": "我的订单" }
```

```js
// miniprogram/pages/common/orders/orders.js
const { queryList, getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')

const STATUS_MAP = {
  pending_payment: '待支付',
  paid: '已支付',
  growing: '生长中',
  harvested: '已收获'
}

Page({
  data: { orders: [], loading: true },
  onShow() { this.loadOrders() },
  async loadOrders() {
    this.setData({ loading: true })
    const app = getApp()
    const user = app.globalData.userInfo

    const adoptions = await queryList('adoptions',
      { userId: user.openId },
      { field: 'createdAt', order: 'desc' },
      50
    )

    const orders = await Promise.all(adoptions.map(async (a) => {
      const veg = await getById('vegetables', a.vegId)
      return {
        ...a,
        vegName: veg.name,
        coverImage: veg.coverImage,
        statusLabel: STATUS_MAP[a.status] || a.status,
        dateStr: formatDate(a.createdAt),
        price: veg.price[a.planType]
      }
    }))

    this.setData({ orders, loading: false })
  },
  goToDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/common/orderDetail/orderDetail?id=${id}` })
  }
})
```

```xml
<!-- miniprogram/pages/common/orders/orders.wxml -->
<view class="orders-page">
  <view wx:if="{{loading}}" class="loading"><text>加载中...</text></view>
  <view wx:elif="{{orders.length > 0}}" class="order-list">
    <view class="order-item" wx:for="{{orders}}" wx:key="_id" data-id="{{item._id}}" bindtap="goToDetail">
      <image class="order-cover" src="{{item.coverImage}}" mode="aspectFill" />
      <view class="order-info">
        <text class="order-name">{{item.vegName}} · {{item.ownerName}}</text>
        <text class="order-meta">{{item.code}} · {{item.planType === 'trial' ? '尝鲜装' : '季度装'}}</text>
        <view class="order-bottom">
          <text class="order-price">¥{{item.price}}</text>
          <text class="order-status">{{item.statusLabel}}</text>
        </view>
      </view>
    </view>
  </view>
  <view wx:else class="empty"><text>暂无订单</text></view>
</view>
```

```css
/* miniprogram/pages/common/orders/orders.wxss */
.order-item {
  display: flex; background: #fff; padding: 24rpx 32rpx;
  border-bottom: 1rpx solid #f0f0f0;
}
.order-cover { width: 120rpx; height: 120rpx; border-radius: 12rpx; flex-shrink: 0; }
.order-info { margin-left: 20rpx; flex: 1; }
.order-name { font-size: 28rpx; font-weight: bold; display: block; }
.order-meta { font-size: 22rpx; color: #999; display: block; margin-top: 4rpx; }
.order-bottom { display: flex; justify-content: space-between; margin-top: 12rpx; }
.order-price { font-size: 28rpx; color: #E53935; font-weight: bold; }
.order-status { font-size: 22rpx; color: #4CAF50; }
.empty, .loading { text-align: center; padding: 200rpx 0; color: #999; }
```

- [ ] **Step 2: 编写订单详情页**

```json
// miniprogram/pages/common/orderDetail/orderDetail.json
{
  "navigationBarTitleText": "订单详情",
  "usingComponents": {
    "name-plate": "/components/name-plate/name-plate"
  }
}
```

```js
// miniprogram/pages/common/orderDetail/orderDetail.js
const { getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')

const STATUS_MAP = {
  pending_payment: '待支付',
  paid: '已支付',
  growing: '生长中',
  harvested: '已收获'
}

Page({
  data: { adoption: null, vegName: '', dateStr: '', statusLabel: '' },
  async onLoad(options) {
    const adoption = await getById('adoptions', options.id)
    const veg = await getById('vegetables', adoption.vegId)
    this.setData({
      adoption,
      vegName: veg.name,
      dateStr: formatDate(adoption.createdAt),
      statusLabel: STATUS_MAP[adoption.status]
    })
  },
  goToTimeline() {
    wx.navigateTo({
      url: `/pages/user/timeline/timeline?id=${this.data.adoption._id}`
    })
  }
})
```

```xml
<!-- miniprogram/pages/common/orderDetail/orderDetail.wxml -->
<view class="detail" wx:if="{{adoption}}">
  <view class="detail-section">
    <text class="detail-label">订单状态</text>
    <text class="detail-status">{{statusLabel}}</text>
  </view>
  <view class="detail-section">
    <text class="detail-label">菜品</text>
    <text>{{vegName}}</text>
  </view>
  <view class="detail-section">
    <text class="detail-label">套餐</text>
    <text>{{adoption.planType === 'trial' ? '一棵菜·尝鲜装' : '一棵菜·季度装'}}</text>
  </view>
  <view class="detail-section">
    <text class="detail-label">下单时间</text>
    <text>{{dateStr}}</text>
  </view>

  <view class="plate-section">
    <name-plate
      vegName="{{vegName}}"
      ownerName="{{adoption.ownerName}}"
      code="{{adoption.code}}"
      startDate="{{dateStr}}"
    />
  </view>

  <button class="timeline-btn" wx:if="{{adoption.status === 'growing'}}" bindtap="goToTimeline">查看成长记录</button>
</view>
```

```css
/* miniprogram/pages/common/orderDetail/orderDetail.wxss */
.detail { padding: 32rpx; }
.detail-section {
  display: flex; justify-content: space-between; padding: 24rpx 0;
  border-bottom: 1rpx solid #f0f0f0; font-size: 28rpx;
}
.detail-label { color: #999; }
.detail-status { color: #4CAF50; font-weight: bold; }
.plate-section { margin-top: 40rpx; }
.timeline-btn {
  margin-top: 40rpx; background: #4CAF50 !important;
  color: #fff !important; border-radius: 40rpx !important;
}
```

- [ ] **Step 3: 验证订单页面**

从「我的」→「我的订单」进入，确认订单列表展示正确，点击进入详情，署名牌和成长记录入口正常。

- [ ] **Step 4: 提交**

```bash
git add miniprogram/pages/common/
git commit -m "feat: 订单列表与订单详情页"
```

---

## Task 15: 订阅消息与超时订单处理

**Files:**
- Create: `miniprogram/utils/subscription.js`
- Create: `cloudfunctions/sendSubscribeMsg/index.js`
- Create: `cloudfunctions/sendSubscribeMsg/package.json`
- Create: `cloudfunctions/cancelExpiredOrders/index.js`
- Create: `cloudfunctions/cancelExpiredOrders/package.json`

- [ ] **Step 1: 编写订阅消息工具**

```js
// miniprogram/utils/subscription.js
const TEMPLATE_IDS = {
  growthUpdate: '', // 在微信公众平台申请后填入实际模板ID
  harvestNotice: '',
  adoptSuccess: ''
}

function requestSubscription(templateKeys) {
  const tmplIds = templateKeys.map(k => TEMPLATE_IDS[k]).filter(Boolean)
  if (tmplIds.length === 0) return Promise.resolve()

  return new Promise((resolve) => {
    wx.requestSubscribeMessage({
      tmplIds,
      success: resolve,
      fail: resolve // 用户拒绝也不阻塞流程
    })
  })
}

module.exports = { TEMPLATE_IDS, requestSubscription }
```

- [ ] **Step 2: 编写发送订阅消息云函数**

```json
// cloudfunctions/sendSubscribeMsg/package.json
{
  "name": "sendSubscribeMsg",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": { "wx-server-sdk": "~2.6.3" }
}
```

```js
// cloudfunctions/sendSubscribeMsg/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event) => {
  const { toUser, templateId, data, page } = event

  try {
    await cloud.openapi.subscribeMessage.send({
      touser: toUser,
      templateId,
      data,
      page: page || ''
    })
    return { code: 0, msg: 'sent' }
  } catch (err) {
    console.error('发送订阅消息失败:', err)
    return { code: -1, msg: err.message }
  }
}
```

- [ ] **Step 3: 编写超时订单取消云函数**

```json
// cloudfunctions/cancelExpiredOrders/package.json
{
  "name": "cancelExpiredOrders",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": { "wx-server-sdk": "~2.6.3" }
}
```

```js
// cloudfunctions/cancelExpiredOrders/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()
const _ = db.command

exports.main = async () => {
  const thirtyMinutesAgo = new Date(Date.now() - 30 * 60 * 1000)

  // 查找超时的待支付订单
  const expired = await db.collection('adoptions').where({
    status: 'pending_payment',
    createdAt: _.lt(thirtyMinutesAgo)
  }).get()

  let cancelled = 0
  for (const adoption of expired.data) {
    // 恢复库存
    await db.collection('vegetables').doc(adoption.vegId).update({
      data: { stock: _.inc(1) }
    })
    // 取消订单
    await db.collection('adoptions').doc(adoption._id).update({
      data: { status: 'cancelled' }
    })
    cancelled++
  }

  return { code: 0, cancelled }
}
```

- [ ] **Step 4: 配置定时触发器**

在云开发控制台为 `cancelExpiredOrders` 云函数配置定时触发器，每 10 分钟执行一次：

```json
{
  "triggers": [
    {
      "name": "cancelExpired",
      "type": "timer",
      "config": "0 */10 * * * * *"
    }
  ]
}
```

- [ ] **Step 5: 上传云函数并验证**

上传 `sendSubscribeMsg` 和 `cancelExpiredOrders` 云函数。在云开发控制台手动触发 `cancelExpiredOrders` 测试，确认超时订单被正确取消。

- [ ] **Step 6: 提交**

```bash
git add miniprogram/utils/subscription.js cloudfunctions/sendSubscribeMsg/ cloudfunctions/cancelExpiredOrders/
git commit -m "feat: 订阅消息推送与超时订单自动取消"
```

---

## Task 16: 端到端集成测试

- [ ] **Step 1: 完整用户端链路测试**

在微信开发者工具中按以下流程测试：

1. 首页浏览菜品列表 → 点击进入详情
2. 选择尝鲜装 → 填写署名"达尔文的菜" → 立即认养 → 完成支付
3. 认养成功页显示署名牌 → 引导订阅消息
4. 跳转我的菜园 → 看到认养卡片（小番茄·达尔文的菜·第0天）
5. 点击查看成长记录 → 看到播种日志
6. 消息 Tab → 看到认养通知
7. 我的 → 我的订单 → 订单详情 → 署名牌展示

- [ ] **Step 2: 完整菜农端链路测试**

1. 我的 → 切换为菜农身份（输入 FARMER2026）
2. 工作台 → 看到新订单 → 确认播种
3. 待拍照列表出现 → 点击进入拍照上传
4. 拍照 + 写日志"今日浇水，长势良好" + 选阶段"发芽" → 提交
5. 返回工作台 → 待拍照数减 1
6. 菜地管理 → 菜品管理 → 新增一个菜品 → 保存
7. 认养列表 → 筛选"生长中" → 标记收获
8. 我的 → 切换回用户身份

- [ ] **Step 3: 身份切换测试**

1. 用户端 → 我的 → 切换为菜农 → 确认跳转工作台
2. 菜农端 → 我的 → 切换为用户 → 确认跳转首页
3. 关闭小程序 → 重新打开 → 确认保持上次的角色视角

- [ ] **Step 4: 边界场景测试**

1. 库存为0的菜品 → 显示"已认满"，下单按钮禁用
2. 署名不填 → 提示"请填写署名"
3. 拍照不选图片 → 提示"请至少拍一张照片"
4. 无认养记录时"我的菜园" → 显示空状态引导

- [ ] **Step 5: 修复发现的问题**

将测试中发现的问题逐一修复，每个修复单独提交。

- [ ] **Step 6: 最终提交**

```bash
git add -A
git commit -m "fix: 集成测试修复"
```
