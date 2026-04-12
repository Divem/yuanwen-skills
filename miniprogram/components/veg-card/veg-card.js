Component({
  properties: {
    veg: { type: Object, value: {} }
  },
  methods: {
    onTap() {
      wx.navigateTo({
        url: `/pages/user/vegDetail/vegDetail?id=${this.data.veg._id}`
      })
    }
  }
})
