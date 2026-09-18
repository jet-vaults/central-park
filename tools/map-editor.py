"""Opens the building-map editor in your browser (serves the repo root so it can read src/buildings.json).
    python tools/map-editor.py
"""
import os, threading, webbrowser, http.server, socketserver, functools
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PORT = 8766
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), functools.partial(Quiet, directory=ROOT))
threading.Thread(target=httpd.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{PORT}/tools/map-editor.html"
print("editor:", url, "\nCtrl+C to stop.")
webbrowser.open(url)
try:
    threading.Event().wait()
except KeyboardInterrupt:
    httpd.shutdown()
