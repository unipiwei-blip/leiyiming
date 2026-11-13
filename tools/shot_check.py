# -*- coding: utf-8 -*-
"""浏览器实测：响应式溢出、页脚高度、单行描述、居中、控制台错误 + 预览截图。"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(ROOT)
OUT = os.path.join(PROJECT, "_work", "preview")
os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PAGES = ["index.html", "about.html", "services.html", "svc-quality.html",
         "svc-practice.html", "svc-thought.html", "svc-lecture.html",
         "svc-counseling.html", "svc-research.html", "founder.html",
         "contact.html", "sitemap.html", "articles.html", "counseling.html",
         "article-lengmen-juexue.html", "article-taitoulv.html",
         "article-keyan-xiezuo.html", "article-shebao.html", "article-studio-intro.html",
         "article-bansheng-guitu.html"]


def url(name):
    return "file:///" + os.path.join(ROOT, name).replace("\\", "/")


def main():
    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=EDGE, headless=True,
                                    args=["--no-sandbox", "--disable-gpu"])
        for width in (1440, 768, 390):
            for name in PAGES:
                page = browser.new_page(viewport={"width": width, "height": 900})
                errs = []
                page.on("pageerror", lambda e: errs.append(str(e)))
                page.goto(url(name), wait_until="load")
                page.wait_for_timeout(220)
                overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
                if overflow:
                    problems.append(f"{width}px {name}: 横向溢出")
                if errs:
                    problems.append(f"{width}px {name}: JS 错误 {errs[:1]}")
                if width == 1440 and name != "sitemap.html":
                    active = page.locator(".nav-menu a.active").count()
                    if active != 1:
                        problems.append(f"{name}: 导航高亮数 = {active}")
                page.close()
            print("responsive checked:", width)

        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url("index.html"), wait_until="load")
        page.wait_for_timeout(900)
        page.screenshot(path=os.path.join(OUT, "01-home-top.png"))
        h = page.evaluate("document.body.scrollHeight")
        for ratio, label in [(0.18, "02-home-mid"), (0.42, "03-home-services"),
                             (0.68, "04-home-moments")]:
            page.evaluate("window.scrollTo(0, %d)" % int(h * ratio))
            page.wait_for_timeout(650)
            page.screenshot(path=os.path.join(OUT, label + ".png"))
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(650)
        page.screenshot(path=os.path.join(OUT, "05-home-footer.png"))

        metrics = page.evaluate("""() => {
          const f = document.querySelector('.footer');
          const ft = document.querySelector('.footer-top');
          const cards = [...document.querySelectorAll('.one-line')];
          const lines = cards.map(el => Math.round(el.scrollHeight / parseFloat(getComputedStyle(el).lineHeight)));
          const grid = getComputedStyle(document.querySelector('.biz-grid')).gridTemplateColumns;
          return {
            footerHeight: Math.round(f.getBoundingClientRect().height),
            footerCols: getComputedStyle(ft).gridTemplateColumns,
            footerTextAlign: getComputedStyle(ft.children[0]).textAlign,
            cardTextAlign: getComputedStyle(document.querySelector('.card')).textAlign,
            oneLineCount: cards.length,
            maxLines: Math.max(...lines),
            bizGrid: grid,
            qrRatios: [...document.querySelectorAll('.footer img[src*="qrcode"]')].map(el => {
              const r = el.getBoundingClientRect(); return +(r.width / r.height).toFixed(2);
            }),
            heroTrustIcons: document.querySelectorAll('.hero-trust svg').length
          };
        }""")
        print("metrics:", metrics)
        if metrics["footerHeight"] > 380:
            problems.append(f"页脚高度 {metrics['footerHeight']}px > 380px")
        if metrics["maxLines"] > 1:
            problems.append("存在换行的一行描述")
        if metrics["footerTextAlign"] != "center" or metrics["cardTextAlign"] != "center":
            problems.append("居中排版未生效")
        if metrics["heroTrustIcons"] > 0:
            problems.append("Hero 信任条含图标")
        if any(abs(r - 1) > 0.02 for r in metrics["qrRatios"]):
            problems.append(f"二维码非正方形 {metrics['qrRatios']}")
        if len(metrics["qrRatios"]) != 2:
            problems.append(f"页脚二维码数量 {len(metrics['qrRatios'])}")

        for name, label in [("svc-quality.html", "06-detail-top"),
                            ("founder.html", "07-founder-top"),
                            ("contact.html", "08-contact-top")]:
            page.goto(url(name), wait_until="load")
            page.wait_for_timeout(700)
            page.screenshot(path=os.path.join(OUT, label + ".png"))
        page.close()

        m = browser.new_page(viewport={"width": 390, "height": 844})
        m.goto(url("index.html"), wait_until="load")
        m.wait_for_timeout(700)
        m.screenshot(path=os.path.join(OUT, "09-mobile-top.png"))
        brand_gap = m.evaluate("""() => {
          const br = document.querySelector('.footer .brand');
          const a = br.querySelector('img').getBoundingClientRect();
          const b = br.querySelector('.brand-txt').getBoundingClientRect();
          return Math.round(b.left - a.right);
        }""")
        print("mobile brand gap:", brand_gap)
        if brand_gap > 24:
            problems.append(f"手机端页脚品牌栏间距异常 {brand_gap}px")
        m.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        m.wait_for_timeout(600)
        m.screenshot(path=os.path.join(OUT, "10-mobile-footer.png"))
        m.close()
        browser.close()

    print("问题数:", len(problems))
    for x in problems:
        print("  -", x)
    print("截图目录:", OUT)
    return len(problems)


if __name__ == "__main__":
    raise SystemExit(0 if main() == 0 else 1)
