const { getById } = require('../../../utils/db')

Page({
  data: {
    veg: null,
    planType: 'trial',
    ownerName: '',
    submitting: false
  },
  onLoad(options) {
    this.loadVeg(options.id)
  },
  async loadVeg(id) {
    const veg = await getById('vegetables', id)
    this.setData({ veg })
  },
  onPlanChange(e) {
    this.setData({ planType: e.currentTarget.dataset.plan })
  },
  onNameInput(e) {
    this.setData({ ownerName: e.detail.value })
  },
  async onAdopt() {
    const { veg, planType, ownerName, submitting } = this.data
    if (submitting) return
    if (!ownerName.trim()) {
      wx.showToast({ title: '请填写署名', icon: 'none' })
      return
    }
    if (veg.stock <= 0) {
      wx.showToast({ title: '该菜品已认满', icon: 'none' })
      return
    }

    this.setData({ submitting: true })
    try {
      const res = await wx.cloud.callFunction({
        name: 'createOrder',
        data: { vegId: veg._id, planType, ownerName: ownerName.trim() }
      })
      const { payment, adoptionId } = res.result.data

      await wx.requestPayment(payment)

      wx.redirectTo({
        url: `/pages/user/adoptSuccess/adoptSuccess?id=${adoptionId}`
      })
    } catch (err) {
      if (err.errMsg !== 'requestPayment:fail cancel') {
        wx.showToast({ title: '下单失败，请重试', icon: 'none' })
      }
    } finally {
      this.setData({ submitting: false })
    }
  }
})
