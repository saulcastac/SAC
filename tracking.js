/* SAC · consentimiento de cookies + Meta Pixel.
 * Inactivo mientras PIXEL_ID esté vacío: sin banner, sin red, sin cookies.
 * Con PIXEL_ID: muestra un banner (Aceptar / Rechazar con el mismo peso) y solo
 * tras aceptar carga fbevents.js. La decisión se guarda 180 días y se puede
 * cambiar desde cualquier elemento [data-cookie-settings].
 * Debe cargarse ANTES de analytics.js y de diagnostico.js (los tres con defer).
 */
(() => {
  'use strict';
  const PIXEL_ID = '1623068712365231';
  const KEY = 'sac:consent:v1';
  const MAX_AGE = 180 * 24 * 60 * 60 * 1000;

  if (!/^\d{10,20}$/.test(PIXEL_ID)) {
    window.SACTrack = () => {};
    return;
  }
  // Habilita el puente de analytics.js; sigue sin emitir nada hasta setConsent(true).
  window.SAC_ANALYTICS_CONFIG = { enabled: true };

  const STANDARD = new Set(['PageView', 'ViewContent', 'Lead', 'Schedule', 'Contact']);
  const read = () => {
    try {
      const v = JSON.parse(localStorage.getItem(KEY));
      if (v && (v.s === 'granted' || v.s === 'denied') && Date.now() - v.t < MAX_AGE) return v.s;
    } catch { /* almacenamiento bloqueado: se vuelve a preguntar */ }
    return null;
  };
  const save = (s) => {
    try { localStorage.setItem(KEY, JSON.stringify({ s, t: Date.now() })); } catch { /* opcional */ }
  };

  let state = read();
  let loaded = false;
  const queue = [];

  const send = (event, data) => window.fbq(STANDARD.has(event) ? 'track' : 'trackCustom', event, data || {});

  function load() {
    if (loaded) { window.fbq('consent', 'grant'); return; }
    loaded = true;
    /* Código base oficial de Meta */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', PIXEL_ID);
    window.fbq('track', 'PageView');
    queue.splice(0).forEach(([e, d]) => send(e, d));
  }

  function revoke() {
    queue.length = 0;
    if (loaded) window.fbq('consent', 'revoke');
    // Borra las cookies propias de Meta en este dominio.
    const host = location.hostname.replace(/^www\./, '');
    for (const name of ['_fbp', '_fbc']) {
      for (const domain of ['', `; domain=${host}`, `; domain=.${host}`]) {
        document.cookie = `${name}=; Max-Age=0; path=/${domain}`;
      }
    }
  }

  /* API pública: el diagnóstico y el puente usan esto en lugar de llamar fbq. */
  window.SACTrack = (event, data) => {
    if (state === 'granted' && loaded) send(event, data);
    else if (state === null && queue.length < 20) queue.push([event, data]);
  };

  /* Puente analytics.js → eventos de Meta (sin datos personales). */
  window.addEventListener('sac:analytics', (e) => {
    const d = e.detail || {};
    // Lead solo con el retorno a gracias tras un envío (contact_completed); el intento va aparte.
    if (d.event === 'contact_completed') window.SACTrack('Lead', { content_name: `contacto_${d.service || 'inicio'}` });
    else if (d.event === 'contact_submit') window.SACTrack('SubmitAttempt', { content_name: `contacto_${d.service || 'inicio'}` });
    else if (d.event === 'whatsapp_click') window.SACTrack('Contact', { content_name: d.service || 'inicio' });
    else if (d.event === 'cta_click') window.SACTrack('CTAClick', { placement: d.placement || '', content_name: d.service || 'inicio' });
    // PageView ya lo envía load(); ViewContent distingue la oferta de dirección de IA (servicio y landing).
    else if (d.event === 'landing_view' && d.service === 'fractional-caio') window.SACTrack('ViewContent', { content_name: 'fractional-caio', content_category: d.landing || '' });
  });

  /* ---------- Banner ---------- */
  const css = `
.sac-cc{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;max-width:560px;margin:0 auto;
  background:#101312;color:#f5f5ef;border:1px solid rgba(245,245,239,.16);border-radius:14px;padding:18px 18px 16px;
  font:400 14px/1.5 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;box-shadow:0 18px 50px rgba(0,0,0,.35)}
.sac-cc p{margin:0 0 14px}
.sac-cc a{color:#a4f47b;text-decoration:underline}
.sac-cc-actions{display:flex;gap:10px;flex-wrap:wrap}
.sac-cc button{flex:1 1 140px;min-height:44px;border-radius:999px;font-family:inherit;font-weight:600;font-size:14px;line-height:1;cursor:pointer;
  border:1px solid #f5f5ef;background:transparent;color:#f5f5ef}
.sac-cc button[data-cc="granted"]{background:#a4f47b;border-color:#a4f47b;color:#101312}
.sac-cc button:focus-visible{outline:2px solid #a4f47b;outline-offset:2px}
[data-cookie-settings]{background:none;border:0;padding:0;color:inherit;font:inherit;text-decoration:inherit;cursor:pointer}`;

  let banner = null;
  function showBanner() {
    if (banner) { banner.hidden = false; banner.querySelector('button').focus(); return; }
    banner = document.createElement('div');
    banner.className = 'sac-cc';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-label', 'Preferencias de cookies');
    banner.innerHTML = '<p>Usamos cookies de Meta para saber qué anuncios te trajeron aquí y mejorar a quién se los mostramos. Solo se activan si aceptas. <a href="/privacidad.html#cookies">Más información</a>.</p>'
      + '<div class="sac-cc-actions"><button type="button" data-cc="denied">Rechazar</button><button type="button" data-cc="granted">Aceptar</button></div>';
    banner.addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-cc]');
      if (!btn) return;
      decide(btn.dataset.cc);
      banner.hidden = true;
    });
    document.body.appendChild(banner);
  }

  function decide(s) {
    state = s;
    save(s);
    if (s === 'granted') {
      load();
      window.SACAnalytics?.setConsent(true);
    } else {
      revoke();
      window.SACAnalytics?.setConsent(false);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
    document.querySelectorAll('[data-cookie-settings]').forEach((el) => {
      el.hidden = false;
      el.addEventListener('click', (e) => { e.preventDefault(); showBanner(); });
    });
    if (state === 'granted') { load(); window.SACAnalytics?.setConsent(true); }
    else if (state === null) showBanner();
  });
})();
