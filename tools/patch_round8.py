# -*- coding: utf-8 -*-
"""第八轮：网站地图页更新 + 全站 SEO 补强。"""
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


p = "tools/build_site.py"
t = read(p)
t = once(t, "import os\nimport json\nimport sys\n",
         "import os\nimport json\nimport sys\nfrom datetime import date\n", "import-date")
write(p, t)

NEW_HEAD = r"""def head(page, title, desc, keywords):
    key = page[:-5] if page.endswith(".html") else page
    # 未列入主导航的业务页，归入「服务体系」栏目高亮
    if key in ("svc-thought", "svc-lecture", "svc-counseling"):
        key = "services"
    if key.startswith("article-"):
        key = "articles"
    url = SITE_URL if page == "index.html" else SITE_URL + page
    art = next((a for a in ARTICLES if a["slug"] == page), None)
    og_img = SITE_URL + ("assets/img/" + art["cover"] if art else "assets/img/og-image.png")
    og_alt = art["cover_alt"] if art else (BRAND + " · " + SLOGAN)
    full_title = title if page == "index.html" else title + " | " + BRAND

    crumbs = [(BRAND, SITE_URL)]
    if page != "index.html":
        if art:
            crumbs.append(("一鸣述评", SITE_URL + "articles.html"))
            crumbs.append((art["card_title"], url))
        else:
            label = next((n for n, h, _ in NAV if h == page), None)
            if label is None:
                if page == "founder.html":
                    crumbs.append(("工作室简介", SITE_URL + "about.html"))
                    label = "主理人"
                elif page.startswith("svc-"):
                    crumbs.append(("服务体系", SITE_URL + "services.html"))
                    label = next((s["title"] for s in SERVICES
                                  if s["slug"] + ".html" == page), title)
                else:
                    label = title
            crumbs.append((label, url))

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": SITE_URL + "#organization",
             "name": BRAND, "url": SITE_URL, "description": SLOGAN,
             "logo": {"@type": "ImageObject", "url": SITE_URL + "assets/img/logo.svg"}},
            {"@type": "WebSite", "@id": SITE_URL + "#website", "url": SITE_URL,
             "name": BRAND, "publisher": {"@id": SITE_URL + "#organization"},
             "inLanguage": "zh-CN"},
            {"@type": "WebPage", "@id": url + "#webpage", "url": url,
             "name": title, "description": desc,
             "isPartOf": {"@id": SITE_URL + "#website"},
             "breadcrumb": {"@id": url + "#breadcrumb"}, "inLanguage": "zh-CN"},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                 for i, (n, u) in enumerate(crumbs)]},
        ],
    }
    if art:
        ld["@graph"].append({
            "@type": "Article", "@id": url + "#article",
            "headline": art["title"], "description": art["desc"],
            "image": og_img, "datePublished": art["date_iso"],
            "author": {"@id": SITE_URL + "#organization"},
            "publisher": {"@id": SITE_URL + "#organization"},
            "mainEntityOfPage": {"@id": url + "#webpage"},
            "articleSection": "一鸣述评", "keywords": art["keywords"],
            "inLanguage": "zh-CN"})
    og_dims = ('' if art else
               '<meta property="og:image:width" content="1200">\n'
               '<meta property="og:image:height" content="630">\n')
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="{BRAND}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1a6bff">
<link rel="canonical" href="{url}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{'article' if art else 'website'}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="zh_CN">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:alt" content="{og_alt}">
{og_dims}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full_title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body data-page="{key}">
'''


"""
replace_between(p, "def head(page, title, desc, keywords):", "def topbar():", NEW_HEAD)

t = read(p)
# 文章页不再单独输出 Article JSON-LD，统一由 head() 生成
t = once(t, '''    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": a["title"], "datePublished": a["date_iso"],
          "author": {"@type": "Organization", "name": BRAND},
          "publisher": {"@type": "Organization", "name": BRAND},
          "description": a["desc"], "inLanguage": "zh-CN"}
    body = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>' + body
''', '', "drop-article-ld")
# 首页标题与描述
t = once(t, '''    return shell("index.html", BRAND + " · " + SLOGAN, SLOGAN,
                 "雷一鸣工作室,雷桂平,大学生思想政治教育,辅导员工作室,六大核心素质,育人实践", b, "index")''',
         '''    return shell("index.html", "雷一鸣工作室｜大学生思想政治教育与成长陪伴",
                 "雷一鸣工作室以雷一鸣老师为主导，集教学、研究、指导和服务于一体，围绕价值引领、六大核心素质培养、专题讲座、主题班会、社会实践与个性化成长辅导，陪伴大学生全面发展。",
                 "雷一鸣工作室,雷桂平,大学生思想政治教育,辅导员工作室,六大核心素质,一鸣述评,心理咨询,育人实践", b, "index")''',
         "index-seo")
# 站点级文件：sitemap.xml 加 lastmod / 分级权重，robots 屏蔽脚本目录
t = once(t, '''        urls.append("  <url><loc>%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>"
                    % (loc, "1.0" if pg == "index.html" else "0.7"))''',
         '''        pr = PRIORITY.get(pg, "0.7" if pg.startswith("svc-") else "0.6")
        cf = ("weekly" if pg in ("index.html", "articles.html")
              else "yearly" if pg.startswith("article-") else "monthly")
        urls.append("  <url><loc>%s</loc><lastmod>%s</lastmod>"
                    "<changefreq>%s</changefreq><priority>%s</priority></url>"
                    % (loc, TODAY, cf, pr))''', "sitemap-url")
t = once(t, '''    # 站点级文件：域名统一取自 SITE_URL
    pages =''',
         '''    # 站点级文件：域名统一取自 SITE_URL
    TODAY = date.today().isoformat()
    PRIORITY = {
        "index.html": "1.0", "about.html": "0.8", "services.html": "0.8",
        "counseling.html": "0.8", "articles.html": "0.8", "founder.html": "0.7",
        "contact.html": "0.7", "sitemap.html": "0.3",
    }
    pages =''', "priority-map")
t = once(t, '''    write("robots.txt", "User-agent: *\\nAllow: /\\nSitemap: " + SITE_URL + "sitemap.xml\\n")''',
         '''    write("robots.txt", "User-agent: *\\nAllow: /\\nDisallow: /tools/\\nSitemap: "
          + SITE_URL + "sitemap.xml\\n")''', "robots")
write(p, t)

# ---------------------------------------------------------------- 网站地图页
NEW_SITEMAP = r'''def page_sitemap():
    b = page_hero("网站地图", "按主题查阅雷一鸣工作室官网的全部栏目与文章。",
                  ["栏目总览", "服务体系", "一鸣述评"], "网站地图")

    def group(title, ico, items):
        lis = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in items)
        return (f'<div class="mini-card glass reveal"><h4>{icon(ico)} {title}</h4>'
                f'<ul class="site-list">{lis}</ul></div>')

    groups = [
        group("主导航", "grid", [(t, h) for t, h, _ in NAV]),
        group("服务体系", "layers", [(s["title"], s["slug"] + ".html") for s in SERVICES]),
        group("一鸣述评", "pen", [("述评栏目总览", "articles.html")]
              + [(a["card_title"], a["slug"]) for a in ARTICLES]),
        group("工作室与站点", "users", [("工作室简介", "about.html"), ("主理人", "founder.html"),
                                    ("六大核心素质", "svc-quality.html"),
                                    ("网站地图", "sitemap.html")]),
    ]
    b += section(sec_head("SITEMAP / 栏目一览", "按主题查阅全部页面",
                          "首页、业务栏目、述评文章与站点信息均可在此找到。")
                 + f'<div class="grid g2 sitemap-grid">{"".join(groups)}</div>')
    b += cta("从服务体系开始了解", "六项服务覆盖价值引领、素质培养、主题活动、成长辅导与教研推广。",
             [("查看服务体系", "services.html", "btn-white"), ("交流合作", "contact.html", "btn-outline")])
    return shell("sitemap.html", "网站地图",
                 "雷一鸣工作室官网网站地图，包含主导航、服务体系、一鸣述评全部文章与工作室相关页面的完整索引。",
                 "雷一鸣工作室,网站地图,栏目索引,一鸣述评,服务体系", b, "sitemap")


'''
replace_between(p, "def page_sitemap():", "def write(name, html):", NEW_SITEMAP)

# ---------------------------------------------------------------- 校验脚本
p = "tools/validate.py"
t = read(p)
t = once(t, '''        if 'canonical" href="https://www.oals.cn/' not in html:
            issues.append(f"{name}: canonical 未绑定 www.oals.cn")''',
         '''        if 'canonical" href="https://www.oals.cn/' not in html:
            issues.append(f"{name}: canonical 未绑定 www.oals.cn")
        for tag in ('rel="canonical"', 'property="og:image"', 'name="twitter:card"',
                    '"BreadcrumbList"', '"WebSite"', '"Organization"'):
            if tag not in html:
                issues.append(f"{name}: SEO 缺 {tag}")''', "seo-tags")
t = once(t, '''    print(f"检查页面 {len(pages)} 个，问题 {len(issues)} 条")''',
         '''    xml = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    for h in pages:
        nm = os.path.basename(h)
        if nm == "index.html":
            if "https://www.oals.cn/<" not in xml:
                issues.append("sitemap.xml 缺首页")
        elif "/" + nm + "<" not in xml:
            issues.append(f"sitemap.xml 缺 {nm}")

    print(f"检查页面 {len(pages)} 个，问题 {len(issues)} 条")''', "sitemap-check")
write(p, t)

# ---------------------------------------------------------------- 样式
CSS_ADD = '''
/* ================= 第八轮：网站地图四组 ================= */
.sitemap-grid .mini-card{padding:26px 28px}
.sitemap-grid .site-list{gap:10px;margin-top:16px}
.sitemap-grid .site-list a{font-size:14px;line-height:1.7}
@media(max-width:640px){.sitemap-grid .mini-card{padding:20px}}
'''
p = "assets/css/style.css"
t = read(p)
if "第八轮：网站地图四组" not in t:
    open(os.path.join(ROOT, p), "a", encoding="utf-8").write(CSS_ADD)
    print("appended", p)
else:
    print("skip (already)", p)
print("round8 done")
