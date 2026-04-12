const { getById, addRecord } = require('../../../utils/db')
const { daysBetween, formatDate } = require('../../../utils/date')
const STAGES = [
  { value: '', label: '不变更' },
  { value: 'seeding', label: '播种' },
  { value: 'sprouting', label: '发芽' },
  { value: 'growing', label: '生长中' },
  { value: 'flowering', label: '开花' },
  { value: 'fruiting', label: '结果' },
  { value: 'harvested', label: '收获' }
]
Page({
  data: {
    adoption: null, vegName: '', growDays: 0, images: [], text: '', stage: '', stages: STAGES, stageIndex: 0, submitting: false
  },
  async onLoad(options) {
    const adoption = await getById('adoptions', options.id)
    const veg = await getById('vegetables', adoption.vegId)
    this.setData({ adoption, vegName: veg.name, growDays: daysBetween(adoption.startDate, Date.now()) })
  },
  chooseImage() {
    const remaining = 9 - this.data.images.length
    if (remaining <= 0) { wx.showToast({ title: '最多9张', icon: 'none' }); return }
    wx.chooseMedia({ count: remaining, mediaType: ['image'], sourceType: ['album', 'camera'], camera: 'back',
      success: (res) => { this.setData({ images: [...this.data.images, ...res.tempFiles.map(f => f.tempFilePath)] }) }
    })
  },
  removeImage(e) { const images = [...this.data.images]; images.splice(e.currentTarget.dataset.index, 1); this.setData({ images }) },
  onTextInput(e) { this.setData({ text: e.detail.value }) },
  onPhraseSelect(e) { const phrase = e.detail.text; this.setData({ text: this.data.text ? `${this.data.text}，${phrase}` : phrase }) },
  onStageChange(e) { this.setData({ stageIndex: e.detail.value, stage: STAGES[e.detail.value].value }) },
  async onSubmit() {
    const { images, text, adoption, submitting } = this.data
    if (submitting) return
    if (images.length === 0) { wx.showToast({ title: '请至少拍一张照片', icon: 'none' }); return }
    this.setData({ submitting: true })
    try {
      const uploadedUrls = []
      for (const img of images) {
        const ext = img.split('.').pop()
        const cloudPath = `growth/${adoption._id}/${Date.now()}_${Math.random().toString(36).slice(2)}.${ext}`
        uploadedUrls.push((await wx.cloud.uploadFile({ cloudPath, filePath: img })).fileID)
      }
      await addRecord('growth_logs', {
        adoptionId: adoption._id, images: uploadedUrls, text: text.trim(), stage: this.data.stage || null,
        logDate: formatDate(new Date()), farmerId: getApp().globalData.userInfo.openId, createdAt: new Date()
      })
      wx.showToast({ title: '上传成功', icon: 'success' })
      setTimeout(() => wx.navigateBack(), 1500)
    } catch (err) {
      wx.showToast({ title: '上传失败，请重试', icon: 'none' })
    } finally { this.setData({ submitting: false }) }
  }
})