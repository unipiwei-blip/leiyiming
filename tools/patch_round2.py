# -*- coding: utf-8 -*-
"""第二轮：加入咨询/公众号二维码、绑定域名 www.oals.cn、生成站点级文件。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def patch(rel, pairs):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, "%s 命中 %d 次: %r" % (rel, n, old[:60])
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8").write(t)
    print("patched", rel)


patch("tools/site_content.py", [
    ('BRAND = "雷一鸣工作室"',
     'SITE_URL = "https://www.oals.cn/"\n\nBRAND = "雷一鸣工作室"'),
    ('''CONTACT_CHANNELS = [
    "微信公众号「雷一鸣工作室」",
    "中国大学生在线专栏",
    "主理人 雷一鸣（雷桂平）",
]''',
     '''CONTACT_CHANNELS = [
    "微信咨询 · 添加主理人好友",
    "微信公众号 · 育人内容分享",
    "主理人 雷一鸣（雷桂平）",
]'''),
    ('"可通过微信公众号「雷一鸣工作室」留言，围绕专题讲座、育人实践共建、辅导员教研交流等方向沟通具体安排。"),',
     '"可扫描咨询二维码添加主理人好友，或关注公众号后留言，围绕专题讲座、育人实践共建、辅导员教研交流等方向沟通具体安排。"),'),
])

patch("tools/build_site.py", [
    ("    NAV, FRIEND_LINKS, FOOT_BIZ, CONTACT_CHANNELS, STATS, ABOUT_CARDS,\n",
     "    NAV, FRIEND_LINKS, FOOT_BIZ, CONTACT_CHANNELS, STATS, ABOUT_CARDS, SITE_URL,\n"),
    ('''<link rel="canonical" href="{page}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">''',
     '''<link rel="canonical" href="{SITE_URL}{'' if page == 'index.html' else page}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}{'' if page == 'index.html' else page}">
<meta property="og:image" content="{SITE_URL}assets/img/svc-lecture.jpg">'''),
    ('<div><h4>联系方式</h4><ul class="foot-contact">{channels}</ul></div>',
     '''<div><h4>联系方式</h4>
<div class="foot-qrs">
<div class="foot-qr-item"><img src="assets/img/qrcode-consult.png" width="400" height="400" alt="微信咨询二维码" loading="lazy"><span>微信咨询</span></div>
<div class="foot-qr-item"><img src="assets/img/qrcode-official.png" width="400" height="400" alt="微信公众号二维码" loading="lazy"><span>微信公众号</span></div>
</div>
<ul class="foot-contact">{channels}</ul></div>'''),
    ('''    ch = [
        ("message", "微信公众号", "「雷一鸣工作室」留言交流"),
        ("file", "专栏平台", "中国大学生在线专栏"),
        ("users", "主理人", "雷一鸣（雷桂平）"),
    ]
    cc = "".join(simple_card(i, t, d, ["", "pink", "cyan"][k]) for k, (i, t, d) in enumerate(ch))
    b += section(sec_head("CHANNELS / 交流渠道", "可通过这些渠道取得联系") + f'<div class="grid g3">{cc}</div>')''',
     '''    qrs = f\'\'\'<div class="grid g2">
<div class="mini-card glass reveal qr-panel"><img src="assets/img/qrcode-consult.png" width="400" height="400" alt="微信咨询二维码" loading="lazy"><h4>{icon("message")} 微信咨询</h4><p class="one-line">扫码添加主理人好友</p></div>
<div class="mini-card glass reveal qr-panel"><img src="assets/img/qrcode-official.png" width="400" height="400" alt="微信公众号二维码" loading="lazy"><h4>{icon("globe")} 微信公众号</h4><p class="one-line">扫码关注工作室动态</p></div>
</div>\'\'\'
    b += section(sec_head("CHANNELS / 交流渠道", "扫一扫，保持联系",
                          "咨询沟通与内容分享各有入口，按需要选择即可。") + qrs)'''),
    ('''                   '均可通过微信公众号「雷一鸣工作室」留言发起。</p></div>', "section tight")''',
     '''                   '均可通过咨询二维码或公众号留言发起。</p></div>', "section tight")'''),
    ('''    for s in SERVICES:
        write(s["slug"] + ".html", page_service(s))
    print("total 12 pages")''',
     '''    for s in SERVICES:
        write(s["slug"] + ".html", page_service(s))

    # 站点级文件：域名统一取自 SITE_URL
    pages = ["index.html"] + [x[1] for x in NAV[1:]] + [s["slug"] + ".html" for s in SERVICES] + ["sitemap.html"]
    seen, urls = set(), []
    for pg in pages:
        if pg in seen:
            continue
        seen.add(pg)
        loc = SITE_URL if pg == "index.html" else SITE_URL + pg
        urls.append("  <url><loc>%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>"
                    % (loc, "1.0" if pg == "index.html" else "0.7"))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n'
          + "\\n".join(urls) + "\\n</urlset>\\n")
    write("robots.txt", "User-agent: *\\nAllow: /\\nSitemap: " + SITE_URL + "sitemap.xml\\n")
    write("CNAME", "www.oals.cn\\n")
    write(".nojekyll", "")
    print("total", len(seen), "pages + sitemap.xml / robots.txt / CNAME / .nojekyll")'''),
])

CSS_ADD = '''
/* ================= 第二轮：双二维码与页脚压缩 ================= */
.foot-qrs{display:flex;justify-content:center;gap:12px;margin:0 auto 10px}
.foot-qr-item{display:flex;flex-direction:column;align-items:center;gap:4px}
.foot-qr-item img{width:74px;height:auto;aspect-ratio:1/1;object-fit:contain;background:#fff;border-radius:8px;padding:4px;box-shadow:0 4px 12px rgba(0,0,0,.14)}
.foot-qr-item span{font-size:10.5px;color:#cfe0ff;font-weight:700;white-space:nowrap}
.qr-panel{display:flex;flex-direction:column;align-items:center}
.qr-panel img{width:190px;max-width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px;box-shadow:0 8px 24px rgba(20,80,180,.10)}
.qr-panel h4{margin-top:14px}
.qr-panel p{margin-top:6px}
.footer-top{padding:22px 0 12px}
.footer-about{line-height:1.6}
.footer-links{padding:8px 0}
.footer-tech{padding:0 0 8px}
.footer-bottom{padding:8px 0 12px}
'''
css = os.path.join(ROOT, "assets", "css", "style.css")
t = open(css, encoding="utf-8").read()
if "第二轮：双二维码与页脚压缩" not in t:
    open(css, "a", encoding="utf-8").write(CSS_ADD)
    print("patched assets/css/style.css")
else:
    print("CSS 已打过补丁，跳过")
