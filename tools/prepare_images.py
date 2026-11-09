# -*- coding: utf-8 -*-
"""图片素材处理：AI 配图裁去底部 7% 水印，公众号真实照片按用途重命名。"""
import os
import glob
import shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.dirname(ROOT)  # 项目根
AI = os.path.join(WORK, "_work", "ai")
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG, exist_ok=True)

# 业务场景配图：按提示词关键词映射到用途名
MAP = [
    ("报告厅", "svc-lecture.jpg"),
    ("社会实践", "svc-practice.jpg"),
    ("线上个性化", "svc-counseling.jpg"),
    ("教学研讨", "svc-research.jpg"),
]

for path in glob.glob(os.path.join(AI, "*.png")):
    name = os.path.basename(path)
    hit = next((out for key, out in MAP if key in name), None)
    if not hit:
        continue
    im = Image.open(path).convert("RGB")
    w, h = im.size
    # 硬性规则：裁掉底部约 7%，去掉右下角「AI生成 WORKBUDDY」水印
    im = im.crop((0, 0, w, int(h * 0.93)))
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    dst = os.path.join(IMG, hit)
    im.save(dst, format="JPEG", quality=88, optimize=True)
    print("AI ->", hit, im.size, os.path.getsize(dst), "bytes")

# 公众号原文中的真实工作影像
PHOTOS = [
    ("wx-1.jpg", "founder-lecture.jpg"),
    ("wx-2.jpg", "activity-training.jpg"),
]
for src, dst in PHOTOS:
    s = os.path.join(IMG, src)
    if os.path.exists(s) and os.path.getsize(s) > 2000:
        im = Image.open(s).convert("RGB")
        im.save(os.path.join(IMG, dst), quality=88, optimize=True)
        print("PHOTO ->", dst, im.size)

# 非工作室素材（第三方公众号二维码、无效响应）移出站点发布目录
BACKUP = os.path.join(WORK, "_work", "unused")
os.makedirs(BACKUP, exist_ok=True)
for f in ("wx-3.jpg", "wx-4.jpg", "wx-1.jpg", "wx-2.jpg"):
    p = os.path.join(IMG, f)
    if os.path.exists(p):
        shutil.move(p, os.path.join(BACKUP, f))
print("done")
