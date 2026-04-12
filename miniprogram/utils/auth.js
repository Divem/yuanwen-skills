async function login() {
  const res = await wx.cloud.callFunction({ name: 'login' })
  const user = res.result.data
  const app = getApp()
  app.globalData.userInfo = user
  app.globalData.currentRole = user.currentRole || 'user'
  return user
}

async function switchRole(targetRole) {
  const app = getApp()
  const user = app.globalData.userInfo
  if (!user.roles.includes(targetRole)) {
    throw new Error('没有该角色权限')
  }

  const { db } = require('./db')
  await db.collection('users').doc(user._id).update({
    data: { currentRole: targetRole }
  })

  app.globalData.currentRole = targetRole
  user.currentRole = targetRole

  if (targetRole === 'farmer') {
    wx.reLaunch({ url: '/pages/farmer/workbench/workbench' })
  } else {
    wx.reLaunch({ url: '/pages/user/home/home' })
  }
}

async function activateFarmerRole(inviteCode) {
  const VALID_CODES = ['FARMER2026']
  if (!VALID_CODES.includes(inviteCode)) {
    throw new Error('邀请码无效')
  }

  const app = getApp()
  const user = app.globalData.userInfo
  const { db } = require('./db')

  await db.collection('users').doc(user._id).update({
    data: { roles: ['user', 'farmer'] }
  })
  user.roles = ['user', 'farmer']
}

module.exports = { login, switchRole, activateFarmerRole }
