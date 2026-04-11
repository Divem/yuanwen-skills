const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()
const _ = db.command
exports.main = async () => {
  const thirtyMinutesAgo = new Date(Date.now() - 30 * 60 * 1000)
  const expired = await db.collection('adoptions').where({ status: 'pending_payment', createdAt: _.lt(thirtyMinutesAgo) }).get()
  let cancelled = 0
  for (const adoption of expired.data) {
    await db.collection('vegetables').doc(adoption.vegId).update({ data: { stock: _.inc(1) } })
    await db.collection('adoptions').doc(adoption._id).update({ data: { status: 'cancelled' } })
    cancelled++
  }
  return { code: 0, cancelled }
}
