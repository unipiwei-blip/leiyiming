# -*- coding: utf-8 -*-
"""第五轮：导航二级化、新增心理咨询、述评列表改造、文章正文居左缩进。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def patch(rel, pairs):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, "%s 命中 %d 次: %r" % (rel, n, old[:70])
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8").write(t)
    print("patched", rel)


def replace_between(rel, start_marker, end_marker, new_text):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    a = t.index(start_marker)
    b = t.index(end_marker, a)
    t = t[:a] + new_text + t[b:]
    open(p, "w", encoding="utf-8").write(t)
    print("replaced block in", rel)


def append_once(rel, marker, text):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    if marker not in t:
        open(p, "a", encoding="utf-8").write(text)
        print("appended", rel)
    else:
        print("skip (already)", rel)


# ---------------------------------------------------------------- 数据
patch("tools/site_content.py", [
    ('''NAV = [
    ("首页", "index.html", "index"),
    ("工作室简介", "about.html", "about"),
    ("服务体系", "services.html", "services"),
    ("六大核心素质", "svc-quality.html", "svc-quality"),
    ("育人实践", "svc-practice.html", "svc-practice"),
    ("教研探索", "svc-research.html", "svc-research"),
    ("一鸣述评", "articles.html", "articles"),
    ("主理人", "founder.html", "founder"),
    ("联系我们", "contact.html", "contact"),
]''',
     '''NAV = [
    ("首页", "index.html", "index"),
    ("工作室简介", "about.html", "about"),
    ("服务体系", "services.html", "services"),
    ("心理咨询", "counseling.html", "counseling"),
    ("育人实践", "svc-practice.html", "svc-practice"),
    ("教研探索", "svc-research.html", "svc-research"),
    ("一鸣述评", "articles.html", "articles"),
    ("联系我们", "contact.html", "contact"),
]'''),
])

append_once("tools/site_content.py", "SUBNAV = {", '''

# 主导航二级栏目
SUBNAV = {
    "about": [("工作室简介", "about.html", "about"),
              ("主理人", "founder.html", "founder")],
    "services": [("服务体系总览", "services.html", "services"),
                 ("六大核心素质", "svc-quality.html", "svc-quality")],
}

COUNSELING = {
    "lead": "以倾听为先，陪伴学生面对成长中的困惑与选择。",
    "tags": ["一对一交流", "身心素质", "持续跟进"],
    "intro_title": "把困惑说出来，才有一起梳理的开始",
    "intro": [
        "工作室关注大学生的成长需求，注重个体差异。学业压力、人际关系、情绪起伏与自我认识，都是青年学生在校期间常常面对的课题。",
        "在平等、安静的交流中，先听清学生真实的处境，再一起梳理可行的方向；不替学生作决定，也不让问题悬空。",
    ],
    "cards": [
        ("message", "情绪与适应", "面对压力与情绪起伏"),
        ("users", "学业与人际", "梳理学习状态与相处困扰"),
        ("spark", "自我认识", "在交流中看清兴趣方向"),
    ],
    "ways": [
        ("globe", "线上交流", "网络平台答疑与分享"),
        ("users", "线下面谈", "谈心谈话与小组交流"),
        ("clock", "持续跟进", "保留长期沟通空间"),
    ],
    "basis": "工作室主持人雷一鸣（雷桂平）为国家二级心理咨询师，曾主编心理学教材两部，长期从事辅导员工作与大学生思想政治教育研究。",
    "desc": "雷一鸣工作室成长交流方向：以倾听为先的一对一沟通，围绕情绪与适应、学业人际与自我认识展开。",
    "keywords": "心理咨询,成长辅导,国家二级心理咨询师,一对一交流,雷一鸣工作室",
}
''')

# ---------------------------------------------------------------- 生成器
patch("tools/build_site.py", [
    ("    FEATURES, DIRECTIONS, FLOW, SERVICES, FAQ, FOUNDER, ARTICLE_COLUMN, ARTICLE_DIRECTIONS,\n)\nfrom article_content import ARTICLE  # noqa: E402",
     "    FEATURES, DIRECTIONS, FLOW, SERVICES, FAQ, FOUNDER, ARTICLE_COLUMN, ARTICLE_DIRECTIONS,\n"
     "    SUBNAV, COUNSELING,\n)\nfrom article_content import ARTICLES, ARTICLE  # noqa: E402"),
])

NEW_NAV = r'''def nav(active):
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
        sub = "".join(f'<a href="{h}" data-nav="{k}">{t}</a>' for t, h, k in subs)
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


'''
replace_between("tools/build_site.py", "def nav(active):", "def footer():", NEW_NAV)

NEW_FUNCS = r"""def article_mini_grid():
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
<span class="pill">{a["label"]}</span>
<h1>{a["title"]}</h1>
<p class="article-meta">{BRAND} · {a["date"]}</p>
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
                      + "".join(parts) + '</div></div>', "section tight")
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


"""
replace_between("tools/build_site.py", "def article_teaser():", "def page_index():", NEW_FUNCS)

patch("tools/build_site.py", [
    ("+ article_teaser())", "+ article_mini_grid())"),
    ('''        group("更多信息", "link", [("工作室简介", "about.html"), ("主理人", "founder.html"),
                                  ("联系我们", "contact.html"), ("网站地图", "sitemap.html"),
                                  ("一鸣述评", "articles.html"), ("最新述评 · 冷门绝学", ARTICLE["slug"])]),''',
     '''        group("更多信息", "link", [("主理人", "founder.html"), ("六大核心素质", "svc-quality.html"),
                                  ("一鸣述评", "articles.html"), ("网站地图", "sitemap.html")]
              + [(a["card_title"], a["slug"]) for a in ARTICLES]),'''),
    ('''    write("articles.html", page_articles())
    write(ARTICLE["slug"], page_article())
    for s in SERVICES:''',
     '''    write("articles.html", page_articles())
    write("counseling.html", page_counseling())
    for a in ARTICLES:
        write(a["slug"], page_article(a))
    for s in SERVICES:'''),
    ('''    pages = (["index.html"] + [x[1] for x in NAV[1:]] + [s["slug"] + ".html" for s in SERVICES]
             + ["sitemap.html", ARTICLE["slug"]])''',
     '''    pages = (["index.html"] + [x[1] for x in NAV[1:]] + [s["slug"] + ".html" for s in SERVICES]
             + ["sitemap.html", "founder.html"] + [a["slug"] for a in ARTICLES])'''),
])

# ---------------------------------------------------------------- 样式
CSS_ADD = r'''
/* ================= 第五轮：二级导航 / 述评列表 / 正文缩进 ================= */
.nav-item{position:relative;display:flex;align-items:center}
.nav-item>a{display:inline-flex;align-items:center;gap:6px}
.caret{width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid currentColor;opacity:.55}
.submenu{position:absolute;top:100%;left:50%;transform:translateX(-50%);min-width:168px;background:rgba(255,255,255,.98);backdrop-filter:blur(18px);border:1px solid var(--line);border-radius:12px;box-shadow:0 16px 36px rgba(15,60,150,.16);padding:8px;display:none;flex-direction:column;gap:2px;z-index:70}
.nav-item:hover .submenu,.nav-item:focus-within .submenu{display:flex}
.submenu a{font-size:13px!important;padding:9px 12px!important;white-space:nowrap;border-radius:8px;color:var(--ink-2)}
.submenu a:hover{background:rgba(26,107,255,.08);color:var(--blue)}
.nav-item.parent-active>a{color:var(--blue);font-weight:800}
@media(max-width:900px){
  .nav-item{display:block;width:100%}
  .nav-item>a{justify-content:flex-start}
  .caret{display:none}
  .submenu{position:static;transform:none;display:flex;box-shadow:none;border:0;background:transparent;padding:0 0 2px 16px;min-width:0}
  .submenu a{font-size:13.5px!important;padding:7px 14px!important;color:var(--muted)}
}
/* 首页三列封面卡 */
.article-mini{display:block;overflow:hidden;border-radius:var(--r);padding:0;text-align:center}
.article-mini .mini-shot{height:180px;overflow:hidden;background:#eaf2ff}
.article-mini .mini-shot img{width:100%;height:100%;object-fit:cover;object-position:center;display:block;margin:0;transition:transform .5s var(--ease)}
.article-mini:hover .mini-shot img{transform:scale(1.05)}
.article-mini .mini-copy{padding:20px 18px 24px;display:flex;flex-direction:column;align-items:center;gap:9px}
.article-mini h3{font-size:17px;font-weight:900;line-height:1.5;color:var(--ink)}
.article-mini p{color:var(--muted);font-size:13px}
/* 栏目页两列文章卡 + 翻页 */
.article-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.article-card{display:flex;flex-direction:column;overflow:hidden;border-radius:var(--r);padding:0;text-align:center;transition:transform .3s var(--ease)}
.article-card:hover{transform:translateY(-6px);box-shadow:var(--shadow-lg)}
.article-card-shot{height:220px;overflow:hidden;background:#eaf2ff}
.article-card-shot img{width:100%;height:100%;object-fit:cover;object-position:center;display:block;margin:0}
.article-card-body{padding:24px 26px 28px;display:flex;flex-direction:column;align-items:center;gap:10px}
.article-card-body h3{font-size:19px;font-weight:900;line-height:1.5;color:var(--ink)}
.article-card-body p{color:var(--muted);font-size:13.5px}
[hidden]{display:none!important}
.pager{display:flex;justify-content:center;align-items:center;gap:10px;margin-top:36px;flex-wrap:wrap}
.pager button{min-width:42px;padding:9px 16px;border-radius:10px;border:1px solid var(--line);background:rgba(255,255,255,.86);color:var(--ink-2);font-size:13.5px;font-weight:800;box-shadow:0 4px 14px rgba(20,80,180,.06);transition:.2s}
.pager button:hover:not(:disabled){border-color:var(--blue);color:var(--blue)}
.pager button.active{background:linear-gradient(105deg,#1668ff,#5b5bff);color:#fff;border-color:transparent}
.pager button:disabled{opacity:.42;cursor:not-allowed}
@media(max-width:640px){.article-grid{grid-template-columns:1fr}.article-card-shot{height:190px}.article-mini .mini-shot{height:165px}}
/* 文章正文：居左、首行空两字符 */
.article-body p{text-align:left;text-indent:2em}
.article-body p.article-h{text-align:left;text-indent:2em}
'''
append_once("assets/css/style.css", "第五轮：二级导航", CSS_ADD)

# ---------------------------------------------------------------- 交互
JS_ADD = r'''
/* 一鸣述评列表翻页（纯静态，无后端） */
(function () {
  'use strict';
  var cards = [].slice.call(document.querySelectorAll('.article-card[data-page]'));
  if (!cards.length) return;
  var btns = [].slice.call(document.querySelectorAll('.pager [data-go]'));
  var total = 0;
  cards.forEach(function (c) { total = Math.max(total, parseInt(c.getAttribute('data-page'), 10) || 1); });
  var cur = 1;
  function show(n) {
    cur = Math.max(1, Math.min(n, total));
    cards.forEach(function (c) { c.hidden = (parseInt(c.getAttribute('data-page'), 10) !== cur); });
    btns.forEach(function (b) {
      var g = b.getAttribute('data-go');
      if (g === 'prev') b.disabled = (cur === 1);
      else if (g === 'next') b.disabled = (cur === total);
      else b.classList.toggle('active', parseInt(g, 10) === cur);
    });
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var g = b.getAttribute('data-go');
      show(g === 'prev' ? cur - 1 : g === 'next' ? cur + 1 : parseInt(g, 10));
    });
  });
  show(1);
})();
'''
append_once("assets/js/main.js", "一鸣述评列表翻页", JS_ADD)

# ---------------------------------------------------------------- 校验
patch("tools/validate.py", [
    ("        if html.count('data-nav=\"') != 9:\n            issues.append(f\"{name}: 主导航项数 != 9\")",
     "        if html.count('data-nav=\"') != 12:\n            issues.append(f\"{name}: 导航项数 != 12\")"),
    ('FORBIDDEN_EXACT = ["—", "–"]  # em dash / en dash',
     'FORBIDDEN_EXACT = []  # 转载原文保留中文破折号'),
])
patch("tools/shot_check.py", [
    ('         "contact.html", "sitemap.html", "articles.html", "article-lengmen-juexue.html"]',
     '''         "contact.html", "sitemap.html", "articles.html", "counseling.html",
         "article-lengmen-juexue.html", "article-taitoulv.html",
         "article-keyan-xiezuo.html", "article-shebao.html", "article-studio-intro.html"]'''),
])
print("round5 done")
