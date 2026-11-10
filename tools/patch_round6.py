# -*- coding: utf-8 -*-
"""第六轮：文章页头部精简 + 全文统一只保留开头一张插画。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


def write(rel, t):
    open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(t)
    print("patched", rel)


def once(t, old, new, tag):
    n = t.count(old)
    assert n == 1, "%s 命中 %d 次: %r" % (tag, n, old[:60])
    return t.replace(old, new, 1)


# ---------------------------------------------------------------- 文章数据
p = "tools/build_article_content.py"
t = read(p)
# 顺序敏感：先把第 3 篇原有 svc-research 换走，再把第 1 篇改为 svc-research
t = once(t, '"cover": "svc-research.jpg", "cover_alt": "教学研讨场景",',
         '"cover": "svc-lecture.jpg", "cover_alt": "专题讲座场景",', "cover3")
t = once(t, '"cover": "article-cover.jpg", "cover_alt": "冷门绝学学院成立仪式现场",',
         '"cover": "svc-research.jpg", "cover_alt": "教学研讨场景",', "cover1")
t = once(t, '"cover": "cover-zhanshi.jpg", "cover_alt": "主理人在培训现场发言",',
         '"cover": "svc-practice.jpg", "cover_alt": "团队协作实践场景",', "cover5")
# 正文不再插图
t = once(t, '''        if i == cfg["body_image_after"]:
            blocks.append({"t": "img", "src": cfg["body_image"], "cap": cfg["body_image_cap"]})
''', '', "drop-body-image")
t = once(t, '''           ("paras", "highlight_idx", "highlight_kw", "highlight_short", "drop_kw", "drop_exact")}''',
         '''           ("paras", "highlight_idx", "highlight_kw", "highlight_short", "drop_kw", "drop_exact",
            "body_image", "body_image_cap", "body_image_after")}''', "drop-fields")
write(p, t)

# ---------------------------------------------------------------- 文章页模板
p = "tools/build_site.py"
t = read(p)
t = once(t, '<span class="pill">{a["label"]}</span>\n', '', "pill")
t = once(t, '<p class="article-meta">{BRAND} · {a["date"]}</p>',
         '<p class="article-meta">{a["date"]}</p>', "meta")
t = once(t, '''+ "".join(parts) + '</div></div>', "section tight")''',
         '''+ "".join(parts) + '</div></div>', "section article-start")''', "section-class")
write(p, t)

# ---------------------------------------------------------------- 样式
CSS_ADD = '''
/* ================= 第六轮：文章页头部精简 ================= */
.article-hero{padding:34px 0 14px}
.article-hero .crumb{text-align:left}
.article-start{padding:18px 0}
.article-start .article-figure:first-child{margin-top:0}
.article-figure{margin:26px auto}
'''
p = "assets/css/style.css"
t = read(p)
if "第六轮：文章页头部精简" not in t:
    open(os.path.join(ROOT, p), "a", encoding="utf-8").write(CSS_ADD)
    print("appended", p)
else:
    print("skip (already)", p)
print("round6 done")
