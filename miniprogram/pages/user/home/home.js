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
