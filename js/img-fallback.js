/* Temple of Sun — image fallbacks.
 *
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
