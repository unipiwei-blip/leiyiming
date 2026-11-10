# -*- coding: utf-8 -*-
"""第四轮：新增「一鸣述评」栏目、文章详情页与首页最新观点模块。"""
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


def append_once(rel, marker, text):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    if marker not in t:
        open(p, "a", encoding="utf-8").write(text)
        print("appended", rel)
    else:
        print("skip (already)", rel)


# ---------------------------------------------------------------- 数据
append_once("tools/site_content.py", "ARTICLE_COLUMN = {", '''

# 「一鸣述评」栏目
ARTICLE_COLUMN = {
    "lead": "围绕大学教育、青年成长与时代变化的观察与思考。",
    "tags": ["教育观察", "成长思考", "学术评论"],
    "list_title": "把对教育的思考写下来",
    "list_lead": "从一所大学、一个专业、一次变化出发，讨论那些值得被认真对待的问题。",
    "topics_title": "常被谈起的三类问题",
    "desc": "一鸣述评是雷一鸣工作室的观点栏目，围绕大学教育、青年成长与学术积累展开观察与思考。",
}

ARTICLE_DIRECTIONS = [
    ("cap", "大学价值", "基础学科与人才培养"),
    ("users", "青年成长", "专业选择与成长路径"),
    ("book", "学术积累", "知识传承与时代变化"),
]
''')

patch("tools/site_content.py", [
    ('    ("教研探索", "svc-research.html", "svc-research"),\n    ("主理人", "founder.html", "founder"),',
     '    ("教研探索", "svc-research.html", "svc-research"),\n    ("一鸣述评", "articles.html", "articles"),\n    ("主理人", "founder.html", "founder"),'),
])

# ---------------------------------------------------------------- 生成器
NEW_FUNCS = r"""def article_teaser():
    a = ARTICLE
    return f'''<article class="article-teaser glass reveal">
<img src="assets/img/{a["cover"]}" alt="{a["cover_alt"]}" loading="lazy">
<div class="teaser-copy">
<span class="pill">{a["column"]} · {a["date"]}</span>
<h3 class="h3">{a["title"]}</h3>
<p class="one-line">{a["teaser"]}</p>
<div class="mt-m"><a class="btn btn-primary" href="{a["slug"]}">阅读述评 {icon("arrow", 16)}</a>
<a class="btn btn-ghost" href="articles.html">述评栏目</a></div>
</div></article>'''


def page_articles():
    b = page_hero("一鸣述评", ARTICLE_COLUMN["lead"],
                  ARTICLE_COLUMN["tags"], "一鸣述评")
    b += section(sec_head("LATEST / 最新述评", ARTICLE_COLUMN["list_title"],
                          ARTICLE_COLUMN["list_lead"]) + article_teaser())
    cards = "".join(simple_card(i, t, d, ["", "pink", "cyan"][k])
                    for k, (i, t, d) in enumerate(ARTICLE_DIRECTIONS))
    b += section(sec_head("TOPICS / 述评方向", ARTICLE_COLUMN["topics_title"])
                 + f'<div class="grid g3">{cards}</div>')
    b += cta("围绕教育话题继续交流", "关于大学教育、青年成长与学术积累的话题，欢迎进一步沟通。",
             [("交流合作", "contact.html", "btn-white"), ("返回首页", "index.html", "btn-outline")])
    return shell("articles.html", "一鸣述评", ARTICLE_COLUMN["desc"],
                 "一鸣述评,教育观察,雷一鸣工作室,冷门绝学", b, "articles")


def page_article():
    a = ARTICLE
    tags = "".join(f'<span class="pill">{t}</span>' for t in a["tags"])
    hero = f'''<section class="article-hero"><div class="container">
<div class="crumb"><a href="index.html">{BRAND}</a> / <a href="articles.html">{a["column"]}</a> / 最新述评</div>
<span class="pill">{a["column"]}</span>
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


"""

patch("tools/build_site.py", [
    ("    FEATURES, DIRECTIONS, FLOW, SERVICES, FAQ, FOUNDER,\n)",
     "    FEATURES, DIRECTIONS, FLOW, SERVICES, FAQ, FOUNDER, ARTICLE_COLUMN, ARTICLE_DIRECTIONS,\n)\nfrom article_content import ARTICLE  # noqa: E402"),
    ('''    if key in ("svc-thought", "svc-lecture", "svc-counseling"):
        key = "services"''',
     '''    if key in ("svc-thought", "svc-lecture", "svc-counseling"):
        key = "services"
    if key.startswith("article-"):
        key = "articles"'''),
    ("def page_index():", NEW_FUNCS + "def page_index():"),
    ('    b += cta("一起把育人工作做深做实",',
     '''    b += section(sec_head("PERSPECTIVES / 一鸣述评", "把对教育的思考写下来",
                          "围绕大学教育、青年成长与时代变化的观察与思考。")
                 + article_teaser())
    b += cta("一起把育人工作做深做实",'''),
    ('''        group("更多信息", "link", [("工作室简介", "about.html"), ("主理人", "founder.html"),
                                  ("联系我们", "contact.html"), ("网站地图", "sitemap.html")]),''',
     '''        group("更多信息", "link", [("工作室简介", "about.html"), ("主理人", "founder.html"),
                                  ("联系我们", "contact.html"), ("网站地图", "sitemap.html"),
                                  ("一鸣述评", "articles.html"), ("最新述评 · 冷门绝学", ARTICLE["slug"])]),'''),
    ('''    write("sitemap.html", page_sitemap())
    for s in SERVICES:''',
     '''    write("sitemap.html", page_sitemap())
    write("articles.html", page_articles())
    write(ARTICLE["slug"], page_article())
    for s in SERVICES:'''),
    ('''    pages = ["index.html"] + [x[1] for x in NAV[1:]] + [s["slug"] + ".html" for s in SERVICES] + ["sitemap.html"]''',
     '''    pages = (["index.html"] + [x[1] for x in NAV[1:]] + [s["slug"] + ".html" for s in SERVICES]
             + ["sitemap.html", ARTICLE["slug"]])'''),
])

# ---------------------------------------------------------------- 样式
CSS_ADD = '''
/* ================= 第四轮：一鸣述评栏目 ================= */
.nav-menu a{padding:9px 10px;font-size:13.5px}
.nav .container{gap:18px}
@media(min-width:901px) and (max-width:1100px){.nav-menu a{padding:9px 7px;font-size:12.5px}.nav .container{gap:12px}}
.article-teaser{display:grid;grid-template-columns:1fr 1fr;max-width:1000px;margin:0 auto;overflow:hidden;border-radius:var(--r);padding:0}
.article-teaser>img{width:100%;height:100%;min-height:290px;object-fit:cover;display:block;margin:0}
.teaser-copy{padding:34px 36px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.teaser-copy h3{font-size:clamp(19px,2vw,25px);font-weight:900;line-height:1.5;margin-top:14px;color:var(--ink)}
.teaser-copy p{margin-top:10px;color:var(--muted);font-size:14px}
.teaser-copy .mt-m{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.article-hero{position:relative;overflow:hidden;padding:64px 0 48px;text-align:center}
.article-hero::before{content:"";position:absolute;left:50%;top:-190px;transform:translateX(-50%);width:820px;height:430px;background:radial-gradient(ellipse,rgba(26,107,255,.18),transparent 68%);filter:blur(18px)}
.article-hero .container{position:relative;z-index:1}
.article-hero h1{font-size:clamp(26px,3.1vw,40px);font-weight:900;line-height:1.4;letter-spacing:-.02em;max-width:900px;margin:18px auto 0;color:var(--ink)}
.article-meta{font-size:13px;color:var(--muted);font-weight:700;margin-top:18px}
.article-lead{font-size:15.5px;color:var(--muted);line-height:1.9;max-width:760px;margin:16px auto 0}
.article-wrap{max-width:880px;margin:0 auto}
.article-body p{font-size:16px;line-height:2.15;color:var(--ink-2);margin:0 auto 22px;text-align:center;max-width:820px}
.article-body p.article-h{font-size:18px;font-weight:900;color:var(--blue-deep);line-height:1.9;margin:38px auto 22px;padding:0 18px}
.article-figure{margin:34px auto;text-align:center;max-width:820px}
.article-figure img{width:100%;max-width:760px;border-radius:18px;border:1px solid rgba(255,255,255,.9);box-shadow:var(--shadow);display:block;margin:0 auto}
.article-figure figcaption{font-size:12.5px;color:var(--muted);margin-top:11px}
@media(max-width:900px){.article-teaser{grid-template-columns:1fr}.article-teaser>img{height:220px;min-height:0}.teaser-copy{padding:26px}}
'''
append_once("assets/css/style.css", "第四轮：一鸣述评栏目", CSS_ADD)

# ---------------------------------------------------------------- 校验脚本
patch("tools/validate.py", [
    ("        if html.count('data-nav=\"') != 8:\n            issues.append(f\"{name}: 主导航项数 != 8\")",
     "        if html.count('data-nav=\"') != 9:\n            issues.append(f\"{name}: 主导航项数 != 9\")"),
])
patch("tools/shot_check.py", [
    ('         "contact.html", "sitemap.html"]',
     '         "contact.html", "sitemap.html", "articles.html", "article-lengmen-juexue.html"]'),
])
print("round4 done")
