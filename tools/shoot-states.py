"""Interaction states: scrolled header, open mobile menu, mid-scroll reveal frames (motion on)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shoot import serve, PORT, OUT
from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
httpd = serve()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    # desktop, motion on: hero at 300ms / 1200ms / 2600ms, then scrolled header + mid reveal
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL")
    pg = ctx.new_page(); pg.goto(f"http://127.0.0.1:{PORT}/index.html")
    prev = 0
    for t in (300, 1200, 2600):
        pg.wait_for_timeout(t if t == 300 else t - prev); prev = t
        pg.screenshot(path=os.path.join(OUT, f"hero-t{t}.png"))
    pg.evaluate("window.scrollTo(0, 700)"); pg.wait_for_timeout(450)
    pg.screenshot(path=os.path.join(OUT, "state-scrolled-1440-mid.png"))
    pg.wait_for_timeout(1400)
    pg.screenshot(path=os.path.join(OUT, "state-scrolled-1440.png"))
    pg.evaluate("window.scrollTo(0, 2600)"); pg.wait_for_timeout(500)
    pg.screenshot(path=os.path.join(OUT, "state-apartments-mid.png"))
    ctx.close()
    # mobile menu
    ctx = b.new_context(viewport={"width": 390, "height": 844}, locale="he-IL", reduced_motion="reduce")
    pg = ctx.new_page(); pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle")
    pg.click(".nav-toggle"); pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(OUT, "state-menu-390.png"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    print("menu closed after Esc:", not pg.evaluate("document.getElementById('menu').classList.contains('is-open')"))
    pg.evaluate("window.scrollTo(0, 900)"); pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(OUT, "state-scrolled-390.png"))
    ctx.close(); b.close()
httpd.shutdown(); print("done")
