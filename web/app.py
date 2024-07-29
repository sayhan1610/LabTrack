import http.server
import socketserver
import os

PORT = 8000
ALLOWED_FILES = {'index.html', 'script.js', 'styles.css'}

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.lstrip('/').split('?')[0] in ALLOWED_FILES:
            super().do_GET()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def scan_files():
    print("Scanning files in the directory:")
    for filename in ALLOWED_FILES:
        if os.path.isfile(filename):
            print(f"Found file: {filename}")
        else:
            print(f"Missing file: {filename}")

def run_server():
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user.")
        finally:
            httpd.server_close()
            print("Server closed.")

if __name__ == "__main__":
    scan_files()  # Scan files in the directory.
    run_server()  # Start the server.
