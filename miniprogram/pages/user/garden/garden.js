const { queryList, getById } = require('../../../utils/db')
Page({
  data: { adoptions: [], selectedId: '', loading: true },
  onShow() { this.loadAdoptions() },
  async loadAdoptions() {
    this.setData({ loading: true })
    const app = getApp()
    const user = app.globalData.userInfo
    if (!user) { this.setData({ loading: false }); return }
    const adoptions = await queryList('adoptions', { userId: user.openId, status: 'growing' }, { field: 'createdAt', order: 'desc' })
    const enriched = await Promise.all(adoptions.map(async (a) => {
      const veg = await getById('vegetables', a.vegId)
      return { ...a, vegName: veg.name, coverImage: veg.coverImage }
    }))
    this.setData({ adoptions: enriched, selectedId: enriched.length > 0 ? enriched[0]._id : '', loading: false })
  },
  onSelectAdoption(e) { this.setData({ selectedId: e.detail.adoption._id }) },
  viewTimeline() {
    if (!this.data.selectedId) return
    wx.navigateTo({ url: `/pages/user/timeline/timeline?id=${this.data.selectedId}` })
  }
})
