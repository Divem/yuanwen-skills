# /// script
# requires-python = ">=3.11"
# dependencies = ["pyobjc-framework-Quartz"]
# ///
"""在屏幕坐标（点，不是像素）上发一次真实的鼠标左键单击。

剪映界面是 CEF 做的，System Events 的 click at 不起作用，只能用 Quartz 事件。
用法：uv run click.py <x> <y>
坐标换算：Retina 屏上 screencapture 是 2 倍像素，点 = 像素 / 2；缩小过的截图再按缩放比例换回。
需要给执行命令的终端 / 应用开「辅助功能」权限。
"""
import sys
import time

import Quartz

x, y = float(sys.argv[1]), float(sys.argv[2])
for kind in (Quartz.kCGEventMouseMoved, Quartz.kCGEventLeftMouseDown, Quartz.kCGEventLeftMouseUp):
    event = Quartz.CGEventCreateMouseEvent(None, kind, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
    time.sleep(0.15)
