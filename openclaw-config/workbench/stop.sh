#!/bin/bash
# 停止修修工作台
pkill -f "openclaw-workbench/server.py" && echo "工作台已停止" || echo "工作台未在运行"
