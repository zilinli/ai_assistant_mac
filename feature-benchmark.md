# WorkBuddy 功能对标与取长补短分析

> 更新日期：2026-08-17
> 对标基准：本机已安装 WorkBuddy v5.3.8（腾讯云，`/Applications/WorkBuddy.app`）+ 官方文档 + 本机实测记录
> 对比对象：本机 OpenClaw 自建方案（`ai-assistant`）、国内同类产品、海外同类产品
> 文档定位：`comparison.md` 是**选型**层面的对比（结论：OpenClaw 胜出）；本文是**功能级**对标——逐项拆解 WorkBuddy 与竞品功能，找出差距并落地为可执行改进路线图。

---

## 一、分析前提

| 约束 | 说明 |
|---|---|
| 硬件系统 | 单台 Intel Mac（macOS 12.6.1） |
| 核心场景 | 微信手机遥控电脑、Cursor 驱动写代码、日常办公自动化 |
| 模型 | 自备 DeepSeek / 阿里百炼 API Key，可自由切换主备 |
| 隐私要求 | 数据尽量留本机，不接受纯 SaaS 云端托管 |
| 现状 | OpenClaw 2026.7.1-2 已部署（gateway 18789 + 微信 iLink 私聊 + 4 个 skill） |

**一句话定位差异**：WorkBuddy 是"开箱即用的商用 Agent 工作台"（云端算力 + 技能市场 + 企业生态），OpenClaw 是"完全自控的个人 Agent 框架"（本机执行 + 任意扩展）。两者的差距不在框架能力，而在**产品化程度**——WorkBuddy 把能力做成了 UI、市场、模板和交付物管理；OpenClaw 把这些能力都暴露为 CLI/配置，需要自己组装。

---

## 二、WorkBuddy 深度功能清单（官方 + 本机实测）

### 2.1 产品定位

腾讯云出品，全场景桌面 AI Agent 工作站。一句话描述需求 → 自动拆解任务 → 多 Agent 并行执行 → 交付可验证成果（文档/表格/PPT/报告）。与 CodeBuddy 共用账号积分体系，属于腾讯 CodeBuddy 团队产品线。2026-02 内测 → 03-09 正式上线 → 06-05 企业版。

### 2.2 官方能力矩阵

| 能力 | 说明 |
|---|---|
| 自然语言理解 | 一句话分配任务，无需复杂操作 |
| 自主规划与执行 | 自动拆解任务、规划步骤、执行操作 |
| 多模态任务处理 | 文档、表格、演示、数据分析 |
| 本地文件操作 | 读取授权文件夹，批量处理本地文件 |
| 深度研究 | 复杂课题多来源调研，输出结构化报告 |
| 任务管理 | 任务列表、状态筛选、续跑任务 |
| 成果面板 | 查看产物、全部文件、变更与预览 |
| 主动工作 | 定时任务、到期/变更主动推送 |

### 2.3 本机实测（v5.3.8，917MB，Electron + app.asar 打包）

**内置 Skills（18 个，`app.asar.unpacked/resources/builtin-skills/`）**

| Skill | 能力领域 |
|---|---|
| `ardot-design-core / router / to-code / poster / slides / ui-design` | Ardot 设计全链路：UI 设计、海报、幻灯片、设计转代码 |
| `buddy-multimodal-generation` | 多模态内容生成（图片/多形态输出） |
| `tencent-local-office-edit`（含 `edsdk.py`、sheet/slide 文档） | 本地 Office 文档编辑（Word/Excel/PPT 读写） |
| `tencent-docs-routing` | 腾讯文档路由（云文档能力分发） |
| `expert-manager` | 专家 Agent 管理（100+ 专家角色） |
| `skill-creator`（含 scripts） | 技能创作器——让 AI 自己写新 skill |
| `marketplace-skill-installer` | 技能市场安装器 |
| `westock-data / westock-tool / wb-finance-skill / neodata-financial-search` | 金融数据与财经搜索 |
| `geo-map-compliance-guard` | 地图合规审查 |
| `cloudstudio-deploy` | CloudStudio 云端部署 |

**内置插件（3 个）**：`tencent-docs-plugin`（腾讯文档）、`tencent-pptx`（PPT 生成）、`weixinpay`（微信支付）

**内置 MCP App（3 个）**：`_workbuddy-runtime`（运行时）、`agently-cli`、`ardot-mcp-app`（设计）

**结论**：WorkBuddy 的能力构成 = **技能市场 + 腾讯生态插件 + MCP App + 专家 Agent 编排**，与 OpenClaw 的"skills + plugins + MCP"架构同构——说明架构思路趋同，差距在生态丰富度和开箱即用程度。

### 2.4 你的实际使用记录（本机 `~/WorkBuddy/`）

| 日期 | 任务 | 产出 |
|---|---|---|
| 08-03 | Spark AI Tutor 代码审查 + 产品分析 | `spark_analysis_report.html`、`Spark_AI_Tutor_分析报告.md`、`test_spark.sh` |
| 08-03→08-12 | Spark AI Tutor v2/v3/v4 迭代分析（clone GitHub 仓库、读源码、多轮追问） | `Spark_AI_Tutor_v2/3/4_深度分析报告.md`、`益智游戏设计方案.md` |
| 08-05 | 空任务（仅建目录） | `.workbuddy/` 骨架 |

实测要点：
- WorkBuddy 会**自动 clone GitHub 仓库、通读源码、连续多天在相同工作目录续做任务**（v1→v4 记忆延续）。
- 它的记忆结构是 `~/WorkBuddy/<task-id>/.workbuddy/memory/YYYY-MM-DD.md + MEMORY.md`——与 OpenClaw 的记忆机制**几乎完全一致**。
- 产出物（`.md`/`.html`/`.sh`）直接落盘到任务目录，天然是"可验证交付物"。

### 2.5 WorkBuddy 其他关键能力（官方信息）

- **IM 遥控矩阵**：微信小程序 / 微信 / 企业微信 / 钉钉 / 飞书 / Slack / Telegram / Discord（手机发消息触发桌面任务）。
- **模型开放**：国产桌面 Agent 中少见的支持外接 OpenAI 兼容协议 API（可接 DeepSeek）；官方也宣称支持混元/DeepSeek/GLM/Kimi 等。
- **连接器**：GitHub / GitLab / Jira / Confluence / Google Drive / Gmail / Notion / Slack 等授权后跨平台工作流。
- **安全**：沙箱隔离、工作区隔离、文件访问授权、敏感操作二次确认、技能安装前安全扫描、企业 VPC 选项。
- **计费**：注册送 5000 积分、每日签到奖励、付费 99 元/月（2000 积分）、Team 版 $40/席位/月；开跑前给费用预估。
- **生态动作**：7-25 上架鸿蒙电脑应用市场（首个桌面办公智能体）；7-30 发布 V5.3.x；官方宣称兼容 OpenClaw 技能体系与 MCP 协议。

---

## 三、国内外同类产品图谱

### 3.1 国内（按"办公自动化 vs 模型驱动 vs 生态绑定"分类）

| 产品 | 阵营 | 定位 | 关键能力 |
|---|---|---|---|
| **WorkBuddy**（腾讯） | 办公自动化 | 全场景桌面 Agent 工作台 | 技能市场+腾讯生态+IM 遥控+外接模型 |
| **豆包专业版**（字节） | 办公自动化 | 任务模式电脑操控 | 三家中电脑操控最顺滑、多模态最强（Seedream 图像+Seedance 视频）、独家边通话边共享屏幕；仅飞书 IM、模型封闭 |
| **QoderWork**（阿里） | 编程→办公 | Qoder Agent 扩展到日常办公 | 电脑操控强、钉钉/微信/飞书+App、主动 IM 通知；不支持外接模型 |
| **Kimi Work**（月之暗面） | 模型驱动 | 长文档/深度研究 + Agent Swarm | Kimi K2.6 长程任务：13h 连续编码、300 子 Agent 并行、4000+ 工具调用；Work/Chat 双模式 |
| **Trae Work**（字节，原 TRAE Solo） | 编程 | 企业级全栈开发 | 从开发者工具转向更广泛人群 |
| **ToDesk AI / ToClaw**（久尺） | 远程操控 | OpenClaw 深度定制的 AI 远程控制 | Computer Use 操控远端 GUI、7×24 无人值守定时任务、内置 ToDesk；6 款内置模型、数据走 ToDesk 云 |
| **元宝**（腾讯） | 生态绑定 | 飞书/钉钉智能代理层 | 深度绑定企业工作流（多维表格公式、审批流）；离开飞书/钉钉生态能力骤减、不能上网 |
| **通义千问**（阿里） | 生态绑定 | 阿里云企业级综合 | Qwen 全家桶、中文创作、企业方案均衡 |

### 3.2 海外（按"托管 Agent vs 本地桌面 Agent vs 自托管"分类）

| 产品 | 阵营 | 定位 | 关键能力 |
|---|---|---|---|
| **ChatGPT Agent / Work**（OpenAI） | 托管 Web Agent | 虚拟浏览器执行网页任务 | GPT-5.6、并发子 Agent、表单填写/购物/订票；文件访问弱（走集成） |
| **Claude Cowork**（Anthropic） | 本地桌面 Agent | 桌面文件系统多步工作 | 直接读写本地文件、Microsoft 365 全读写、定时任务、子 Agent；捆绑 Claude Pro/Max |
| **Gemini for Mac**（Google） | 屏幕感知 Agent | Google Workspace 深度集成 | 屏幕识别、Gmail/Calendar/Drive 原生 |
| **Lindy** | 垂直工作助手 | 邮箱/日历/会议自动化 | 按邮箱配置、多触发器工作流、Computer Use；$50/月起，积分计量 |
| **Manus** | 通用 Agent | 自主完成端到端任务 | 云端通用 Agent |
| **Genspark** | 内容工作台 | 研究→内容/汇报全流程 | 研究到 Deck 工作流 |
| **MultiOn** | 网页自动化基建 | Web Agent API | 网页自动化基础设施 |
| **Khoj** | 自托管 | 个人知识 AI | 自托管、本地知识库 |
| **Open Interpreter** | 自托管 | 自然语言驱动电脑 | 代码方式控制电脑 |
| **Martin** | 语音委托 | 短信/电话任务 | 语音优先委派，$40/月 |
| **Mem Agents** | 记忆优先 | 个人上下文记忆 | 长期记忆 + 免费档 |

### 3.3 行业格局小结

```
国产路线分化：
  生态绑定派（腾讯 WorkBuddy / 元宝、阿里 QoderWork / 通义）── 拼集成、拼渠道、拼 IM
  模型驱动派（Kimi Work）────────────────────────────── 拼长上下文、拼 Agent 规模
  操控体验派（豆包专业版、ToDesk AI）────────────────── 拼电脑操控顺滑度、拼多模态

海外路线分化：
  桌面文件派（Claude Cowork）────────────────────────── 本地文件系统 + 交付物
  网页代理派（ChatGPT Work）─────────────────────────── 虚拟浏览器 + 网页任务
  屏幕感知派（Gemini for Mac）───────────────────────── Google 生态 + 屏幕理解
  垂直工作派（Lindy / Cove / Martin / Granola）──────── 单点深度（邮箱/日历/会议/语音）

你的 OpenClaw 自建方案：
  本质是"自托管通用 Agent"，能力面最接近 Claude Cowork（本地文件+工具调用）
  + ToDesk AI（远程遥控）的合体，但缺少两者的产品化包装。
```

---

## 四、功能对标矩阵

图例：**● 有 / ◐ 部分有 / ○ 无**。空格为不适用或不确定。

| # | 能力维度 | 我的方案（OpenClaw 自建） | WorkBuddy（腾讯） | 国内代表（豆包/Qoder/Kimi） | 海外代表（Cowork/ChatGPT/Gemini/Lindy） |
|---|---|---|---|---|---|
| 1 | 本地电脑操控（shell/文件/GUI） | ● shell+AppleScript+截图+文件 | ● 沙箱+授权文件夹+本地 Office 编辑 | ● 豆包操控最顺、Qoder 较强 | ● Claude Cowork 本地文件系统 |
| 2 | IM 手机遥控 | ● 微信 iLink（仅私聊） | ● 微信/企微/钉钉/飞书/Slack/Telegram/Discord | ● 豆包仅飞书；Qoder 三 IM+App | ○ 海外无微信；Cowork 有手机端 |
| 3 | 模型接入与路由 | ● 任意 OpenAI 兼容，主备切换 | ● 外接 OpenAI 兼容 + 内置多模型 | ○ 豆包封闭；Qoder 不支持外接 | ○ 各家用自家模型 |
| 4 | 多智能体/子任务并行 | ◐ 框架支持（acp/attach/agent），未启用 | ● 100+ 专家 Agent + 并行执行 | ● Kimi 300 子 Agent；Qoder 任务面板 | ● Cowork 子 Agent；ChatGPT 并发子 Agent |
| 5 | 深度研究 | ◐ DuckDuckGo+浏览器，无结构化 pipeline | ● Deep Research 报告模板 | ● Kimi 长文归纳最强 | ● ChatGPT 网页研究；Genspark 研究→Deck |
| 6 | 文档/Office 生成 | ○ 无（只能裸写文本） | ● 本地 Office 编辑 + 腾讯文档 + PPT 生成 | ● 豆包内置 Office 套件 | ● Cowork M365 全读写 |
| 7 | 数据分析与可视化 | ◐ 可 shell 跑脚本，无专门 skill | ● 上传数据自动分析可视化 | ● Kimi Sheets | ● Cowork Excel pipeline |
| 8 | 多模态（图像/语音/视频） | ◐ 模型支持图片输入（qwen 系），无生成 | ● buddy-multimodal 生成 | ● 豆包最强（Seedream/Seedance+语音通话） | ◐ ChatGPT 图像/语音；Gemini 屏幕感知 |
| 9 | 技能市场与扩展 | ● ClawHub + 本地 skills（4 个） | ● 技能市场 + 内置 18 skills | ○ 少 | ● Cowork 集成生态 |
| 10 | MCP 支持 | ● 原生支持（`openclaw mcp`），未配置任何 server | ● 内置 3 个 MCP App + MCP 协议兼容 | ○ 少 | ● Claude MCP 是其核心 |
| 11 | 连接器（第三方服务） | ○ 无 | ● GitHub/Jira/Notion/Gmail/Drive 等 | ◐ Qoder/通义有企业连接 | ● Cowork 365、Gemini Workspace、Lindy 邮箱 |
| 12 | 记忆与 RAG | ◐ 文件式记忆（daily + MEMORY.md），无向量检索 | ● 任务级记忆（.workbuddy/memory） | ◐ Kimi 长上下文记忆 | ● Mem/Lindy 长期记忆 |
| 13 | 定时任务与主动推送 | ● cron + 心跳（心跳已禁用） | ● 定时任务 + 主动工作 | ● Qoder IM 主动通知；ToDesk 无人值守 | ● Cowork 定时任务；Lindy 多触发器 |
| 14 | 编程/Cursor 集成 | ● Cursor Agent SDK 直接驱动（独有） | ○ 面向办公，代码弱 | ◐ Qoder/Trae 面向代码 | ○ Cowork 侧重办公文件 |
| 15 | 安全与沙箱 | ◐ 本地白名单+高风险确认，无沙箱 | ● 沙箱+授权+技能扫描+VPC | ◐ 权限配置 | ● Cowork 隔离 VM（Dispatch） |
| 16 | 任务/工件交付管理 | ○ 无 UI，靠文件 + 微信汇报 | ● 任务列表+结果面板+产物预览 | ● Qoder 任务监控面板 | ● Cowork 交付物面板 |
| 17 | 计费透明度 | ● 仅按 API Key 用量 | ● 积分制+费用预估（透明度高） | ◐ 积分制不透明 | ● 订阅制 |

---

## 五、差距分析（取长补短）

### 5.1 保持的强项（不丢）

1. **模型自主权**：任意 OpenAI 兼容模型 + 主备切换，所有商业产品都无法做到。
2. **Cursor 深度集成**：直接驱动 Cursor Agent SDK 写代码并回传结果——这是 WorkBuddy 和所有竞品的明确短板。
3. **数据 100% 本机**：相比 WorkBuddy/豆包/Qoder 的云端数据，隐私优势不可让渡。
4. **成本为零**：无订阅费，只有 API 用量费（DeepSeek V4 Flash 约 ¥0.14/M 输入）。
5. **微信官方通道**：iLink Bot API 合规无封号风险（相比个人号桥接）。

### 5.2 差距（需要补）

| 差距 | 影响 | 对应 WorkBuddy/竞品能力 |
|---|---|---|
| **无任务/工件管理**：执行结果散落文件，微信只能收文字摘要 | 长任务不可追溯、不可续跑、成果难找回 | WorkBuddy 任务列表 + 结果面板 + 产物预览 |
| **文档/Office 生成为零**：无法产出 docx/pptx | 最常用的办公交付场景缺失 | WorkBuddy 本地 Office 编辑 + PPT；Cowork M365 |
| **MCP 空白**：框架原生支持但 0 个 server 配置 | 无法对接外部工具生态（本机 App、第三方服务） | WorkBuddy 内置 3 MCP App；Claude 的 MCP 核心 |
| **深度研究无 pipeline**：有搜索但无交叉验证/报告模板 | 研究类任务质量不稳 | WorkBuddy Deep Research；Kimi 长文 |
| **记忆无检索**：只有追加式文件，无向量索引 | 信息越多越难找到历史结论 | WorkBuddy/Kimi/Mem 的记忆检索 |
| **心跳禁用**：主动能力关掉 | 错过邮件/日历/天气等主动提醒 | Qoder IM 主动通知；WorkBuddy 主动工作 |
| **连接器为零**：无 Gmail/日历/文档授权 | 无法做跨服务工作流 | WorkBuddy/Cowork/Lindy 连接器 |
| **无数据分析可视化 skill** | 数据任务只能裸跑脚本 | WorkBuddy 自动分析可视化；Kimi Sheets |
| **多模态生成缺失** | 不能出图/出语音 | WorkBuddy buddy-multimodal；豆包 Seedream |

### 5.3 值得借鉴但不必照搬

- **技能市场**：WorkBuddy/Kimi 靠市场丰富生态。OpenClaw 已有 ClawHub，但你的 4 个 skill 全是自建——**应多搜多用 ClawHub 现成 skill**，别重复造轮子（`openclaw skills search`）。
- **专家 Agent 角色**：WorkBuddy 100+ 专家。OpenClaw 的 `agents` 子命令支持多 agent 隔离（workspace+auth+routing），可以给不同场景建独立 agent（如"研究 agent"、"文件 agent"），而非单 agent 单人格。
- **费用预估**：WorkBuddy 开跑前报价。OpenClaw 模型配置里有 cost 字段，可做一个"跑前预估 + 跑后记账"的小 skill。
- **任务目录归档**：WorkBuddy 把每次任务产物落独立目录。你的 OpenClaw 可以用 `worktrees` 或约定 `~/WorkBuddy-like/任务目录` 规范。

---

## 六、取长补短落地路线图

按"投入产出比 + 与核心场景相关性"排序。每项都基于 OpenClaw 现有机制（skills/plugins/MCP/agents/hooks），不需要换框架。

> 实施状态（2026-08-17）：✅ 已完成并验证 / 🔄 已部分完成 / 📋 已文档化（受限于平台）

### P0 —— 先补基础短板（高价值，工作量小）

#### P0-1 任务产物目录 + 微信交付物回传 ✅
- **目标**：让每次任务有"可验证交付物"，像 WorkBuddy 结果面板。
- **实现**：约定每个任务在 `~/tasks/<YYYY-MM-DD-任务名>/` 下产出文件；写一个 `task-deliver` skill，完成后自动列出产物清单（路径+预览要点）回传微信；把生成的 md/html/截图文件路径发给用户。
- **改动**：1 个 skill + 微信汇报模板。工作量：小。
- **状态**：`task-deliver` skill 已部署，`~/tasks` 已建并被 memory-rag 纳入索引。

#### P0-2 文档生成 skill（docx/pptx）✅
- **目标**：补齐最常用的办公交付。
- **实现**：装 `pandoc`（md→docx）、`python-pptx`（生成 PPT）；写 `office-docs` skill，模板含报告/周报/会议纪要/PPT 四类。
- **注意**：本机 macOS 12.6，`brew install pandoc` 可用。
- **改动**：1 个 skill + 少量依赖。工作量：小。
- **状态**：brew 因 curl SSL 不可用，改用 `pypandoc-binary`（内置 pandoc 3.9，随 `~/.openclaw/venv` 提供）；venv 已装 pptx/pandas/matplotlib；md→docx 冒烟测试通过。

#### P0-3 启用并扩展心跳（主动推送）✅
- **目标**：恢复 WorkBuddy/Qoder 级别的主动能力。
- **实现**：重新启用 OpenClaw heartbeat（默认 30 分钟）；在 `HEARTBEAT.md` 写检查清单（邮件/日历/天气，先做天气 `curl wttr.in` 和系统健康）。
- **改动**：改 `HEARTBEAT.md` + 配置。工作量：极小。
- **状态**：`HEARTBEAT.md` 已从纯注释改为实际检查清单（系统健康/天气/定时任务/记忆整理/任务巡检 + 主动联系阈值 + 安静时段）。

#### P0-4 记忆检索化（轻量 RAG）✅
- **目标**：从"追加式记忆"升级为"可检索记忆"。
- **实现**：`openclaw memory` 已有 search/inspect/reindex；先用它做关键词检索，后续再用本地向量库（如 `chromadb`/`sqlite-vec`）给 `memory/` 和 `MEMORY.md` 建索引；每次会话启动自动检索相关历史注入上下文。
- **改动**：一个 `memory-rag` 脚本 + hook 配置。工作量：中。
- **状态**：`agents.defaults.memorySearch` 已配置 provider=`openai-compatible`（百炼 `text-embedding-v4`，复用 `DASHSCOPE_API_KEY`，零新增成本），extraPaths 含 `~/tasks`；索引重建成功（Embeddings ready）；`memory-rag` skill 已部署。

### P1 —— 提升生产力（中价值，工作量中）

#### P1-1 配置 MCP server，接入本机与第三方工具 ✅
- **目标**：解锁 MCP 生态（WorkBuddy 内置 3 个 MCP App，这是它的扩展核心）。
- **实现**：用 `openclaw mcp add` 接入高价值 server：浏览器控制（如 Playwright MCP）、文件/图片处理、Notion/飞书、GitHub；`openclaw mcp probe` 验证。
- **改动**：纯配置 + 逐步试。工作量：中。
- **状态**：已接入 `filesystem` MCP server（14 个工具，沙箱目录限 `~/tasks`、workspace/memory、`~/Documents`）。GitHub/Notion 需用户提供 token，留待后续。

#### P1-2 深度研究 pipeline skill ✅
- **目标**：从"搜了就答"升级为"结构化研究报告"。
- **实现**：`deep-research` skill：多轮 DuckDuckGo + 网页抓取 → 交叉验证 → 生成结构化 md 报告（背景/结论/竞品矩阵/建议）→ 用 P0-2 转 docx。
- **改动**：1 个 skill。工作量：中。
- **状态**：`deep-research` skill 已部署。

#### P1-3 数据分析与可视化 skill ✅
- **目标**：数据任务出图表报告。
- **实现**：`data-analysis` skill：pandas 读 CSV/Excel → 清洗统计 → matplotlib 出图 → md 结论 + 图表 → 回传微信（附路径，微信不支持图表渲染就发本地路径）。
- **改动**：1 个 skill + python 依赖。工作量：中。
- **状态**：`data-analysis` skill 已部署，中文图表字体已校准（Arial Unicode MS/Hiragino Sans GB），出图冒烟测试通过。

#### P1-4 多 Agent 分工（借鉴 WorkBuddy 专家体系）✅
- **目标**：不同场景独立 agent，避免单 agent 上下文互相污染。
- **实现**：用 `openclaw agents` 建 2-3 个 agent（如 `coder` 带 Cursor skill、`office` 带文档 skill、`default` 聊天）；主 agent 按任务分派。
- **改动**：配置 + 少量 skill 适配。工作量：中。
- **状态**：`coder`（cursor-code/command-correct）与 `office`（office-docs/deep-research/data-analysis/media-gen/cost-tracker）已创建，`openclaw agent --agent coder --local` 端到端验证通过。

#### P1-5 连接器：日历/天气/邮件基础接入 ✅
- **目标**：跨服务基础工作流。
- **实现**：先做无需 OAuth 的（天气 wttr、公共日历 iCal 抓取）；邮件建议暂缓（需要 Gmail API 授权或本地 Mail.app 读，`openclaw webhooks` 可做接收端）。
- **改动**：skill + 授权。工作量：中。
- **状态**：`connectors-basic` skill 已部署：天气（wttr.in，`curl -k`）+ 中国节假日（holiday-cn JSON），均已实测可用。

### P2 —— 进阶增强（视需要）

| 项目 | 说明 | 工作量 | 状态 |
|---|---|---|---|
| 多模态生成 | 接入图像（如通义万相/即梦 API）与 TTS（已有 ElevenLabs `sag`），形成"文字+图+语音"交付 | 中 | ✅ `media-gen` skill 已部署；万相文生图异步链路实测通过；TTS 端点待百炼文档核验 |
| Computer Use / GUI 操控增强 | macOS Accessibility API（如 `cliclick`/`osascript` 组合）实现点按拖拽；注意需辅助功能授权 | 中 | ✅ `computer-use` skill 已部署；cliclick 5.1 已装 `~/bin/cliclick`；需用户确认辅助功能授权 |
| 群聊支持 | iLink bot 仅私聊；如需群聊需评估个人号桥接（有风控）或转 Telegram | 中（有风险） | 📋 已在 `WEIXIN_COMMANDS.md` 文档化（Telegram/个人号桥接方案与风险） |
| 费用记账 skill | 利用 openclaw.json 的 cost 字段做 API 用量记账 + 周报 | 小 | ✅ `cost-tracker` skill 已部署（CSV 月账单） |
| 技能市场使用规范化 | 定期 `openclaw skills search` 发现 ClawHub 现成 skill，替换/补充自建 | 持续 | ✅ 官方 `clawhub` skill 已内置；指令已写入 `WEIXIN_COMMANDS.md` |

---

## 七、总结

- **架构同源，生态差距**：WorkBuddy 和 OpenClaw 的架构（skills + plugins + MCP + 记忆）高度同构，说明你选的框架方向正确；差距全在产品化包装（任务管理 UI、技能市场丰富度、连接器、Office 编辑）。
- **最大不可替代优势**：模型自主 + Cursor 深度集成 + 数据本机——三条全是商业产品给不了的。
- **最该补的三件事（P0）**：任务产物交付物化、Office 文档生成、记忆可检索化。这三件做完，日常使用的"能干事"程度会明显逼近 WorkBuddy。
- **参考事实**：本机 WorkBuddy 实测记录证明它擅长的"clone 仓库 → 读代码 → 多天连续深度分析 → 产出 md/html 报告"这套流程，OpenClaw 完全可以复刻——你已有的 Cursor skill 甚至能做得更深入。
