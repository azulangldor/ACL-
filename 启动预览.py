#!/usr/bin/env python3
"""RehabGuide v0.1.0-beta.1 本地预览服务器（零依赖，带 SPA 回退）。

用法：
    cd "RehabGuide v0.1.0-beta.1"
    python3 启动预览.py            # 默认 http://localhost:8080
    python3 启动预览.py 9090       # 换端口

说明：页面用的是绝对路径（/assets/...），所以务必**从本目录启动**；
带 SPA 回退（找不到的路径交给 index.html），深链如 /library、/me 才能正常打开。
"""
import http.server, os, socketserver, sys, mimetypes

mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('image/webp', '.webp')
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        path = self.translate_path(self.path)
        if not os.path.exists(path) or os.path.isdir(path) and not os.path.exists(os.path.join(path, 'index.html')):
            self.path = '/index.html'  # SPA 回退
        return super().do_GET()

    def end_headers(self):
        if self.path in ('/', '/index.html', '/sw.js'):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, *a):
        pass


with socketserver.TCPServer(('127.0.0.1', PORT), Handler) as httpd:
    print(f'RehabGuide v0.1.0-beta.1 → http://localhost:{PORT}   （Ctrl+C 停止）')
    httpd.serve_forever()
