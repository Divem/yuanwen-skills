Component({
  properties: { log: { type: Object, value: {} } },
  methods: {
    previewImage(e) {
      const url = e.currentTarget.dataset.url
      wx.previewImage({ current: url, urls: this.data.log.images })
    }
  }
})
