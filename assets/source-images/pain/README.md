# Pain landing source images

Originals (high-resolution JPEG) for the hero images that appear on the pain
landing pages at `/en/{slug}`. Filename pattern: `{slug}.source.{ext}`.

The build pipeline does NOT read from this folder. The web-optimized
WebP versions live in `en/static/images/pain/{slug}.webp` and are
referenced from `data/pains.json` under each pain's `hero_image` field.

Keep these around so we can regenerate the WebP at a different size or
quality without re-running the generator from scratch.

To rebuild the WebP from a source:

```bash
python -c "
from PIL import Image
img = Image.open('assets/source-images/pain/parent-stuck.source.jpeg')
img.thumbnail((1200, 1600), Image.LANCZOS)
img.save('en/static/images/pain/parent-stuck.webp', 'WEBP', quality=85, method=6)
"
```
