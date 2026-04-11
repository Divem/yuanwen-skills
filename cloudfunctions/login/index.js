const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
  const { OPENID } = cloud.getWXContext()

  const userRes = await db.collection('users').where({ openId: OPENID }).get()

  if (userRes.data.length > 0) {
    return { code: 0, data: userRes.data[0] }
  }

  const newUser = {
    openId: OPENID,
    nickName: '',
    phone: '',
    avatar: '',
    roles: ['user'],
    currentRole: 'user',
    createdAt: db.serverDate()
  }

  const addRes = await db.collection('users').add({ data: newUser })
  newUser._id = addRes._id
  return { code: 0, data: newUser }
}
