/* Horses of Florence — movimenti legati allo scorrimento. Nessuna dipendenza, nessun cookie.
 *
 *  [data-scene]  scena che resta ferma mentre si scorre: riceve --p da 0 a 1
 *  [data-view]   elemento qualsiasi: riceve --v (0 quando entra dal basso, 1 quando esce in alto)
 *                ed --e (0 quando entra, 1 quando la sua parte alta arriva a metà schermo)
 *  [data-hscroll] scena con una striscia orizzontale: l'altezza della scena è calcolata qui
 *
 * Tutti i valori dipendono solo dalla posizione di scorrimento: niente parte a tempo,
 * e tornando indietro ogni movimento si riavvolge.
 */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var still = root.classList.contains('still');
  var header = doc.querySelector('.site-header');
  var menuBtn = doc.querySelector('.menu-btn');
  var menu = doc.getElementById('menu');

  /* ---------- Menu a tutto schermo ---------- */
  function setMenu(open) {
    root.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.querySelector('.sr-only').textContent = menuBtn.getAttribute(open ? 'data-close' : 'data-open');
    if (open) { var first = menu.querySelector('a'); if (first) first.focus({ preventScroll: true }); }
  }
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', function () { setMenu(!root.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('menu-open')) { setMenu(false); menuBtn.focus(); }
    });
  }

  /* ---------- Misure ---------- */
  var vh = window.innerHeight;
  var scenes = [].slice.call(doc.querySelectorAll('[data-scene]'));
  var views = [].slice.call(doc.querySelectorAll('[data-view]'));
  var tones = [].slice.call(doc.querySelectorAll('[data-tone]'));
  var hero = doc.querySelector('.hero[data-scene]');
  var wide = window.matchMedia('(min-width: 900px)');

  function clamp(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }

  // Posizione di impaginazione nel documento: non risente delle trasformazioni,
  // così un elemento non «insegue» il proprio movimento.
  var viewBoxes = [];
  function docTop(el) {
    var t = 0;
    while (el) { t += el.offsetTop; el = el.offsetParent; }
    return t;
  }
  function measureViews() {
    viewBoxes = views.map(function (v) { return { top: docTop(v), h: v.offsetHeight }; });
  }

  // Striscia orizzontale delle esperienze: la scena è alta quanto serve per scorrerla tutta
  function layoutHorizontal() {
    doc.querySelectorAll('[data-hscroll]').forEach(function (s) {
      var track = s.querySelector('.xp__track');
      if (still || !wide.matches || !track) {
        s.style.height = '';
        s.removeAttribute('data-active');
        s.style.removeProperty('--shift');
        return;
      }
      s.setAttribute('data-active', '');
      var shift = Math.max(0, track.scrollWidth - window.innerWidth);
      s.style.setProperty('--shift', shift.toFixed(0));
      s.style.height = (shift + vh) + 'px';
    });
  }

  /* ---------- Un fotogramma: si leggono tutte le posizioni, poi si scrive ---------- */
  var queued = false;
  function frame() {
    queued = false;
    var y = window.scrollY;
    var sceneRects = scenes.map(function (s) { return s.getBoundingClientRect(); });

    scenes.forEach(function (s, i) {
      var r = sceneRects[i];
      var run = r.height - vh;
      var p = run > 0 ? clamp(-r.top / run) : clamp((vh - r.top) / (vh + r.height));
      s.style.setProperty('--p', p.toFixed(4));
    });
    views.forEach(function (v, i) {
      var top = viewBoxes[i].top - y;
      var vv = clamp((vh - top) / (vh + viewBoxes[i].h));
      var e = clamp((vh - top) / (vh * 0.5));
      v.style.setProperty('--v', vv.toFixed(4));
      v.style.setProperty('--e', e.toFixed(4));
    });

    // Intestazione: chiara o scura secondo la sezione che le passa sotto
    if (header) {
      var probe = header.offsetHeight / 2;
      var dark = false;
      for (var k = 0; k < tones.length; k++) {
        var t = tones[k].getBoundingClientRect();
        if (t.top <= probe && t.bottom > probe) { dark = tones[k].getAttribute('data-tone') === 'dark'; break; }
      }
      header.classList.toggle('is-dark', dark);
      var heroP = hero ? parseFloat(hero.style.getPropertyValue('--p')) || 0 : 1;
      var heroDone = !hero || hero.getBoundingClientRect().bottom <= header.offsetHeight;
      header.classList.toggle('show-brand', !hero || heroP > 0.3);
      header.classList.toggle('is-solid', heroDone || (!hero && y > 10));
    }
  }
  function request() {
    if (!queued) { queued = true; window.requestAnimationFrame(frame); }
  }
  function measure() {
    vh = window.innerHeight;
    layoutHorizontal();
    measureViews();
    request();
  }

  if (still) {
    if (header) header.classList.add('show-brand');
    window.addEventListener('scroll', function () {
      if (header) header.classList.toggle('is-solid', window.scrollY > 10);
    }, { passive: true });
    return;
  }

  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', measure);
  if (wide.addEventListener) wide.addEventListener('change', measure);
  window.addEventListener('load', measure);
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(measure);
  measure();
  frame();
  // le immagini che arrivano dopo possono spostare l'impaginazione: si rimisura
  doc.querySelectorAll('img').forEach(function (img) {
    if (!img.complete) img.addEventListener('load', measure, { once: true });
  });
})();
