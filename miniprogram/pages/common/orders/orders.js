const { queryList, getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')
const STATUS_MAP = { pending_payment: '待支付', paid: '已支付', growing: '生长中', harvested: '已收获' }
Page({
  data: { orders: [], loading: true },
  onShow() { this.loadOrders() },
  async loadOrders() {
    this.setData({ loading: true })
    const app = getApp()
    const user = app.globalData.userInfo
    const adoptions = await queryList('adoptions', { userId: user.openId }, { field: 'createdAt', order: 'desc' }, 50)
    const orders = await Promise.all(adoptions.map(async (a) => {
      const veg = await getById('vegetables', a.vegId)
      return { ...a, vegName: veg.name, coverImage: veg.coverImage, statusLabel: STATUS_MAP[a.status] || a.status, dateStr: formatDate(a.createdAt), price: veg.price[a.planType] }
    }))
    this.setData({ orders, loading: false })
  },
  goToDetail(e) { wx.navigateTo({ url: `/pages/common/orderDetail/orderDetail?id=${e.currentTarget.dataset.id}` }) }
})
