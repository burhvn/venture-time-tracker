#!/usr/bin/env python3
"""Tiny write-enabled static server for the Venture Time Tracker.
Serves the folder's files, plus:
  GET  /api/data  -> {"state": <time-data.json>, "timers": <timers.json>, "savedAt": <ms>}
  POST /api/data  -> body {"state":..., "timers":...}; writes both atomically; returns {"savedAt": <ms>}
Usage: tracker-server.py "<dir>" [port]
"""
import json, os, sys, tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT   = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
PORT   = int(sys.argv[2]) if len(sys.argv) > 2 else 8890
DATA   = os.path.join(ROOT, 'time-data.json')
TIMERS = os.path.join(ROOT, 'timers.json')

def read_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default

def saved_at():
    m = 0.0
    for p in (DATA, TIMERS):
        try:
            m = max(m, os.path.getmtime(p))
        except OSError:
            pass
    return int(m * 1000)

def write_atomic(path, obj):
    d = os.path.dirname(path) or '.'
    fd, tmp = tempfile.mkstemp(dir=d, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(obj, f, indent=2)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

class H(BaseHTTPRequestHandler):
    def _send(self, code, body=b'', ctype='application/json'):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        path = self.path.split('?')[0]
        if path.endswith('/api/data'):
            payload = {'state': read_json(DATA, None), 'timers': read_json(TIMERS, []), 'savedAt': saved_at()}
            return self._send(200, json.dumps(payload).encode())
        self._serve_static(path)

    def do_POST(self):
        path = self.path.split('?')[0]
        if path.endswith('/api/data'):
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n) or b'{}')
                if isinstance(body.get('state'), dict) and body['state'].get('ventures') is not None:
                    write_atomic(DATA, body['state'])
                write_atomic(TIMERS, body.get('timers', []))
                return self._send(200, json.dumps({'savedAt': saved_at()}).encode())
            except Exception as e:
                return self._send(400, json.dumps({'error': str(e)}).encode())
        self._send(404)

    def _serve_static(self, path):
        rel = path.lstrip('/')
        if rel == '' or rel.endswith('/'):
            rel += 'index.html'
        full = os.path.normpath(os.path.join(ROOT, rel))
        if not (full == ROOT or full.startswith(ROOT + os.sep)):
            return self._send(403)
        if not os.path.isfile(full):
            return self._send(404)
        ctype = ('text/html' if full.endswith('.html')
                 else 'application/json' if full.endswith('.json')
                 else 'text/plain')
        with open(full, 'rb') as f:
            body = f.read()
        self._send(200, body, ctype)

    def log_message(self, *a):
        pass

if __name__ == '__main__':
    print(f'tracker-server: serving {ROOT} on 127.0.0.1:{PORT}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
