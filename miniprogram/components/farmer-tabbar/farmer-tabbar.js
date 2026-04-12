Component({
  properties: {
    active: { type: Number, value: 0 }
  },
  data: {
    tabs: [
      { icon: '📋', text: '工作台', url: '/pages/farmer/workbench/workbench' },
      { icon: '🌾', text: '菜地管理', url: '/pages/farmer/fieldManage/fieldManage' },
      { icon: '👤', text: '我的', url: '/pages/farmer/farmerProfile/farmerProfile' }
    ]
  },
  methods: {
    onTabTap(e) {
      const index = e.currentTarget.dataset.index
      if (index === this.data.active) return
      const url = this.data.tabs[index].url
      wx.reLaunch({ url })
    }
  }
})
