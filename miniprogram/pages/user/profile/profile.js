const { switchRole, activateFarmerRole } = require('../../../utils/auth')

Page({
  data: { userInfo: null, isFarmer: false },
  onShow() {
    const app = getApp()
    const user = app.globalData.userInfo
    if (user) { this.setData({ userInfo: user, isFarmer: user.roles.includes('farmer') }) }
  },
  goToOrders() { wx.navigateTo({ url: '/pages/common/orders/orders' }) },
  async onSwitchToFarmer() {
    if (this.data.isFarmer) {
      await switchRole('farmer')
    } else {
      const self = this
      wx.showModal({
        title: '激活菜农身份', content: '请输入邀请码', editable: true, placeholderText: '请输入邀请码',
        async success(res) {
          if (res.confirm && res.content) {
            try {
              await activateFarmerRole(res.content.trim())
              wx.showToast({ title: '激活成功', icon: 'success' })
              self.setData({ isFarmer: true })
              setTimeout(() => switchRole('farmer'), 1500)
            } catch (err) { wx.showToast({ title: err.message, icon: 'none' }) }
          }
        }
      })
    }
  }
})
