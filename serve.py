import http.server
import socketserver

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Strip conditional headers so the server always returns 200, never 304
        for h in ('If-Modified-Since', 'If-None-Match', 'If-Unmodified-Since'):
            if h in self.headers:
                del self.headers[h]
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        print(format % args, flush=True)

class ReuseServer(socketserver.TCPServer):
    allow_reuse_address = True

with ReuseServer(("0.0.0.0", 5000), NoCacheHandler) as httpd:
    print("Serving on port 5000", flush=True)
    httpd.serve_forever()
