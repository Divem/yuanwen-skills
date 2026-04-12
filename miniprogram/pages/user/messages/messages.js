const { queryList, getById, db, _ } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')

Page({
  data: { messages: [], loading: true },
  onShow() { this.loadMessages() },
  async loadMessages() {
    this.setData({ loading: true })
    const app = getApp()
    const user = app.globalData.userInfo
    if (!user) { this.setData({ loading: false }); return }

    const adoptions = await queryList('adoptions', { userId: user.openId }, { field: 'createdAt', order: 'desc' })
    if (adoptions.length === 0) { this.setData({ messages: [], loading: false }); return }

    const adoptionIds = adoptions.map(a => a._id)
    const adoptionMap = {}
    for (const a of adoptions) {
      const veg = await getById('vegetables', a.vegId)
      adoptionMap[a._id] = { ownerName: a.ownerName, vegName: veg.name, code: a.code }
    }

    const logs = await queryList('growth_logs', { adoptionId: _.in(adoptionIds) }, { field: 'logDate', order: 'desc' }, 50)
    const messages = logs.map(log => {
      const info = adoptionMap[log.adoptionId] || {}
      return { ...log, vegName: info.vegName || '', ownerName: info.ownerName || '', dateStr: formatDate(log.logDate), adoptionId: log.adoptionId }
    })
    this.setData({ messages, loading: false })
  },
  goToTimeline(e) {
    wx.navigateTo({ url: `/pages/user/timeline/timeline?id=${e.currentTarget.dataset.id}` })
  }
})
