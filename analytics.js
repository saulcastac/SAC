/* Future analytics bridge. No vendor SDK, identifiers, cookies or network calls.
 * Wire a consent manager and an approved adapter before enabling measurement.
 */
(() => {
  'use strict';
  const enabled = window.SAC_ANALYTICS_CONFIG?.enabled === true;
  let consent = false;
  const pendingKey = 'sac:pending-contact';
  const service = document.body.dataset.service || (location.pathname.endsWith('/gracias.html') ? 'confirmacion' : 'inicio');
  const campaign = {};
  for (const key of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']) {
    const value = new URLSearchParams(location.search).get(key);
    if (value) campaign[key] = value.slice(0, 200);
  }
  const emit = (event, detail = {}) => {
    if (!enabled || !consent) return;
    // Never include form values, email, name, message, full URL or arbitrary query params.
    window.dispatchEvent(new CustomEvent('sac:analytics', {
      detail: { event, service, landing: location.pathname, ...campaign, ...detail }
    }));
  };
  const completion = () => {
    if (!enabled || !consent || !location.pathname.endsWith('/gracias.html')) return;
    try {
      const raw = sessionStorage.getItem(pendingKey);
      sessionStorage.removeItem(pendingKey);
      if (!raw) return;
      const pending = JSON.parse(raw);
      const age = Date.now() - pending.time;
      if (age >= 0 && age < 30 * 60 * 1000) {
        emit('contact_completed', { service: pending.service, landing: pending.landing, ...pending.campaign });
      }
    } catch { /* A blocked browser store must never break contact. */ }
  };
  window.SACAnalytics = Object.freeze({
    setConsent(granted) {
      const changed = consent !== (granted === true);
      consent = granted === true;
      if (!consent) {
        try { sessionStorage.removeItem(pendingKey); } catch { /* optional storage */ }
      }
      if (consent && changed && enabled) { emit('landing_view'); completion(); }
    },
    markSubmission(originService) {
      if (!enabled || !consent) return;
      emit('contact_submit', { service: originService });
      try {
        sessionStorage.setItem(pendingKey, JSON.stringify({ service: originService, landing: location.pathname, campaign, time: Date.now() }));
      } catch { /* No measurement when storage is unavailable. */ }
    }
  });
  document.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    if (link.dataset.cta) emit('cta_click', { placement: link.dataset.cta });
    if (new URL(link.href, location.href).hostname === 'wa.me') emit('whatsapp_click');
  });
})();
