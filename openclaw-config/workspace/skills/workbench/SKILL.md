---
name: workbench
description: "本地网页工作台：浏览器访问 http://127.0.0.1:18790 可直接给修修发指令（相当于网页版聊天）、查看任务产物（~/tasks 文件树与预览）、技能清单与记忆。启动：bash ~/openclaw-workbench/start.sh；停止：bash ~/openclaw-workbench/stop.sh。当用户说'工作台/网页版/浏览器打开/结果面板'时使用。"
---

# Workbench（网页工作台）

给用户提供一个类似 WorkBuddy 的网页工作台：不用打开客户端、不用手机，在浏览器里就能给修修发指令并查看交付物。

## 地址

- 工作台：http://127.0.0.1:18790
- OpenClaw 官方 Control UI：http://127.0.0.1:18789/（会话管理、更完整的配置，`openclaw dashboard` 打开）

## 启动 / 停止

```bash
bash ~/openclaw-workbench/start.sh        # 启动并自动打开浏览器
bash ~/openclaw-workbench/start.sh 18791 # 自定义端口
bash ~/openclaw-workbench/stop.sh         # 停止
```

- 启动失败看日志：`~/openclaw-workbench/workbench.log`。
- 工作台仅绑定 127.0.0.1，只有本机能访问；不要用 SSH 隧道等方式对外暴露（个人工具，无鉴权）。

## 工作台能力

| 面板 | 能力 |
|---|---|
| 顶部 | 输入指令 + 选择 agent（main/coder/office）+ 快捷指令按钮 |
| 任务结果 | 发送后实时轮询执行状态，展示修修的回复 |
| 任务产物 | 浏览 `~/tasks` 目录树，点击文本文件预览，可下载 |
| 技能 | 展示已安装的 skills 与描述 |
| 记忆 | 展示 `memory/` 记忆文件 |
| 最近任务 | 历史指令记录 |

## 与微信的关系

- 微信遥控与网页工作台**并存**：两边发指令都会由同一个 OpenClaw agent 执行。
- 工作台的 `openclaw agent` 调用不带 `--deliver`，回复只出现在工作台，不会反向推送到微信。
- 产物统一落在 `~/tasks`，两端都能看到（工作台直接浏览；微信里修修回传路径）。

## 规则

- 用户说"开个工作台 / 网页版打开"时执行 `bash ~/openclaw-workbench/start.sh` 并回报地址。
- 工作台服务异常（打不开 18790）时：检查 `workbench.log`、确认 18790 未被占用，必要时 `stop.sh` 后重新 `start.sh`。
