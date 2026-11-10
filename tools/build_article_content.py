# -*- coding: utf-8 -*-
"""批量生成 article_content.py：五篇「一鸣述评」栏目文章，正文取自公众号原文。"""
import os
import json

TOOLS = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(TOOLS)
PROJECT = os.path.dirname(SITE)
W1 = os.path.join(PROJECT, "_work", "article")
W4 = os.path.join(PROJECT, "_work", "articles")

META = [
    {
        "paras": os.path.join(W1, "paragraphs.txt"),
        "slug": "article-lengmen-juexue.html",
        "label": "一鸣述评", "date": "2026年11月10日", "date_iso": "2026-11-10",
        "title": "当AI无所不能，我们为什么还要守护那些“冷门绝学”？",
        "card_title": "当AI无所不能，为何守护“冷门绝学”",
        "full_title": "一鸣述评｜当AI无所不能，我们为什么还要守护那些“冷门绝学”？",
        "summary": "从教师、学生、社会与教育四个角度，重新思考大学的价值与知识守护的意义。",
        "teaser": "四个角度重看大学价值",
        "cover": "article-cover.jpg", "cover_alt": "冷门绝学学院成立仪式现场",
        "body_image": "svc-research.jpg", "body_image_cap": "教学研讨场景", "body_image_after": 2,
        "tags": ["教育观察", "冷门绝学", "人工智能", "大学价值"],
        "keywords": "一鸣述评,冷门绝学,人工智能,大学教育,雷一鸣工作室,教育观察",
        "desc": "中国社会科学院大学成立冷门绝学学院引发的思考：从教师、学生、社会与教育四个角度，讨论AI时代基础学科与知识传承的价值。",
        "highlight_idx": [6, 10, 15, 19, 22, 27],
    },
    {
        "paras": os.path.join(W4, "a3_paras.txt"),
        "slug": "article-taitoulv.html",
        "label": "一鸣述评", "date": "2026年11月8日", "date_iso": "2026-11-08",
        "title": "当大学开始统计“抬头率”，智慧教育就有了值得警惕的方向",
        "card_title": "当大学开始统计“抬头率”",
        "full_title": "一鸣述评｜当大学开始统计“抬头率”，智慧教育就有了值得警惕的方向",
        "summary": "从教师、学生与大学治理三个角度，讨论技术进入课堂的边界与教育评价的尺度。",
        "teaser": "技术进入课堂的边界",
        "cover": "cover-taitoulv.jpg", "cover_alt": "教室里被摄像头环绕的学生漫画",
        "body_image": "founder-classroom.jpg", "body_image_cap": "课堂授课现场", "body_image_after": 8,
        "tags": ["教育观察", "智慧教育", "课堂评价", "学生成长"],
        "keywords": "一鸣述评,抬头率,智慧教室,教育评价,雷一鸣工作室",
        "desc": "由高校智慧教室统计抬头率引发的思考：从教师、学生与大学治理角度，讨论教育数字化的边界与评价尺度。",
        "highlight_kw": ["首先：", "其次：", "再次：", "说到底，", "其实我想说的是："],
    },
    {
        "paras": os.path.join(W4, "a2_paras.txt"),
        "slug": "article-keyan-xiezuo.html",
        "label": "一鸣述评", "date": "2026年11月5日", "date_iso": "2026-11-05",
        "title": "从选题到发表：AI时代高校教师如何做好一篇有质量的原创科研论文",
        "card_title": "AI时代如何做好一篇原创科研",
        "full_title": "一鸣述评｜从选题到发表：AI时代高校教师如何做好一篇有质量的原创科研论文",
        "summary": "从选题、破题、题目、摘要、文献综述、创新点到行文，梳理AI时代高校教师的科研写作方法。",
        "teaser": "从选题到行文的科研方法",
        "cover": "svc-research.jpg", "cover_alt": "教学研讨场景",
        "body_image": "svc-lecture.jpg", "body_image_cap": "专题讲座场景", "body_image_after": 12,
        "tags": ["教育观察", "科研写作", "人工智能", "教师发展"],
        "keywords": "一鸣述评,科研论文,选题,文献综述,AI写作,高校教师",
        "desc": "围绕选题、破题、题目、摘要、文献综述、创新点与行文，讨论AI时代高校教师做好原创科研论文的方法与学术责任。",
        "highlight_kw": ["一、", "二、", "三、", "四、", "五、", "六、", "七、", "八、"],
    },
    {
        "paras": os.path.join(W4, "a1_paras.txt"),
        "slug": "article-shebao.html",
        "label": "一鸣述评", "date": "2026年10月14日", "date_iso": "2026-10-14",
        "title": "当社保开始“找人”：比参保率更值得关注的，是普通人的缴费能力",
        "card_title": "比参保率更值得关注缴费能力",
        "full_title": "一鸣述评｜当社保开始“找人”：比参保率更值得关注的，是普通人的缴费能力",
        "summary": "从普通劳动者的收入与生活成本出发，讨论持续缴费能力比参保数字更值得被看见。",
        "teaser": "普通人的缴费能力",
        "cover": "cover-shebao.jpg", "cover_alt": "社会保障主题插画",
        "body_image": "svc-counseling.jpg", "body_image_cap": "线上交流场景", "body_image_after": 5,
        "tags": ["社会观察", "劳动者", "社会保障", "民生"],
        "keywords": "一鸣述评,社保,参保率,灵活就业,缴费能力,雷一鸣工作室",
        "desc": "由社保从人找政策走向政策找人谈起，讨论普通劳动者的持续缴费能力与社会保障制度的现实温度。",
        "highlight_kw": ["更值得我们关注的是", "这也正是我认为", "从这个角度看", "同时，我们也应当看到"],
    },
    {
        "paras": os.path.join(W4, "a4_paras.txt"),
        "slug": "article-studio-intro.html",
        "label": "工作室展示", "date": "2021年7月8日", "date_iso": "2021-07-08",
        "title": "辅导员工作室展示④ | 雷一鸣工作室",
        "card_title": "雷一鸣工作室建设经验展示",
        "full_title": "辅导员工作室展示④ | 雷一鸣工作室",
        "summary": "工作室定位、六大核心素质培养与线上+线下育人模式的系统介绍。",
        "teaser": "工作室定位与育人模式",
        "cover": "cover-zhanshi.jpg", "cover_alt": "主理人在培训现场发言",
        "body_image": "studio-plaque.jpg", "body_image_cap": "工作室书法牌匾", "body_image_after": 8,
        "tags": ["工作室介绍", "辅导员", "六大核心素质", "育人模式"],
        "keywords": "雷一鸣工作室,辅导员工作室,工作室定位,六大核心素质,线上+线下",
        "desc": "雷一鸣工作室的工作定位、平台介绍、六大核心素质培养与线上+线下育人模式，以及运营人专业背景。",
        "highlight_short": 14,
        "drop_kw": ["来源 |", "来源|", "排版 |", "校对 |", "审核 |", "如有侵权"],
        "drop_exact": ["END", "01", "02", "03"],
    },
]


def clean(p):
    return p.strip().replace("**", "")


def is_drop(p, cfg):
    if p in cfg.get("drop_exact", []):
        return True
    return any(k in p for k in cfg.get("drop_kw", []))


def is_h(i, p, cfg):
    if "highlight_idx" in cfg:
        return i in cfg["highlight_idx"]
    if "highlight_kw" in cfg:
        return p.startswith(tuple(cfg["highlight_kw"]))
    if "highlight_short" in cfg:
        return len(p) <= cfg["highlight_short"] and not p.endswith(("。", "！", "？"))
    return False


articles = []
for cfg in META:
    raw = [x.strip() for x in open(cfg["paras"], encoding="utf-8").read().split("\n\n") if x.strip()]
    blocks = []
    for i, p in enumerate(raw):
        if is_drop(p, cfg):
            continue
        s = clean(p)
        if not s:
            continue
        blocks.append({"t": "h" if is_h(i, s, cfg) else "p", "x": s})
        if i == cfg["body_image_after"]:
            blocks.append({"t": "img", "src": cfg["body_image"], "cap": cfg["body_image_cap"]})
    art = {k: v for k, v in cfg.items() if k not in
           ("paras", "highlight_idx", "highlight_kw", "highlight_short", "drop_kw", "drop_exact")}
    art["blocks"] = blocks
    articles.append(art)
    print(cfg["slug"], "原始段", len(raw), "-> blocks", len(blocks),
          "配图", sum(1 for b in blocks if b["t"] == "img"))

out = ("# -*- coding: utf-8 -*-\n"
       '"""「一鸣述评」栏目文章数据；正文取自公众号原文，仅作标点和尾注清理。"""\n\n'
       "ARTICLES = " + json.dumps(articles, ensure_ascii=False, indent=4) + "\n\n"
       "ARTICLE = ARTICLES[0]  # 兼容旧引用\n")
path = os.path.join(TOOLS, "article_content.py")
open(path, "w", encoding="utf-8").write(out)
print("write", path, len(out), "chars")
