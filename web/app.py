import http.server
import socketserver
import webbrowser
import threading

PORT = 5500
URL = f"http://127.0.0.1:{PORT}"

class OpenBrowser(threading.Thread):
    def run(self):
        webbrowser.open(URL)

Handler = http.server.SimpleHTTPRequestHandler

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at {URL}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Open the browser in a separate thread
    OpenBrowser().start()
    # Start the server
    run_server()
