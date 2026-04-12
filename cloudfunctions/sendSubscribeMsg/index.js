const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
exports.main = async (event) => {
  const { toUser, templateId, data, page } = event
  try {
    await cloud.openapi.subscribeMessage.send({ touser: toUser, templateId, data, page: page || '' })
    return { code: 0, msg: 'sent' }
  } catch (err) { console.error('发送订阅消息失败:', err); return { code: -1, msg: err.message } }
}
