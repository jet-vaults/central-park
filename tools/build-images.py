"""
Image pipeline for the Central Park site.

Reads the ORIGINAL renderings (never modified) and writes optimized web copies to
wwwroot/assets/img/<name>-<width>.{avif,webp}.  Re-run whenever a source changes.

    python tools/build-images.py            # build everything
    python tools/build-images.py hero       # build only entries whose name contains "hero"

Sources live outside the repo (client delivery folder + prospectus extracts).
"""
import os, sys, glob
from PIL import Image, ImageOps
import pillow_avif  # noqa: F401  (registers the AVIF encoder)

Image.MAX_IMAGE_PIXELS = None

SRC_DIR = r"C:\Users\Osher\Downloads\wetransfer_shtila_0776day-png_2026-09-17_0853"
PDF_DIR = os.path.join(os.path.dirname(__file__), "..", "source", "prospectus-extracts")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "wwwroot", "assets", "img")

WIDTHS_WIDE = (768, 1280, 1920, 2560)   # full-bleed / hero imagery
WIDTHS_HALF = (640, 1024, 1600)         # split layouts (max ~50vw)
WIDTHS_TILE = (480, 800)                # circles / small tiles

# name, source path, widths, optional center crop aspect (w/h) -- None keeps native ratio
IMAGES = [
    # hero + full bleed
    ("hero-terrace",      os.path.join(PDF_DIR, "p01_cover_terrace_a.jpg"),      WIDTHS_WIDE, None),
    ("aerial-skyline",    os.path.join(SRC_DIR, "Shtila_0776Day.png"),          WIDTHS_WIDE, 16/9),
    ("aerial-hills",      os.path.join(SRC_DIR, "Shtila_0760Day.png"),          WIDTHS_WIDE, 16/9),
    ("panorama",          os.path.join(SRC_DIR, "003Day.png"),                  WIDTHS_WIDE, None),   # 3:1
    ("aerial-top",        os.path.join(SRC_DIR, "004Day.png"),                  WIDTHS_WIDE, None),
    ("balconies",         os.path.join(SRC_DIR, "007Day.png"),                  WIDTHS_WIDE, None),
    ("elevation",         os.path.join(SRC_DIR, "001Day.png"),                  WIDTHS_WIDE, None),
    ("boulevard",         os.path.join(SRC_DIR, "002Day.png"),                  WIDTHS_WIDE, None),
    ("plaza",             os.path.join(SRC_DIR, "019Day (2).png"),              WIDTHS_WIDE, None),
    ("sunset-terrace",    os.path.join(PDF_DIR, "p12_sunset_terrace.jpg"),      WIDTHS_WIDE, None),
    # split / half width
    ("father-son",        os.path.join(PDF_DIR, "p03_father_son_park.jpg"),     WIDTHS_HALF, None),
    ("bike-sunset",       os.path.join(PDF_DIR, "p02_bike_sunset_a.jpg"),       WIDTHS_HALF, None),
    ("terrace-pool",      os.path.join(PDF_DIR, "p07_terrace_pool_a.jpg"),      WIDTHS_HALF, None),
    ("garden-pool",       os.path.join(PDF_DIR, "p08_garden_pool.jpg"),         WIDTHS_HALF, None),
    ("terrace-jacuzzi",   os.path.join(PDF_DIR, "p09_terrace_jacuzzi.jpg"),     WIDTHS_HALF, None),
    ("living-room",       os.path.join(PDF_DIR, "p11_living_room_a.jpg"),       WIDTHS_HALF, None),
    ("boulevard-shops",   os.path.join(PDF_DIR, "p06_boulevard_newstyle.jpg"),  WIDTHS_HALF, None),
    ("bedroom",           os.path.join(PDF_DIR, "p09_bedroom_circle.jpg"),      WIDTHS_HALF, 1),
    ("site-plan",         os.path.join(SRC_DIR, "ELAD-25-12-25.jpg"),           WIDTHS_HALF, None),
    # circular detail tiles (native ~830px)
    ("tile-lobby",        os.path.join(PDF_DIR, "p10_lobby.jpg"),               WIDTHS_TILE, 1),
    ("tile-elevators",    os.path.join(PDF_DIR, "p10_elevators.jpg"),           WIDTHS_TILE, 1),
    ("tile-balcony",      os.path.join(PDF_DIR, "p10_balcony.jpg"),             WIDTHS_TILE, 1),
    ("tile-parking",      os.path.join(PDF_DIR, "p10_parking.jpg"),             WIDTHS_TILE, 1),
    ("tile-kitchen",      os.path.join(PDF_DIR, "p10_kitchen.jpg"),             WIDTHS_TILE, 1),
    ("tile-living",       os.path.join(PDF_DIR, "p10_living_view.jpg"),         WIDTHS_TILE, 1),
    # paper texture (cream page background of the prospectus)
    ("texture-paper",     os.path.join(PDF_DIR, "texture_paper.jpg"),           (1200,), None),
]

def build(name, src, widths, aspect):
    im = Image.open(src)
    im = ImageOps.exif_transpose(im).convert("RGB")
    if aspect:
        im = ImageOps.fit(im, (im.width, int(round(im.width / aspect))) if im.width / im.height > aspect
                          else (int(round(im.height * aspect)), im.height), Image.LANCZOS, centering=(0.5, 0.5))
    print(f"{name:18s} {im.width}x{im.height}  ->", end=" ", flush=True)
    for w in widths:
        if w > im.width:  # never upscale
            continue
        h = int(round(im.height * w / im.width))
        r = im.resize((w, h), Image.LANCZOS)
        r.save(os.path.join(OUT_DIR, f"{name}-{w}.webp"), "WEBP", quality=82, method=6)
        r.save(os.path.join(OUT_DIR, f"{name}-{w}.avif"), "AVIF", quality=62, speed=4)
        print(w, end=" ", flush=True)
    print()
    return im.width, im.height

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    flt = sys.argv[1] if len(sys.argv) > 1 else ""
    for name, src, widths, aspect in IMAGES:
        if flt and flt not in name:
            continue
        if not os.path.exists(src):
            print(f"{name:18s} MISSING {src}"); continue
        build(name, src, widths, aspect)
