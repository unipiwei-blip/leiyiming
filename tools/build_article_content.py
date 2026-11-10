# -*- coding: utf-8 -*-
"""从公众号正文提取结果生成 article_content.py，保证原文一字不改。"""
import os
import json

TOOLS = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(TOOLS)
PROJECT = os.path.dirname(SITE)
SRC = os.path.join(PROJECT, "_work", "article", "paragraphs.txt")

paras = [x.strip() for x in open(SRC, encoding="utf-8").read().split("\n\n") if x.strip()]
assert len(paras) == 32, "段落数变化，请复核: %d" % len(paras)

# 原文中承上启下的强调段，用加粗段落突出，不改动文字
HIGHLIGHT = {6, 10, 15, 19, 22, 27}
# 正文配图插入点（在某段之后）
FIGURES = {
    5: ("article-event.jpg", "启动大会现场"),
    9: ("founder-classroom.jpg", "课堂授课现场"),
    21: ("svc-research.jpg", "教学研讨场景"),
}

blocks = []
for i, text in enumerate(paras):
    blocks.append({"t": "h" if i in HIGHLIGHT else "p", "x": text})
    if i in FIGURES:
        src, cap = FIGURES[i]
        blocks.append({"t": "img", "src": src, "cap": cap})

meta = {
    "slug": "article-lengmen-juexue.html",
    "column": "一鸣述评",
    "title": "当AI无所不能，我们为什么还要守护那些“冷门绝学”？",
    "full_title": "一鸣述评｜当AI无所不能，我们为什么还要守护那些“冷门绝学”？",
    "date": "2026年11月10日",
    "date_iso": "2026-11-10",
    "summary": "从教师、学生、社会与教育四个角度，重新思考大学的价值与知识守护的意义。",
    "teaser": "四个角度重看大学价值",
    "cover": "article-cover.jpg",
    "cover_alt": "冷门绝学学院成立仪式现场",
    "tags": ["教育观察", "冷门绝学", "人工智能", "大学价值"],
    "keywords": "一鸣述评,冷门绝学,人工智能,大学教育,雷一鸣工作室,教育观察",
    "desc": "中国社会科学院大学成立冷门绝学学院引发的思考：从教师、学生、社会与教育四个角度，讨论AI时代基础学科与知识传承的价值。",
}

out = (
    "# -*- coding: utf-8 -*-\n"
    '"""「一鸣述评」栏目文章数据；正文源自雷一鸣工作室公众号原文，未作改写。"""\n\n'
    "ARTICLE = " + json.dumps(meta, ensure_ascii=False, indent=4) + "\n\n"
    "ARTICLE['blocks'] = [\n"
    + "".join("    " + json.dumps(b, ensure_ascii=False) + ",\n" for b in blocks)
    + "]\n"
)
path = os.path.join(TOOLS, "article_content.py")
open(path, "w", encoding="utf-8").write(out)
print("write", path, "blocks:", len(blocks), "chars:", len(out))
