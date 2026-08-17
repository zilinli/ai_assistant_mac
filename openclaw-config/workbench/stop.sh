#!/bin/bash
# 停止修修工作台
if lsof -tiTCP:18790 -sTCP:LISTEN >/dev/null 2>&1; then
  lsof -tiTCP:18790 -sTCP:LISTEN | xargs kill 2>/dev/null
  sleep 1
  echo "工作台已停止"
else
  echo "工作台未在运行"
fi
