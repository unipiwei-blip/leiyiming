# -*- coding: utf-8 -*-
"""雷一鸣工作室官网构建器：仿 gd.ippi.com.cn 设计系统，输出纯静态多页站点。
改文案请编辑 site_content.py，然后运行：python tools/build_site.py
"""
import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_content import (  # noqa: E402
    BRAND, SLOGAN, TOPBAR_LEFT, TOPBAR_RIGHT, FOOTER_ABOUT, COPYRIGHT_NOTE,
    NAV, FRIEND_LINKS, FOOT_BIZ, CONTACT_CHANNELS, STATS, ABOUT_CARDS, SITE_URL,
    FEATURES, DIRECTIONS, FLOW, SERVICES, FAQ, FOUNDER, ARTICLE_COLUMN, ARTICLE_DIRECTIONS,
    SUBNAV, COUNSELING,
)
from article_content import ARTICLES, ARTICLE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVC = {s["slug"]: s for s in SERVICES}

# ------------------------------------------------------------------ 图标
P = {
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "layers": '<path d="m12 2 9 5-9 5-9-5zM3 12l9 5 9-5M3 17l9 5 9-5"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3 21v-2a6 6 0 0 1 12 0v2M16 5a3 3 0 0 1 0 6M18 21v-2a5 5 0 0 0-2-4"/>',
    "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "heart": '<path d="M20.8 5.6a5.5 5.5 0 0 0-7.8 0L12 6.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 22l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>',
    "spark": '<path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16v3M17.5 17.5h3"/>',
    "message": '<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pen": '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z"/>',
    "megaphone": '<path d="M3 11v2a2 2 0 0 0 2 2h2l8 5V4L7 9H5a2 2 0 0 0-2 2zM18 9a4 4 0 0 1 0 6"/>',
    "check": '<path d="m4 12 5 5L20 6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l2-2a5 5 0 0 0-7-7l-1 1M14 11a5 5 0 0 0-7.5-.5l-2 2a5 5 0 0 0 7 7l1-1"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5zM6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5M22 9v6"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/><path d="M8 11h8M8 14h5"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5"/>',
    "quote": '<path d="M7 7h4v6a4 4 0 0 1-4 4M17 7h4v6a4 4 0 0 1-4 4"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
}


def icon(name, size=0, cls=""):
    st = ' style="width:%dpx;height:%dpx"' % (size, size) if size else ""
    return ('<svg class="%s"%s viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (cls, st, P.get(name, P["spark"])))


def city_svg():
    heights = [92, 146, 112, 188, 130, 214, 160, 246, 192, 148, 224, 120, 172, 205,
               140, 182, 104, 156, 236, 132, 196, 164, 116, 208, 144, 176, 226, 124, 184, 152, 200, 118]
    rects, x, i = [], 0, 0
    while x < 1460:
        h = heights[i % len(heights)]
        w = 38 + (i % 4) * 9
        rects.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="url(#bld)"/>'
                     % (x, 330 - h, w - 7, h))
        for wy in range(330 - h + 16, 316, 24):
            rects.append('<rect x="%d" y="%d" width="%d" height="3" rx="1.5" fill="rgba(255,255,255,.5)"/>'
                         % (x + 9, wy, w - 25))
        x += w
        i += 1
    return ('<svg class="city" viewBox="0 0 1440 330" preserveAspectRatio="none" aria-hidden="true">'
            '<defs><linearGradient id="bld" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="rgba(96,164,255,.34)"/>'
            '<stop offset="1" stop-color="rgba(255,255,255,.02)"/></linearGradient></defs>'
            + "".join(rects) + '</svg>')


# ------------------------------------------------------------------ 框架
def head(page, title, desc, keywords):
    key = page[:-5] if page.endswith(".html") else page
    # 未列入主导航的业务页，归入「服务体系」栏目高亮
    if key in ("svc-thought", "svc-lecture", "svc-counseling"):
        key = "services"
    if key.startswith("article-"):
        key = "articles"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "name": BRAND, "description": SLOGAN},
            {"@type": "WebPage", "name": title, "description": desc, "inLanguage": "zh-CN"},
        ],
    }
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | {BRAND}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="{BRAND}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1a6bff">
<link rel="canonical" href="{SITE_URL}{'' if page == 'index.html' else page}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}{'' if page == 'index.html' else page}">
<meta property="og:image" content="{SITE_URL}assets/img/svc-lecture.jpg">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="zh_CN">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body data-page="{key}">
'''


def topbar():
    return (f'<div class="topbar"><div class="container">'
            f'<span><span class="spark"></span>{TOPBAR_LEFT}</span>'
            f'<span class="hide-sm">{TOPBAR_RIGHT}</span></div></div>')


def nav(active):
    parent_active = set()
    for key, subs in SUBNAV.items():
        if active in [k for _, _, k in subs]:
            parent_active.add(key)
    items = []
    for label, href, key in NAV:
        subs = SUBNAV.get(key)
        if not subs:
            items.append(f'<a href="{href}" data-nav="{key}">{label}</a>')
            continue
        sub_parts = []
        for t, h, k in subs:
            attr = "" if k == key else f' data-nav="{k}"'
            sub_parts.append(f'<a href="{h}"{attr}>{t}</a>')
        sub = "".join(sub_parts)
        cls = " parent-active" if key in parent_active else ""
        items.append(f'<div class="nav-item{cls}"><a href="{href}" data-nav="{key}">'
                     f'{label}<i class="caret" aria-hidden="true"></i></a>'
                     f'<div class="submenu">{sub}</div></div>')
    return (f'<header class="nav"><div class="container">'
            f'<a class="brand" href="index.html" aria-label="{BRAND}">'
            f'<img src="assets/img/logo.svg" alt="{BRAND}"><span class="brand-txt"><strong>{BRAND}</strong></span></a>'
            f'<nav class="nav-menu" aria-label="主导航">{"".join(items)}</nav>'
            f'<a class="btn btn-primary nav-cta" href="contact.html">{icon("chat", 15)} 交流合作</a>'
            f'<button class="menu-btn" aria-label="展开导航菜单" aria-expanded="false"><i></i></button>'
            f'</div></header>')


def footer():
    biz = "".join(f'<a href="{h}">{t}</a>' for t, h in FOOT_BIZ)
    friends = "".join(
        f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in FRIEND_LINKS
    )
    channels = "".join(f'<li>{c}</li>' for c in CONTACT_CHANNELS)
    return f'''<footer class="footer"><div class="container">
<div class="footer-top">
<div>
<a class="brand" href="index.html"><img src="assets/img/logo.svg" alt="{BRAND}"><span class="brand-txt"><strong>{BRAND}</strong></span></a>
<p class="footer-about">{FOOTER_ABOUT}</p>
</div>
<div><h4>重点业务</h4><div class="biz-grid">{biz}</div></div>
<div><h4>联系方式</h4>
<div class="foot-qrs">
<div class="foot-qr-item"><img src="assets/img/qrcode-consult.png" width="400" height="400" alt="微信咨询二维码" loading="lazy"><span>微信咨询</span></div>
<div class="foot-qr-item"><img src="assets/img/qrcode-official.png" width="400" height="400" alt="微信公众号二维码" loading="lazy"><span>微信公众号</span></div>
</div>
<ul class="foot-contact">{channels}</ul></div>
</div>
<div class="footer-links"><span class="fl-label">友情链接</span>{friends}<span class="fl-sep">·</span><a href="sitemap.html">网站地图</a></div>
<div class="footer-tech"><span>网站技术服务支持：</span><a href="https://www.gdiis.com/" target="_blank" rel="noopener"><img src="assets/img/gdiis-logo.png" alt="创享互联 GDIIS" loading="lazy"> GDIIS · 创享互联</a></div>
<div class="footer-bottom"><span>&copy; <span data-year>2026</span> {BRAND} · {COPYRIGHT_NOTE}</span></div>
</div></footer>
</body>
</html>'''


def shell(page, title, desc, keywords, body, active):
    return (head(page, title, desc, keywords) + topbar() + nav(active)
            + "<main>" + body + "</main>" + footer())


# ------------------------------------------------------------------ 组件
def sec_head(eyebrow, h2, lead=""):
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return (f'<div class="sec-head center reveal"><div class="eyebrow">{eyebrow}</div>'
            f'<h2 class="h2">{h2}</h2>{l}</div>')


def section(inner, cls="section"):
    return f'<section class="{cls}"><div class="container">{inner}</div></section>'


def feature_card(num, ico, title, desc, tone=""):
    t = f" {tone}" if tone else ""
    return (f'<article class="card glass reveal"><span class="num">{num}</span>'
            f'<div class="ico{t}">{icon(ico)}</div><h3 class="h3">{title}</h3>'
            f'<p class="one-line">{desc}</p></article>')


def simple_card(ico, title, desc, tone="", link=None):
    t = f" {tone}" if tone else ""
    more = (f'<div class="mt-s"><a class="link-more" href="{link[1]}">{link[0]} {icon("arrow", 15)}</a></div>'
            if link else "")
    return (f'<article class="card glass reveal"><div class="ico{t}">{icon(ico)}</div>'
            f'<h3 class="h3">{title}</h3><p class="one-line">{desc}</p>{more}</article>')


def service_card(s, idx=0):
    tone = {"": "", "pink": " pink", "cyan": " cyan", "orange": " orange"}[s["tone"]]
    return (f'<article class="card glass reveal d{idx % 4}">'
            f'<div class="ico{tone}">{icon(s["icon"])}</div>'
            f'<h3 class="h3"><a href="{s["slug"]}.html">{s["title"]}</a></h3>'
            f'<p class="one-line">{s["short"]}</p>'
            f'<div class="mt-s"><a class="link-more" href="{s["slug"]}.html">了解服务内容 {icon("arrow", 15)}</a></div>'
            f'</article>')


def stats_strip():
    cells = "".join(
        f'<div class="stat"><b>{a}<small>{b}</small></b><span>{c}</span></div>'
        for a, b, c in STATS
    )
    return f'<div class="container"><div class="stat-strip glass reveal">{cells}</div></div>'


def flow(items, labels=None):
    out = []
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            title, desc, label = it
        else:
            title, desc, label = it, "", (labels[i] if labels else "")
        day = f'<span class="day">{label}</span>' if label else ""
        out.append(f'<div class="flow-item reveal d{i % 4}"><div class="flow-dot">{i+1:02d}</div>'
                   f'<h4>{title}</h4><p>{desc}</p>{day}</div>')
    return f'<div class="flow">{"".join(out)}</div>'


def faq(items):
    out = "".join(
        f'<details class="faq-item reveal"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(items)
    )
    return f'<div class="faq">{out}</div>'


def cta(title, desc, buttons=None, note=""):
    btns = buttons or [("交流合作", "contact.html", "btn-white"), ("了解服务体系", "services.html", "btn-outline")]
    links = "".join(f'<a class="btn {cls}" href="{h}">{t}</a>' for t, h, cls in btns)
    n = f'<p class="cta-note">{note}</p>' if note else ""
    return (f'<section class="section tight"><div class="container">'
            f'<div class="cta-dark reveal"><h2>{title}</h2><p>{desc}</p>'
            f'<div class="cta-actions">{links}</div>{n}</div></div></section>')


def page_hero(title, lead, pills=None, crumb=None):
    ps = "".join(f'<span class="pill">{p}</span>' for p in (pills or []))
    cr = (f'<div class="crumb"><a href="index.html">{BRAND}</a> / {crumb}</div>') if crumb else ""
    return (f'<section class="page-hero"><div class="container">{cr}'
            f'<h1>{title}</h1><p>{lead}</p>'
            f'<div class="pills">{ps}</div>'
            f'</div></section>')


def split_text_image(text_html, image, alt, reverse=False):
    pic = f'<div class="visual pic"><img src="assets/img/{image}" alt="{alt}" loading="lazy"></div>'
    left, right = (pic, f'<div class="split-copy">{text_html}</div>') if reverse else (
        f'<div class="split-copy">{text_html}</div>', pic)
    return f'<div class="split">{left}{right}</div>'


def case_card(image, alt, tag, title, desc, points, href, more="了解内容"):
    pts = "".join(f'<span>{p}</span>' for p in points)
    return (f'<article class="case-card reveal"><div class="case-shot">'
            f'<img src="assets/img/{image}" alt="{alt}" loading="lazy">'
            f'</div><div class="case-body"><div class="case-meta"><span class="tagx">{tag}</span></div>'
            f'<h3>{title}</h3><p class="one-line">{desc}</p>'
            f'<div class="case-points">{pts}</div>'
            f'<div class="case-foot"><span class="no">{alt}</span>'
            f'<a class="link-more" href="{href}">{more} {icon("arrow", 15)}</a></div>'
            f'</div></article>')


# ------------------------------------------------------------------ 首页
def hero_art():
    chips_l = [("价", "人生观", "#2932e1"), ("值", "价值观", "#008373"),
               ("世", "世界观", "#19b955"), ("素", "核心素质", "#f04b22"),
               ("能", "核心能力", "#07c160"), ("责", "社会责任", "#7a4bff")]
    chips_r = [("讲", "专题讲座", "#07c160"), ("谈", "座谈交流", "#1a6bff"),
               ("班", "主题班会", "#2b7bff"), ("践", "社会实践", "#111827"),
               ("辅", "成长辅导", "#e2157f"), ("研", "教学研究", "#4d6bff")]
    def chips(items):
        return "".join(f'<span class="chip"><i style="background:{c}">{k}</i>{t}</span>' for k, t, c in items)
    return f'''<div class="hero-bg"><div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div>{city_svg()}</div>
<div class="container"><div class="hero-inner">
<div class="hero-copy">
<div class="hero-kicker"><span></span>高校辅导员工作室 · 综合性育人平台</div>
<h1><span class="l1">以大学生思想政治教育为核心</span>
<span class="l2"><span class="t-blue">立德树人</span> · <span class="t-grad">陪伴成长</span></span></h1>
<p class="hero-sub"><strong>教学 · 研究 · 指导 · 服务。</strong>雷一鸣工作室以雷一鸣老师为主导，在教书育人、管理育人、服务育人的实践中，关注成长需求，尊重个体差异，陪伴大学生全面发展。</p>
<div class="hero-actions"><a class="btn btn-primary btn-lg" href="services.html">{icon("grid", 16)} 了解服务体系</a>
<a class="btn btn-ghost btn-lg" href="founder.html">{icon("users", 16)} 认识主理人</a></div>
<div class="hero-trust"><div><b>2016</b> 年创建</div><div><b>六大</b> 核心素质</div><div><b>三育人</b> 协同模式</div><div><b>双线</b> 融合育人</div></div>
</div>
<div class="hero-art" aria-hidden="true">
<div class="art-halo"></div><div class="art-ring"></div><div class="art-beam l"></div><div class="art-beam r"></div>
<div class="glass-panel left"><div class="panel-title">{icon("compass", 14)} 价值引领</div><div class="chips">{chips(chips_l)}</div></div>
<div class="glass-panel right"><div class="panel-title">{icon("users", 14)} 协同育人</div><div class="chips">{chips(chips_r)}</div></div>
<div class="core"><div class="core-shape"></div><div class="core-inner">
<div class="core-badge">{icon("cap", 23)}</div>
<div class="core-name">雷一鸣工作室</div>
<div class="core-tag">线上 + 线下 · 协同育人</div>
<div class="core-sub">教学 / 研究 / 指导 / 服务<br>陪伴青年全面成长</div>
</div></div>
<div class="pedestal"></div>
<span class="float-tag f1">三育人模式</span><span class="float-tag f2">六大核心素质</span><span class="float-tag f3">陪伴青年成长</span>
</div></div></div></section>'''


def article_mini_grid():
    cards = []
    for i, a in enumerate(ARTICLES[:3]):
        cards.append(f'''<a class="article-mini glass reveal d{i}" href="{a["slug"]}">
<div class="mini-shot"><img src="assets/img/{a["cover"]}" alt="{a["cover_alt"]}" loading="lazy"></div>
<div class="mini-copy"><span class="pill">{a["label"]} · {a["date"]}</span>
<h3 class="h3">{a["card_title"]}</h3><p class="one-line">{a["teaser"]}</p></div>
</a>''')
    more = ('<div class="center mt-l"><a class="btn btn-primary" href="articles.html">查看全部述评 '
            + icon("arrow", 16) + '</a></div>')
    return f'<div class="grid g3 article-mini-grid">{"".join(cards)}</div>' + more


def article_cards():
    cards, per = [], 4
    for i, a in enumerate(ARTICLES):
        pg = i // per + 1
        cards.append(f'''<a class="article-card glass reveal" href="{a["slug"]}" data-page="{pg}">
<div class="article-card-shot"><img src="assets/img/{a["cover"]}" alt="{a["cover_alt"]}" loading="lazy"></div>
<div class="article-card-body"><span class="pill">{a["label"]} · {a["date"]}</span>
<h3 class="h3">{a["card_title"]}</h3><p class="one-line">{a["teaser"]}</p>
<span class="link-more">阅读述评 {icon("arrow", 15)}</span></div></a>''')
    total = (len(ARTICLES) + per - 1) // per
    nums = "".join(f'<button class="page-num{" active" if n == 1 else ""}" data-go="{n}">{n}</button>'
                   for n in range(1, total + 1))
    pager = ('<div class="pager"><button data-go="prev">上一页</button>' + nums
             + '<button data-go="next">下一页</button></div>')
    return f'<div class="article-grid">{"".join(cards)}</div>' + pager


def page_articles():
    b = page_hero("一鸣述评", ARTICLE_COLUMN["lead"],
                  ARTICLE_COLUMN["tags"], "一鸣述评")
    b += section(sec_head("LATEST / 最新述评", ARTICLE_COLUMN["list_title"],
                          ARTICLE_COLUMN["list_lead"]) + article_cards())
    cards = "".join(simple_card(i, t, d, ["", "pink", "cyan"][k])
                    for k, (i, t, d) in enumerate(ARTICLE_DIRECTIONS))
    b += section(sec_head("TOPICS / 述评方向", ARTICLE_COLUMN["topics_title"])
                 + f'<div class="grid g3">{cards}</div>')
    b += cta("围绕教育话题继续交流", "关于大学教育、青年成长与学术积累的话题，欢迎进一步沟通。",
             [("交流合作", "contact.html", "btn-white"), ("返回首页", "index.html", "btn-outline")])
    return shell("articles.html", "一鸣述评", ARTICLE_COLUMN["desc"],
                 "一鸣述评,教育观察,雷一鸣工作室,述评文章", b, "articles")


def page_article(a):
    tags = "".join(f'<span class="pill">{t}</span>' for t in a["tags"])
    hero = f'''<section class="article-hero"><div class="container">
<div class="crumb"><a href="index.html">{BRAND}</a> / <a href="articles.html">一鸣述评</a> / 正文</div>
<h1>{a["title"]}</h1>
<p class="article-meta">{a["date"]}</p>
<p class="article-lead">{a["summary"]}</p>
<div class="pills">{tags}</div>
</div></section>'''
    cover = (f'<figure class="article-figure"><img src="assets/img/{a["cover"]}" '
             f'alt="{a["cover_alt"]}" loading="lazy"><figcaption>{a["cover_alt"]}</figcaption></figure>')
    parts = []
    for blk in a["blocks"]:
        if blk["t"] == "h":
            parts.append(f'<p class="article-h">{blk["x"]}</p>')
        elif blk["t"] == "p":
            parts.append(f'<p>{blk["x"]}</p>')
        else:
            parts.append(f'<figure class="article-figure"><img src="assets/img/{blk["src"]}" '
                         f'alt="{blk["cap"]}" loading="lazy"><figcaption>{blk["cap"]}</figcaption></figure>')
    rel = [s for s in SERVICES if s["slug"] in ("svc-research", "svc-quality", "svc-counseling")]
    rel_cards = "".join(service_card(s, i) for i, s in enumerate(rel))
    body = (hero
            + section(f'<div class="article-wrap">{cover}<div class="article-body">'
                      + "".join(parts) + '</div></div>', "section article-start")
            + section(sec_head("MORE / 延伸阅读", "与述评相关的工作方向")
                      + f'<div class="grid g3">{rel_cards}</div>'
                      + '<div class="center mt-l"><a class="btn btn-primary" href="articles.html">返回一鸣述评 '
                      + icon("arrow", 16) + '</a></div>'))
    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": a["title"], "datePublished": a["date_iso"],
          "author": {"@type": "Organization", "name": BRAND},
          "publisher": {"@type": "Organization", "name": BRAND},
          "description": a["desc"], "inLanguage": "zh-CN"}
    body = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>' + body
    return shell(a["slug"], a["full_title"], a["desc"], a["keywords"], body, "articles")


def page_counseling():
    c = COUNSELING
    b = page_hero("心理咨询", c["lead"], c["tags"], "心理咨询")
    text = ('<div class="eyebrow">GUIDANCE / 成长交流</div><h2 class="h2">'
            + c["intro_title"] + '</h2>'
            + "".join(f'<p class="lead">{p}</p>' for p in c["intro"]))
    b += section(split_text_image(text, "svc-counseling.jpg", "线上交流场景"))
    cards = "".join(simple_card(i, t, d, ["", "pink", "cyan"][k])
                    for k, (i, t, d) in enumerate(c["cards"]))
    b += section(sec_head("FOCUS / 交流主题", "常被谈起的三个方向")
                 + f'<div class="grid g3">{cards}</div>')
    ways = "".join(simple_card(i, t, d, ["", "pink", "cyan"][k])
                   for k, (i, t, d) in enumerate(c["ways"]))
    b += section(sec_head("METHODS / 交流方式", "线上与线下相互补充")
                 + f'<div class="grid g3">{ways}</div>')
    b += section(sec_head("BACKGROUND / 专业基础", "育人实践中的长期积累")
                 + f'<div class="mini-card glass reveal"><p>{c["basis"]}</p></div>', "section tight")
    b += cta("把想说的话说出来", "围绕成长中的困惑与选择，欢迎通过公众号或咨询二维码发起交流。",
             [("交流合作", "contact.html", "btn-white"), ("了解服务体系", "services.html", "btn-outline")])
    return shell("counseling.html", "心理咨询", c["desc"], c["keywords"], b, "counseling")


def page_index():
    b = '<section class="hero">' + hero_art()
    b += stats_strip()

    # 概览三卡
    cards = "".join(feature_card("", ico, title, desc, tone)
                    for i, (ico, title, desc, tone) in enumerate(
                        [(a, b_, c, ["", "pink", "cyan"][i]) for i, (a, b_, c) in enumerate(ABOUT_CARDS)]))
    b += section(sec_head("ABOUT / 平台概览", "育人不止于课堂，更在成长的每一天",
                          "工作室关注大学生的成长需求，注重个体差异，通过深入了解学生的思想观念、价值观念和生活状态，提供有针对性的指导和帮助。")
                 + f'<div class="grid g3">{cards}</div>')

    # 六条特色
    feats = "".join(feature_card(n, ico, title, desc, ["", "pink", "cyan", "orange"][i % 4])
                    for i, (n, ico, title, desc) in enumerate(FEATURES))
    b += section(sec_head("STRENGTHS / 育人特色", "把育人做进日常",
                          "从价值引领到实践体验，从个体辅导到教学研究，形成相互支撑的育人链条。")
                 + f'<div class="grid g3">{feats}</div>')

    # 两大服务方向
    biz = []
    for d in DIRECTIONS:
        lis = "".join(f'<li>{icon("check", 15)} {x}</li>' for x in d["items"])
        biz.append(f'<article class="biz-card glass {d["cls"]} reveal"><div class="radial"></div>'
                   f'<div class="biz-ico">{icon(d["icon"])}</div><h3>{d["title"]}</h3>'
                   f'<div class="sub">{d["sub"]}</div><p>{d["desc"]}</p>'
                   f'<ul class="biz-list">{lis}</ul>'
                   f'<div class="biz-foot"><a class="link-more" href="{d["href"]}">{d["more"]} {icon("arrow", 15)}</a></div></article>')
    b += section(sec_head("DIRECTIONS / 服务方向", "一边陪伴学生，一边支持育人者",
                          "既为大学生答疑解惑，也为辅导员同仁提供育人经验与工作方法参考。")
                 + f'<div class="grid g2">{"".join(biz)}</div>')

    # 育人路径
    b += section(sec_head("PATH / 育人路径", "从走近青年，到沉淀方法",
                          "五个环节前后衔接，让指导有依据、实践有落点、经验可延续。")
                 + flow(FLOW))

    # 服务体系六卡
    svcs = "".join(service_card(s, i) for i, s in enumerate(SERVICES))
    b += section(sec_head("SERVICES / 服务体系", "六项服务，覆盖成长全过程",
                          "价值引领、素质培养、讲座座谈、育人实践、成长辅导与教研推广协同推进。")
                 + f'<div class="grid g3">{svcs}</div>'
                 + '<div class="center mt-l"><a class="btn btn-primary" href="services.html">查看服务体系 '
                 + icon("arrow", 16) + '</a></div>')

    # 主理人
    founder_html = (f'<div class="eyebrow">HOST / 主理人</div><h2 class="h2">以雷一鸣老师为主导</h2>'
                    f'<p class="lead">雷一鸣（雷桂平）长期从事大学生思想政治教育与辅导员工作，'
                    f'是同济大学软件工程专业毕业生、讲师、国家二级心理咨询师，'
                    f'主编心理学教材两部、计算机专业教材一部，发表学生工作相关论文 10 余篇。</p>'
                    f'<div class="mt-m"><a class="btn btn-ghost" href="founder.html">了解主理人 {icon("arrow", 16)}</a></div>')
    b += section(split_text_image(founder_html, "founder-classroom.jpg", "主理人课堂授课现场"))

    # 育人影像三卡
    cases = [
        case_card("studio-plaque.jpg", "雷一鸣工作室牌匾", "工作室实景", "一方牌匾，一处育人平台",
                  "书法牌匾与中式陈设", ["品牌印记", "工作室", "育人平台"],
                  "about.html"),
        case_card("founder-classroom.jpg", "主理人课堂授课现场", "课堂教学", "陪你更加认识自己",
                  "在课堂上陪学生认识自己", ["价值引领", "成长引导", "课堂互动"],
                  "founder.html"),
        case_card("activity-training.jpg", "辅导员培训交流", "实践育人", "同行研讨中的经验沉淀",
                  "在同行研讨中沉淀方法", ["同行交流", "实践体验", "经验分享"],
                  "svc-practice.html"),
    ]
    b += section(sec_head("SCENES / 工作室实景", "从牌匾到课堂",
                          "工作室牌匾、课堂授课与同行交流，呈现育人工作的日常场景。")
                 + f'<div class="grid g3">{"".join(cases)}</div>')

    b += section(sec_head("PERSPECTIVES / 一鸣述评", "把对教育的思考写下来",
                          "围绕大学教育、青年成长与时代变化的观察与思考。")
                 + article_mini_grid())
    b += cta("一起把育人工作做深做实",
             "围绕专题讲座、育人实践共建、辅导员教研交流等方向，欢迎高校、辅导员同仁与青年学生开展交流。",
             note="以大学生思想政治教育为核心，注重实践创新与学术研究。")
    b += section(sec_head("FAQ / 常见问题", "关于工作室，先了解这些") + faq(FAQ[:4]))
    return shell("index.html", BRAND + " · " + SLOGAN, SLOGAN,
                 "雷一鸣工作室,雷桂平,大学生思想政治教育,辅导员工作室,六大核心素质,育人实践", b, "index")


# ------------------------------------------------------------------ 内页
def page_about():
    b = page_hero("工作室简介", "以雷一鸣老师为主导，集教学、研究、指导和服务于一体的综合性工作平台，"
                  "致力于提升大学生思想政治教育的质量和效果。",
                  ["2016 年创建", "三育人模式", "线上 + 线下"], "工作室简介")
    intro = (f'<div class="eyebrow">POSITION / 平台定位</div><h2 class="h2">以引领大学生思想政治教育为切入点</h2>'
             f'<p class="lead">工作室通过对大学生人生观、价值观、世界观的重新认识和重新构建，'
             f'以线上与线下相结合的方式，从不同角度了解青年学生的困惑、迷茫以及核心能力的得失；'
             f'在教书育人、管理育人、服务育人的模式下，帮助学生以更好的状态面对生活、面对自己、面对社会。</p>'
             f'<p class="lead">与此同时，工作室为改进大学生思想政治教育工作方式方法提供参考，'
             f'也为辅导员同仁更好地服务学生、教育学生、管理学生、引领学生提供力所能及的帮助。</p>')
    b += section(split_text_image(intro, "studio-plaque.jpg", "雷一鸣工作室牌匾"))

    cards = "".join(simple_card(ico, t, d, ["", "pink", "cyan"][i]) for i, (ico, t, d) in enumerate(ABOUT_CARDS))
    b += section(sec_head("PRINCIPLES / 工作理念", "关注成长需求，尊重个体差异") + f'<div class="grid g3">{cards}</div>')

    tri = [
        ("cap", "教书育人", "在课堂与分享中启发思考"),
        ("grid", "管理育人", "在日常关照中明确方向"),
        ("heart", "服务育人", "在回应需求中传递温度"),
    ]
    tric = "".join(simple_card(i, t, d, ["", "pink", "orange"][k]) for k, (i, t, d) in enumerate(tri))
    b += section(sec_head("FRAMEWORK / 三育人", "教书 · 管理 · 服务同向发力",
                          "三个环节共同承担育人责任，让价值塑造伴随学生成长的全过程。")
                 + f'<div class="grid g3">{tric}</div>')

    timeline = [
        "2016 年年初，雷一鸣工作室创建，搭建促进交流、探索育人机制的平台。",
        "围绕学生「自我管理、自我教育、自我服务」与辅导员「专业化、职业化、专家化」持续开展内容建设。",
        "通过微信公众号、网络平台与线下活动，形成线上与线下相互补充的工作模式。",
        "工作室建设经验在全国高校辅导员工作室建设经验展示中交流分享。",
        "持续开展教学研究与学术探索，总结推广辅导员工作的先进经验与做法。",
    ]
    lis = "".join(f'<li>{x}</li>' for x in timeline)
    b += section(sec_head("JOURNEY / 发展脉络", "从一处平台，到一条持续的育人路径")
                 + f'<ul class="num-list">{lis}</ul>')

    kws = ["思想政治教育", "六大核心素质", "价值引领", "主题班会", "社会实践", "个性化辅导",
           "教学研究", "辅导员队伍", "线上 + 线下", "全面发展"]
    b += section(sec_head("KEYWORDS / 工作关键词", "围绕这些关键词展开日常") +
                 f'<div class="keywords">{"".join(f"<span>{k}</span>" for k in kws)}</div>', "section tight")
    b += cta("了解工作室的服务体系", "价值引领、素质培养、讲座座谈、育人实践、成长辅导与教研推广，协同支撑学生全面发展。",
             [("查看服务体系", "services.html", "btn-white"), ("认识主理人", "founder.html", "btn-outline")])
    return shell("about.html", "工作室简介", "雷一鸣工作室简介、平台定位、三育人模式与发展脉络。",
                 "雷一鸣工作室简介,平台定位,三育人,发展脉络,雷桂平", b, "about")


def page_services():
    b = page_hero("服务体系", "围绕大学生成长需求与辅导员专业发展，形成六项相互支撑的服务内容。",
                  ["价值引领", "素质培养", "主题活动", "成长辅导", "教研推广"], "服务体系")
    svcs = "".join(service_card(s, i) for i, s in enumerate(SERVICES))
    b += section(sec_head("OVERVIEW / 服务总览", "六项服务，覆盖成长全过程") + f'<div class="grid g3">{svcs}</div>')

    biz = []
    for d in DIRECTIONS:
        lis = "".join(f'<li>{icon("check", 15)} {x}</li>' for x in d["items"])
        biz.append(f'<article class="biz-card glass {d["cls"]} reveal"><div class="radial"></div>'
                   f'<div class="biz-ico">{icon(d["icon"])}</div><h3>{d["title"]}</h3>'
                   f'<div class="sub">{d["sub"]}</div><p>{d["desc"]}</p><ul class="biz-list">{lis}</ul>'
                   f'<div class="biz-foot"><a class="link-more" href="{d["href"]}">{d["more"]} {icon("arrow", 15)}</a></div></article>')
    b += section(sec_head("AUDIENCE / 服务对象", "一边陪伴学生，一边支持育人者")
                 + f'<div class="grid g2">{"".join(biz)}</div>')

    ways = [
        ("globe", "线上平台", "微信公众号与网络平台持续交流"),
        ("users", "线下活动", "讲座、座谈、班会与实践现场"),
        ("message", "一对一辅导", "按个体差异回应具体困惑"),
        ("book", "教研转化", "把一线经验整理为可参考资料"),
    ]
    wc = "".join(simple_card(i, t, d, ["", "pink", "cyan", "orange"][k]) for k, (i, t, d) in enumerate(ways))
    b += section(sec_head("METHODS / 工作方式", "线上与线下相互补充",
                          "两类方式覆盖学生多样化的学习需求，也让育人经验得以沉淀与传递。")
                 + f'<div class="grid g4">{wc}</div>')
    b += section(sec_head("PATH / 育人路径", "从走近青年，到沉淀方法") + flow(FLOW))
    b += cta("围绕具体需求开展交流", "专题讲座、育人实践共建、辅导员教研交流等方向，欢迎进一步沟通。")
    return shell("services.html", "服务体系", "雷一鸣工作室六项服务内容、服务对象与育人路径。",
                 "雷一鸣工作室,服务体系,思想引领,核心素质,成长辅导,教研推广", b, "services")


def page_service(s):
    slug = s["slug"]
    b = page_hero(s["title"], s["lead"], s["pills"], s["title"])
    text = (f'<div class="eyebrow">{s["eyebrow"]}</div><h2 class="h2">{s["title"]}</h2>'
            + "".join(f'<p class="lead">{p}</p>' for p in s["intro"]))
    b += section(split_text_image(text, s["image"], s["title"] + "场景"))

    pts = "".join(simple_card(i, t, d, ["", "pink", "cyan"][k]) for k, (i, t, d) in enumerate(s["points"]))
    b += section(sec_head("FOCUS / 工作重点", "三个着力点") + f'<div class="grid g3">{pts}</div>')

    b += section(sec_head("PROCESS / 实施路径", "循序渐进，落到具体环节")
                 + flow([(x, "", "") for x in s["steps"]]))

    forms = "".join(f'<li>{icon("check", 17)} {x}</li>' for x in s["forms"])
    b += section(sec_head("FORMATS / 常见形式", "以多样载体承载育人目标",
                          "围绕学生实际需求组合使用，兼顾覆盖面与针对性。")
                 + f'<div class="grid g2"><div class="mini-card glass reveal"><ul class="check-list">{forms}</ul></div>'
                 + f'<div class="mini-card glass reveal"><h4>{icon("target")} 工作取向</h4>'
                 f'<p class="mt-s">尊重个体差异，注重实践体验，在持续交流中把方法沉淀为可复用的经验。</p>'
                 f'<div class="tag-list"><span>因材施教</span><span>实践导向</span><span>持续跟进</span><span>经验沉淀</span></div>'
                 f'</div></div>')

    # 六大核心素质专页附加完整六项
    if "qualities" in s:
        qc = "".join(simple_card(["shield", "compass", "heart", "spark", "book", "layers"][i], t, d,
                                 ["", "pink", "cyan", "orange", "", "pink"][i])
                     for i, (t, d) in enumerate(s["qualities"]))
        b += section(sec_head("SIX QUALITIES / 六大核心素质", "六项素质，支撑全面发展")
                     + f'<div class="grid g3">{qc}</div>')

    # 育人实践专页附真实影像
    if slug == "svc-practice":
        imgs = (f'<div class="grid g2"><div class="mini-card glass reveal">'
                f'<img src="assets/img/activity-training.jpg" alt="辅导员培训交流" loading="lazy">'
                f'<p class="mt-s">辅导员培训交流</p></div>'
                f'<div class="mini-card glass reveal">'
                f'<img src="assets/img/founder-classroom.jpg" alt="主理人课堂授课现场" loading="lazy">'
                f'<p class="mt-s">课堂授课现场</p></div></div>')
        b += section(sec_head("MOMENTS / 育人影像", "在真实的相处中看见成长") + imgs)

    # 相关服务
    rel = [x for x in SERVICES if x["slug"] != slug][:3]
    rc = "".join(service_card(x, i) for i, x in enumerate(rel))
    b += section(sec_head("RELATED / 相关服务", "与其他服务协同推进") + f'<div class="grid g3">{rc}</div>')
    b += cta("围绕具体需求开展交流", f"关于{s['title']}的更多安排，欢迎进一步沟通。",
             [("交流合作", "contact.html", "btn-white"), ("返回服务体系", "services.html", "btn-outline")])
    return shell(slug + ".html", s["title"], s["lead"],
                 "雷一鸣工作室," + s["title"] + "," + ",".join(s["pills"]), b, slug)


def page_founder():
    b = page_hero("主理人 · 雷一鸣", FOUNDER["lead"],
                  ["工作室主持人", "国家二级心理咨询师", "中国大学生在线专栏作者"], "主理人")
    text = (f'<div class="eyebrow">HOST / 主理人</div>'
            f'<h2 class="h2">雷一鸣（雷桂平）</h2>'
            f'<p class="lead">雷一鸣工作室由雷一鸣老师主导，其本名为雷桂平。'
            f'同济大学软件工程专业毕业，讲师、国家二级心理咨询师，长期从事辅导员工作与大学生思想政治教育研究。</p>'
            f'<p class="lead">在十余年一线工作中，他持续记录学生成长中的故事与困惑，'
            f'撰写思想政治教育相关文章数十万字，并把这些观察转化为教材、论文与可交流的育人经验。</p>')
    b += section(split_text_image(text, "founder-classroom.jpg", "主理人课堂授课现场"))

    b += section(sec_head("BELIEF / 育人理念", "做青年朋友的知心人、热心人、引路人")
                 + f'<div class="mini-card glass reveal"><div class="quote-mark">{icon("quote", 30)}</div>'
                 f'<p class="quote-text">{FOUNDER["quote"]}</p>'
                 f'<p class="mt-s">主动走近青年、倾听青年，真情关心青年、关爱青年，悉心教育青年、引导青年。</p></div>',
                 "section tight")

    groups = "".join(
        f'<div class="mini-card glass reveal"><h4>{icon(g[1])} {g[0]}</h4>'
        + "".join(f'<p>{x}</p>' for x in g[2]) + '</div>'
        for g in [(t, i, ls) for t, i, ls in FOUNDER["groups"]]
    )
    b += section(sec_head("PROFILE / 专业履历", "教学、研究与育人实践并行")
                 + f'<div class="grid g2">{groups}</div>')

    ideas = [
        ("eye", "走近青年", "先理解，再引导"),
        ("message", "平等交流", "在对话中回应困惑"),
        ("pen", "持续记录", "把观察沉淀为方法"),
    ]
    ic = "".join(simple_card(i, t, d, ["", "pink", "cyan"][k]) for k, (i, t, d) in enumerate(ideas))
    b += section(sec_head("APPROACH / 工作取向", "用心、用情、用爱") + f'<div class="grid g3">{ic}</div>')
    b += cta("与主理人开展交流", "围绕专题讲座、育人实践共建、辅导员教研交流等方向，欢迎留言沟通。")
    return shell("founder.html", "主理人 · 雷一鸣（雷桂平）",
                 "雷一鸣工作室主持人雷一鸣（雷桂平）的专业背景、教材课题、论文荣誉与育人理念。",
                 "雷一鸣,雷桂平,工作室主持人,辅导员,国家二级心理咨询师", b, "founder")


def page_contact():
    b = page_hero("联系我们", "围绕专题讲座、育人实践共建、辅导员教研交流等方向，欢迎开展交流。",
                  ["交流合作", "育人实践", "教研交流"], "联系我们")
    qrs = f'''<div class="grid g2">
<div class="mini-card glass reveal qr-panel"><img src="assets/img/qrcode-consult.png" width="400" height="400" alt="微信咨询二维码" loading="lazy"><h4>{icon("message")} 微信咨询</h4><p class="one-line">扫码添加主理人好友</p></div>
<div class="mini-card glass reveal qr-panel"><img src="assets/img/qrcode-official.png" width="400" height="400" alt="微信公众号二维码" loading="lazy"><h4>{icon("globe")} 微信公众号</h4><p class="one-line">扫码关注工作室动态</p></div>
</div>'''
    b += section(sec_head("CHANNELS / 交流渠道", "扫一扫，保持联系",
                          "咨询沟通与内容分享各有入口，按需要选择即可。") + qrs)

    coop = [
        ("megaphone", "专题讲座与座谈", "面向学生开展主题分享"),
        ("flag", "育人实践共建", "主题班会与社会实践协同"),
        ("book", "辅导员教研交流", "经验分享与工作方法研讨"),
    ]
    oc = "".join(simple_card(i, t, d, ["", "pink", "cyan"][k]) for k, (i, t, d) in enumerate(coop))
    b += section(sec_head("COOPERATION / 合作方向", "可围绕这些方向展开")
                 + f'<div class="grid g3">{oc}</div>')

    b += section(sec_head("NOTE / 沟通说明", "把需求说清楚，交流更高效",
                          "建议说明交流主题、参与对象、预期形式与时间范围，便于就具体安排充分沟通。")
                 + '<div class="mini-card glass reveal"><p>工作室以大学生思想政治教育为核心，'
                   '兼顾教学研究、指导与服务。面向学生的成长辅导与面向辅导员同仁的经验交流，'
                   '均可通过咨询二维码或公众号留言发起。</p></div>', "section tight")

    b += section(sec_head("FAQ / 常见问题", "关于交流合作，先了解这些") + faq(FAQ))
    return shell("contact.html", "联系我们", "雷一鸣工作室交流渠道、合作方向与常见问题。",
                 "雷一鸣工作室,联系我们,交流合作,育人实践,教研交流", b, "contact")


def page_sitemap():
    b = page_hero("网站地图", "雷一鸣工作室官网栏目一览。", ["栏目总览", "服务体系", "交流合作"], "网站地图")
    def group(title, ico, items):
        lis = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in items)
        return (f'<div class="mini-card glass reveal"><h4>{icon(ico)} {title}</h4>'
                f'<ul class="site-list">{lis}</ul></div>')
    groups = [
        group("主导航", "grid", [(t, h) for t, h, _ in NAV]),
        group("服务体系", "layers", [(s["title"], s["slug"] + ".html") for s in SERVICES]),
        group("更多信息", "link", [("主理人", "founder.html"), ("六大核心素质", "svc-quality.html"),
                                  ("一鸣述评", "articles.html"), ("网站地图", "sitemap.html")]
              + [(a["card_title"], a["slug"]) for a in ARTICLES]),
    ]
    b += section(sec_head("SITEMAP / 栏目一览", "按主题查阅全部内容")
                 + f'<div class="grid g3">{"".join(groups)}</div>')
    b += cta("从服务体系开始了解", "六项服务覆盖价值引领、素质培养、主题活动、成长辅导与教研推广。",
             [("查看服务体系", "services.html", "btn-white"), ("交流合作", "contact.html", "btn-outline")])
    return shell("sitemap.html", "网站地图", "雷一鸣工作室官网全部栏目与页面索引。",
                 "雷一鸣工作室,网站地图,栏目索引", b, "sitemap")


# ------------------------------------------------------------------ 输出
def write(name, html):
    path = os.path.join(ROOT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("write", name, len(html), "chars")


def main():
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    write("index.html", page_index())
    write("about.html", page_about())
    write("services.html", page_services())
    write("founder.html", page_founder())
    write("contact.html", page_contact())
    write("sitemap.html", page_sitemap())
    write("articles.html", page_articles())
    write("counseling.html", page_counseling())
    for a in ARTICLES:
        write(a["slug"], page_article(a))
    for s in SERVICES:
        write(s["slug"] + ".html", page_service(s))

    # 站点级文件：域名统一取自 SITE_URL
    pages = (["index.html"] + [x[1] for x in NAV[1:]] + [s["slug"] + ".html" for s in SERVICES]
             + ["sitemap.html", "founder.html"] + [a["slug"] for a in ARTICLES])
    seen, urls = set(), []
    for pg in pages:
        if pg in seen:
            continue
        seen.add(pg)
        loc = SITE_URL if pg == "index.html" else SITE_URL + pg
        urls.append("  <url><loc>%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>"
                    % (loc, "1.0" if pg == "index.html" else "0.7"))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: " + SITE_URL + "sitemap.xml\n")
    write("CNAME", "www.oals.cn\n")
    write(".nojekyll", "")
    print("total", len(seen), "pages + sitemap.xml / robots.txt / CNAME / .nojekyll")


if __name__ == "__main__":
    main()
