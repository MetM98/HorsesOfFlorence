/* Horses of Florence — piccoli comportamenti, nessuna dipendenza, nessun cookie. */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var header = doc.querySelector('.site-header');
  var hero = doc.querySelector('.hero, [data-hero]');
  var toggle = doc.querySelector('.menu-toggle');
  var nav = doc.getElementById('nav');
  var hasIO = 'IntersectionObserver' in window;

  /* Header: diventa avorio e sfocato quando si lascia l'apertura */
  if (header && hero && hasIO) {
    new IntersectionObserver(function (entries) {
      header.classList.toggle('is-solid', !entries[0].isIntersecting);
    }, { rootMargin: '-76px 0px 0px 0px' }).observe(hero);
  } else if (header) {
    header.classList.add('is-solid');
  }

  /* Menu mobile */
  function setMenu(open) {
    root.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.sr-only').textContent = toggle.getAttribute(open ? 'data-close' : 'data-open');
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('menu-open')) { setMenu(false); toggle.focus(); }
    });
    window.matchMedia('(min-width: 1101px)').addEventListener('change', function (mq) {
      if (mq.matches) setMenu(false);
    });
  }

  /* Comparsa morbida delle sezioni */
  var reveals = doc.querySelectorAll('.reveal');
  if (hasIO) {
    var revealIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealIO.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { revealIO.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* Voce di menu attiva in base alla sezione visibile */
  var links = doc.querySelectorAll('.nav__link');
  if (hasIO && links.length) {
    var byId = {};
    links.forEach(function (a) {
      var hash = a.getAttribute('href').split('#')[1];
      if (hash) byId[hash] = a;
    });
    var activeIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = byId[entry.target.id];
        if (link && entry.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('is-active'); });
          link.classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(byId).forEach(function (id) {
      var section = doc.getElementById(id);
      if (section) activeIO.observe(section);
    });
  }

  /* Modulo contatti → messaggio WhatsApp o email già compilato */
  var form = doc.getElementById('contact-form');
  if (!form) return;
  var i18n = JSON.parse(doc.getElementById('form-i18n').textContent);
  var el = form.elements;

  // «Chiedi informazioni» sull'abbigliamento preseleziona l'interesse giusto
  doc.querySelectorAll('[data-interest]').forEach(function (a) {
    a.addEventListener('click', function () { el.interest.value = a.getAttribute('data-interest'); });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var via = (e.submitter && e.submitter.value) || 'whatsapp';
    var interest = el.interest.options[el.interest.selectedIndex].text;
    var riders = form.querySelector('input[name="riders"]:checked');
    var lines = [i18n.greeting, ''];
    if (el.name.value.trim()) lines.push(i18n.name + ': ' + el.name.value.trim());
    lines.push(i18n.interest + ': ' + interest);
    lines.push(i18n.riders + ': ' + (riders ? riders.value : '1'));
    lines.push(i18n.own_horse + ': ' + (el.own_horse.checked ? i18n.yes : i18n.no));
    if (el.period.value.trim()) lines.push(i18n.period + ': ' + el.period.value.trim());
    lines.push(i18n.gaits + ': ' + (el.gaits.checked ? i18n.yes : i18n.no));
    if (el.message.value.trim()) lines.push('', el.message.value.trim());
    var text = lines.join('\n');

    if (via === 'email') {
      window.location.href = 'mailto:' + (form.dataset.email || '') +
        '?subject=' + encodeURIComponent(i18n.subject + ' · Horses of Florence') +
        '&body=' + encodeURIComponent(text);
    } else {
      var number = (form.dataset.whatsapp || '').replace(/\D/g, '');
      window.open('https://wa.me/' + number + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
    }
  });
})();
