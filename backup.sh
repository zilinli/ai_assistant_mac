#!/bin/bash
# 一键备份 AI 助理配置到 GitHub（zilinli/ai_assistant_mac）
# 用法: bash ~/ai-assistant/backup.sh
set -e

REPO_DIR="$HOME/ai-assistant"
CONFIG_SRC="$HOME/.openclaw"

cd "$REPO_DIR"

# 1. 同步最新的 openclaw 配置
echo "[1/3] 同步配置..."
cp "$CONFIG_SRC/openclaw.json" openclaw-config/ 2>/dev/null || true
cp "$CONFIG_SRC/openclaw.json.bak" openclaw-config/ 2>/dev/null || true
cp "$CONFIG_SRC/openclaw.json.last-good" openclaw-config/ 2>/dev/null || true
cp "$CONFIG_SRC/cursor/cursor-run.mjs" openclaw-config/cursor/ 2>/dev/null || true
cp "$CONFIG_SRC/cursor/package.json" openclaw-config/cursor/ 2>/dev/null || true
cp "$CONFIG_SRC/workspace/AGENTS.md" openclaw-config/workspace/ 2>/dev/null || true
cp "$CONFIG_SRC/workspace/WEIXIN_COMMANDS.md" openclaw-config/workspace/ 2>/dev/null || true

# 2. 提交
echo "[2/3] 提交变更..."
MSG="backup $(date +%F_%H%M)"
git add -A
if git diff --cached --quiet; then
  echo "无变更，跳过提交"
else
  git -c core.editor=true commit --file=/dev/stdin <<EOF
$MSG
EOF
fi

# 3. 推送
echo "[3/3] 推送到 GitHub..."
git push

echo "✅ 备份完成: $(git rev-parse --short HEAD)"
