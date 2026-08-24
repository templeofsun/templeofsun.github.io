/* ============================================================
   TEMPLE OF SUN — site.js
   Shared header/footer, nav, motion. No dependencies.
   ============================================================ */
(function () {
  'use strict';

  var SUN =
    '<svg width="__S__" height="__S__" viewBox="0 0 64 64" fill="none" aria-hidden="true">' +
    '<circle cx="32" cy="32" r="13" stroke="__C__" stroke-width="2"/>' +
    '<g stroke="__C__" stroke-width="2" stroke-linecap="round">' +
    '<line x1="32" y1="4" x2="32" y2="12"/><line x1="32" y1="52" x2="32" y2="60"/>' +
    '<line x1="4" y1="32" x2="12" y2="32"/><line x1="52" y1="32" x2="60" y2="32"/>' +
    '<line x1="12.2" y1="12.2" x2="17.9" y2="17.9"/><line x1="46.1" y1="46.1" x2="51.8" y2="51.8"/>' +
    '<line x1="12.2" y1="51.8" x2="17.9" y2="46.1"/><line x1="46.1" y1="17.9" x2="51.8" y2="12.2"/>' +
    '</g></svg>';

  function sun(size, color) {
    return SUN.replace(/__S__/g, size).replace(/__C__/g, color);
  }

  /* ---------- shared header ---------- */
  var HEADER =
    '<a class="brand" href="index.html"><img class="brand-logo" src="assets/img/logo2-brown.webp" alt="templeofsun · Alchemy of souls" onerror="this.hidden=true;this.nextElementSibling.hidden=false"><span hidden>Temple of Sun</span></a>' +
    '<nav class="nav-desktop" aria-label="Main">' +
    '  <div class="nav-item"><button class="nav-link" type="button" aria-haspopup="true">Aromatherapy<span class="caret">▼</span></button>' +
    '    <div class="dd"><a href="aromatherapy.html">Introduction</a>' +
    '    <div class="dd-item"><a href="collections.html">Collections<span class="dd-arr" aria-hidden="true">›</span></a>' +
    '      <div class="dd-fly">' +
    '        <a href="rainbow-collection.html">The Rainbow Collection</a>' +
    '        <a href="5-elements.html">The 5 Elements</a>' +
    '      </div></div>' +
    '    <a href="create-your-own-formula.html">Create Your Own Formula</a></div></div>' +
    '  <div class="nav-item"><button class="nav-link" type="button" aria-haspopup="true">Experiences<span class="caret">▼</span></button>' +
    '    <div class="dd"><a href="retreats.html">Soul Alchemy Retreats</a><a href="treatments.html">Treatments</a>' +
    '    <a href="mindfulness-labs.html">Mindfulness LABs</a><a href="meditation.html">Meditation Classes</a></div></div>' +
    '  <a class="nav-link" href="online-sessions.html">Online Sessions</a>' +
    '  <div class="nav-item"><button class="nav-link" type="button" aria-haspopup="true">About<span class="caret">▼</span></button>' +
    '    <div class="dd"><a href="bio.html">Bio</a><a href="about.html">My Story</a><a href="philosophy.html">Philosophy</a></div></div>' +
    '  <a class="nav-link" href="contact.html" data-nav="contact">Contact</a>' +
    '  <a class="btn btn-nav" href="contact.html?topic=session">Book a Session</a>' +
    '</nav>' +
    '<button class="burger" type="button" aria-label="Open menu"><span></span><span></span><span></span></button>';

  var MOBILE =
    '<div class="m-group"><a href="index.html">Home</a></div>' +
    '<div class="m-group"><div class="m-label">Aromatherapy</div>' +
    '  <a href="aromatherapy.html">Introduction</a><a href="collections.html">Collections</a>' +
    '  <a class="m-sub" href="rainbow-collection.html">The Rainbow Collection</a>' +
    '  <a class="m-sub" href="5-elements.html">The 5 Elements</a>' +
    '  <a href="create-your-own-formula.html">Create Your Own Formula</a></div>' +
    '<div class="m-group"><div class="m-label">Experiences</div>' +
    '  <a href="retreats.html">Soul Alchemy Retreats</a><a href="treatments.html">Treatments</a>' +
    '  <a href="mindfulness-labs.html">Mindfulness LABs</a><a href="meditation.html">Meditation Classes</a></div>' +
    '<div class="m-group"><a href="online-sessions.html">Online Sessions</a></div>' +
    '<div class="m-group"><div class="m-label">About</div>' +
    '  <a href="bio.html">Bio</a><a href="about.html">My Story</a><a href="philosophy.html">Philosophy</a></div>' +
    '<div class="m-group"><a href="contact.html">Contact</a></div>' +
    '<div class="m-group m-small"><div class="m-label">Say hello</div>' +
    '  <a href="mailto:templeofsunofficial@gmail.com">templeofsunofficial@gmail.com</a>' +
    '  <a href="https://wa.me/36702879225">WhatsApp</a>' +
    '  <a href="https://www.instagram.com/templeofsun/">Instagram</a></div>';

  /* ---------- shared footer (minimal) ---------- */
  var IC = {
    email: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7.5l8.5 5.8 8.5-5.8"/></svg>',
    whatsapp: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.2a8.8 8.8 0 0 0-7.6 13.2L3.2 20.8l4.5-1.2A8.8 8.8 0 1 0 12 3.2z"/><path d="M9.1 8.6c.3-.7 1.3-.8 1.6-.1l.5 1.1c.1.3 0 .7-.2 1l-.5.5c.5 1.1 1.4 2 2.5 2.5l.5-.5c.3-.3.7-.4 1-.2l1.1.5c.7.3.6 1.3-.1 1.6-1 .4-2.1.3-3.1-.2a9.4 9.4 0 0 1-3.5-3.5c-.5-1-.6-2.1-.2-3.1z" stroke-width="1.2"/></svg>',
    telegram: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 3.8L2.9 11l5.5 1.9.3 5.4 3.1-3.2 4.8 3.5 4.7-14.8z"/><path d="M8.4 12.9l12.9-9.1"/></svg>',
    instagram: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="3.8"/><circle cx="17.2" cy="6.8" r="0.5" fill="currentColor" stroke="none"/></svg>',
    tiktok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.6 3.5c.4 2.4 2 4 4.4 4.4v3a7.9 7.9 0 0 1-4.4-1.4v5.4a5.4 5.4 0 1 1-5.4-5.4c.3 0 .7 0 1 .1v3.2a2.3 2.3 0 1 0 1.3 2.1V3.5h3.1z"/></svg>',
    spotify: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="8.6"/><path d="M8 9.9c2.8-.8 5.7-.5 8.1.9M8.3 12.6c2.3-.6 4.7-.3 6.6.8M8.7 15.1c1.8-.4 3.5-.2 5 .6"/></svg>'
  };
  var FOOTER =
    '<div class="footer-min">' +
    '  <a class="brand" href="index.html"><img class="brand-logo-f" src="assets/img/logo2-brown.webp" alt="templeofsun · Alchemy of souls" onerror="this.hidden=true;this.nextElementSibling.hidden=false"><span hidden>Temple of Sun</span></a>' +
    '  <p class="f-tag">holistic wellness experiences by Péter Frák</p>' +
    '  <div class="f-icons">' +
    '    <a href="mailto:templeofsunofficial@gmail.com" aria-label="Email" title="templeofsunofficial@gmail.com">' + IC.email + '</a>' +
    '    <a href="https://wa.me/36702879225" aria-label="WhatsApp" title="WhatsApp +36 70 287 9225">' + IC.whatsapp + '</a>' +
    '    <a href="https://t.me/Templeofsunofficial" aria-label="Telegram" title="Telegram @Templeofsunofficial">' + IC.telegram + '</a>' +
    '    <a href="https://www.instagram.com/templeofsun/" aria-label="Instagram" title="Instagram @templeofsun">' + IC.instagram + '</a>' +
    '    <a href="https://www.tiktok.com/@templeofsun" aria-label="TikTok" title="TikTok @templeofsun">' + IC.tiktok + '</a>' +
    '    <a href="https://open.spotify.com/user/templeofsun2017" aria-label="Spotify" title="Spotify">' + IC.spotify + '</a>' +
    '  </div>' +
    '</div>' +
    '<div class="footer-bottom">' +
    '  <span>© <span data-year></span> Temple of Sun · Aromatherapy &amp; Healing Retreats · Péter Frák, IFA member · <a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a> · <a href="faq.html">FAQ</a></span>' +
    '  <span class="f-legal">Aromatherapy at Temple of Sun is a complementary practice; it supports wellbeing and never replaces medical diagnosis, treatment or care.</span>' +
    '</div>';

  /* ---------- inject ---------- */
  var mainEl = document.querySelector('main');
  if (mainEl && !mainEl.id) mainEl.id = 'main';
  var skip = document.createElement('a');
  skip.className = 'skip'; skip.href = '#main'; skip.textContent = 'Skip to content';
  document.body.insertBefore(skip, document.body.firstChild);

  /* nav + footer ship as static HTML (stamped at build time) so crawlers see
     the full link graph; JS only fills a host that is still empty. */
  var headerHost = document.querySelector('[data-site-header]');
  if (headerHost) { headerHost.className = 'site-header'; if (!headerHost.firstElementChild) headerHost.innerHTML = HEADER; }
  var mobileHost = document.querySelector('[data-site-mobile]');
  if (mobileHost) { mobileHost.className = 'mobile-menu'; if (!mobileHost.firstElementChild) mobileHost.innerHTML = MOBILE; }
  var footerHost = document.querySelector('[data-site-footer]');
  if (footerHost) { footerHost.className = 'site-footer'; if (!footerHost.firstElementChild) footerHost.innerHTML = FOOTER; }

  /* floating WhatsApp — a real human answers */
  var wa = document.createElement('a');
  wa.className = 'wa-float';
  wa.href = 'https://wa.me/36702879225';
  wa.target = '_blank'; wa.rel = 'noopener';
  wa.setAttribute('aria-label', 'Write to Peter on WhatsApp');
  wa.title = 'Write to Peter';
  wa.innerHTML = IC.whatsapp;
  document.body.appendChild(wa);

  var yearEl = document.querySelector('[data-year]');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* dropdown parents: don't latch focus on click (open on hover / keyboard only) */
  document.querySelectorAll('.nav-item > .nav-link').forEach(function (btn) {
    btn.addEventListener('mousedown', function (e) { e.preventDefault(); });
    btn.addEventListener('click', function () { this.blur(); });
  });

  /* ---------- header scroll state ---------- */
  var header = document.querySelector('.site-header');
  function onScroll() {
    if (!header) return;
    var solid = window.scrollY > 60 || !document.body.classList.contains('has-hero');
    header.classList.toggle('is-solid', solid);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- burger ---------- */
  var burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open) staggerMenu();
    });
  }
  function staggerMenu() {
    var links = document.querySelectorAll('.mobile-menu a');
    links.forEach(function (a, i) {
      a.style.transitionDelay = (0.05 + i * 0.045) + 's';
    });
  }

  /* ---------- scroll reveals ---------- */
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* auto-stagger siblings inside grids so groups cascade in */
  document.querySelectorAll('.grid-2,.grid-3,.grid-4,.gallery').forEach(function (g) {
    var kids = g.querySelectorAll(':scope > .reveal');
    kids.forEach(function (el, i) {
      if (!el.style.getPropertyValue('--d')) el.style.setProperty('--d', (i * 0.08) + 's');
    });
  });
  /* image-led reveals open like a window; text keeps the soft blur-rise */
  document.querySelectorAll('.reveal').forEach(function (el) {
    var onlyFrame = el.children.length === 1 && el.children[0].classList && el.children[0].classList.contains('frame');
    if (el.classList.contains('media') || onlyFrame) el.classList.add('reveal-img');
  });
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length && !reduceMotion) {
    /* plays every time an element enters the view — scrolling down OR back up.
       exception: photo product cards reveal once and stay (replaying image grids
       reads as images re-loading and makes long grids feel heavy on scroll) */
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          if (e.target.classList.contains('prod-img')) io.unobserve(e.target);
        }
        else e.target.classList.remove('in');   /* resets quietly off-screen, ready to play again */
      });
    }, { threshold: 0.04, rootMargin: '0px 0px 12% 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- gentle parallax on page-header images ---------- */
  var plxImgs = [];
  document.querySelectorAll('.subhero .frame img').forEach(function (img) { plxImgs.push(img); });
  if (plxImgs.length && !reduceMotion) {
    var ticking = false;
    function plx() {
      ticking = false;
      var vh = window.innerHeight;
      plxImgs.forEach(function (img) {
        var r = img.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var progress = (r.top + r.height / 2 - vh / 2) / vh;   /* -0.5 … 0.5 */
        img.style.transform = 'scale(1.14) translateY(' + (progress * 36).toFixed(1) + 'px)';
      });
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(plx); }
    }, { passive: true });
    plx();
  }

  /* ---------- hero slideshow ---------- */
  var slides = document.querySelectorAll('.hero-slide');
  var dotsWrap = document.querySelector('.hero-dots');
  if (slides.length > 1) {
    var current = 0, timer = null;
    slides.forEach(function (_, i) {
      var b = document.createElement('button');
      b.setAttribute('aria-label', 'Slide ' + (i + 1));
      if (i === 0) b.classList.add('is-active');
      b.addEventListener('click', function () { go(i); restart(); });
      dotsWrap && dotsWrap.appendChild(b);
    });
    var dots = dotsWrap ? dotsWrap.querySelectorAll('button') : [];
    function go(i) {
      var old = current;
      current = (i + slides.length) % slides.length;
      if (current === old) return;
      slides.forEach(function (s) { s.classList.remove('is-under'); });
      slides[old].classList.remove('is-active');
      slides[old].classList.add('is-under');           /* stays visible & drifting underneath */
      slides[current].classList.add('is-active');      /* new photo breathes in on top */
      if (dots[old]) dots[old].classList.remove('is-active');
      if (dots[current]) dots[current].classList.add('is-active');
    }
    function restart() { clearInterval(timer); timer = setInterval(function () { go(current + 1); }, 6000); }
    restart();
    var prevBtn = document.querySelector('.hero-arrow.prev');
    var nextBtn = document.querySelector('.hero-arrow.next');
    if (prevBtn) prevBtn.addEventListener('click', function () { go(current - 1); restart(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { go(current + 1); restart(); });
  }

  /* ---------- testimonials rotator (avatars or dots) ---------- */
  var testis = document.querySelectorAll('.testi');
  if (testis.length > 1) {
    var tCur = 0, tTimer = null;
    var tAvas = document.querySelectorAll('.testi-avatars button');
    var tDotsWrap = document.querySelector('.testi-dots');
    if (!tAvas.length && tDotsWrap) {
      testis.forEach(function (_, i) {
        var b = document.createElement('button');
        b.setAttribute('aria-label', 'Testimonial ' + (i + 1));
        if (i === 0) b.classList.add('is-active');
        tDotsWrap.appendChild(b);
      });
    }
    var tNav = tAvas.length ? tAvas : (tDotsWrap ? tDotsWrap.querySelectorAll('button') : []);
    function tGo(i) {
      testis[tCur].classList.remove('is-active');
      if (tNav[tCur]) tNav[tCur].classList.remove('is-active');
      tCur = (i + testis.length) % testis.length;
      testis[tCur].classList.add('is-active');
      if (tNav[tCur]) tNav[tCur].classList.add('is-active');
    }
    function tRestart() { clearInterval(tTimer); tTimer = setInterval(function () { tGo(tCur + 1); }, 7000); }
    tNav.forEach(function (b, i) {
      b.addEventListener('click', function () { tGo(i); tRestart(); });
    });
    tRestart();
  }

  /* ---------- lightbox with prev / next ---------- */
  var lbLinks = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (lbLinks.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Image viewer');
    lb.setAttribute('aria-hidden', 'true');
    lb.innerHTML =
      '<button class="lightbox-close" aria-label="Close">×</button>' +
      '<button class="lightbox-nav prev" aria-label="Previous image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="14.5 5.5 8.5 12 14.5 18.5"/></svg></button>' +
      '<img alt="">' +
      '<button class="lightbox-nav next" aria-label="Next image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9.5 5.5 15.5 12 9.5 18.5"/></svg></button>';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector('img');
    var lbPrev = lb.querySelector('.lightbox-nav.prev');
    var lbNext = lb.querySelector('.lightbox-nav.next');
    var lbCur = 0;
    if (lbLinks.length < 2) { lbPrev.style.display = 'none'; lbNext.style.display = 'none'; }
    lbImg.addEventListener('load', function () { lbImg.style.opacity = 1; });
    function lbSrc(i) {
      var t = lbLinks[i].querySelector('img');
      return (t && (t.currentSrc || t.src)) || lbLinks[i].getAttribute('href');
    }
    function lbShow(i) {
      lbCur = (i + lbLinks.length) % lbLinks.length;
      lbImg.style.opacity = 0;
      lbImg.src = lbSrc(lbCur);
    }
    var lbReturn = null;
    lbLinks.forEach(function (a, i) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        lbReturn = a;
        lbShow(i);
        lb.classList.add('is-open');
        document.body.classList.add('lb-open');
        lb.setAttribute('aria-hidden', 'false');
        lb.querySelector('.lightbox-close').focus();
      });
    });
    function closeLb() {
      lb.classList.remove('is-open');
      document.body.classList.remove('lb-open');
      lb.setAttribute('aria-hidden', 'true');
      if (lbReturn) { lbReturn.focus(); lbReturn = null; }
    }
    lb.addEventListener('click', closeLb);
    lb.querySelector('.lightbox-close').addEventListener('click', function (e) { e.stopPropagation(); closeLb(); });
    lbImg.addEventListener('click', function (e) { e.stopPropagation(); });
    lbPrev.addEventListener('click', function (e) { e.stopPropagation(); lbShow(lbCur - 1); });
    lbNext.addEventListener('click', function (e) { e.stopPropagation(); lbShow(lbCur + 1); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') closeLb();
      if (e.key === 'ArrowLeft') lbShow(lbCur - 1);
      if (e.key === 'ArrowRight') lbShow(lbCur + 1);
    });
  }

  /* ---------- video testimonials player ---------- */
  var vtBtns = Array.prototype.slice.call(document.querySelectorAll('.vt-strip button[data-video]'));
  if (vtBtns.length) {
    /* paint a real first frame into each tile (metadata alone can leave them blank) */
    vtBtns.forEach(function (b) {
      var tv = b.querySelector('video');
      if (!tv) return;
      tv.preload = 'auto';
      function paintFrame() { try { tv.currentTime = 0.6; } catch (err) {} }
      if (tv.readyState >= 1) paintFrame();
      else tv.addEventListener('loadedmetadata', paintFrame);
    });
    var vlb = document.createElement('div');
    vlb.className = 'lightbox';
    vlb.setAttribute('role', 'dialog');
    vlb.setAttribute('aria-modal', 'true');
    vlb.setAttribute('aria-label', 'Video player');
    vlb.setAttribute('aria-hidden', 'true');
    vlb.innerHTML =
      '<button class="lightbox-close" aria-label="Close">×</button>' +
      '<button class="lightbox-nav prev" aria-label="Previous video"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="14.5 5.5 8.5 12 14.5 18.5"/></svg></button>' +
      '<video controls playsinline></video>' +
      '<button class="lightbox-nav next" aria-label="Next video"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9.5 5.5 15.5 12 9.5 18.5"/></svg></button>';
    document.body.appendChild(vlb);
    var vv = vlb.querySelector('video');
    var vCur = 0;
    function vShow(i) {
      vCur = (i + vtBtns.length) % vtBtns.length;
      vv.src = vtBtns[vCur].getAttribute('data-video');
      vv.play().catch(function () {});
    }
    var vReturn = null;
    function vClose() {
      vlb.classList.remove('is-open');
      document.body.classList.remove('lb-open');
      vlb.setAttribute('aria-hidden', 'true');
      vv.pause(); vv.removeAttribute('src'); vv.load();
      if (vReturn) { vReturn.focus(); vReturn = null; }
    }
    vtBtns.forEach(function (b, i) {
      b.addEventListener('click', function () {
        vReturn = b;
        vShow(i);
        vlb.classList.add('is-open');
        document.body.classList.add('lb-open');
        vlb.setAttribute('aria-hidden', 'false');
        vlb.querySelector('.lightbox-close').focus();
      });
    });
    vlb.addEventListener('click', vClose);
    vlb.querySelector('.lightbox-close').addEventListener('click', function (e) { e.stopPropagation(); vClose(); });
    vv.addEventListener('click', function (e) { e.stopPropagation(); });
    vlb.querySelector('.lightbox-nav.prev').addEventListener('click', function (e) { e.stopPropagation(); vShow(vCur - 1); });
    vlb.querySelector('.lightbox-nav.next').addEventListener('click', function (e) { e.stopPropagation(); vShow(vCur + 1); });
    document.addEventListener('keydown', function (e) {
      if (!vlb.classList.contains('is-open')) return;
      if (e.key === 'Escape') vClose();
      if (e.key === 'ArrowLeft') vShow(vCur - 1);
      if (e.key === 'ArrowRight') vShow(vCur + 1);
    });
  }

  /* ---------- guest voices: looping carousel ---------- */
  var vcTrack = document.getElementById('vcTrack');
  if (vcTrack) {
    var vcShell = vcTrack.parentElement;
    var vcBarFill = document.getElementById('vcBarFill');
    var masters = [].slice.call(vcTrack.children).map(function (el) { el.remove(); return el; });
    var CLONES = 4;
    var spanW = 0;          /* width of one full set of visible originals */
    var vcStart = 0;        /* where the originals begin (after the tail clones) */
    var paused = false;
    var drifting = !reduceMotion;

    function visibleMasters(key) {
      return masters.filter(function (m) {
        return key === 'ALL' || (m.getAttribute('data-topics') || '').split(' ').indexOf(key) >= 0;
      });
    }

    function build(key) {
      var vis = visibleMasters(key);
      vcTrack.innerHTML = '';
      var loop = vis.length > 3;
      var head = loop ? vis.slice(0, CLONES) : [];
      var tail = loop ? vis.slice(-CLONES) : [];
      tail.forEach(function (m) { var c = m.cloneNode(true); c.setAttribute('data-clone', '1'); vcTrack.appendChild(c); });
      vis.forEach(function (m) { vcTrack.appendChild(m); });
      head.forEach(function (m) { var c = m.cloneNode(true); c.setAttribute('data-clone', '1'); vcTrack.appendChild(c); });
      vcTrack.style.justifyContent = loop ? '' : 'center';
      requestAnimationFrame(function () {
        if (!loop) { spanW = 0; vcStart = 0; vcTrack.scrollLeft = 0; return; }
        var first = vcTrack.children[tail.length];
        var gap = parseFloat(getComputedStyle(vcTrack).columnGap || getComputedStyle(vcTrack).gap || 20);
        spanW = 0;
        for (var i = 0; i < vis.length; i++) spanW += vis[i].getBoundingClientRect().width + gap;
        vcStart = first.offsetLeft - vcTrack.offsetLeft;
        vcTrack.scrollLeft = vcStart;
      });
    }

    function wrap() {
      if (!spanW) return;
      if (vcTrack.scrollLeft >= vcStart + spanW) vcTrack.scrollLeft -= spanW;
      else if (vcTrack.scrollLeft <= vcStart * 0.25) vcTrack.scrollLeft += spanW;
      if (vcBarFill) {
        var p = ((((vcTrack.scrollLeft - vcStart) % spanW) + spanW) % spanW) / spanW * 100;
        vcBarFill.style.width = p + '%';
      }
    }
    vcTrack.addEventListener('scroll', wrap, { passive: true });

    /* slow drift, both directions reachable by hand */
    var driftAcc = 0;
    var vcRunning = false;
    function tick() {
      if (!vcRunning) return;
      if (drifting && !paused && spanW && document.visibilityState === 'visible') {
        driftAcc += 0.45;
        var whole = Math.floor(driftAcc);
        if (whole) { vcTrack.scrollLeft += whole; driftAcc -= whole; }
      }
      requestAnimationFrame(tick);
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        var vis = en[0].isIntersecting;
        if (vis && !vcRunning) { vcRunning = true; requestAnimationFrame(tick); }
        else if (!vis) vcRunning = false;
      }).observe(vcShell);
    } else { vcRunning = true; requestAnimationFrame(tick); }
    ['mouseenter', 'focusin', 'touchstart'].forEach(function (ev) { vcShell.addEventListener(ev, function () { paused = true; }, { passive: true }); });
    ['mouseleave', 'focusout'].forEach(function (ev) { vcShell.addEventListener(ev, function () { paused = false; }); });

    /* grab-drag on desktop */
    var dragX = null, dragStart = 0;
    vcTrack.addEventListener('pointerdown', function (e) {
      dragX = e.clientX; dragStart = vcTrack.scrollLeft;
      vcTrack.classList.add('is-drag');
    });
    window.addEventListener('pointermove', function (e) {
      if (dragX === null) return;
      vcTrack.scrollLeft = dragStart - (e.clientX - dragX);
    });
    window.addEventListener('pointerup', function () { dragX = null; vcTrack.classList.remove('is-drag'); });

    var vcStep = function () { return Math.min(vcTrack.clientWidth, 800) * 0.9; };
    vcShell.querySelector('.vc-arrow.prev').addEventListener('click', function () { vcTrack.scrollBy({ left: -vcStep(), behavior: 'smooth' }); });
    vcShell.querySelector('.vc-arrow.next').addEventListener('click', function () { vcTrack.scrollBy({ left: vcStep(), behavior: 'smooth' }); });
    vcTrack.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); vcTrack.scrollBy({ left: -vcStep(), behavior: 'smooth' }); }
      if (e.key === 'ArrowRight') { e.preventDefault(); vcTrack.scrollBy({ left: vcStep(), behavior: 'smooth' }); }
    });

    document.querySelectorAll('[data-vchip]').forEach(function (ch) {
      ch.addEventListener('click', function () {
        document.querySelectorAll('[data-vchip]').forEach(function (c) { c.classList.remove('is-on'); });
        ch.classList.add('is-on');
        build(ch.getAttribute('data-vchip'));
      });
    });

    build('ALL');
  }

  /* ---------- expandable blocks (guest voices wall) ---------- */
  document.querySelectorAll('[data-expand]').forEach(function (btn) {
    var target = document.getElementById(btn.getAttribute('data-expand'));
    if (!target) return;
    btn.addEventListener('click', function () {
      var open = target.classList.toggle('is-open');
      btn.textContent = open ? (btn.getAttribute('data-less') || 'Show less')
                             : (btn.getAttribute('data-more') || 'Show all');
      if (!open) target.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
  });

  /* ---------- forms (visual only — wiring comes later) ---------- */
  document.querySelectorAll('form[data-soft]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var box = form.closest('[data-form-box]') || form.parentElement;
      box.classList.add('form-done');
    });
  });

  /* ---------- contact topic pre-select ---------- */
  var topicSel = document.querySelector('select[name="topic"]');
  if (topicSel) {
    var m = window.location.search.match(/[?&]topic=([a-z-]+)/);
    if (m) {
      var map = {
        session: 'A healing session',
        online: 'An online session',
        retreat: 'The next retreat',
        oils: 'The oils',
        blend: 'Help choosing my blend',
        order: 'An order or delivery',
        gift: 'A gift for someone',
        formula: 'A signature formula for my space',
        workshop: 'A workshop, group or private retreat',
        group: 'A workshop, group or private retreat',
        collab: 'A collaboration or stocking the oils',
        wholesale: 'A collaboration or stocking the oils',
        press: 'Press or an interview'
      };
      if (map[m[1]]) topicSel.value = map[m[1]];
    }
  }

  /* ---------- image fallback: keep the calm placeholder ---------- */
  document.querySelectorAll('.frame img').forEach(function (img) {
    img.addEventListener('error', function () { img.style.display = 'none'; });
  });

  /* ---------- page fade transitions ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    requestAnimationFrame(function () { document.body.classList.add('is-ready'); });
  });
  if (document.readyState !== 'loading') document.body.classList.add('is-ready');
  document.addEventListener('click', function (e) {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    var a = e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (a.target === '_blank' || href.indexOf('http') === 0 || href.indexOf('#') === 0 ||
        href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0 || a.hasAttribute('data-lightbox')) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    e.preventDefault();
    document.body.classList.add('is-leaving');
    setTimeout(function () { window.location.href = href; }, 280);
  });
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { document.body.classList.remove('is-leaving'); document.body.classList.add('is-ready'); }
  });
})();
