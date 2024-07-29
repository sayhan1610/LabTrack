import http.server
import socketserver
import webbrowser
import threading
import signal
import sys

PORT = 5500
URL = f"http://127.0.0.1:{PORT}"

class OpenBrowser(threading.Thread):
    def run(self):
        webbrowser.open(URL)

Handler = http.server.SimpleHTTPRequestHandler

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
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

    OpenBrowser().start()  # Start the browser in a new thread.
    run_server()  # Start the server.
