Component({
  data: { phrases: ['今日浇水', '长势良好', '施肥一次', '开始发芽', '阳光充足', '修剪枝叶', '病虫防治'] },
  methods: { onTap(e) { this.triggerEvent('select', { text: e.currentTarget.dataset.text }) } }
})