// SAC Technology Studio — progressive enhancement without dependencies.
document.documentElement.classList.add('js');
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
if (menuToggle && nav) {
  const closeMenu = () => {
    nav.classList.remove('nav-open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Abrir menú');
  };
  menuToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('nav-open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('nav-open')) {
      closeMenu();
      menuToggle.focus();
    }
  });
  window.addEventListener('resize', () => { if (window.innerWidth > 760) closeMenu(); });
}

const tabs = [...document.querySelectorAll('.process-tab')];
const panels = [...document.querySelectorAll('.process-panel')];
const progressBar = document.querySelector('.progress-bar');
if (tabs.length && tabs.length === panels.length && progressBar) {
  const activateStep = (index, focus = false) => {
    tabs.forEach((tab, i) => {
      const selected = i === index;
      tab.classList.toggle('active', selected);
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focus) tab.focus();
    });
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
    progressBar.style.width = `${((index + 1) / tabs.length) * 100}%`;
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activateStep(index));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); activateStep(next, true); }
    });
  });
}

// Read campaign data only from the current URL; no cookies or persistent attribution.
const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
const campaign = new URLSearchParams(window.location.search);
const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');
if (form) {
  utmKeys.forEach(key => {
    const input = form.elements.namedItem(key);
    if (input) input.value = (campaign.get(key) || '').slice(0, 200);
  });
  // Keep the native POST, validation and CAPTCHA. No preventDefault or AJAX.
  form.addEventListener('submit', () => {
    if (status) status.textContent = 'Continuando a la verificación segura de FormSubmit…';
    window.SACAnalytics?.markSubmission(form.dataset.service || 'inicio');
  });
  window.addEventListener('pageshow', () => {
    if (status) status.textContent = 'Al continuar, FormSubmit verificará el envío para protegernos del spam.';
  });
}
// Preserve explicit campaign parameters when a visitor explores another service.
document.querySelectorAll('a[href]').forEach(link => {
  const url = new URL(link.href, window.location.href);
  if (url.origin !== window.location.origin || !(url.pathname.startsWith('/servicios/') || url.pathname === '/direccion-ia')) return;
  utmKeys.forEach(key => {
    if (campaign.has(key)) url.searchParams.set(key, campaign.get(key).slice(0, 200));
  });
  link.href = url.href;
});
const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();
