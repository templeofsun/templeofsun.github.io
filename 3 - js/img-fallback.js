/* Temple of Sun — image fallbacks, and the "JavaScript is on" flag.
 *
 * FIRST, before anything else: mark the page as having JavaScript.
 *
 * The site fades in — the body starts invisible and the sections rise into
 * place. That is fine when JavaScript runs, because JavaScript is what makes
 * them appear. With JavaScript off, nothing ever did, and every page rendered
 * as a blank cream rectangle.
 *
 * So the hiding is now conditional on this one class. No JavaScript means no
 * class, which means nothing is hidden and the page simply shows. This file is
 * loaded in <head> on all 48 pages, so the class lands before the body paints
 * and there is no flicker.
 */
document.documentElement.classList.add("js");

/*
 * Replaces the old inline onerror="..." attributes on <img> tags, which a
 * strict Content-Security-Policy blocks. Same behaviour, one shared handler.
 *
 * Loaded in <head> so it is listening before any image on the page loads.
 *
 * Mark an image with data-onerr="..." to pick what happens if it fails:
 *   hide     — hide the image
 *   swap     — hide it and reveal the next element (text logo fallback)
 *   remote   — retry once from data-remote, then hide
 *   parent   — add class "t-fallback" to the parent (logo strip)
 *   text     — replace the image with the text in data-onerr-text
 */
(function () {
  'use strict';

  function handle(el) {
    switch (el.getAttribute('data-onerr')) {
      case 'hide':
        el.style.display = 'none';
        break;

      case 'swap':
        el.hidden = true;
        if (el.nextElementSibling) el.nextElementSibling.hidden = false;
        break;

      case 'remote':
        if (el.dataset.f || !el.dataset.remote) {
          el.style.display = 'none';
        } else {
          el.dataset.f = 1;
          el.src = el.dataset.remote;
        }
        break;

      case 'parent':
        if (el.parentElement) el.parentElement.classList.add('t-fallback');
        break;

      case 'text':
        el.outerHTML = el.getAttribute('data-onerr-text') || '';
        break;
    }
  }

  /* Capture phase: error events on images do not bubble. */
  document.addEventListener('error', function (e) {
    var el = e.target;
    if (el && el.tagName === 'IMG' && el.hasAttribute('data-onerr')) handle(el);
  }, true);

  /* Safety net: catch images that already failed before this ran,
     and any that are added to the page later by site.js. */
  function sweep() {
    var imgs = document.querySelectorAll('img[data-onerr]');
    for (var i = 0; i < imgs.length; i++) {
      var el = imgs[i];
      if (el.complete && el.naturalWidth === 0 && el.getAttribute('src')) handle(el);
    }
  }

  document.addEventListener('DOMContentLoaded', sweep);
  window.addEventListener('load', sweep);
})();
