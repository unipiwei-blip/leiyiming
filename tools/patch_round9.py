# -*- coding: utf-8 -*-
"""第九轮：上传 404 页、扩充友情链接、优化 robots.txt 与 sitemap.xml。"""
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


def replace_between(rel, start_marker, end_marker, new_text):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    a = t.index(start_marker)
    b = t.index(end_marker, a)
    open(p, "w", encoding="utf-8").write(t[:a] + new_text + t[b:])
    print("replaced block in", rel)


# ---------------------------------------------------------------- 友情链接
p = "tools/site_content.py"
t = read(p)
t = once(t, '''FRIEND_LINKS = [
    ("广东省湖南攸县商会", "https://www.zyyous.com/"),
    ("才猎天下大数据", "https://www.91cailie.com/"),
    ("湾区（广东）数字经济研究院", "https://www.baydea.com/"),
]''',
         '''FRIEND_LINKS = [
    ("广东省湖南攸县商会", "https://www.zyyous.com/"),
    ("才猎天下大数据", "https://www.91cailie.com/"),
    ("湾区（广东）数字经济研究院", "https://www.baydea.com/"),
    ("AI建站-跨境极站", "https://www.gosite.com.cn/"),
    ("莞促集团", "https://www.guancu.com/"),
    ("东莞市常平个体私营企业协会", "https://www.ichangping.cn/"),
]''', "friend-links")
write(p, t)

# ---------------------------------------------------------------- 站点级文件
NEW_SITE_FILES = r'''    # 站点级文件：域名统一取自 SITE_URL
    TODAY = date.today().isoformat()
    PRIORITY = {
        "index.html": "1.0", "about.html": "0.8", "services.html": "0.8",
        "counseling.html": "0.8", "articles.html": "0.8", "founder.html": "0.7",
        "contact.html": "0.7", "sitemap.html": "0.3",
    }
    # 逻辑顺序：首页 -> 主导航 -> 业务详情 -> 二级页 -> 述评文章 -> 网站地图
    pages = (["index.html"] + [x[1] for x in NAV[1:]]
             + [s["slug"] + ".html" for s in SERVICES]
             + ["founder.html"] + [a["slug"] for a in ARTICLES]
             + ["sitemap.html"])
    seen, urls = set(), []
    for pg in pages:
        if pg in seen or pg == "404.html":
            continue
        seen.add(pg)
        path = os.path.join(ROOT, pg)
        lm = (date.fromtimestamp(os.path.getmtime(path)).isoformat()
              if os.path.exists(path) else TODAY)
        loc = SITE_URL if pg == "index.html" else SITE_URL + pg
        pr = PRIORITY.get(pg, "0.7" if pg.startswith("svc-") else "0.6")
        cf = ("weekly" if pg in ("index.html", "articles.html")
              else "yearly" if pg.startswith("article-") else "monthly")
        urls.append("  <url><loc>%s</loc><lastmod>%s</lastmod>"
                    "<changefreq>%s</changefreq><priority>%s</priority></url>"
                    % (loc, lm, cf, pr))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", "User-agent: *\nAllow: /\n"
          "Disallow: /tools/\nDisallow: /404.html\n"
          "Disallow: /CNAME\nDisallow: /.nojekyll\n"
          "Sitemap: " + SITE_URL + "sitemap.xml\n")
'''
replace_between("tools/build_site.py", "    # 站点级文件：域名统一取自 SITE_URL",
                '    write("CNAME", "www.oals.cn\\n")', NEW_SITE_FILES)

# ---------------------------------------------------------------- 校验脚本
p = "tools/validate.py"
t = read(p)
t = once(t, '''    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))''',
         '''    pages = sorted(p for p in glob.glob(os.path.join(ROOT, "*.html"))
                   if os.path.basename(p) != "404.html")
    # 404 页：独立自包含、故意不含 canonical / noindex / JSON-LD，且不能被收录
    nf = os.path.join(ROOT, "404.html")
    if not os.path.exists(nf):
        issues.append("缺 404.html")
    else:
        f404 = open(nf, encoding="utf-8").read()
        for bad in ("canonical", "noindex", "404-promo.jpg", "订阅", "meta refresh"):
            if bad in f404:
                issues.append(f"404.html 含 {bad}")
        if 'href="/"' not in f404:
            issues.append("404.html 缺首页入口")
    rb = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
    if "Disallow: /404.html" not in rb:
        issues.append("robots.txt 未屏蔽 404.html")
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    if "404.html" in sm:
        issues.append("sitemap.xml 不应包含 404.html")''', "validate-404")
write(p, t)

# ---------------------------------------------------------------- 页脚压缩
CSS_ADD = '''
/* ================= 第九轮：友情链接扩容后保持页脚紧凑 ================= */
.footer-links{padding:6px 0;gap:5px 10px;font-size:11.5px}
.footer-links a{font-size:11.5px}
.footer-links .fl-label{font-size:11.5px}
.footer-top{padding:18px 0 10px}
.footer-tech{padding:0 0 6px}
.footer-bottom{padding:6px 0 10px}
'''
p = "assets/css/style.css"
t = read(p)
if "第九轮：友情链接扩容后保持页脚紧凑" not in t:
    open(os.path.join(ROOT, p), "a", encoding="utf-8").write(CSS_ADD)
    print("appended", p)
else:
    print("skip (already)", p)
print("round9 done")
