/* Horses of Florence · proposta «natura»: movimenti lenti legati allo scroll. Nessuna dipendenza. */
(function () {
  'use strict';

  var doc = document;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var vh = window.innerHeight;
  window.addEventListener('resize', function () { vh = window.innerHeight; });

  /* Parallasse delle colline all'alba */
  var dawn = doc.querySelector('.dawn');
  var layers = doc.querySelectorAll('.dawn [data-depth]');

  /* Sentiero del viaggio e staccionata che si disegnano scorrendo */
  var drawn = [
    { box: doc.querySelector('.journey__track'), el: doc.querySelector('.journey__ink'), start: .85, end: .35 },
    { box: doc.querySelector('.fence'), el: doc.querySelector('.fence'), start: 1, end: .55 }
  ].filter(function (d) { return d.box && d.el; });

  function progress(box, start, end) {
    // 0 quando la parte alta arriva a «start» della finestra, 1 quando la parte bassa arriva a «end»
    var r = box.getBoundingClientRect();
    var total = r.height + vh * (start - end);
    return Math.max(0, Math.min(1, (vh * start - r.top) / total));
  }

  var ticking = false;
  function update() {
    ticking = false;
    var y = window.scrollY;
    if (dawn && y < dawn.offsetHeight) {
      layers.forEach(function (l) {
        l.style.transform = 'translate3d(0,' + (y * parseFloat(l.getAttribute('data-depth'))).toFixed(1) + 'px,0)';
      });
    }
    drawn.forEach(function (d) {
      d.el.style.setProperty('--draw', (1 - progress(d.box, d.start, d.end)).toFixed(4));
    });
  }
  function onScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }
  if (!reduce) {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }

  /* Il ritmo della giornata: alba, mattino, mezzogiorno, pomeriggio, tramonto, notte */
  var phases = doc.querySelector('.phases');
  if (phases && 'IntersectionObserver' in window) {
    var items = phases.querySelectorAll('li');
    var sections = doc.querySelectorAll('[data-phase-section]');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var i = +entry.target.getAttribute('data-phase-section');
        items.forEach(function (li, k) { li.classList.toggle('is-current', k === i); });
        phases.classList.toggle('is-dark', i >= 4 && !entry.target.classList.contains('dusk'));
      });
    }, { rootMargin: '-50% 0px -50% 0px' });
    sections.forEach(function (s) { io.observe(s); });
  }

  /* Mappa: le esperienze accendono i luoghi */
  var map = doc.querySelector('[data-map]');
  var buttons = doc.querySelectorAll('.xp-item[data-spot]');
  if (map && buttons.length) {
    var pinned = null;
    var show = function (spot) {
      map.classList.toggle('has-active', !!spot);
      map.querySelectorAll('[data-spot]').forEach(function (g) {
        g.classList.toggle('is-active', g.getAttribute('data-spot') === spot);
      });
    };
    buttons.forEach(function (b) {
      var spot = b.getAttribute('data-spot');
      b.addEventListener('mouseenter', function () { show(spot); });
      b.addEventListener('mouseleave', function () { show(pinned); });
      b.addEventListener('focus', function () { show(spot); });
      b.addEventListener('blur', function () { show(pinned); });
      b.addEventListener('click', function () {
        pinned = pinned === spot ? null : spot;
        buttons.forEach(function (o) { o.setAttribute('aria-pressed', String(o.getAttribute('data-spot') === pinned)); });
        show(pinned);
      });
    });
  }
})();
