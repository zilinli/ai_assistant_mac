#!/usr/bin/env bash
# 验证 deAPI 密钥与 music-gen 技能可用性（读取 ~/.openclaw/.env）
set -euo pipefail

ENV_FILE="${OPENCLAW_ENV:-$HOME/.openclaw/.env}"
SKILL_PY="$HOME/.openclaw/workspace/skills/music-gen/generate_music.py"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "❌ 未找到 $ENV_FILE" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

if [[ -z "${DEAPI_API_KEY:-}" ]]; then
  echo "❌ DEAPI_API_KEY 未设置" >&2
  exit 1
fi

echo "=== 1/2 余额查询 ==="
BALANCE=$(curl -sk -m 20 \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -H "Accept: application/json" \
  "https://api.deapi.ai/api/v2/account/balance")
echo "$BALANCE"
echo "$BALANCE" | grep -q '"balance"' || { echo "❌ 余额接口失败，请检查 Key" >&2; exit 1; }

echo ""
echo "=== 2/2 音乐生成 smoke test（约 10s，10 秒片段）==="
OUT="/tmp/deapi-verify-$(date +%s).mp3"
python3 "$SKILL_PY" \
  --caption "short upbeat test jingle instrumental" \
  --lyrics "[Instrumental]" \
  --duration 10 \
  --out "$OUT"
ls -lh "$OUT"
echo "✅ deAPI 可用：$OUT"
