/* ============================================================
   TEMPLE OF SUN: shop.js
   The cart, the cart panel, checkout and the thank-you page.
   No payment happens on the site: the order is sent to Péter, who
   confirms postage and how to pay.

   Loaded on every page by js/site.js. Reads the price list from
   js/shop-data.js (generated, do not edit), the postage rates from
   js/shop-postage.js (edit by hand) and its look from css/shop.css.
   No dependencies.

   Contents
     1. Settings
     2. Helpers
     3. Cart storage
     4. Header button and cart panel
     5. Product pages: quantity and "Add to cart"
     6. Checkout page
     7. Thank-you page
     8. Start
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. Settings ---------- */
  var SETTINGS = {
    /* Where the order request is sent, to be emailed to Péter. Planned: a
       Cloudflare function on the site itself, e.g. '/api/order', once the
       domain is on Cloudflare. It receives the JSON below and answers
       { "success": true }.
       TEST SITE: while this is empty, "Send order request" goes straight to
       the thank-you page and nothing is sent to anyone. */
    orderUrl: '',
    maxQty: 20,
    cartKey: 'tos-cart',
    lastOrderKey: 'tos-last-order'
  };

  var ROOT = document.documentElement.getAttribute('data-root') || '';
  var PRODUCTS = {};
  var POSTAGE = [];

  /* ---------- 2. Helpers ---------- */
  function money(cents) {
    return '€' + (cents / 100).toFixed(2);
  }
  function esc(text) {
    return String(text).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function clampQty(n) {
    n = parseInt(n, 10);
    if (isNaN(n) || n < 1) return 1;
    return Math.min(n, SETTINGS.maxQty);
  }
  function loadOnce(tag, attrs) {
    return new Promise(function (resolve, reject) {
      var el = document.createElement(tag);
      Object.keys(attrs).forEach(function (k) { el[k] = attrs[k]; });
      el.onload = resolve; el.onerror = reject;
      document.head.appendChild(el);
    });
  }
  /* order number like TOS-2611-4F7Q: year, month, four random letters */
  function orderRef() {
    var d = new Date();
    var letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    var code = '';
    for (var i = 0; i < 4; i++) code += letters[Math.floor(Math.random() * letters.length)];
    return 'TOS-' + String(d.getFullYear()).slice(2) + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + code;
  }

  var ICON_BAG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.5 8h13l-1 12.5h-11z"/><path d="M9 10.5V7a3 3 0 0 1 6 0v3.5"/></svg>';
  var ICON_CLOSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  /* ---------- 3. Cart storage ---------- */
  /* The cart is a list of { id, qty } kept in the visitor's own browser.
     Names and prices always come from the price list, never from storage. */
  function readCart() {
    var list;
    try { list = JSON.parse(localStorage.getItem(SETTINGS.cartKey)) || []; } catch (e) { list = []; }
    return list.filter(function (row) { return row && PRODUCTS[row.id]; })
               .map(function (row) { return { id: row.id, qty: clampQty(row.qty) }; });
  }
  function saveCart(list) {
    try { localStorage.setItem(SETTINGS.cartKey, JSON.stringify(list)); } catch (e) {}
    render();
  }
  function addItem(id, qty) {
    var list = readCart();
    var row = list.filter(function (r) { return r.id === id; })[0];
    if (row) row.qty = clampQty(row.qty + qty);
    else list.push({ id: id, qty: clampQty(qty) });
    saveCart(list);
  }
  function setQty(id, qty) {
    saveCart(readCart().map(function (r) { return r.id === id ? { id: id, qty: clampQty(qty) } : r; }));
  }
  function removeItem(id) {
    saveCart(readCart().filter(function (r) { return r.id !== id; }));
  }
  function clearCart() { saveCart([]); }

  function lines(list) {
    return list.map(function (r) {
      var p = PRODUCTS[r.id];
      return { id: r.id, qty: r.qty, name: p.name, size: p.size, price: p.price,
               total: p.price * r.qty, url: ROOT + p.url, image: ROOT + p.image };
    });
  }
  function count(list) { return list.reduce(function (n, r) { return n + r.qty; }, 0); }
  function subtotal(list) { return lines(list).reduce(function (n, l) { return n + l.total; }, 0); }

  /* ---------- 4. Header button and cart panel ---------- */
  var cartBtn, drawer, shade, lastFocus;

  function buildChrome() {
    var tools = document.querySelector('.site-header .hdr-tools');
    if (tools) {
      cartBtn = document.createElement('button');
      cartBtn.type = 'button';
      cartBtn.className = 'cart-btn';
      cartBtn.hidden = true;
      cartBtn.innerHTML = ICON_BAG + '<span class="cart-count" aria-hidden="true">0</span>';
      tools.insertBefore(cartBtn, tools.firstChild);
      cartBtn.addEventListener('click', openDrawer);
    }

    shade = document.createElement('div');
    shade.className = 'cart-shade';
    shade.hidden = true;
    shade.addEventListener('click', closeDrawer);

    drawer = document.createElement('aside');
    drawer.className = 'cart-drawer';
    drawer.hidden = true;
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-modal', 'true');
    drawer.setAttribute('aria-labelledby', 'cart-title');
    drawer.innerHTML =
      '<div class="cd-head">' +
      '  <h2 id="cart-title" class="cd-title">Your cart</h2>' +
      '  <button type="button" class="cd-close" aria-label="Close cart">' + ICON_CLOSE + '</button>' +
      '</div>' +
      '<div class="cd-body" data-cart-lines></div>' +
      '<div class="cd-foot">' +
      '  <p class="cd-sub"><span>Subtotal</span><strong data-cart-subtotal></strong></p>' +
      '  <p class="cd-note" data-cart-postage-note>No payment is taken online. Postage is added at checkout, once you choose your country.</p>' +
      '  <a class="btn btn-solid cd-checkout" href="' + ROOT + 'checkout.html">Checkout</a>' +
      '  <button type="button" class="cd-continue">Continue browsing</button>' +
      '</div>';
    document.body.appendChild(shade);
    document.body.appendChild(drawer);

    drawer.querySelector('.cd-close').addEventListener('click', closeDrawer);
    drawer.querySelector('.cd-continue').addEventListener('click', closeDrawer);
    drawer.addEventListener('click', onLineClick);
    drawer.addEventListener('change', onLineChange);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('cart-open')) closeDrawer();
    });
  }

  function openDrawer() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    drawer.hidden = false; shade.hidden = false;
    void drawer.offsetWidth; /* let the browser place it first, so it slides in */
    document.body.classList.add('cart-open');
    drawer.querySelector('.cd-close').focus({ preventScroll: true });
  }
  function closeDrawer() {
    if (!drawer || !document.body.classList.contains('cart-open')) return;
    document.body.classList.remove('cart-open');
    setTimeout(function () { drawer.hidden = true; shade.hidden = true; }, 350);
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }

  function lineHtml(l, editable) {
    return '<li class="cl" data-id="' + esc(l.id) + '">' +
      '<a class="cl-img" href="' + esc(l.url) + '"><img src="' + esc(l.image) + '" alt="" width="64" height="64" loading="lazy"></a>' +
      '<div class="cl-main">' +
      '  <a class="cl-name" href="' + esc(l.url) + '">' + esc(l.name) + '</a>' +
      '  <span class="cl-meta">' + (l.size ? esc(l.size) + ' · ' : '') + money(l.price) + '</span>' +
      (editable
        ? '  <div class="cl-row">' +
          '    <div class="qty qty-sm">' +
          '      <button type="button" data-step="-1" aria-label="One less ' + esc(l.name) + '">−</button>' +
          '      <input type="number" min="1" max="' + SETTINGS.maxQty + '" value="' + l.qty + '" inputmode="numeric" aria-label="Quantity of ' + esc(l.name) + '">' +
          '      <button type="button" data-step="1" aria-label="One more ' + esc(l.name) + '">+</button>' +
          '    </div>' +
          '    <button type="button" class="cl-remove" data-remove>Remove</button>' +
          '  </div>'
        : '  <span class="cl-meta">Quantity ' + l.qty + '</span>') +
      '</div>' +
      '<strong class="cl-total">' + money(l.total) + '</strong>' +
      '</li>';
  }

  function onLineClick(e) {
    var row = e.target.closest('.cl');
    if (!row) return;
    var id = row.getAttribute('data-id');
    var step = e.target.closest('[data-step]');
    if (step) {
      var input = row.querySelector('input');
      var next = parseInt(input.value, 10) + parseInt(step.getAttribute('data-step'), 10);
      if (next < 1) removeItem(id); else setQty(id, next);
    } else if (e.target.closest('[data-remove]')) {
      removeItem(id);
    }
  }
  function onLineChange(e) {
    var row = e.target.closest('.cl');
    if (row && e.target.matches('input')) setQty(row.getAttribute('data-id'), e.target.value);
  }

  /* Draw everything that shows the cart: badge, panel, checkout summary. */
  function render() {
    var list = readCart();
    var n = count(list);

    if (cartBtn) {
      cartBtn.hidden = n === 0;
      cartBtn.querySelector('.cart-count').textContent = n;
      cartBtn.setAttribute('aria-label', 'Open your cart, ' + n + (n === 1 ? ' item' : ' items'));
    }
    if (drawer) {
      var body = drawer.querySelector('[data-cart-lines]');
      body.innerHTML = n
        ? '<ul class="cl-list">' + lines(list).map(function (l) { return lineHtml(l, true); }).join('') + '</ul>'
        : '<p class="cd-empty">Your cart is empty.</p>';
      drawer.querySelector('[data-cart-subtotal]').textContent = money(subtotal(list));
      if (POSTAGE.length) {
        drawer.querySelector('[data-cart-postage-note]').textContent =
          'No payment is taken online. Postage from ' + money(lowestPostage()) +
          ' is added at checkout, once you choose your country.';
      }
      drawer.querySelector('.cd-foot').hidden = n === 0;
    }
    renderCheckout(list);
  }

  /* ---------- 5. Product pages: quantity and "Add to cart" ---------- */
  function bindProductPage() {
    document.addEventListener('click', function (e) {
      var step = e.target.closest('[data-qty] [data-step]');
      if (step) {
        var input = step.closest('[data-qty]').querySelector('input');
        input.value = clampQty(parseInt(input.value, 10) + parseInt(step.getAttribute('data-step'), 10));
        return;
      }
      var add = e.target.closest('[data-add-to-cart]');
      if (!add) return;
      var id = add.getAttribute('data-add-to-cart');
      if (!PRODUCTS[id]) return; /* unknown blend: let the link work as before */
      e.preventDefault();
      var picker = document.querySelector('[data-qty] input');
      addItem(id, picker ? clampQty(picker.value) : 1);
      if (picker) picker.value = 1;
      flash(add);
      openDrawer();
    }, true); /* capture: runs before the page-fade link handler in site.js */
  }
  function flash(btn) {
    var label = btn.textContent;
    btn.textContent = 'Added';
    btn.classList.add('is-added');
    setTimeout(function () { btn.textContent = label; btn.classList.remove('is-added'); }, 1600);
  }

  /* ---------- 6. Checkout page ---------- */
  var checkout = null;

  function renderCheckout(list) {
    if (!checkout) return;
    var n = count(list);
    checkout.querySelector('[data-checkout-full]').hidden = n === 0;
    checkout.querySelector('[data-checkout-empty]').hidden = n !== 0;
    var box = checkout.querySelector('[data-order-summary]');
    if (!n) { box.innerHTML = ''; return; }
    box.innerHTML =
      '<h2 class="co-sum-title">Order summary</h2>' +
      '<ul class="cl-list">' + lines(list).map(function (l) { return lineHtml(l, true); }).join('') + '</ul>' +
      '<p class="cd-sub"><span>Subtotal</span><span>' + money(subtotal(list)) + '</span></p>' +
      postageRows(subtotal(list), postageFor(chosenCountry())) +
      '<p class="cd-note">Delivery usually takes around five working days, depending on the country.</p>';
  }

  /* ---- postage (rates live in js/shop-postage.js) ---- */
  function postageFor(country) {
    if (!country) return null;
    for (var i = 0; i < POSTAGE.length; i++) {
      if (POSTAGE[i].countries.indexOf(country) !== -1) return POSTAGE[i];
    }
    return null;
  }
  function chosenCountry() {
    var sel = checkout && checkout.querySelector('select[name="country"]');
    return sel ? sel.value : '';
  }
  function lowestPostage() {
    return POSTAGE.reduce(function (m, r) { return Math.min(m, r.price); }, Infinity);
  }
  function postageRows(sub, region) {
    if (!region) {
      return '<p class="cd-sub cd-sub-soft"><span>Postage</span><span>choose your country</span></p>';
    }
    return '<p class="cd-sub cd-sub-soft"><span>Postage, ' + esc(region.name) + '</span><span>' + money(region.price) + '</span></p>' +
      (region.note ? '<p class="cd-note">' + esc(region.note) + '</p>' : '') +
      '<p class="cd-sub cd-total"><span>Total</span><strong>' + money(sub + region.price) + '</strong></p>';
  }
  function fillCountries(sel) {
    var keep = sel.value;
    sel.innerHTML = '<option value="">Choose your country</option>' +
      POSTAGE.map(function (r) {
        return '<optgroup label="' + esc(r.name + ' · postage ' + money(r.price)) + '">' +
          r.countries.slice().sort().map(function (c) {
            return '<option value="' + esc(c) + '">' + esc(c) + '</option>';
          }).join('') + '</optgroup>';
      }).join('');
    sel.value = keep;
  }

  function field(form, name) {
    var el = form.elements[name];
    return el ? String(el.value || '').trim() : '';
  }

  function buildOrder(form) {
    var list = readCart();
    var order = {
      ref: orderRef(),
      date: new Date().toISOString().slice(0, 10),
      lines: lines(list).map(function (l) {
        return { id: l.id, name: l.name, size: l.size, qty: l.qty, price: l.price, total: l.total };
      }),
      subtotal: subtotal(list),
      name: field(form, 'name'),
      email: field(form, 'email'),
      phone: field(form, 'phone'),
      street: field(form, 'street'),
      postcode: field(form, 'postcode'),
      city: field(form, 'city'),
      country: field(form, 'country'),
      postage: 0,
      postageRegion: '',
      invoice: form.elements.invoice && form.elements.invoice.checked,
      company: field(form, 'company'),
      vat: field(form, 'vat'),
      billing: field(form, 'billing'),
      gift: field(form, 'gift'),
      message: field(form, 'message')
    };
    var region = postageFor(order.country);
    if (region) { order.postage = region.price; order.postageRegion = region.name; }
    order.total = order.subtotal + order.postage;
    order.text = orderText(order);
    return order;
  }

  function orderText(o) {
    var t = [];
    t.push('New order request ' + o.ref + ' (' + o.date + ')');
    t.push('');
    o.lines.forEach(function (l) {
      t.push(l.qty + ' × ' + l.name + (l.size ? ' (' + l.size + ')' : '') +
             (l.qty > 1 ? ', ' + money(l.price) + ' each = ' : ' = ') + money(l.total));
    });
    t.push('Subtotal: ' + money(o.subtotal));
    t.push('Postage (' + o.postageRegion + '): ' + money(o.postage));
    t.push('Total: ' + money(o.total) + ' (payment to arrange)');
    t.push('');
    t.push('Name: ' + o.name);
    t.push('Email: ' + o.email);
    t.push('Phone: ' + o.phone);
    t.push('Ship to: ' + [o.street, o.postcode + ' ' + o.city, o.country].join(', '));
    if (o.invoice) {
      t.push('');
      t.push('Invoice wanted');
      if (o.company) t.push('Company: ' + o.company);
      if (o.vat) t.push('VAT number: ' + o.vat);
      if (o.billing) t.push('Billing address: ' + o.billing);
    }
    if (o.gift) { t.push(''); t.push('Gift note: ' + o.gift); }
    if (o.message) { t.push(''); t.push('Message: ' + o.message); }
    return t.join('\n');
  }

  function finish(order) {
    try {
      sessionStorage.setItem(SETTINGS.lastOrderKey, JSON.stringify({
        ref: order.ref, lines: order.lines, subtotal: order.subtotal, email: order.email,
        postage: order.postage, postageRegion: order.postageRegion, total: order.total,
        firstName: order.name.split(/\s+/)[0]
      }));
    } catch (e) {}
    clearCart();
    location.href = ROOT + 'thanks.html';
  }

  function bindCheckout() {
    checkout = document.querySelector('[data-checkout]');
    if (!checkout) return;
    var form = checkout.querySelector('form');
    var invoice = form.elements.invoice;
    var invoiceBox = checkout.querySelector('[data-invoice-fields]');
    var status = checkout.querySelector('[data-order-status]');
    var submit = form.querySelector('[type="submit"]');

    invoice.addEventListener('change', function () {
      invoiceBox.hidden = !invoice.checked;
      invoiceBox.querySelectorAll('input').forEach(function (i) {
        if (i.name === 'company') i.required = invoice.checked;
      });
    });
    checkout.addEventListener('click', onLineClick);
    checkout.addEventListener('change', onLineChange);

    var countrySel = form.elements.country;
    fillCountries(countrySel);
    countrySel.addEventListener('change', function () { render(); });

    /* the browser checks the required fields before this runs */
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!count(readCart())) return;
      if (form.elements.botcheck && form.elements.botcheck.checked) return; /* a bot ticked the hidden box */
      var order = buildOrder(form);

      if (!SETTINGS.orderUrl) { finish(order); return; } /* test site: nothing is sent */

      submit.disabled = true;
      status.textContent = 'Sending your order request…';
      fetch(SETTINGS.orderUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          subject: 'New order request ' + order.ref + ' · ' + money(order.subtotal),
          ref: order.ref,
          name: order.name,
          email: order.email,
          phone: order.phone,
          text: order.text
        })
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (!res || !res.success) throw new Error('not sent');
          finish(order);
        })
        .catch(function () {
          submit.disabled = false;
          status.textContent = '';
          status.textContent = 'Your order request could not be sent just now. Please try again in a moment.';
        });
    });
  }

  /* ---------- 7. Thank-you page ---------- */
  function bindThanks() {
    var box = document.querySelector('[data-thanks]');
    if (!box) return;
    var order;
    try { order = JSON.parse(sessionStorage.getItem(SETTINGS.lastOrderKey)); } catch (e) {}
    if (!order) return; /* opened directly: the general text stays */
    /* one bottle: "Your blend is…", more: "Your blends are…" */
    var bottles = order.lines.reduce(function (n, l) { return n + l.qty; }, 0);
    if (bottles === 1) {
      box.querySelectorAll('[data-one]').forEach(function (el) { el.textContent = el.getAttribute('data-one'); });
    }
    if (order.firstName) {
      box.querySelector('[data-thanks-title]').textContent = 'Thank you, ' + order.firstName + '!';
    }
    var refBtn = box.querySelector('[data-thanks-ref]');
    var hint = box.querySelector('[data-copy-hint]');
    refBtn.textContent = order.ref;
    refBtn.setAttribute('aria-label', 'Order number ' + order.ref + ', click to copy');
    refBtn.addEventListener('click', function () {
      copyText(order.ref).then(function (ok) {
        hint.textContent = ok ? 'Copied ✓' : 'Select the number to copy it';
        refBtn.classList.toggle('is-copied', ok);
        setTimeout(function () {
          hint.textContent = 'Click the number to copy it';
          refBtn.classList.remove('is-copied');
        }, 2200);
      });
    });
    box.querySelector('[data-thanks-lines]').innerHTML =
      order.lines.map(function (l) {
        var label = l.qty + ' × ' + esc(l.name) + (l.size ? ' (' + esc(l.size) + ')' : '');
        var page = PRODUCTS[l.id] ? ROOT + PRODUCTS[l.id].url : '';
        return '<li>' + (page ? '<a href="' + esc(page) + '">' + label + '</a>' : '<span>' + label + '</span>') +
               '<span>' + money(l.total) + '</span></li>';
      }).join('') +
      '<li><span>Subtotal</span><span>' + money(order.subtotal) + '</span></li>' +
      (order.postageRegion
        ? '<li><span>Postage, ' + esc(order.postageRegion) + '</span><span>' + money(order.postage) + '</span></li>' +
          '<li class="th-sub"><span>Total</span><span>' + money(order.total) + '</span></li>'
        : '');
    box.querySelector('[data-thanks-order]').hidden = false;
  }

  /* copy to the clipboard, with an older fallback for browsers without the API */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return false; });
    }
    var area = document.createElement('textarea');
    area.value = text; area.setAttribute('readonly', '');
    area.style.cssText = 'position:fixed;left:-9999px';
    document.body.appendChild(area); area.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(area);
    return Promise.resolve(ok);
  }

  /* ---------- 8. Start ---------- */
  function start() {
    PRODUCTS = window.TOS_PRODUCTS || {};
    POSTAGE = (window.TOS_POSTAGE && window.TOS_POSTAGE.regions) || [];
    buildChrome();
    bindProductPage();
    bindCheckout();
    bindThanks();
    render();
    /* keep several open tabs in step */
    window.addEventListener('storage', function (e) { if (e.key === SETTINGS.cartKey) render(); });
  }

  var needsCss = !document.querySelector('link[href$="css/shop.css"]');
  Promise.all([
    needsCss ? loadOnce('link', { rel: 'stylesheet', href: ROOT + 'css/shop.css' }) : null,
    window.TOS_PRODUCTS ? null : loadOnce('script', { src: ROOT + 'js/shop-data.js' }),
    window.TOS_POSTAGE ? null : loadOnce('script', { src: ROOT + 'js/shop-postage.js' })
  ]).then(start, start);
})();
