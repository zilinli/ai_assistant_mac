# AI 助理全面对比：WorkBuddy 及相关产品

> 更新时间：2026-08-17
> 场景前提：仅在一台 macOS（Intel, 12.6）上使用，可任意操控电脑，支持手机远程遥控（期望微信），主力用途为 Cursor 写代码，自备 DeepSeek / 阿里百炼（通义千问）API Key。

---

## 一、结论速览

| 维度 | WorkBuddy（腾讯） | QoderWork（阿里） | 豆包专业版（字节） | ToDesk AI | OpenClaw（开源，已选定） |
|---|---|---|---|---|---|
| 本地电脑操控 | 有，实测偏弱 | 较强 | 最强 | 远程GUI+AI | 最强（shell/AppleScript/浏览器/GUI） |
| 手机遥控 | 微信全家桶+Slack/Telegram/Discord | 钉钉/微信/飞书+App | 仅飞书 | App+微信小程序 | 29通道+官方微信插件 |
| 外接自备模型 | 仅 OpenAI 兼容 | 不支持 | 仅字节自家 | 内置6款 | 任意 OpenAI 兼容（DeepSeek/百炼官方插件） |
| Cursor 集成 | 弱（面向办公） | 弱 | 无 | 无 | 可直接驱动 Cursor Agent SDK/CLI |
| 数据隐私 | 走腾讯云 | 走阿里云 | 走字节云 | 走 ToDesk | 100% 本机 |
| 价格 | 免费 5000 积分，付费 99 元/月 | 免费 300 积分，59 元/月 | 68~500 元/月 | 免费/118 元/年 | 免费开源 |
| 微信渠道 | 微信小程序/微信/企微/钉钉/飞书 | 微信/钉钉/飞书 | 仅飞书 | 微信小程序 | 官方 iLink Bot API |

**结论**：在"只在这台 Mac、任意操控、主力 Cursor 写码、手机微信遥控、自备 DeepSeek/百炼 Key"五项条件下，**OpenClaw 自建是唯一全部满足的方案**。商业产品均为 SaaS，数据走云端，且 Cursor 集成弱或不可控。

---

## 二、各产品详解

### 1. WorkBuddy（腾讯云）

- **定位**：全场景桌面 AI 智能体工作站，主打腾讯生态适配，与 CodeBuddy 共用账号与积分。
- **发布时间线**：2026-02 内测 → 03-09 正式上线 → 06-05 企业版。
- **电脑操控**：具备 Computer Use，但第三方 8 任务实测中默认"爱写代码绕路"（打开浏览器等操作用脚本实现而非直接 GUI），完成同一任务比竞品多花约 20 分钟。
- **手机遥控**：IM 生态最全——微信小程序、微信、企业微信、钉钉、飞书、Slack/Telegram/Discord 都能接，支持从手机触发桌面任务。
- **模型开放**：唯一支持外接 OpenAI 兼容协议 API 的国产桌面 Agent，可接入 DeepSeek 等（用你的 DeepSeek Key 可行）。
- **价格**：注册送 5000 积分，签到月入约 3000-4000 积分；付费版 99 元/月（2000 积分）。计费透明度最好（开跑前给费用预估）。
- **不足**：数据走腾讯云；电脑操控能力在实测中偏弱；积分是虚拟货币，可比性差。

### 2. QoderWork（阿里）

- **定位**：Qoder 的 Agent 能力从代码扩展到日常办公，2026-01-30 发布，3-03 全面开放 Mac/Windows，另有 Mobile 端。
- **电脑操控**：较强，与豆包方案类似，需手动开启系统权限；右侧任务监控面板显示待办进度和所用技能。
- **手机遥控**：打通钉钉、微信、飞书三大国内 IM，另可下载 Mobile App；实测中唯一能通过 IM 主动通知用户的方案。
- **模型**：不支持外接自定义模型，但支持所有主流国产模型（含通义）。
- **价格**：社区版 0 元，注册送 2 周 Pro 试用+300 积分；Pro 59 元/月（2000 积分）；签到每天送 100 积分。
- **不足**：多模态弱、上手略难、需手动配权限；数据走阿里云。

### 3. 豆包专业版（字节）

- **定位**：办公任务模式，操作本地电脑、浏览器、Skills、定时任务，内置 Office 套件。
- **电脑操控**：三家实测中最强最顺滑（后台开网页、滚动、翻页一气呵成）。
- **手机遥控**：仅支持飞书，无微信生态，且切企业账号入口不顺畅。
- **模型**：完全封闭，仅豆包自家模型。
- **多模态**：最强，内置 Seedream 图像 + Seedance 视频模型。
- **语音**：独家支持边通话边共享屏幕（远程指导长辈神器）。
- **价格**：标准 68 元/月、加强 200 元/月、高级 500 元/月。
- **不足**：生态封闭；IM 只认飞书；付费版额度撑不起高频视频需求。

### 4. ToDesk AI（ToClaw）

- **定位**：基于 OpenClaw 深度优化的 AI 远程控制，内置于 ToDesk，从"控制电脑"进化为"指挥电脑"。
- **能力**：Computer Use 操控远端 GUI、跨应用调度、7×24 无人值守定时任务；账号为中心，多设备协同集群。
- **手机**：Android/iOS/微信小程序均可。
- **模型**：内置六款大模型，模型灵活性一般。
- **价格**：个人版免费，专业版 118 元/年；ToClaw 公测免费。
- **不足**：模型不可外接自定义；数据走 ToDesk 云；深度代码能力不如本地方案。

### 5. OpenClaw（开源，已选定并部署）

- **定位**：个人 AI 助手框架，运行在自己电脑上，通过 29 种消息通道（WhatsApp/Telegram/Discord/Slack/Signal/iMessage/微信等）聊天并实际操控设备。
- **电脑操控**：shell 命令、文件操作、浏览器（web/browser 插件）、AppleScript（GUI 自动化）、屏幕截图/录制、Canvas A2UI，本质上是完整本机 Agent。
- **手机遥控**：官方微信通道 `@tencent-weixin/openclaw-weixin`（腾讯微信团队维护），走官方 iLink Bot API（`ilinkai.weixin.qq.com`），扫码创建 bot 身份（`xxx@im.bot`），私聊收发消息，安全合规无封号风险。
- **模型**：官方 DeepSeek provider 插件 + 官方 Qwen（阿里百炼）provider 插件，OpenAI 兼容，可自由切换主/备用模型。
- **Cursor 集成**：可用 Cursor Agent SDK（`@cursor/sdk`）+ 自备 `CURSOR_API_KEY` 直接驱动 Cursor Agent 在本地项目写代码。
- **数据隐私**：100% 本机，状态存 `~/.openclaw`，API 请求直连各模型厂商。
- **价格**：完全免费开源。

---

## 三、微信接入方案对比（手机遥控 Mac）

| 方案 | 渠道 | 安全性 | 是否需公网 | 群聊 | 备注 |
|---|---|---|---|---|---|
| **微信 iLink Bot API（OpenClaw 官方插件）** | 微信 | 官方合规（腾讯 ClawBot） | 否 | 仅私聊 | 本次部署采用的方案 |
| 微信个人号桥接（openclaw-weixin UI 自动化） | 微信 | 有风控风险 | 否 | 可 | 体验最像真人但易触发封号 |
| Telegram / Discord 等 IM | 海外 | 官方 API | 视情况 | 可 | 国内需代理 |
| 微信小程序（WorkBuddy 等） | 微信 | 商业合规 | 否 | - | 数据走厂商云 |

---

## 四、本机部署实录（2026-08-17）

### 环境
- macOS 12.6.1（Intel），Node v24.15，Homebrew，已装 Cursor/Claude/微信。

### 已完成的配置
1. **OpenClaw 2026.7.1-2** 通过 npm 全局安装（本机 curl SSL 证书问题不影响 npm）。
2. **模型提供商**：
   - 主模型 `deepseek/deepseek-v4-flash`（`DEEPSEEK_API_KEY`，已连通，status 200）
   - 备用模型 `qwen/qwen3.5-plus`（阿里百炼，`DASHSCOPE_API_KEY`，已连通，status 200）
   - Cursor Key `CURSOR_API_KEY` 存于 `~/.openclaw/.env`（权限 600）
3. **微信通道**：`openclaw-weixin` v2.4.6 官方插件，已扫码登录（bot: `2c2b05571dbf-im-bot`），通道 running。
4. **安全白名单**：将本人微信 ID 写入 allowFrom 白名单，仅自己可控制。
5. **Cursor 集成**：`~/.openclaw/cursor/cursor-run.mjs`（基于 `@cursor/sdk`）+ `cursor-code` skill，已验证端到端（在 `/tmp/cursor-demo` 生成 `hello.txt` 和 `app.py` 并成功运行）。
6. **macOS 权限**：辅助功能、屏幕录制、通知均已可用。
7. **网关**：LaunchAgent 守护进程，端口 18789，loopback + token 认证，7×24 待命。

### 已验证的功能链路
- 微信发消息 → DeepSeek 回复 ✓
- Agent 本机执行 shell/AppleScript（查电量、系统事件） ✓
- Cursor Agent SDK 写代码并运行 ✓
- 模型主备切换（DeepSeek → 百炼） ✓

### 备注 / 限制
- **macOS 菜单栏 App（OpenClaw.app）** 需要更高系统版本（本机 macOS 12.6 报 `kLSIncompatibleSystemVersionErr`）。CLI + Gateway 方式已具备全部核心能力，App 仅是便利界面，不影响使用。
- 微信 iLink bot 仅支持**私聊**，不支持群聊。
- 本机需保持开机（可配合 `caffeinate` 或系统设置防休眠）以便远程随时待命。

---

## 五、选型建议

- **如果你要"开箱即用、不想折腾、能接受数据上云"** → WorkBuddy（微信生态最全、可外接 DeepSeek、计费透明）或豆包专业版（操控最强但封闭）。
- **如果你要"完全本地、任意操控、深度驱动 Cursor、用自己 Key、微信遥控"** → 本次已部署的 **OpenClaw 自建方案**。

### 日常使用示例
- 微信发："帮我查一下这台 Mac 还剩多少电" → 本机执行 `pmset -g batt` 并回复。
- 微信发："用 Cursor 在 ~/Projects/demo 写一个 Python 脚本处理 CSV" → 调用 Cursor Agent 完成并汇报。
- 微信发："明天早上 9 点提醒我开会" → OpenClaw 定时任务 + 微信通知。

---

## 六、安全提示

- 三个 API Key 曾在对话中出现，建议在各自平台**轮换新的 Key** 后更新 `~/.openclaw/.env`（权限已设 600）。
- `~/.openclaw` 目录含模型凭据与微信 token，勿分享、勿备份到云盘明文。
- 高风险操作（删除文件、git push、改系统配置）建议保持人工确认习惯。
