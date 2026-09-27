# 在剪映里验证

脚本自带的校验（帧数、PSNR、混音比对、帧对齐）能说明草稿本身对不对，但只有在剪映里打开过，才能确认剪映认得它。

## 先想清楚能不能动剪映

- 剪映是用户的应用，常开在后台。**有草稿正开着（有 `.locked`）时不要碰它的界面**，否则会打断用户编辑。
- 最好是用户明确说可以，或者确认剪映停在首页、用户不在用。做完要把剪映退回首页，把原来的前台应用切回来。
- 不打开界面也能确认剪映读成功了：用户自己打开过草稿后，看 `.backup/*.load.bak` 的字节数是否等于 `draft_content.json`（见 `format.md` 最后一节）。

## 步骤

1. 看状态：`osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true'`，再查有没有 `.locked`。
2. 把剪映切到前台：`osascript -e 'tell application id "com.lemon.lvpro" to activate'`，截屏：`screencapture -x /tmp/jy.png && sips -Z 1400 /tmp/jy.png --out /tmp/jy-s.png`。确认停在首页（有「本地草稿」列表）。
3. 点草稿卡片。剪映界面是 CEF（内嵌 Chromium）做的，**System Events 的 `click at` 不起作用**，要用 Quartz 发真实鼠标事件：

   ```bash
   uv run ~/.claude/skills/jianying-draft/scripts/click.py <x> <y>
   ```

   坐标用「点」而不是像素：Retina 屏上 `screencapture` 是 2 倍像素，点 = 像素 / 2；截图缩小过就再按缩放比例换算（比如 3024 宽缩到 1400 宽，点 = 缩略图坐标 × 1512 / 1400）。
4. 等 6～7 秒再截屏，检查：
   - 标题栏是草稿名，播放器总时长和成片一致；
   - 轨道齐全，画面主轨的片段名对得上；
   - 字幕轨的眼睛图标是划掉的（隐藏）。可以点时间标尺把播放头挪到有字幕的地方，确认画面上不显示。
5. 点编辑器左上角的红色关闭按钮（全屏窗口大约在点坐标 (19, 51)）回到首页，剪映会保存并删掉 `.locked`。
6. 切回原来的前台应用：`osascript -e 'tell application "<应用名>" to activate'`。

## 注意

- 打开后剪映会把草稿升级保存，此后脚本再生成就需要 `--force`。验证完如果还要改生成逻辑，改完用 `--force` 重建，或者换一个草稿名。
- 在剪映界面里点过的东西（比如为了实测点了轨道的眼睛）会被剪映保存进草稿，验证用的操作只做观察性的，比如移动播放头。
- 需要测试某个写法（比如 attribute 的某一位、占位符路径）时，另建一个名字醒目的临时草稿（如「zz-测试-可删」），测完删掉文件夹，剪映会记一条 `delete_draft_external`。
