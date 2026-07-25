import http.server
import socketserver
import os
import mimetypes

class NoCacheHandler(http.server.BaseHTTPRequestHandler):
    """Serves files with absolutely no caching — always returns 200, never 304."""

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/' or path == '':
            path = '/index.html'
        file_path = os.path.join(os.getcwd(), path.lstrip('/'))

        if not os.path.isfile(file_path):
            self.send_error(404, 'Not found')
            return

        ctype = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        if ctype.startswith('text') and 'charset' not in ctype:
            ctype += '; charset=utf-8'

        with open(file_path, 'rb') as f:
            data = f.read()

        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)

class ReuseServer(socketserver.TCPServer):
    allow_reuse_address = True

with ReuseServer(('0.0.0.0', 5000), NoCacheHandler) as httpd:
    print('Serving on port 5000', flush=True)
    httpd.serve_forever()
