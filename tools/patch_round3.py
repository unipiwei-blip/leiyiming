# -*- coding: utf-8 -*-
"""第三轮：加入工作室牌匾与主理人课堂授课两张实景照片。"""
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


patch("tools/build_site.py", [
    ('    b += section(split_text_image(founder_html, "founder-lecture.jpg", "课堂与培训现场"))',
     '    b += section(split_text_image(founder_html, "founder-classroom.jpg", "主理人课堂授课现场"))'),
    ('''    cases = [
        case_card("svc-lecture.jpg", "专题讲座场景", "讲座交流", "面对面的交流",
                  "讲者与学生面对面交流", ["视野拓展", "双向交流", "思维训练"],
                  "svc-lecture.html"),
        case_card("activity-training.jpg", "辅导员培训交流", "实践育人", "同行研讨中的经验沉淀",
                  "在同行研讨中沉淀方法", ["同行交流", "实践体验", "经验分享"],
                  "svc-practice.html"),
        case_card("founder-lecture.jpg", "课堂与培训现场", "育人一线", "扎根日常的陪伴",
                  "扎根课堂与日常交流", ["价值引领", "日常关照", "持续陪伴"],
                  "svc-thought.html"),
    ]
    b += section(sec_head("MOMENTS / 育人影像", "在真实的相处中看见成长",
                          "讲座、培训、班会与日常交流，构成工作室育人工作的具体场景。")
                 + f'<div class="grid g3">{"".join(cases)}</div>')''',
     '''    cases = [
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
                 + f'<div class="grid g3">{"".join(cases)}</div>')'''),
    ('    b += section(split_text_image(intro, "svc-counseling.jpg", "线上辅导与内容分享场景"))',
     '    b += section(split_text_image(intro, "studio-plaque.jpg", "雷一鸣工作室牌匾"))'),
    ('''                f'<img src="assets/img/founder-lecture.jpg" alt="课堂与培训现场" loading="lazy">'
                f'<p class="mt-s">课堂与培训现场</p></div></div>')''',
     '''                f'<img src="assets/img/founder-classroom.jpg" alt="主理人课堂授课现场" loading="lazy">'
                f'<p class="mt-s">课堂授课现场</p></div></div>')'''),
    ('    b += section(split_text_image(text, "founder-lecture.jpg", "课堂与培训现场"))',
     '    b += section(split_text_image(text, "founder-classroom.jpg", "主理人课堂授课现场"))'),
])

CSS_ADD = '''
/* ================= 第三轮：工作室实景照片裁切 ================= */
.case-shot img[src*="studio-plaque"]{object-position:center 70%}
.split .visual.pic img[src*="studio-plaque"]{object-position:center 72%}
'''
css = os.path.join(ROOT, "assets", "css", "style.css")
t = open(css, encoding="utf-8").read()
if "第三轮：工作室实景照片裁切" not in t:
    open(css, "a", encoding="utf-8").write(CSS_ADD)
    print("patched assets/css/style.css")
else:
    print("CSS 已打过补丁，跳过")
