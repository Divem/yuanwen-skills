# 剪映草稿的格式与行为（实测）

环境：剪映专业版 Mac 10.5.0（`/Applications/VideoFusion-macOS.app`，bundle id `com.lemon.lvpro`，沙盒应用），2026-09 实测。
新版本剪映行为可能变化，拿不准时先用 `check_draft.py` 看现状，或按 `verify-in-app.md` 在剪映里开一次。

## 目录与文件

- 草稿目录：`~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/<草稿名>/`，文件夹名就是剪映首页显示的名字。
- `root_meta_info.json`（草稿目录根下，明文）：剪映的草稿登记表。`all_draft_store` 每项有 `draft_name`、`draft_fold_path`、`draft_id`、`draft_json_file`（Mac 指向 `draft_info.json`）、`tm_duration`。
- 草稿文件夹里：
  - `draft_info.json`：时间线本体，**Mac 版读这个**。Windows 版读 `draft_content.json`，本技能两份都写。
  - `draft_meta_info.json`：元信息，从 pyJianYingDraft 的模板改写（草稿名、路径、ID、时长、封面）。
  - `draft_cover.jpg`：首页卡片的封面，640 宽就够。
  - 剪映打开后会自己加一批文件：`.locked`（正开着）、`.backup/*.load.bak|save.bak|close.bak`、`Resources/`、`template*.tmp`、`timeline_layout.json` 等。

## 加密

- 剪映 6 起，剪映**自己保存**的 `draft_info.json`、`draft_meta_info.json` 是加密的（一串 base64 样的文本），读不了。
- 但它**能读明文**。第一次打开明文草稿时，剪映会把它升级（文件变大一倍左右），通常先存一份明文版，之后每次保存都加密。
- 所以草稿在剪映里保存过以后，就看不到用户做了什么改动。本技能额外留一份 `draft_content.json` 作为生成时的明文副本，诊断时用它；再写一个 `.jianying-draft-generated`（内容是 draft_info.json 的 sha256），判断剪映有没有动过。
- 不要尝试破解加密格式。

## 登记与草稿 ID

- 剪映**监听草稿目录**：出现新文件夹会自动登记（操作日志里是 `copy_draft_external`），并分配**自己的** `draft_id`，不会用元信息里写的那个。本技能在元信息里沿用登记表里的 ID；还没登记时用 uuid5 顶上。
- **剪映停在编辑界面时不登记新文件夹**，回到首页或重启后才出现。
- 重建草稿要原地覆盖文件，不要把整个文件夹删掉再建，否则剪映会把它当成先删除、再新建的另一个草稿。

## 操作日志

`~/Library/Containers/com.lemon.lvpro/Data/Movies/JianyingPro/User Data/Log/draft_acion_watch.json`（文件名里的 acion 就是原样拼写），每行一条 JSON：`type`（`copy_draft_external` / `create_draft` / `rename_draft` / `delete_draft_external`）、`new_draft_info` / `old_draft_info`（名字、文件夹、ID）、`time_nsec`（实际是微秒）。排查「草稿去哪了」「是谁改的名」先看它。

## 时间线 JSON 的要点

- 时间单位是微秒。片段的 `target_timerange`、`source_timerange` 都是 `{start, duration}`。
- **边界必须落在整帧上。** 剪映会把片段边界吸附到帧；不在帧上的相邻片段吸附后可能重叠一帧，剪映会把后一个片段挪到一条新建的轨道上。本技能用 `[fus(a), fus(b))`（第 a 帧到第 b 帧的起点微秒数）表示片段，相邻片段严格首尾相接。
- 轨道 `attribute` 是位掩码：**1 静音、2 隐藏、4 锁定**。pyJianYingDraft 的 `mute=True` 只写 1，这个位对文字轨无效（字照样显示），隐藏要写 2。
- 同一轨道上的片段不能重叠，重叠的要放到另一条轨道。
- 主轨磁吸（`maintrack_adsorb`）默认开，和剪映新建草稿一致。

## 素材路径

- 剪映是沙盒应用，只能读 `~/Movies` 这类授权目录和用户手动选过的文件。**素材拷进草稿文件夹**最稳妥（本技能放在 `素材/<轨道名>/`）。
- 路径写绝对路径时，剪映能读。但**在剪映里改名会重命名文件夹**，绝对路径就指向了不存在的旧文件夹，剪映有没有顺带修正路径看不到（它存的是加密文件）。
- 剪映程序里有草稿目录占位符 `##_draftpath_placeholder_0E685133-18CE-45ED-8CB8-2904A212EC80_##`（二进制里出现 26 处），素材路径写成「占位符 + /素材/…」理论上改名、搬家都不断链，`--portable` 就是这么写的。**尚未在剪映里实测**，用之前先生成一个测试草稿在剪映里打开，确认素材正常显示。

## 声音素材的电平

- 剪映怎么把单声道铺到双声道没验证过。本技能把素材都预先转成双声道，电平按成片混音时的升声道方式：
  - bed.py 里人声用 numpy 满幅复制到左右声道；
  - mix_audio 用 ffmpeg `aformat=channel_layouts=stereo` 升声道，**每声道乘 0.7071（-3 dB）**，实测确认过。
- 片段 `volume` 是线性倍数，大于 1 也可以（音效常见 +8～+12 dB）。

## 怎么确认剪映读成功了（不用打开界面）

剪映打开草稿时，会把载入前的内容备份成 `.backup/<时间>_<hash>.load.bak`。如果它和 `draft_content.json` 字节数一样，而且之后出现了 `save.bak`、`draft_info.json` 变大并被加密，就说明剪映完整读取了这份草稿并做了升级。
