# -*- coding: utf-8 -*-
"""静态自检：内链 / 图片 / 禁词 / 结构 / 文案长度。"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD = [
    "每项都有专页", "各有专页", "独立成页", "进入详情页", "点击任意卡片", "点击卡片",
    "本页", "本站", "本栏目", "按需进入", "写清能做什么", "一句话讲清", "逐项展开",
    "上线前", "匿名化示例", "占位说明", "反直觉", "值得注意的是", "订阅", "资讯推送",
    "example.com", "粤ICP备 00000000", "进入板块", "专页", "示意", "点击查看",
    "本组", "同组", "中文转载", "本次检索", "未核到",
]
FORBIDDEN_EXACT = []  # 转载原文保留中文破折号


def main():
    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    issues = []
    for p in pages:
        name = os.path.basename(p)
        html = open(p, encoding="utf-8").read()

        for m in re.findall(r'(?:href|src)="([^"]+)"', html):
            if m.startswith(("http", "#", "mailto:", "data:")):
                continue
            target = m.split("#")[0].split("?")[0]
            if not target:
                continue
            if not os.path.exists(os.path.join(ROOT, target)):
                issues.append(f"{name}: 缺失资源 {m}")

        for w in BAD:
            if w in html:
                issues.append(f"{name}: 禁词「{w}」")
        for w in FORBIDDEN_EXACT:
            if w in html:
                issues.append(f"{name}: 禁用符号「{w}」")

        h1 = len(re.findall(r"<h1[\s>]", html))
        if h1 != 1:
            issues.append(f"{name}: h1 数量 = {h1}")

        if html.count('class="footer-top"') != 1:
            issues.append(f"{name}: 页脚结构异常")
        if 'class="biz-grid"' not in html:
            issues.append(f"{name}: 页脚重点业务双列缺失")
        for t in ("广东省湖南攸县商会", "才猎天下大数据", "湾区（广东）数字经济研究院"):
            if t not in html:
                issues.append(f"{name}: 友情链接缺「{t}」")
        if html.count('data-nav="') != 10:
            issues.append(f"{name}: 导航项数 != 10")
        for q in ("qrcode-consult.png", "qrcode-official.png"):
            if q not in html:
                issues.append(f"{name}: 页脚缺二维码 {q}")
        if 'canonical" href="https://www.oals.cn/' not in html:
            issues.append(f"{name}: canonical 未绑定 www.oals.cn")
        for tag in ('rel="canonical"', 'property="og:image"', 'name="twitter:card"',
                    '"BreadcrumbList"', '"WebSite"', '"Organization"'):
            if tag not in html:
                issues.append(f"{name}: SEO 缺 {tag}")

        for txt in re.findall(r'<p class="one-line">(.*?)</p>', html, re.S):
            plain = re.sub(r"<[^>]+>", "", txt).strip()
            if len(plain) > 16:
                issues.append(f"{name}: 卡片描述超 16 字（{len(plain)}）「{plain}」")

        # 页脚不得出现「首页」导航项
        foot = html.split('<footer class="footer"')[-1]
        if ">首页</a>" in foot:
            issues.append(f"{name}: 页脚导航含首页")

    xml = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    for h in pages:
        nm = os.path.basename(h)
        if nm == "index.html":
            if "https://www.oals.cn/<" not in xml:
                issues.append("sitemap.xml 缺首页")
        elif "/" + nm + "<" not in xml:
            issues.append(f"sitemap.xml 缺 {nm}")

    print(f"检查页面 {len(pages)} 个，问题 {len(issues)} 条")
    for x in issues:
        print("  -", x)
    return len(issues)


if __name__ == "__main__":
    raise SystemExit(0 if main() == 0 else 1)
