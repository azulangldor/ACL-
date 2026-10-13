#!/usr/bin/env python3
"""RehabGuide v0.1.0-beta.1 本地预览服务器（零依赖，带 SPA 回退）。

用法：
    cd "RehabGuide v0.1.0-beta.1"
    python3 启动预览.py            # 默认 http://localhost:8080（被占用时自动顺延 8090/8181/8282）
    python3 启动预览.py 9090       # 显式指定端口（占用即报错退出，不静默换端口）

说明：页面用的是绝对路径（/assets/...），所以务必**从本目录启动**；
带 SPA 回退（找不到的路径交给 index.html），深链如 /library、/me 才能正常打开。

R48⁗ ⑦（交付包清扫连带项）：默认端口被占用时**自动顺延**并打印醒目提示——
8080 是本地开发的高频端口，且"上一次的预览进程还在跑"意味着它服务的是**旧文件**，
静默失败或静默沿用都会让人以为改动没生效，所以这里明确提示"新端口 / 旧进程可能是旧包"。
"""
import http.server, os, socketserver, sys, mimetypes

mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('image/webp', '.webp')
ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 8080
FALLBACK_PORTS = (8090, 8181, 8282)


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


class Server(socketserver.TCPServer):
    allow_reuse_address = True


def try_bind(port):
    """端口可用则返回 server，占用则返回 None。"""
    try:
        return Server(('127.0.0.1', port), Handler)
    except OSError:
        return None


def main():
    explicit = len(sys.argv) > 1
    if explicit:
        port = int(sys.argv[1])
        httpd = try_bind(port)
        if httpd is None:
            print(f'✗ 端口 {port} 已被占用（换个端口：python3 启动预览.py 8090）', file=sys.stderr)
            return 1
    else:
        port, httpd = None, None
        for cand in (DEFAULT_PORT, *FALLBACK_PORTS):
            httpd = try_bind(cand)
            if httpd is not None:
                port = cand
                break
        if httpd is None:
            print(f'✗ {DEFAULT_PORT}/{"/".join(map(str, FALLBACK_PORTS))} 全部被占用，'
                  f'请显式指定端口：python3 启动预览.py 9090', file=sys.stderr)
            return 1
        if port != DEFAULT_PORT:
            print(f'⚠ 默认端口 {DEFAULT_PORT} 已被占用 —— 本次改用 {port}。')
            print(f'  若 {DEFAULT_PORT} 上是上一次的预览进程，它服务的是**旧文件**：')
            print(f'  要么访问本端口（{port}，新包），要么先停掉旧进程再重跑本脚本。')

    print(f'RehabGuide v0.1.0-beta.1 → http://localhost:{port}   （Ctrl+C 停止）')
    print(f'  从本目录起服务；深链如 /library、/me 可直接打开。')
    with httpd:
        httpd.serve_forever()
    return 0


if __name__ == '__main__':
    sys.exit(main())
