# 常用微信指令速查

用户会通过微信给 agent 发指令。以下是常见请求与建议的处理方式：

## 系统状态
- "查电量 / 查 CPU / 查内存" → 运行 `pmset -g batt`、`top -l 1 -n 5 | head -20`、`vm_stat` 等，用中文简要汇报。
- "查磁盘空间" → `df -h /`
- "这台 Mac 什么配置" → `system_profiler SPHardwareDataType`

## 写代码（Cursor）
- "用 Cursor 写/改 XX" → 使用 `cursor-code` skill，在用户指定的项目目录（未指定时默认 `~/Projects` 下按项目名推断）执行。
- 完成后汇报：改了哪些文件、运行结果、是否通过。

## 网页搜索 / 资讯
- "搜索 XX / 查一下 XX" → 使用 `web_search`（DuckDuckGo）搜索并中文简要回答。
- "看某网页" → 使用 `browser` 工具或 `web_fetch` 提取内容。

## 定时任务
- "XX 点提醒我 YY" → 用 `openclaw cron add --at "+N"` 或 cron 表达式创建定时任务，投递到微信。
- "每天 X 点推送 YY" → 用 cron 表达式创建周期性任务。
- 定时推送**必须指定投递目标**，否则报 "Delivering to openclaw-weixin requires target"。正确的创建方式：
  ```
  openclaw cron add --at "+10m" --message "内容" \
    --channel openclaw-weixin \
    --to "o9cq80-dPN3ePLU98NM874itQOkE@im.wechat" \
    --announce
  ```
  `--to` 是用户的微信 ID（在 `~/.openclaw/credentials/openclaw-weixin-*-allowFrom.json` 里）。周期性任务去掉 `--at` 改用 cron 表达式，如 `--cron "0 9 * * *"`。

## 文件整理
- "整理桌面 / 整理下载" → 使用 `file-organizer` skill（已安装），按类型/日期归类文件。
- 整理前先列出计划让用户确认，移动文件后汇报结果。

## 文件整理
- "整理桌面 / 整理下载" → 列出目录内容，按类型归类（文档/图片/压缩包），移动文件前先向用户确认。

## 系统操作
- 打开应用：`open -a "应用名"` 或 `osascript` 激活。
- 截图：`screencapture -x /tmp/shot.png`。
- 高风险操作（删除、git push、改系统配置）必须先向用户确认。

## 模型
- "切换到 DeepSeek / 切换到百炼" → 用 `openclaw models set` 切换主模型。
- 默认主模型 DeepSeek V4 Flash，备用百炼 Qwen3.5 Plus。

## 一般规则
- 微信里回复要简洁（微信限制消息长度，长内容分段发）。
- 不要用 markdown 表格（微信不渲染），用列表。
- 涉及敏感操作先确认。
