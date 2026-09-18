"""
Builds wwwroot/index.html from src/index.html.

Two tiny macros keep the page source readable and consistent:

  {{svg logo_full class="foo"}}          -> inlines wwwroot/assets/brand/logo_full.svg (so currentColor works)
  {{img name=hero-terrace widths=768,1280,1920,2560 sizes="100vw" w=4015 h=2837
        alt="..." class="..." loading=lazy fetchpriority=high}}
                                        -> <picture> with AVIF + WebP srcsets from wwwroot/assets/img

    python tools/build-html.py
"""
import os, re, shlex

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC_DIR = os.path.join(ROOT, "src")
OUT_DIR = os.path.join(ROOT, "wwwroot")
BRAND = os.path.join(ROOT, "wwwroot", "assets", "brand")
IMG = os.path.join(ROOT, "wwwroot", "assets", "img")


def kv(argstr):
    out = {}
    for tok in shlex.split(argstr):
        if "=" in tok:
            k, v = tok.split("=", 1)
            out[k] = v
        else:
            out[tok] = True
    return out


def svg_macro(m):
    parts = m.group(1).split(None, 1)
    name = parts[0]
    attrs = kv(parts[1]) if len(parts) > 1 else {}
    svg = open(os.path.join(BRAND, name + ".svg"), encoding="utf-8").read().strip()
    # drop fixed width/height so CSS controls size; keep viewBox
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    extra = " ".join(f'{k}="{v}"' for k, v in attrs.items()) or ""
    if "aria-hidden" not in extra and "role" not in extra:
        extra += ' aria-hidden="true" focusable="false"'
    svg = svg.replace("<svg ", f"<svg {extra} ", 1)
    return svg


def img_macro(m):
    a = kv(m.group(1))
    name = a["name"]
    widths = [int(w) for w in a["widths"].split(",")]
    widths = [w for w in widths if os.path.exists(os.path.join(IMG, f"{name}-{w}.webp"))]
    if not widths:
        raise SystemExit(f"no built images for {name}")
    sizes = a.get("sizes", "100vw")
    avif = ", ".join(f"/assets/img/{name}-{w}.avif {w}w" for w in widths)
    webp = ", ".join(f"/assets/img/{name}-{w}.webp {w}w" for w in widths)
    fallback = widths[min(len(widths) - 1, 2)]
    w, h = a["w"], a["h"]
    loading = a.get("loading", "lazy")
    attrs = [f'src="/assets/img/{name}-{fallback}.webp"', f'srcset="{webp}"', f'sizes="{sizes}"',
             f'width="{w}"', f'height="{h}"', f'alt="{a.get("alt", "")}"', 'decoding="async"']
    if loading == "lazy":
        attrs.append('loading="lazy"')
    if a.get("fetchpriority"):
        attrs.append(f'fetchpriority="{a["fetchpriority"]}"')
    if a.get("imgclass"):
        attrs.append(f'class="{a["imgclass"]}"')
    pic_class = f' class="{a["class"]}"' if a.get("class") else ""
    return (f"<picture{pic_class}>"
            f'<source type="image/avif" srcset="{avif}" sizes="{sizes}">'
            f"<img {' '.join(attrs)}></picture>")


def rings_macro(m):
    """{{rings class="rings--gold" n=4 r0=44 r1=196 sw=2.5}} -> concentric-ring SVG that draws itself."""
    a = kv(m.group(1))
    n = int(a.get("n", 4)); r0 = float(a.get("r0", 44)); r1 = float(a.get("r1", 196))
    sw = a.get("sw", "2.5")
    step = (r1 - r0) / max(n - 1, 1)
    circles = "".join(f'<circle cx="200" cy="200" r="{r0 + i*step:.1f}" pathLength="1"/>' for i in range(n))
    cls = ("rings " + a.get("class", "")).strip()
    return (f'<svg class="{cls}" viewBox="0 0 400 400" style="--sw:{sw}" data-observe aria-hidden="true" focusable="false">'
            f"{circles}</svg>")


def build(name):
    html = open(os.path.join(SRC_DIR, name), encoding="utf-8").read()
    html = re.sub(r"\{\{rings\s+(.+?)\}\}", rings_macro, html)
    html = re.sub(r"\{\{svg\s+(.+?)\}\}", svg_macro, html)
    html = re.sub(r"\{\{img\s+(.+?)\}\}", img_macro, html, flags=re.S)
    out = os.path.join(OUT_DIR, name)
    open(out, "w", encoding="utf-8", newline="\n").write(html)
    print(f"wrote {os.path.relpath(out, ROOT)} ({len(html.encode('utf-8'))//1024} KB)")


def main():
    for name in sorted(os.listdir(SRC_DIR)):
        if name.endswith(".html"):
            build(name)


if __name__ == "__main__":
    main()
