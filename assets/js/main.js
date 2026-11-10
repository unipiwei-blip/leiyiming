/* 极站 GOSITE · 交互脚本（纯静态、无依赖） */
(function () {
  'use strict';

  var nav = document.querySelector('.nav');
  var btn = document.querySelector('.menu-btn');
  var menu = document.querySelector('.nav-menu');

  /* 导航滚动阴影 */
  function onScroll() {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* 移动端菜单 */
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        menu.classList.remove('open');
        btn.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('click', function (e) {
      if (!menu.contains(e.target) && !btn.contains(e.target)) {
        menu.classList.remove('open');
        btn.classList.remove('open');
      }
    });
  }

  /* 当前栏目高亮 */
  var page = document.body.getAttribute('data-page');
  if (page && menu) {
    menu.querySelectorAll('a').forEach(function (a) {
      if (a.getAttribute('data-nav') === page) a.classList.add('active');
    });
  }

  /* 滚动入场 */
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  /* 页脚年份 */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();

/* 一鸣述评列表翻页（纯静态，无后端） */
(function () {
  'use strict';
  var cards = [].slice.call(document.querySelectorAll('.article-card[data-page]'));
  if (!cards.length) return;
  var btns = [].slice.call(document.querySelectorAll('.pager [data-go]'));
  var total = 0;
  cards.forEach(function (c) { total = Math.max(total, parseInt(c.getAttribute('data-page'), 10) || 1); });
  var cur = 1;
  function show(n) {
    cur = Math.max(1, Math.min(n, total));
    cards.forEach(function (c) { c.hidden = (parseInt(c.getAttribute('data-page'), 10) !== cur); });
    btns.forEach(function (b) {
      var g = b.getAttribute('data-go');
      if (g === 'prev') b.disabled = (cur === 1);
      else if (g === 'next') b.disabled = (cur === total);
      else b.classList.toggle('active', parseInt(g, 10) === cur);
    });
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var g = b.getAttribute('data-go');
      show(g === 'prev' ? cur - 1 : g === 'next' ? cur + 1 : parseInt(g, 10));
    });
  });
  show(1);
})();
