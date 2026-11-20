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
        "paras": os.path.join(W4, "a7_paras.txt"),
        "slug": "article-xinli-zixun.html",
        "label": "心理成长", "date": "2026年11月20日", "date_iso": "2026-11-20",
        "title": "大学生心理咨询怎么做？从求助时机到咨询方式的完整指引",
        "card_title": "大学生心理咨询完整指引",
        "full_title": "大学生心理咨询怎么做？从求助时机到咨询方式的完整指引",
        "summary": "从求助信号、咨询设置到线上与线下的选择，梳理大学生使用心理咨询服务时需要了解的常见问题。",
        "teaser": "从求助时机到方式选择",
        "cover": "svc-counseling.jpg", "cover_alt": "线上交流与书卷主题插画",
        "tags": ["心理咨询", "大学生成长", "情绪适应", "咨询方式"],
        "keywords": "大学生心理咨询,心理咨询怎么做,高校心理咨询,心理求助,线上咨询,雷一鸣工作室",
        "desc": "雷一鸣工作室心理成长文章：梳理大学生何时值得寻求心理咨询、首次咨询如何准备，以及线上与线下咨询方式如何选择。",
        "highlight_kw": ["一、什么时候值得寻求专业帮助", "二、高校心理咨询与社会机构咨询有什么不同",
                         "三、第一次咨询前，可以做哪些准备", "四、线上还是线下，怎么选",
                         "五、几个常见问题"],
        "see_also": [("心理咨询栏目", "counseling.html"),
                     ("个性化成长辅导", "svc-counseling.html"),
                     ("情感支持与联系", "contact.html")],
    },
    {
        "paras": os.path.join(W4, "a8_paras.txt"),
        "slug": "article-gongzuoshi-jianshe.html",
        "label": "育人实践", "date": "2026年11月20日", "date_iso": "2026-11-20",
        "title": "高校辅导员工作室建设路径：从定位到育人实践的完整方法",
        "card_title": "辅导员工作室建设路径",
        "full_title": "高校辅导员工作室建设路径：从定位到育人实践的完整方法",
        "summary": "围绕定位、运行机制、核心素质培养与线上线下协同，梳理高校辅导员工作室可复制的建设方法。",
        "teaser": "从定位到运行的建设方法",
        "cover": "svc-research.jpg", "cover_alt": "团队围桌研讨场景插画",
        "tags": ["辅导员工作室", "思政教育", "六大核心素质", "育人实践"],
        "keywords": "辅导员工作室建设,高校辅导员工作室,思政教育创新,六大核心素质,育人实践,雷一鸣工作室",
        "desc": "雷一鸣工作室育人实践文章：从定位、团队机制、六大核心素质培养到线上线下协同，梳理辅导员工作室的建设路径与常见误区。",
        "highlight_kw": ["一、先明确工作室解决什么问题", "二、团队构成与运行机制",
                         "三、六大核心素质培养框架怎么落地", "四、线上与线下协同的育人模式",
                         "五、常见误区与可复制的做法"],
        "see_also": [("工作室简介", "about.html"),
                     ("服务体系", "services.html"),
                     ("六大核心素质", "svc-quality.html"),
                     ("工作室建设经验展示", "article-studio-intro.html")],
    },
    {
        "paras": os.path.join(W4, "a6_paras.txt"),
        "slug": "article-hejie.html",
        "label": "一鸣述评", "date": "2026年11月15日", "date_iso": "2026-11-15",
        "title": "与自己和解，不是向生活认输",
        "card_title": "与自己和解，不是向生活认输",
        "full_title": "一鸣述评｜与自己和解，不是向生活认输",
        "summary": "从中年的回望出发，谈努力与结果、被外界定义的困境，以及看清生活之后依然认真生活。",
        "teaser": "看清生活之后，依然好好生活",
        "cover": "cover-hejie.jpg", "cover_alt": "中年男子与镜中的自己相望的漫画",
        "tags": ["人生随笔", "中年思考", "自我接纳", "教育人生"],
        "keywords": "一鸣述评,与自己和解,中年,自我接纳,孔乙己的长衫,雷一鸣工作室",
        "desc": "雷一鸣工作室一鸣述评：从中年回望出发，谈努力与结果、被外界定义的困境，以及看清生活之后接纳自己、继续认真生活。",
        "highlight_kw": ["仿佛每个人都在向前奔跑", "有时候，我们不是不懂道理",
                         "可人生真的需要这样吗？", "接纳自己的普通",
                         "人到中年，最大的成长", "与自己和解，不是向生活认输"],
    },
    {
        "paras": os.path.join(W4, "a5_paras.txt"),
        "slug": "article-bansheng-guitu.html",
        "label": "特刊", "date": "2026年11月13日", "date_iso": "2026-11-13",
        "title": "四十四岁，人生二州一城，半生归途",
        "card_title": "四十四岁，人生二州一城",
        "full_title": "特刊｜四十四岁，人生二州一城，半生归途",
        "summary": "从江州、洪州到莞城，回望四十四年走过的路，也写下对教育与生活的新理解。",
        "teaser": "三个地方，三段人生",
        "cover": "cover-guitu.jpg", "cover_alt": "通往城市天际线的道路插画",
        "tags": ["人生随笔", "教育人生", "江州洪州莞城", "半生归途"],
        "keywords": "雷一鸣,四十四岁,江州,洪州,莞城,半生归途,雷一鸣工作室,特刊",
        "desc": "雷一鸣工作室特刊：四十四岁生日之际，从故乡江州、求学洪州到谋生莞城，回望二十年教育生涯与半生归途。",
        "highlight_kw": ["四十四岁了。", "不知不觉，半生已过。", "江州，是我出生和成长的地方。",
                         "洪州，是我求学的地方。", "莞城，是我谋生的地方。",
                         "三个地方，三段人生。", "江州是来处，洪州是青春，莞城是当下。",
                         "半生已过，归途尚远。"],
    },
    {
        "paras": os.path.join(W1, "paragraphs.txt"),
        "slug": "article-lengmen-juexue.html",
        "label": "一鸣述评", "date": "2026年11月10日", "date_iso": "2026-11-10",
        "title": "当AI无所不能，我们为什么还要守护那些“冷门绝学”？",
        "card_title": "当AI无所不能，为何守护“冷门绝学”",
        "full_title": "一鸣述评｜当AI无所不能，我们为什么还要守护那些“冷门绝学”？",
        "summary": "从教师、学生、社会与教育四个角度，重新思考大学的价值与知识守护的意义。",
        "teaser": "四个角度重看大学价值",
        "cover": "svc-research.jpg", "cover_alt": "教学研讨场景",
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
        "cover": "svc-lecture.jpg", "cover_alt": "专题讲座场景",
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
        "cover": "svc-practice.jpg", "cover_alt": "团队协作实践场景",
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
    art = {k: v for k, v in cfg.items() if k not in
           ("paras", "highlight_idx", "highlight_kw", "highlight_short", "drop_kw", "drop_exact",
            "body_image", "body_image_cap", "body_image_after")}
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
