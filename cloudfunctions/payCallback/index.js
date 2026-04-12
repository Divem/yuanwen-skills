const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { outTradeNo, resultCode, transactionId } = event

  if (resultCode !== 'SUCCESS') {
    const adoption = await db.collection('adoptions').doc(outTradeNo).get()
    await db.collection('vegetables').doc(adoption.data.vegId).update({
      data: { stock: db.command.inc(1) }
    })
    await db.collection('adoptions').doc(outTradeNo).update({
      data: { status: 'payment_failed' }
    })
    return { errcode: 0, errmsg: 'handled' }
  }

  await db.collection('adoptions').doc(outTradeNo).update({
    data: {
      status: 'growing',
      orderId: transactionId
    }
  })

  const adoption = await db.collection('adoptions').doc(outTradeNo).get()
  const veg = await db.collection('vegetables').doc(adoption.data.vegId).get()

  await db.collection('growth_logs').add({
    data: {
      adoptionId: outTradeNo,
      images: [],
      text: `🌱 ${veg.data.name}已播种，开始成长之旅！`,
      stage: 'seeding',
      logDate: db.serverDate(),
      farmerId: 'system',
      createdAt: db.serverDate()
    }
  })

  return { errcode: 0, errmsg: 'SUCCESS' }
}
