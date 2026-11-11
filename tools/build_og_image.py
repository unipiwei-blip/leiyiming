# -*- coding: utf-8 -*-
"""生成全站默认社交分享图 1200x630（代码绘制，无水印）。"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "og-image.png")
BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
REG = r"C:\Windows\Fonts\msyh.ttc"

W, H = 1200, 630
x = np.linspace(0, 1, W)[None, :]
y = np.linspace(0, 1, H)[:, None]
t = x * 0.62 + y * 0.38
c1 = np.array([10, 47, 134])
c2 = np.array([82, 76, 226])
c3 = np.array([184, 33, 124])
arr = np.zeros((H, W, 3), dtype=np.uint8)
for i in range(3):
    a = c1[i] + (c2[i] - c1[i]) * np.clip(t / 0.55, 0, 1)
    b = c2[i] + (c3[i] - c2[i]) * np.clip((t - 0.55) / 0.45, 0, 1)
    arr[:, :, i] = np.where(t < 0.55, a, b).astype(np.uint8)
im = Image.fromarray(arr)
d = ImageDraw.Draw(im, "RGBA")

# 柔光圆斑与细线网格
for cx, cy, r, alpha in [(1010, 90, 260, 26), (170, 570, 300, 18), (620, 320, 380, 10)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, alpha))
for gx in range(0, W, 80):
    d.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 10), width=1)
for gy in range(0, H, 80):
    d.line([(0, gy), (W, gy)], fill=(255, 255, 255, 10), width=1)

f1 = ImageFont.truetype(BOLD, 78)
f2 = ImageFont.truetype(REG, 34)
f3 = ImageFont.truetype(REG, 26)


def center_text(text, font, yy, fill):
    box = d.textbbox((0, 0), text, font=font)
    tw = box[2] - box[0]
    d.text(((W - tw) / 2, yy), text, font=font, fill=fill)


d.rounded_rectangle([(W / 2 - 46, 150), (W / 2 + 46, 242)], radius=24,
                    fill=(255, 255, 255, 235))
d.text((W / 2, 196), "雷", font=ImageFont.truetype(BOLD, 58),
       fill=(26, 107, 255), anchor="mm")

center_text("雷一鸣工作室", f1, 286, (255, 255, 255, 255))
center_text("以大学生思想政治教育为核心", f2, 400, (235, 243, 255, 255))
d.line([(W / 2 - 150, 480), (W / 2 + 150, 480)], fill=(255, 255, 255, 90), width=2)
center_text("教学 · 研究 · 指导 · 服务", f3, 505, (220, 234, 255, 235))

im.save(OUT, optimize=True)
print("write", OUT, im.size, os.path.getsize(OUT), "bytes")
