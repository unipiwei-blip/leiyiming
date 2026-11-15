# -*- coding: utf-8 -*-
"""为所有内容详情页生成 400x400 方形分享图（中心裁切，不生成新画面）。"""
import os
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
from PIL import Image  # noqa: E402
from build_site import share_image_name, ARTICLES, SERVICES  # noqa: E402

ROOT = os.path.dirname(TOOLS)
IMG = os.path.join(ROOT, "assets", "img")

pairs = ([(a["slug"], a["cover"]) for a in ARTICLES]
         + [(s["slug"] + ".html", s["image"]) for s in SERVICES])

for slug, src in pairs:
    path = os.path.join(IMG, src)
    if not os.path.exists(path):
        raise SystemExit("缺源图: " + path)
    im = Image.open(path).convert("RGB")   # 重建像素对象，自动丢弃 EXIF
    w, h = im.size
    side = min(w, h)
    left, top = (w - side) // 2, (h - side) // 2
    im = im.crop((left, top, left + side, top + side))
    im = im.resize((400, 400), Image.LANCZOS)

    out = os.path.join(IMG, share_image_name(slug))
    q = 85
    while True:
        im.save(out, format="JPEG", quality=q, optimize=True)
        if os.path.getsize(out) <= 100 * 1024 or q <= 70:
            break
        q -= 5
    print("%-42s <- %-24s 400x400 q=%d %dKB" %
          (os.path.basename(out), src, q, os.path.getsize(out) // 1024))

print("total", len(pairs), "share images")
