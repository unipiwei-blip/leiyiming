# -*- coding: utf-8 -*-
"""第七轮：栏目页首屏精简 + 文章页返回按钮移到正文底部居中。"""
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

# 1) page_hero 支持紧凑样式类
t = once(t, "def page_hero(title, lead, pills=None, crumb=None):",
         'def page_hero(title, lead, pills=None, crumb=None, extra_cls=""):', "hero-signature")
t = once(t, """    return (f'<section class="page-hero"><div class="container">{cr}'""",
         """    cls = f' {extra_cls}' if extra_cls else ''
    return (f'<section class="page-hero{cls}"><div class="container">{cr}'""", "hero-class")

# 2) 栏目页：去面包屑、去 LATEST 小标、压缩留白
t = once(t, '''def page_articles():
    b = page_hero("一鸣述评", ARTICLE_COLUMN["lead"],
                  ARTICLE_COLUMN["tags"], "一鸣述评")
    b += section(sec_head("LATEST / 最新述评", ARTICLE_COLUMN["list_title"],
                          ARTICLE_COLUMN["list_lead"]) + article_cards())
''',
         '''def page_articles():
    b = page_hero("一鸣述评", ARTICLE_COLUMN["lead"],
                  ARTICLE_COLUMN["tags"], extra_cls="hero-compact")
    list_head = (f'<div class="sec-head center reveal"><h2 class="h2">{ARTICLE_COLUMN["list_title"]}</h2>'
                 f'<p class="lead">{ARTICLE_COLUMN["list_lead"]}</p></div>')
    b += section(list_head + article_cards(), "section articles-first")
''', "articles-page")

# 3) 文章页：返回按钮移到正文末尾居中，延伸阅读区收紧
t = once(t, '''    body = (hero
            + section(f'<div class="article-wrap">{cover}<div class="article-body">'
                      + "".join(parts) + '</div></div>', "section article-start")
            + section(sec_head("MORE / 延伸阅读", "与述评相关的工作方向")
                      + f'<div class="grid g3">{rel_cards}</div>'
                      + '<div class="center mt-l"><a class="btn btn-primary" href="articles.html">返回一鸣述评 '
                      + icon("arrow", 16) + '</a></div>'))
''',
         '''    back = ('<div class="article-back center"><a class="btn btn-primary" href="articles.html">返回一鸣述评 '
             + icon("arrow", 16) + '</a></div>')
    body = (hero
            + section(f'<div class="article-wrap">{cover}<div class="article-body">'
                      + "".join(parts) + '</div>' + back + '</div>', "section article-start")
            + section(sec_head("MORE / 延伸阅读", "与述评相关的工作方向")
                      + f'<div class="grid g3">{rel_cards}</div>', "section rel-tight"))
''', "article-body")
write(p, t)

CSS_ADD = '''
/* ================= 第七轮：栏目页首屏精简 / 文章返回按钮 ================= */
.page-hero.hero-compact{padding:46px 0 20px}
.page-hero.hero-compact .pills{margin-top:18px}
.section.articles-first{padding:26px 0 60px}
.section.articles-first .sec-head{margin-bottom:30px}
.article-back{margin-top:34px}
.section.rel-tight{padding:26px 0}
@media(max-width:640px){
  .page-hero.hero-compact{padding:36px 0 16px}
  .section.articles-first{padding:22px 0 44px}
}
'''
p = "assets/css/style.css"
t = read(p)
if "第七轮：栏目页首屏精简" not in t:
    open(os.path.join(ROOT, p), "a", encoding="utf-8").write(CSS_ADD)
    print("appended", p)
else:
    print("skip (already)", p)
print("round7 done")
