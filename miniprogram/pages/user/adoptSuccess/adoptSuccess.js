const { getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')
Page({
  data: { adoption: null, vegName: '', dateStr: '' },
  async onLoad(options) {
    const adoption = await getById('adoptions', options.id)
    const veg = await getById('vegetables', adoption.vegId)
    this.setData({ adoption, vegName: veg.name, dateStr: formatDate(adoption.startDate) })
    this.requestSubscription()
  },
  requestSubscription() {
    wx.requestSubscribeMessage({
      tmplIds: ['TEMPLATE_GROWTH_UPDATE', 'TEMPLATE_HARVEST_NOTICE'],
      success(res) { console.log('订阅消息授权结果:', res) }
    })
  },
  goToGarden() { wx.switchTab({ url: '/pages/user/garden/garden' }) }
})
