# timeline.json 规格

`jianying_draft.py` 的输入。时间都用**秒**，核心会取整到帧：片段起点按 `round(start × fps)`，终点按 `round((start + duration) × fps)`，所以首尾相接的片段取整后仍然相接。

```json
{
  "name": "ChatPage-企业篇",
  "width": 1920, "height": 1080, "fps": 30,
  "cover": {"image": "/abs/covers/cover-16x9.png"},
  "tracks": [
    {"type": "video", "name": "画面", "clips": [
      {"file": "/abs/00-开场.mp4", "start": 0, "duration": 7.4},
      {"file": "/abs/01-品牌.mp4", "start": 7.4, "duration": 7.8, "source_start": 0}
    ]},
    {"type": "audio", "name": "配乐", "clips": [
      {"file": "/abs/配乐.wav", "start": 0, "duration": 90, "volume": 0.74}
    ]},
    {"type": "audio", "name": "旁白", "clips": [
      {"file": "/abs/旁白01.wav", "start": 0.5, "duration": 2.97, "volume": 0.74}
    ]},
    {"type": "audio", "name": "音效", "split_overlaps": true, "clips": [
      {"file": "/abs/click.wav", "start": 18.8, "duration": 0.13, "volume": 2.6}
    ]},
    {"type": "text", "name": "字幕", "hidden": true, "srt": "字幕.srt",
     "style": {"size": 7, "color": [1, 1, 1], "border": {"color": [0, 0, 0], "width": 40}, "y": -0.82},
     "clips": [{"text": "一份周报 要登录五个系统来拼", "start": 0.5, "duration": 2.97}]}
  ],
  "extra_files": [{"file": "/abs/music.wav", "to": "配乐/配乐-原始.wav"}]
}
```

## 字段

| 字段 | 说明 |
|---|---|
| `name` | 草稿名，也就是草稿文件夹名 |
| `width` / `height` / `fps` | 画布和帧率，默认 1920 / 1080 / 30 |
| `cover` | `{"image": 路径}`，或 `{"video": 路径, "at": 秒}` 从视频截一帧；可省略 |
| `tracks` | 按顺序建轨道；视觉轨越靠后越在上层 |
| `tracks[].type` | `video` / `audio` / `text` |
| `tracks[].name` | 轨道名，也是素材子文件夹名（`素材/<name>/`，可用 `folder` 另指） |
| `tracks[].split_overlaps` | 片段有重叠时自动分到多条子轨，命名为「名字 1」「名字 2」…；不开时片段重叠会报错 |
| `tracks[].hidden` / `mute` / `locked` | 写进轨道 attribute 位掩码（2 / 1 / 4） |
| `tracks[].srt` | 文字轨另存一份 SRT 到草稿文件夹 |
| `tracks[].style` | 文字轨样式：`size`（默认 7）、`color`（RGB 0～1）、`border`（`null` 为不描边）、`y`（-1 底 ～ 1 顶，默认 -0.82）、`align`（0 左 / 1 中 / 2 右）、`max_line_width` |
| `clips[].file` | 素材路径，会拷进草稿文件夹，同一个源文件只拷一次 |
| `clips[].start` / `duration` | 在时间线上的起点和时长（秒） |
| `clips[].source_start` | 从素材的第几秒开始截，默认 0 |
| `clips[].volume` | 线性音量，默认 1.0，可以大于 1 |
| `clips[].text` | 文字轨的内容 |
| `extra_files` | 不上时间线、只随草稿放一份的文件（比如换曲用的原始配乐） |

## 注意

- 素材比要求的时长短时，按素材长度截短并提示；截取范围完全超出素材会报错。
- 单声道素材在剪映里怎么铺到双声道没验证过，要精确还原电平时先自己转成双声道。
- 视频素材最好是 H.264 / yuv420p（或 yuvj420p）的 mp4，帧率和时间线一致；从成片切镜头时按帧号 trim 并重新编码（`from_guizang.py` 用 CRF 12），不要按时间拷贝流。
