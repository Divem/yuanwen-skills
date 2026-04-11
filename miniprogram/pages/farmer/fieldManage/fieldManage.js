const { queryList, getById, updateRecord } = require('../../../utils/db')
Page({
  data: { tab: 'vegetables', vegetables: [], adoptions: [], adoptionFilter: 'all', loading: true },
  onShow() { this.loadData() },
  switchTab(e) { this.setData({ tab: e.currentTarget.dataset.tab }) },
  async loadData() {
    this.setData({ loading: true })
    const vegetables = await queryList('vegetables', {}, { field: 'createdAt', order: 'desc' }, 100)
    const adoptions = await queryList('adoptions', {}, { field: 'createdAt', order: 'desc' }, 100)
    const enriched = await Promise.all(adoptions.map(async (a) => { const veg = await getById('vegetables', a.vegId); return { ...a, vegName: veg.name } }))
    this.setData({ vegetables, adoptions: enriched, loading: false })
  },
  goToAddVeg() { wx.navigateTo({ url: '/pages/farmer/vegEdit/vegEdit' }) },
  goToEditVeg(e) { wx.navigateTo({ url: `/pages/farmer/vegEdit/vegEdit?id=${e.currentTarget.dataset.id}` }) },
  filterAdoptions(e) { this.setData({ adoptionFilter: e.currentTarget.dataset.filter }) },
  markHarvested(e) {
    wx.showModal({ title: '确认收获', content: '标记为已收获后将通知用户',
      success: async (res) => {
        if (res.confirm) {
          await updateRecord('adoptions', e.currentTarget.dataset.id, { status: 'harvested' })
          wx.showToast({ title: '已标记收获', icon: 'success' })
          this.loadData()
        }
      }
    })
  }
})