const { daysBetween } = require('../../utils/date')
Component({
  properties: {
    adoption: { type: Object, value: {} },
    vegName: { type: String, value: '' },
    coverImage: { type: String, value: '' },
    selected: { type: Boolean, value: false }
  },
  data: { growDays: 0 },
  lifetimes: {
    attached() {
      this.setData({ growDays: daysBetween(this.data.adoption.startDate, Date.now()) })
    }
  },
  methods: {
    onTap() { this.triggerEvent('select', { adoption: this.data.adoption }) }
  }
})
