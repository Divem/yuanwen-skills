const TEMPLATE_IDS = { growthUpdate: '', harvestNotice: '', adoptSuccess: '' }
function requestSubscription(templateKeys) {
  const tmplIds = templateKeys.map(k => TEMPLATE_IDS[k]).filter(Boolean)
  if (tmplIds.length === 0) return Promise.resolve()
  return new Promise((resolve) => { wx.requestSubscribeMessage({ tmplIds, success: resolve, fail: resolve }) })
}
module.exports = { TEMPLATE_IDS, requestSubscription }
