#!/usr/bin/env bash
# Bolt Console API 验收：health / Range / 媒体 / Office 预览
set -euo pipefail

BASE="${CONSOLE_URL:-http://127.0.0.1:18790}"
TASKS="${HOME}/tasks"
SONG_DIR="${TASKS}/2026-08-17-世界杯西班牙之歌"
FIX="${TASKS}/_console-fixtures"
VENV="${HOME}/.openclaw/venv/bin/python3"
fail=0

check() {
  local name="$1"; shift
  if "$@"; then
    echo "OK  $name"
  else
    echo "FAIL $name"
    fail=1
  fi
}

echo "=== health ==="
HEALTH=$(curl -sf "$BASE/api/health")
echo "$HEALTH"
check "version 2.0" grep -q '"version": "2.0"' <<<"$HEALTH"
check "product Console" grep -q 'Bolt Console' <<<"$HEALTH"

echo ""
echo "=== existing media ==="
SONG_PATH="2026-08-17-世界杯西班牙之歌/song.mp3"
COVER_PATH="2026-08-17-世界杯西班牙之歌/封面.png"
LYRIC_PATH="2026-08-17-世界杯西班牙之歌/歌词.md"

RANGE=$(curl -sI -H "Range: bytes=0-1023" "$BASE/api/media?path=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$SONG_PATH")")
echo "$RANGE" | head -8
check "audio 206" grep -qi "HTTP/1.0 206" <<<"$RANGE" || grep -qi "HTTP/1.1 206" <<<"$RANGE"
check "accept-ranges" grep -qi "Accept-Ranges: bytes" <<<"$RANGE"
check "content-range" grep -qi "Content-Range: bytes 0-1023/" <<<"$RANGE"

COVER_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/api/media?path=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COVER_PATH")")
check "cover 200" test "$COVER_CODE" = "200"

MD=$(curl -sf "$BASE/api/file?path=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$LYRIC_PATH")")
check "lyrics md nonempty" test -n "$MD"

echo ""
echo "=== office fixtures ==="
mkdir -p "$FIX"
"$VENV" - <<'PY'
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches
import pandas as pd
import pypandoc

fix = Path.home() / "tasks" / "_console-fixtures"
fix.mkdir(parents=True, exist_ok=True)

docx = fix / "sample.docx"
pypandoc.convert_text("# Console 验收\n\n这是一段用于预览的 **Word** 正文。", "docx", format="md", outputfile=str(docx))

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Bolt Console"
slide.placeholders[1].text = "PPT 预览验收页"
prs.save(str(fix / "sample.pptx"))

pd.DataFrame({"品类": ["家电", "数码"], "销售额": [42, 18]}).to_excel(str(fix / "sample.xlsx"), index=False)
print("wrote fixtures", list(fix.iterdir()))
PY

enc() { python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1"; }

DOCX=$(curl -sf "$BASE/api/preview?path=$(enc "_console-fixtures/sample.docx")")
echo "$DOCX" | head -c 240; echo
check "docx preview" grep -q "Word\|Console\|验收" <<<"$DOCX"

PPTX=$(curl -sf "$BASE/api/preview?path=$(enc "_console-fixtures/sample.pptx")")
echo "$PPTX" | head -c 240; echo
check "pptx preview" grep -q "Console\|PPT\|预览" <<<"$PPTX"

XLSX=$(curl -sf "$BASE/api/preview?path=$(enc "_console-fixtures/sample.xlsx")")
echo "$XLSX" | head -c 240; echo
check "xlsx preview" grep -q "家电\|销售额" <<<"$XLSX"

DL=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/api/download?path=$(enc "$SONG_PATH")")
check "download 200" test "$DL" = "200"

TASKS_JSON=$(curl -sf "$BASE/api/tasks")
check "kind audio" grep -q '"kind": "audio"' <<<"$TASKS_JSON"
check "kind image" grep -q '"kind": "image"' <<<"$TASKS_JSON"

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "✅ Bolt Console API 验收通过"
else
  echo "❌ 有失败项"
  exit 1
fi
