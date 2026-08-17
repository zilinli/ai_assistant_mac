# API Key 轮换指引

> 更新 `~/.openclaw/.env` 前，请先在下方各平台生成新 Key，然后把新 Key 发给本机助手（或自行编辑 `.env`）。

## 为什么轮换

本机 `.env` 与对话记录中曾出现过 API Key，为安全起见建议轮换：

| 平台 | 用途 | 控制台 |
|---|---|---|
| DeepSeek | 主模型 | https://platform.deepseek.com/api_keys |
| 阿里云百炼（DashScope） | 备用模型 + 万相文生图 | https://bailian.console.aliyun.com（API-KEY 管理） |
| Cursor | 驱动 Cursor Agent SDK | https://cursor.com/settings/api-keys（Settings → API Keys） |
| deAPI.ai | 文生曲（Ace-Step） | https://deapi.ai（Billing / API keys） |

## 轮换步骤

### 1. DeepSeek
1. 登录 https://platform.deepseek.com/api_keys
2. 删除现有 Key，点击「创建 API Key」，复制新 Key（形如 `sk-...`）
3. 新 Key 立即生效，无需等待

### 2. 阿里云百炼
1. 登录 https://bailian.console.aliyun.com
2. 右上角头像 → API-KEY 管理 → 创建新的 API Key（形如 `sk-...`）
3. 可同时停用旧的 Key

### 3. Cursor
1. 登录 https://cursor.com/settings/api-keys
2. 生成新 API Key（形如 `crsr_...`）
3. 旧 Key 可删除

### 4. deAPI（music-gen 文生曲）
1. 登录 [app.deapi.ai/dashboard/api-keys](https://app.deapi.ai/dashboard/api-keys)
2. 点击 **Create new secret key**，复制新 Key（格式通常为 `数字|token`，含 `|`）
3. 更新 `DEAPI_API_KEY='新Key'`（**必须用单引号**）
4. 在 Dashboard 删除或禁用旧 Key
5. 运行下方「验证」中的 deAPI 检查

## 更新方式

拿到四个新 Key 后，任选其一：

**方式 A（推荐）**：把新 Key 直接发到微信或本对话，由助手更新 `~/.openclaw/.env` 并重启网关。

**方式 B（自行编辑）**：编辑 `~/.openclaw/.env`：

```bash
nano ~/.openclaw/.env
```

替换为：

```env
DEEPSEEK_API_KEY='sk-新key'
DASHSCOPE_API_KEY='sk-新key'
CURSOR_API_KEY='crsr_新key'
DEAPI_API_KEY='id|新token'   # 含竖线，必须用单引号
```

格式参考仓库根目录 `.env.example`（勿提交真实 Key）。

保存后执行：

```bash
chmod 600 ~/.openclaw/.env
openclaw gateway restart
```

## 验证

```bash
openclaw gateway status                    # 网关正常
openclaw models status                     # 主/备用模型均可用
openclaw agent -m "hi"                     # 对话正常
openclaw channels status --probe           # 微信通道正常

# deAPI 余额 + music-gen 短片段（约 15s）
bash /Users/chingching/ai-assistant/scripts/verify-deapi.sh
```
