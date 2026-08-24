# 关键词自动回复插件 (astrbot_plugin_mj)

## 功能

| 关键词 | 行为 |
|--------|------|
| `mj` | 可选发文字「mj」+ 轮流/随机发 `mj1.mp4` / `mj2.mp4` |
| `isa` | 可选发文字「isa」+ 发图片 `isa.png` |
| `牛来` | 发文字「牛来」 |

## 插件目录文件

```
astrbot_plugin_mj/
├── main.py
├── metadata.yaml
├── _conf_schema.json   ← WebUI 配置
├── README.md
├── mj1.mp4             ← 自行放置
├── mj2.mp4             ← 自行放置
└── isa.png             ← 自行放置
```

## WebUI 配置

插件管理 → 本插件 → 配置：

- **触发 mj 时是否先发送文字「mj」**（默认开）
- **触发 isa 时是否先发送文字「isa」**（默认开）

关闭后只发媒体，不发对应文字。

## Docker 权限提醒

NapCat 与 AstrBot 共用 `./data:/AstrBot/data` 时：

```bash
cd ~/astrbot/data
chmod 755 plugins plugins/astrbot_plugin_mj
chmod 644 plugins/astrbot_plugin_mj/mj*.mp4 plugins/astrbot_plugin_mj/isa.png
# 仍 EACCES 时把 napcat 的 NAPCAT_UID/GID 设为 0
```

## 版本

- v1.3.0：isa 发图；WebUI 可配置是否发送 mj/isa 文字
- v1.2.3：mj 视频轮流+随机
