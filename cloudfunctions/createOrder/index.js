const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { OPENID } = cloud.getWXContext()
  const { vegId, planType, ownerName } = event

  const vegRes = await db.collection('vegetables').doc(vegId).get()
  const veg = vegRes.data

  if (veg.stock <= 0) {
    return { code: -1, msg: '库存不足' }
  }

  const price = veg.price[planType]
  const duration = veg.duration[planType]

  const now = new Date()
  const dateStr = `${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}`
  const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
  const code = `ZD-${dateStr}-${random}`

  const endDate = new Date(now.getTime() + duration * 24 * 60 * 60 * 1000)

  const adoption = {
    userId: OPENID,
    vegId,
    code,
    ownerName,
    planType,
    status: 'pending_payment',
    startDate: db.serverDate(),
    endDate: new Date(endDate),
    orderId: '',
    createdAt: db.serverDate()
  }

  const addRes = await db.collection('adoptions').add({ data: adoption })
  const adoptionId = addRes._id

  await db.collection('vegetables').doc(vegId).update({
    data: { stock: db.command.inc(-1) }
  })

  const payRes = await cloud.cloudPay.unifiedOrder({
    body: `种点什么-${veg.name}-${planType === 'trial' ? '尝鲜装' : '季度装'}`,
    outTradeNo: adoptionId,
    totalFee: price * 100,
    spbillCreateIp: '127.0.0.1',
    envId: cloud.DYNAMIC_CURRENT_ENV,
    functionName: 'payCallback',
    nonceStr: String(Date.now()),
    tradeType: 'JSAPI'
  })

  return {
    code: 0,
    data: { adoptionId, payment: payRes.payment }
  }
}
