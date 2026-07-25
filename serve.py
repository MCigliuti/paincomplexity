import http.server
import socketserver

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
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
