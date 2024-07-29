import http.server
import socketserver
import webbrowser
import threading
import signal
import sys
import os

PORT = 8000
URL = f"http://0.0.0.0:{PORT}"
ALLOWED_FILES = {'index.html', 'script.js', 'styles.css'}

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.lstrip('/').split('?')[0] in ALLOWED_FILES:
            super().do_GET()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

class OpenBrowser(threading.Thread):
    def run(self):
        webbrowser.open(URL)

def scan_files():
    print("Scanning files in the directory:")
    for filename in ALLOWED_FILES:
        if os.path.isfile(filename):
            print(f"Found file: {filename}")
        else:
            print(f"Missing file: {filename}")

def run_server():
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving at {URL}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user.")
        finally:
            httpd.server_close()
            print("Server closed.")

def signal_handler(sig, frame):
    print("\nSignal received, stopping server.")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handling for a graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signals

    scan_files()  # Scan files in the directory.
    OpenBrowser().start()  # Start the browser in a new thread.
    run_server()  # Start the server.
