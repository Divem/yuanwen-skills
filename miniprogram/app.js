const { login } = require('./utils/auth')

App({
  onLaunch() {
    wx.cloud.init({
      env: 'zhongseed-dev',
      traceUser: true
    })
    this.autoLogin()
  },
  async autoLogin() {
    try {
      const user = await login()
      if (user.currentRole === 'farmer' && user.roles.includes('farmer')) {
        wx.reLaunch({ url: '/pages/farmer/workbench/workbench' })
      }
    } catch (err) {
      console.error('自动登录失败:', err)
    }
  },
  globalData: {
    userInfo: null,
    currentRole: 'user'
  }
})
