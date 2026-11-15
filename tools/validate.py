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
    issues = []
    pages = sorted(p for p in glob.glob(os.path.join(ROOT, "*.html"))
                   if os.path.basename(p) != "404.html")
    # 404 页：独立自包含、故意不含 canonical / noindex / JSON-LD，且不能被收录
    nf = os.path.join(ROOT, "404.html")
    if not os.path.exists(nf):
        issues.append("缺 404.html")
    else:
        f404 = open(nf, encoding="utf-8").read()
        for bad in ("canonical", "404-promo.jpg", "订阅", "meta refresh"):
            if bad in f404:
                issues.append(f"404.html 含 {bad}")
        if 'content="noindex,follow"' not in f404:
            issues.append("404.html 缺 noindex,follow")
        if 'href="/"' not in f404:
            issues.append("404.html 缺首页入口")
    rb = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
    for ua in ("Baiduspider", "Googlebot"):
        if ua not in rb:
            issues.append("robots.txt 缺 " + ua)
    if "Allow: /assets/" not in rb:
        issues.append("robots.txt 未显式允许 /assets/")
    if "Host: www.oals.cn" not in rb:
        issues.append("robots.txt 缺 Host")
    if "Disallow: /404.html" in rb:
        issues.append("robots.txt 不应屏蔽 404.html")
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    if "404.html" in sm:
        issues.append("sitemap.xml 不应包含 404.html")
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

    # 微信分享卡片验收
    from PIL import Image
    detail = [q for q in pages if os.path.basename(q).startswith(("article-", "svc-"))]
    others = [q for q in pages if q not in detail]
    shares = sorted(glob.glob(os.path.join(ROOT, "assets", "img", "share-*.jpg")))
    if len(detail) != len(shares):
        issues.append(f"详情页 {len(detail)} 与方图 {len(shares)} 数量不等")
    for f in shares:
        im = Image.open(f)
        if im.size != (400, 400):
            issues.append(f"{os.path.basename(f)} 尺寸非 400x400")
        if im.format != "JPEG":
            issues.append(f"{os.path.basename(f)} 非 JPEG")
        if im.getexif():
            issues.append(f"{os.path.basename(f)} 含 EXIF")
        if os.path.getsize(f) > 100 * 1024:
            issues.append(f"{os.path.basename(f)} 超过 100KB")
    for q in detail:
        h = open(q, encoding="utf-8").read()
        nm = os.path.basename(q)
        for tag in ('itemprop="name"', 'itemprop="description"', 'itemprop="image"',
                    'og:image:width" content="400"', 'og:image:height" content="400"',
                    'class="wx-share-thumb"', 'twitter:card" content="summary_large_image"'):
            if tag not in h:
                issues.append(f"{nm}: 缺 {tag}")
        got = []
        for pat in (r'property="og:image" content="([^"]+)"',
                    r'itemprop="image" content="([^"]+)"',
                    r'class="wx-share-thumb" src="([^"]+)"'):
            m = re.search(pat, h)
            got.append(m.group(1) if m else "")
        if any(not u.startswith("https://www.oals.cn/assets/img/share-") for u in got):
            issues.append(f"{nm}: 方图 URL 非 HTTPS 绝对地址")
        if len(set(got)) != 1:
            issues.append(f"{nm}: og/itemprop/首图 三处 URL 不一致")
        if 'loading="lazy"' in h.split("wx-share-thumb")[1][:200]:
            issues.append(f"{nm}: 首图使用了 lazy")
    for q in others:
        h = open(q, encoding="utf-8").read()
        if "itemprop=" in h or "wx-share-thumb" in h:
            issues.append(f"{os.path.basename(q)}: 非详情页误带分享标签")
    f404 = os.path.join(ROOT, "404.html")
    if os.path.exists(f404):
        h = open(f404, encoding="utf-8").read()
        if "itemprop=" in h or "wx-share-thumb" in h:
            issues.append("404.html 误带分享标签")

    print(f"检查页面 {len(pages)} 个，问题 {len(issues)} 条")
    for x in issues:
        print("  -", x)
    return len(issues)


if __name__ == "__main__":
    raise SystemExit(0 if main() == 0 else 1)
