const { getById, addRecord, updateRecord } = require('../../../utils/db')
Page({
  data: { id: '', name: '', desc: '', coverImage: '', priceTrial: 39, priceQuarterly: 99, durationTrial: 30, durationQuarterly: 90, stock: 10, growthInfo: '', status: 'on_sale', submitting: false },
  async onLoad(options) {
    if (options.id) {
      const veg = await getById('vegetables', options.id)
      this.setData({ id: options.id, name: veg.name, desc: veg.desc, coverImage: veg.coverImage, priceTrial: veg.price.trial, priceQuarterly: veg.price.quarterly, durationTrial: veg.duration.trial, durationQuarterly: veg.duration.quarterly, stock: veg.stock, growthInfo: veg.growthInfo, status: veg.status })
      wx.setNavigationBarTitle({ title: '编辑菜品' })
    } else { wx.setNavigationBarTitle({ title: '新增菜品' }) }
  },
  onInput(e) { this.setData({ [e.currentTarget.dataset.field]: e.detail.value }) },
  chooseCover() {
    wx.chooseMedia({ count: 1, mediaType: ['image'],
      success: async (res) => {
        const tempPath = res.tempFiles[0].tempFilePath
        const ext = tempPath.split('.').pop()
        this.setData({ coverImage: (await wx.cloud.uploadFile({ cloudPath: `vegetables/${Date.now()}.${ext}`, filePath: tempPath })).fileID })
      }
    })
  },
  async onSubmit() {
    const { id, name, coverImage, submitting } = this.data
    if (submitting) return
    if (!name.trim() || !coverImage) { wx.showToast({ title: '请填写名称和封面图', icon: 'none' }); return }
    this.setData({ submitting: true })
    const vegData = { name: name.trim(), desc: this.data.desc.trim(), coverImage, price: { trial: Number(this.data.priceTrial), quarterly: Number(this.data.priceQuarterly) }, duration: { trial: Number(this.data.durationTrial), quarterly: Number(this.data.durationQuarterly) }, stock: Number(this.data.stock), growthInfo: this.data.growthInfo.trim(), status: this.data.status }
    try {
      if (id) { await updateRecord('vegetables', id, vegData) } else { vegData.createdAt = new Date(); await addRecord('vegetables', vegData) }
      wx.showToast({ title: '保存成功', icon: 'success' })
      setTimeout(() => wx.navigateBack(), 1500)
    } catch (err) { wx.showToast({ title: '保存失败', icon: 'none' }) } finally { this.setData({ submitting: false }) }
  },
  toggleStatus() { this.setData({ status: this.data.status === 'on_sale' ? 'off_shelf' : 'on_sale' }) }
})