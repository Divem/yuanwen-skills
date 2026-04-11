const { switchRole } = require('../../../utils/auth')
const { queryList } = require('../../../utils/db')
Page({
  data: { userInfo: null, stats: { photoCount: 0, vegCount: 0 } },
  async onShow() {
    const app = getApp()
    this.setData({ userInfo: app.globalData.userInfo })
    this.loadStats()
  },
  async loadStats() {
    const app = getApp()
    const farmerId = app.globalData.userInfo.openId
    const { db } = require('../../../utils/db')
    const logCount = await db.collection('growth_logs').where({ farmerId }).count()
    const vegCount = await db.collection('vegetables').count()
    this.setData({ stats: { photoCount: logCount.total, vegCount: vegCount.total } })
  },
  async onSwitchToUser() { await switchRole('user') }
})