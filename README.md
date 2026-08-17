# ai_assistant_mac 备份仓库

> AI 助理（OpenClaw + 微信遥控 + Cursor 集成）Mac 端配置与文档的版本备份。
> 私有仓库，仅本账号可访问。

## 内容结构

```
├── README.md                 本说明
├── USAGE.md                  ★ 使用手册（微信遥控日常操作指南）
├── comparison.md             AI 助理产品对比文档
├── feature-benchmark.md      WorkBuddy 功能对标 + 取长补短路线图（含实施状态）
├── rotate-keys.md            API Key 轮换指引
├── backup.sh                 一键备份脚本（配置+文档+技能）
├── openclaw-config/          OpenClaw 配置备份
│   ├── openclaw.json         主配置（API key 均为环境变量引用，无明文）
│   ├── openclaw.json.bak     备份副本
│   ├── openclaw.json.last-good 上次可用配置
│   ├── cursor/               Cursor Agent 驱动脚本（cursor-run.mjs）
│   ├── workbench/            修修 Console（server.py + index.html + 启停脚本）
│   └── workspace/            AGENTS.md、技能库、微信指令速查、心跳清单、记忆
└── .gitignore                排除敏感文件
```

## 排除项（敏感，永不提交）

- `~/.openclaw/.env`（API 密钥）
- `~/.openclaw/credentials/`（微信凭据，含 pairing token）
- `~/.openclaw/service-env/`（网关环境）
- `~/.openclaw/identity/`（设备身份）
- `~/.openclaw/logs/`、`state/`、`cache/`
- `cursor/node_modules/`

## 备份方式

```bash
# 一键备份（同步配置 + 提交 + 推送）
bash ~/ai-assistant/backup.sh

# 或手动
cd ~/ai-assistant
cp ~/.openclaw/openclaw.json openclaw-config/
git add -A
git commit --file=/dev/stdin <<'EOF'
backup message
EOF
git push
```

## 恢复方式

1. 从 GitHub 克隆本仓库
2. `openclaw.json` 放回 `~/.openclaw/`
3. 重新创建 `~/.openclaw/.env` 填入新 API key（见 rotate-keys.md）
4. 重新安装 cursor 依赖：`cd ~/.openclaw/cursor && npm install`
5. 微信凭据需重新扫码登录（credentials 未备份）
