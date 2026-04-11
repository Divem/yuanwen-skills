const { getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')
const STATUS_MAP = { pending_payment: '待支付', paid: '已支付', growing: '生长中', harvested: '已收获' }
Page({
  data: { adoption: null, vegName: '', dateStr: '', statusLabel: '' },
  async onLoad(options) {
    const adoption = await getById('adoptions', options.id)
    const veg = await getById('vegetables', adoption.vegId)
    this.setData({ adoption, vegName: veg.name, dateStr: formatDate(adoption.createdAt), statusLabel: STATUS_MAP[adoption.status] })
  },
  goToTimeline() { wx.navigateTo({ url: `/pages/user/timeline/timeline?id=${this.data.adoption._id}` }) }
})
