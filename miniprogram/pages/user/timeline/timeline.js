const { queryList, getById } = require('../../../utils/db')
const { formatDate } = require('../../../utils/date')
const STAGE_LABELS = { seeding:'播种', sprouting:'发芽', growing:'生长中', flowering:'开花', fruiting:'结果', harvested:'收获' }
Page({
  data: { adoption: null, vegName: '', logs: [], loading: true },
  async onLoad(options) {
    const adoption = await getById('adoptions', options.id)
    const veg = await getById('vegetables', adoption.vegId)
    this.setData({ adoption, vegName: veg.name })
    this.loadLogs(options.id)
  },
  async loadLogs(adoptionId) {
    this.setData({ loading: true })
    const logs = await queryList('growth_logs', { adoptionId }, { field: 'logDate', order: 'desc' }, 100)
    const enriched = logs.map(log => ({ ...log, logDateStr: formatDate(log.logDate), stageLabel: STAGE_LABELS[log.stage] || '' }))
    this.setData({ logs: enriched, loading: false })
  },
  onPullDownRefresh() { this.loadLogs(this.data.adoption._id).then(() => wx.stopPullDownRefresh()) }
})
