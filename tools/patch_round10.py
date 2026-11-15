# -*- coding: utf-8 -*-
"""第十轮：微信分享卡片静态兜底（方图 + og/itemprop/body 首图，仅详情页）。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


def write(rel, t):
    open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(t)
    print("patched", rel)


def once(t, old, new, tag):
    n = t.count(old)
    assert n == 1, "%s 命中 %d 次: %r" % (tag, n, old[:70])
    return t.replace(old, new, 1)


p = "tools/build_site.py"
t = read(p)

# 1) re 与两个工具函数
t = once(t, "import os\nimport json\nimport sys\n",
         "import os\nimport json\nimport sys\nimport re\n", "import-re")

HELPERS = r'''def share_image_name(page):
    base = page[:-5] if page.endswith(".html") else page
    for pre in ("article-", "svc-"):
        if base.startswith(pre):
            base = base[len(pre):]
            break
    return "share-" + base + ".jpg"


def share_summary(text, limit=60):
    s = re.sub(r"\s+", " ", (text or "")).strip()
    s = s[:limit]
    return s.rstrip("，。；、,.;:：!！?？…—- ")


'''
t = once(t, "def head(page, title, desc, keywords):",
         HELPERS + "def head(page, title, desc, keywords):", "helpers")

# 2) 原封面 URL 独立保留给 JSON-LD，避免结构化数据被改动
t = once(t, '    og_img = SITE_URL + ("assets/img/" + art["cover"] if art else "assets/img/og-image.png")',
         '    cover_url = SITE_URL + ("assets/img/" + art["cover"] if art else "assets/img/og-image.png")\n'
         '    og_img = cover_url', "cover-url")
t = once(t, '"image": og_img,', '"image": cover_url,', "ld-image")

# 3) 详情页专用变量
DETAIL = r'''    full_title = title if page == "index.html" else title + " | " + BRAND

    is_detail = page.startswith("article-") or page.startswith("svc-")
    itemprop = ""
    thumb = ""
    og_desc = desc
    if is_detail:
        share_url = SITE_URL + "assets/img/" + share_image_name(page)
        og_img = share_url
        og_desc = share_summary(desc)
        itemprop = (f'<meta itemprop="name" content="{full_title}">\n'
                    f'<meta itemprop="description" content="{og_desc}">\n'
                    f'<meta itemprop="image" content="{share_url}">\n')
        thumb = (f'<img class="wx-share-thumb" src="{share_url}" alt="" '
                 f'width="300" height="300" aria-hidden="true">\n')
        og_dims = ('<meta property="og:image:width" content="400">\n'
                   '<meta property="og:image:height" content="400">\n')
    else:
        og_dims = ('<meta property="og:image:width" content="1200">\n'
                   '<meta property="og:image:height" content="630">\n')

    crumbs = [(BRAND, SITE_URL)]
'''
t = once(t, '''    full_title = title if page == "index.html" else title + " | " + BRAND

    crumbs = [(BRAND, SITE_URL)]
''', DETAIL, "detail-block")

# 4) 删除旧的 og_dims 定义（已由 detail 块统一输出）
OLD_DIMS = (
    "    og_dims = ('' if art else\n"
    "               '<meta property=\"og:image:width\" content=\"1200\">\\n'\n"
    "               '<meta property=\"og:image:height\" content=\"630\">\\n')\n"
)
t = once(t, OLD_DIMS, "", "drop-old-dims")

# 5) head 模板：摘要、itemprop、body 首图
t = once(t, '<meta property="og:description" content="{desc}">',
         '<meta property="og:description" content="{og_desc}">', "og-desc")
t = once(t, '{og_dims}<meta name="twitter:card" content="summary_large_image">',
         '{og_dims}{itemprop}<meta name="twitter:card" content="summary_large_image">', "itemprop")
t = once(t, '<body data-page="{key}">\n',
         '<body data-page="{key}">\n{thumb}', "body-thumb")
write(p, t)

# ---------------------------------------------------------------- CSS
CSS_ADD = '''
/* ================= 第十轮：微信分享卡片方图（离屏，不使用 display:none） ================= */
.wx-share-thumb{position:absolute;top:0;left:-9999px;width:300px;height:300px;pointer-events:none;z-index:-1}
'''
p = "assets/css/style.css"
t = read(p)
if "第十轮：微信分享卡片方图" not in t:
    open(os.path.join(ROOT, p), "a", encoding="utf-8").write(CSS_ADD)
    print("appended", p)
else:
    print("skip (already)", p)

# ---------------------------------------------------------------- 验收脚本
p = "tools/validate.py"
t = read(p)
CHECK = r'''    # 微信分享卡片验收
    from PIL import Image
    detail = [q for q in pages if os.path.basename(q).startswith(("article-", "svc-"))]
    others = [q for q in pages if q not in detail]
    shares = sorted(glob.glob(os.path.join(ROOT, "assets", "img", "share-*.jpg")))
    if len(detail) != len(shares):
        issues.append(f"详情页 {len(detail)} 与方图 {len(shares)} 数量不等")
    for f in shares:
        im = Image.open(f)
        if im.size != (400, 400):
            issues.append(f"{os.path.basename(f)} 尺寸非 400x400")
        if im.format != "JPEG":
            issues.append(f"{os.path.basename(f)} 非 JPEG")
        if im.getexif():
            issues.append(f"{os.path.basename(f)} 含 EXIF")
        if os.path.getsize(f) > 100 * 1024:
            issues.append(f"{os.path.basename(f)} 超过 100KB")
    for q in detail:
        h = open(q, encoding="utf-8").read()
        nm = os.path.basename(q)
        for tag in ('itemprop="name"', 'itemprop="description"', 'itemprop="image"',
                    'og:image:width" content="400"', 'og:image:height" content="400"',
                    'class="wx-share-thumb"', 'twitter:card" content="summary_large_image"'):
            if tag not in h:
                issues.append(f"{nm}: 缺 {tag}")
        got = []
        for pat in (r'property="og:image" content="([^"]+)"',
                    r'itemprop="image" content="([^"]+)"',
                    r'class="wx-share-thumb" src="([^"]+)"'):
            m = re.search(pat, h)
            got.append(m.group(1) if m else "")
        if any(not u.startswith("https://www.oals.cn/assets/img/share-") for u in got):
            issues.append(f"{nm}: 方图 URL 非 HTTPS 绝对地址")
        if len(set(got)) != 1:
            issues.append(f"{nm}: og/itemprop/首图 三处 URL 不一致")
        if 'loading="lazy"' in h.split("wx-share-thumb")[1][:200]:
            issues.append(f"{nm}: 首图使用了 lazy")
    for q in others:
        h = open(q, encoding="utf-8").read()
        if "itemprop=" in h or "wx-share-thumb" in h:
            issues.append(f"{os.path.basename(q)}: 非详情页误带分享标签")
    f404 = os.path.join(ROOT, "404.html")
    if os.path.exists(f404):
        h = open(f404, encoding="utf-8").read()
        if "itemprop=" in h or "wx-share-thumb" in h:
            issues.append("404.html 误带分享标签")

'''
t = once(t, '    print(f"检查页面 {len(pages)} 个，问题 {len(issues)} 条")',
         CHECK + '    print(f"检查页面 {len(pages)} 个，问题 {len(issues)} 条")', "wx-check")
write(p, t)
print("round10 done")
