import http.server
import socketserver

PORT = 80

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length)  
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = f"Received POST request: {post_data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))

def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler):
    with server_class(("", PORT), handler_class) as httpd:
        print(f"Serving HTTP on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
