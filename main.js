// SAC Technology Studio — JavaScript sin dependencias.

const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
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
window.addEventListener('resize', () => { if (window.innerWidth > 760) closeMenu(); });

const tabs = [...document.querySelectorAll('.process-tab')];
const panels = [...document.querySelectorAll('.process-panel')];
const progressBar = document.querySelector('.progress-bar');
function activateStep(index, focus = false) {
  tabs.forEach((tab, i) => {
    const selected = i === index;
    tab.classList.toggle('active', selected);
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
    if (selected && focus) tab.focus();
  });
  panels.forEach((panel, i) => { panel.hidden = i !== index; });
  progressBar.style.width = `${((index + 1) / tabs.length) * 100}%`;
}
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

// Native POST keeps FormSubmit's CAPTCHA and works without JavaScript.
const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');
form.addEventListener('submit', () => {
  status.textContent = 'Continuando a la verificación segura de FormSubmit…';
});
window.addEventListener('pageshow', () => {
  status.textContent = 'Al continuar, FormSubmit verificará el envío para protegernos del spam.';
});

document.getElementById('year').textContent = new Date().getFullYear();
