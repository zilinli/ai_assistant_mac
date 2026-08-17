#!/bin/bash
# 停止修修 Console
if lsof -tiTCP:18790 -sTCP:LISTEN >/dev/null 2>&1; then
  lsof -tiTCP:18790 -sTCP:LISTEN | xargs kill 2>/dev/null
  sleep 1
  echo "修修 Console 已停止"
else
  echo "修修 Console 未在运行"
fi
