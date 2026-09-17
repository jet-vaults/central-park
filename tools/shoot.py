"""
Visual QA: serves wwwroot locally and screenshots the page at the target widths.

    python tools/shoot.py                 # full-page shots at every width -> qa/
    python tools/shoot.py 1440 390        # only these widths
    python tools/shoot.py --motion 1440   # normal motion, scrolls through slowly (checks reveals)
"""
import os, sys, threading, http.server, socketserver, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WWW = os.path.join(ROOT, "wwwroot")
OUT = os.path.join(ROOT, "qa")
WIDTHS = [1920, 1680, 1440, 1366, 1280, 1024, 768, 430, 390]
PORT = 8765


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    handler = functools.partial(Quiet, directory=WWW)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    args = [a for a in sys.argv[1:]]
    motion = "--motion" in args
    widths = [int(a) for a in args if a.isdigit()] or WIDTHS
    os.makedirs(OUT, exist_ok=True)
    httpd = serve()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for w in widths:
            h = 900 if w >= 1024 else 844
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                      reduced_motion=None if motion else "reduce", locale="he-IL")
            page = ctx.new_page()
            page.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle")
            page.wait_for_timeout(600)
            # scroll through once so lazy images load and reveals fire
            total = page.evaluate("document.documentElement.scrollHeight")
            y = 0
            while y < total:
                page.mouse.wheel(0, 600); y += 600; page.wait_for_timeout(90 if not motion else 160)
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            page.wait_for_load_state("networkidle")
            page.evaluate("() => Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))")
            if not motion:
                page.evaluate("document.querySelectorAll('.reveal,.mask,.rings').forEach(e=>e.classList.add('is-in'))")
            page.wait_for_timeout(1200 if motion else 300)
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            page.screenshot(path=os.path.join(OUT, f"full-{w}.png"), full_page=True)
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(200)
            page.screenshot(path=os.path.join(OUT, f"fold-{w}.png"))
            print(f"{w:5d}px  height={page.evaluate('document.documentElement.scrollHeight')}  h-overflow={overflow}px")
            ctx.close()
        browser.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
