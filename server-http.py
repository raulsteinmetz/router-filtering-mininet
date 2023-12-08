import http.server
import socketserver

PORT = 80  # Standard HTTP port

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, this is server1 responding to your request!")

def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler):
    with server_class(("", PORT), handler_class) as httpd:
        print(f"Serving HTTP on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
