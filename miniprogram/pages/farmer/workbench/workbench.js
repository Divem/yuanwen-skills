const { queryList, db, _ } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')
Page({
  data: { todayStats: { pending: 0, done: 0, newOrders: 0 }, pendingPhotos: [], newOrders: [], loading: true },
  onShow() { this.loadWorkbench() },
  async loadWorkbench() {
    this.setData({ loading: true })
    const today = formatDate(new Date())
    const adoptions = await queryList('adoptions', { status: 'growing' }, { field: 'createdAt', order: 'desc' }, 100)
    const todayLogs = await queryList('growth_logs', { logDate: db.RegExp({ regexp: today }) }, null, 100)
    const doneIds = new Set(todayLogs.map(l => l.adoptionId))
    const { getById } = require('../../../utils/db')
    const enriched = await Promise.all(adoptions.map(async (a) => {
      const veg = await getById('vegetables', a.vegId)
      return { ...a, vegName: veg.name, hasTodayLog: doneIds.has(a._id) }
    }))
    const pending = enriched.filter(a => !a.hasTodayLog)
    const done = enriched.filter(a => a.hasTodayLog)
    const newOrders = await queryList('adoptions', { status: 'paid' }, { field: 'createdAt', order: 'desc' })
    this.setData({ todayStats: { pending: pending.length, done: done.length, newOrders: newOrders.length }, pendingPhotos: pending, newOrders, loading: false })
  },
  goToPhoto(e) { wx.navigateTo({ url: `/pages/farmer/photoUpload/photoUpload?id=${e.currentTarget.dataset.id}` }) },
  async confirmOrder(e) {
    const { updateRecord } = require('../../../utils/db')
    await updateRecord('adoptions', e.currentTarget.dataset.id, { status: 'growing' })
    wx.showToast({ title: '已确认播种', icon: 'success' })
    this.loadWorkbench()
  }
})