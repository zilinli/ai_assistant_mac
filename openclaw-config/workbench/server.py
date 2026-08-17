#!/usr/bin/env python3
"""
修修工作台（OpenClaw Workbench）本地后端
- 仅绑定 127.0.0.1，个人本机使用
- 前端通过 fetch 调用以下 API
- 无第三方依赖，Python 3.9+ 标准库
"""
import json
import os
import subprocess
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 18790
HOST = "127.0.0.1"

HOME = str(Path.home())
TASKS_DIR = os.path.join(HOME, "tasks")
WORKSPACE_DIR = os.path.join(HOME, ".openclaw", "workspace")
MEMORY_DIR = os.path.join(WORKSPACE_DIR, "memory")
SKILLS_DIR = os.path.join(WORKSPACE_DIR, "skills")
WORKBENCH_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(WORKBENCH_DIR, "history.json")

# 允许读取的根目录（产物/记忆/技能），防止目录穿越
ALLOWED_ROOTS = [TASKS_DIR, MEMORY_DIR, SKILLS_DIR]
TEXT_EXTS = {
    ".md", ".txt", ".html", ".json", ".csv", ".log", ".py", ".sh",
    ".mjs", ".js", ".css", ".yml", ".yaml", ".xml", ".ts", ".toml", ".ini",
}

AGENTS = ["main", "coder", "office"]

_tasks = {}  # task_id -> {status, text, error, agent, message, started, duration}
_hist = []   # 最近任务记录
_lock = threading.Lock()


def log(msg):
    print("[workbench] %s" % msg, flush=True)


# ---------------- 任务执行 ----------------

def run_openclaw_agent(task_id, agent, message):
    env = dict(os.environ)
    cmd = ["openclaw", "agent", "--agent", agent, "--json", "-m", message]
    started = time.time()
    try:
        log("run task %s agent=%s msg=%s..." % (task_id, agent, message[:60]))
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=900, env=env)
        out = proc.stdout
        text = None
        try:
            data = json.loads(out)
            payloads = (data.get("result") or {}).get("payloads") or []
            joined = "".join(p.get("text") or "" for p in payloads).strip()
            if joined:
                text = joined
            else:
                text = data.get("status") or data.get("summary") or out[-2000:]
        except json.JSONDecodeError:
            text = out.strip() or ("stderr: " + (proc.stderr or "")[-1000:]) or "（无输出）"
        with _lock:
            _tasks[task_id] = {
                "status": "done",
                "text": text,
                "error": None,
                "agent": agent,
                "message": message,
                "started": started,
                "duration": round(time.time() - started, 1),
            }
    except Exception as e:  # noqa: BLE001
        log("task %s error: %s" % (task_id, e))
        with _lock:
            _tasks[task_id] = {
                "status": "error",
                "text": "",
                "error": str(e),
                "agent": agent,
                "message": message,
                "started": started,
                "duration": round(time.time() - started, 1),
            }


def save_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(_hist[-50:], f, ensure_ascii=False, indent=2)
    except Exception:  # noqa: BLE001
        pass


def load_history():
    global _hist
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, encoding="utf-8") as f:
                _hist = json.load(f)
    except Exception:  # noqa: BLE001
        _hist = []


# ---------------- 文件系统工具 ----------------

def safe_resolve(rel_path):
    """把相对路径解析到允许的根目录内，返回绝对路径或 None。"""
    p = os.path.normpath(rel_path)
    for root in ALLOWED_ROOTS:
        if not os.path.exists(root):
            continue
        cand = os.path.join(root, p)
        cand = os.path.abspath(cand)
        if cand == os.path.abspath(root) or cand.startswith(os.path.abspath(root) + os.sep):
            return cand
    return None


def walk_tree(root, max_depth=3):
    """返回目录树（列表），用于产物面板。"""
    if not os.path.isdir(root):
        return []
    items = []
    for entry in sorted(os.listdir(root), key=lambda x: (not os.path.isdir(os.path.join(root, x)), x.lower())):
        fp = os.path.join(root, entry)
        rel = os.path.relpath(fp, TASKS_DIR)
        if os.path.isdir(fp):
            children = walk_tree(fp, max_depth - 1) if max_depth > 0 else []
            items.append({"name": entry, "type": "dir", "path": rel, "children": children})
        else:
            st = os.stat(fp)
            items.append({
                "name": entry, "type": "file", "path": rel,
                "size": st.st_size, "mtime": int(st.st_mtime),
            })
    return items


def list_skills():
    if not os.path.isdir(SKILLS_DIR):
        return []
    out = []
    for entry in sorted(os.listdir(SKILLS_DIR)):
        skill_dir = os.path.join(SKILLS_DIR, entry)
        if not os.path.isdir(skill_dir):
            continue
        desc = ""
        smd = os.path.join(skill_dir, "SKILL.md")
        if os.path.exists(smd):
            try:
                with open(smd, encoding="utf-8") as f:
                    content = f.read(2000)
                for line in content.splitlines():
                    if line.lower().startswith("description:"):
                        desc = line.split(":", 1)[1].strip().strip('"').strip("'")[:120]
                        break
            except Exception:  # noqa: BLE001
                pass
        out.append({"name": entry, "description": desc})
    return out


def list_memory():
    if not os.path.isdir(MEMORY_DIR):
        return []
    out = []
    for entry in sorted(os.listdir(MEMORY_DIR), reverse=True):
        fp = os.path.join(MEMORY_DIR, entry)
        if os.path.isfile(fp):
            st = os.stat(fp)
            out.append({"name": entry, "size": st.st_size, "mtime": int(st.st_mtime)})
    return out


# ---------------- HTTP 处理 ----------------

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            return self._serve_static("index.html", "text/html; charset=utf-8")

        if path == "/api/health":
            ok = os.path.exists(os.path.join(HOME, ".openclaw", "openclaw.json"))
            return self._json(200, {
                "ok": ok, "tasks_dir": TASKS_DIR, "port": PORT,
                "agents": AGENTS, "version": "1.0",
            })

        if path == "/api/tasks":
            return self._json(200, walk_tree(TASKS_DIR))

        if path == "/api/skills":
            return self._json(200, list_skills())

        if path == "/api/memory":
            return self._json(200, list_memory())

        if path == "/api/history":
            return self._json(200, _hist)

        if path.startswith("/api/task/"):
            tid = path.split("/")[-1]
            with _lock:
                t = _tasks.get(tid)
            if not t:
                return self._json(404, {"error": "task not found"})
            return self._json(200, t)

        if path == "/api/file":
            rel = qs.get("path", [""])[0]
            fp = safe_resolve(rel)
            if not fp or not os.path.isfile(fp):
                return self._json(404, {"error": "file not found"})
            ext = os.path.splitext(fp)[1].lower()
            if ext not in TEXT_EXTS:
                return self._json(415, {"error": "binary file, use /api/download"})
            with open(fp, encoding="utf-8", errors="replace") as f:
                return self._send(200, f.read()[:200000], "text/plain; charset=utf-8")

        if path == "/api/download":
            rel = qs.get("path", [""])[0]
            fp = safe_resolve(rel)
            if not fp or not os.path.isfile(fp):
                return self._json(404, {"error": "file not found"})
            name = os.path.basename(fp)
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition", 'attachment; filename="%s"' % name)
            self.send_header("Content-Length", str(os.path.getsize(fp)))
            self.end_headers()
            with open(fp, "rb") as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
            return

        return self._json(404, {"error": "not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path != "/api/task":
            return self._json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", 0))
        if length > 200000:
            return self._json(413, {"error": "message too long"})
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception:  # noqa: BLE001
            return self._json(400, {"error": "bad json"})
        message = (data.get("message") or "").strip()
        agent = data.get("agent") or "main"
        if not message:
            return self._json(400, {"error": "empty message"})
        if agent not in AGENTS:
            return self._json(400, {"error": "unknown agent"})
        task_id = "%s-%d" % (int(time.time() * 1000), len(_tasks) + 1)
        with _lock:
            _tasks[task_id] = {
                "status": "running", "text": "", "error": None,
                "agent": agent, "message": message,
                "started": time.time(), "duration": 0,
            }
            _hist.insert(0, {"task_id": task_id, "agent": agent, "message": message,
                             "status": "running", "time": time.strftime("%Y-%m-%d %H:%M:%S")})
            save_history()
        threading.Thread(target=run_openclaw_agent, args=(task_id, agent, message), daemon=True).start()
        return self._json(200, {"task_id": task_id})

    def _serve_static(self, name, ctype):
        fp = os.path.join(WORKBENCH_DIR, name)
        if not os.path.exists(fp):
            return self._json(404, {"error": "missing %s" % name})
        with open(fp, encoding="utf-8") as f:
            return self._send(200, f.read(), ctype)

    def log_message(self, *args):
        pass  # 静默访问日志


def main():
    load_history()
    os.makedirs(TASKS_DIR, exist_ok=True)
    log("starting on http://%s:%d" % (HOST, PORT))
    log("tasks dir: %s" % TASKS_DIR)
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    srv.serve_forever()


if __name__ == "__main__":
    main()
