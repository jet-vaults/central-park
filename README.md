# central-park

## Status

| | |
|---|---|
| **Domain** | `https://centralpark.co.il` |
| **Pages URL** | `https://central-park.pages.dev` |
| **Storage mode** | `Standard` (`standard`) |
| **Storage account** | `jetvaults` |
| **Public storage** | `https://jetvaults.blob.core.windows.net/central-park/` |
| **Private storage** | `https://jetvaults.blob.core.windows.net/central-park-private/` |
| **Public container** | `central-park` |
| **Private container** | `central-park-private` |
| **Activated** | No |

## Nameservers

Set these at your domain registrar:

```
gordon.ns.cloudflare.com
sureena.ns.cloudflare.com
```

## Development

Edit files in `wwwroot/` and push to `main` - Cloudflare Pages auto-deploys.

Only the `wwwroot/` directory is served. Everything else stays in the repo.

## Build notes

- `src/index.html` is the editable page source. `python tools/build-html.py` inlines the brand SVGs and expands
  the `{{img …}}` macros into responsive `<picture>` markup, writing `wwwroot/index.html`. Edit `src/`, not `wwwroot/index.html`.
- `python tools/build-images.py` regenerates AVIF/WebP variants in `wwwroot/assets/img` from the client's original
  renderings and the prospectus extracts (`source/`, local only, gitignored).
- `python tools/shoot.py` screenshots every target width into `qa/` (gitignored); `tools/shoot-states.py` covers
  the hero entrance, scrolled header and mobile menu.
- Design tokens and the rationale for every value are in `DESIGN.md`.
- Fonts: the prospectus uses Ploni + Almoni Tzar (Fontef, commercial). Heebo is the interim stand-in; drop licensed
  `woff2` files into `wwwroot/assets/fonts/` and update the `@font-face` rules in `assets/css/base.css`.
