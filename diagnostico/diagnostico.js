/* Diagnóstico IA SAC — prototipo (todo corre en el navegador).
   Pendiente de conectar: CONFIG.leadEndpoint (CRM/email), CONFIG.bookingUrl (Cal.com) y píxeles. */
(() => {
  const CONFIG = {
    // HubSpot Forms API (pública, sin llaves secretas). Ver docs/hubspot-diagnostico.md
    hubspot: {
      portalId: '52351349',    // Cuenta HubSpot "SAC"
      formId: '1ff7b757-e186-4977-8121-fe5dba9ecabc', // formulario "Diagnóstico IA"
      host: 'api.hsforms.com', // cuentas en la UE: 'api-eu1.hsforms.com'
    },
    bookingUrl: 'https://meetings.hubspot.com/saulcastac', // enlace de reuniones de HubSpot
  };
  const HS_READY = !!(CONFIG.hubspot.portalId && CONFIG.hubspot.formId);

  /* ---------- Variantes de titular (message-match con cada reel/anuncio) ---------- */
  const VARIANTS = {
    roi: {
      h1: 'Descubre en 3 minutos dónde la IA <em>sí le deja dinero</em> a tu empresa.',
    },
    ep03: {
      h1: '¿Quieres usar IA pero <em>no sabes ni qué pedirle?</em> Empieza por aquí.',
    },
  };

  /* ---------- Preguntas ---------- */
  const QUESTIONS = [
    { id: 'giro', title: '¿A qué se dedica tu empresa?', type: 'single', options: [
      ['manufactura', 'Manufactura'], ['distribucion', 'Distribución y logística'], ['comercio', 'Comercio o retail'],
      ['servicios', 'Servicios profesionales'], ['salud', 'Salud'], ['construccion', 'Construcción o inmobiliario'], ['otro', 'Otro'] ] },
    { id: 'tamano', title: '¿Cuántas personas trabajan ahí?', type: 'single', options: [
      ['1-10', '1 a 10'], ['11-50', '11 a 50'], ['51-200', '51 a 200'], ['200+', 'Más de 200'] ] },
    { id: 'rol', title: '¿Cuál es tu rol?', type: 'single', options: [
      ['dueno', 'Dueño o director general'], ['gerente', 'Director o gerente de área'], ['ops', 'Operaciones o TI'], ['otro', 'Otro'] ] },
    { id: 'areas', title: '¿Qué áreas se comen más tiempo de tu equipo?', help: 'Elige hasta 3.', type: 'multi', max: 3, options: [
      ['facturacion', 'Facturación y cobranza'], ['ventas', 'Ventas y seguimiento a clientes'], ['atencion', 'Atención a clientes'],
      ['reportes', 'Reportes y juntas'], ['inventario', 'Inventario y compras'], ['rh', 'RH y nómina'], ['operacion', 'Operación o producción'] ] },
    { id: 'horas', title: '¿Cuántas horas a la semana se van, entre todo el equipo, en tareas repetitivas?', help: 'Capturar datos, copiar y pegar, armar reportes, contestar lo mismo una y otra vez.', type: 'single', options: [
      ['<5', 'Menos de 5'], ['5-20', '5 a 20'], ['20-50', '20 a 50'], ['50+', 'Más de 50'], ['nose', 'No sé'] ] },
    { id: 'datos', title: '¿Dónde vive la información de tu negocio?', type: 'single', options: [
      ['excel', 'Excel y papel'], ['basico', 'Un sistema contable o administrativo básico'], ['erp', 'Un ERP o CRM conectado'], ['mezcla', 'Un poco de todo'] ] },
    { id: 'ia', title: '¿Qué han hecho con IA hasta hoy?', type: 'single', options: [
      ['nada', 'Nada todavía'], ['individual', 'Algunos usan ChatGPT por su cuenta'], ['pilotos', 'Probamos algo y no vimos resultados'], ['resultados', 'Ya tenemos algo funcionando con resultados medibles'] ] },
    { id: 'freno', title: '¿Qué es lo que más te frena?', type: 'single', options: [
      ['empezar', 'No sé por dónde empezar'], ['confianza', 'No confío en los resultados'], ['equipo', 'Mi equipo no sabe usarla'], ['costo', 'El costo'], ['datos', 'Mis datos están desordenados'] ] },
    { id: 'dolor', title: 'Si pudieras quitarte un dolor de cabeza en los próximos 90 días, ¿cuál sería?', help: 'Opcional. Con tus palabras.', type: 'text', placeholder: 'Ej. "Que las cotizaciones no se queden sin seguimiento"' },
    { id: 'cuando', title: '¿Para cuándo te gustaría tener algo funcionando?', type: 'single', options: [
      ['trimestre', 'Este trimestre'], ['semestre', 'Este semestre'], ['explorando', 'Solo estoy explorando'] ] },
  ];

  /* ---------- Biblioteca de procesos (PENDIENTE: validar con la metodología SAC) ---------- */
  const PROCESSES = {
    facturacion: { title: 'Captura y conciliación automática de facturas', impact: 3, ease: 3,
      desc: 'Leer facturas y comprobantes, capturarlos en tu sistema y conciliarlos contra pagos sin que alguien los teclee uno por uno.',
      tomorrow: 'Anota cuántas facturas captura tu equipo en un día normal y cuántos minutos toma cada una. Ese número es tu línea base para medir el ahorro.',
      case: 'Caso Vax Solutions: 250–300 facturas/día · ~16 h/semana ahorradas' },
    ventas: { title: 'Seguimiento automático a cotizaciones y prospectos', impact: 3, ease: 2,
      desc: 'Recordatorios y mensajes de seguimiento que salen solos, y un resumen de cada oportunidad para que ninguna cotización se quede olvidada.',
      tomorrow: 'Saca la lista de cotizaciones de los últimos 30 días y marca cuántas nunca recibieron un segundo contacto. Ahí está dinero sobre la mesa.' },
    atencion: { title: 'Respuestas a preguntas frecuentes por WhatsApp', impact: 2, ease: 3,
      desc: 'Un asistente que contesta lo repetitivo (horarios, precios, estatus de pedidos) y pasa a una persona lo que de verdad lo necesita.',
      tomorrow: 'Pide a tu equipo las 10 preguntas que más contestan y pídele a una IA que redacte una respuesta clara para cada una. Ya tienes tu primera base de conocimiento.' },
    reportes: { title: 'Reporte semanal que se arma solo', impact: 2, ease: 3,
      desc: 'Tomar los datos de tus hojas o sistema y entregar cada lunes el reporte con los números que importan, sin que alguien lo arme a mano.',
      tomorrow: 'Escribe las 5 cifras que de verdad revisas cada semana. Si un reporte tiene más que eso, la mitad sobra.' },
    inventario: { title: 'Alertas de reorden y comparación de cotizaciones', impact: 2, ease: 2,
      desc: 'Avisos cuando un producto baja de su mínimo y comparación automática de cotizaciones de proveedores para decidir más rápido.',
      tomorrow: 'Identifica tus 10 productos o insumos que más se agotan y define su punto mínimo. Es la base de cualquier automatización de compras.' },
    rh: { title: 'Filtro de candidatos y respuestas a dudas internas', impact: 1, ease: 3,
      desc: 'Preclasificar CVs contra el perfil del puesto y contestar dudas frecuentes del equipo (vacaciones, nómina, políticas) sin interrumpir a RH.',
      tomorrow: 'Junta en un documento las políticas que más te preguntan. Con eso una IA ya puede responder la mayoría de las dudas.' },
    operacion: { title: 'Bitácoras y reportes de incidencias por voz o foto', impact: 2, ease: 2,
      desc: 'Que el personal reporte avances o problemas con un audio o una foto, y que eso se convierta en un registro ordenado y en alertas.',
      tomorrow: 'Pregunta a tu equipo de operación qué información capturan dos veces (en papel y luego en sistema). Ese es tu primer candidato.' },
  };
  const FALLBACK = ['reportes', 'atencion', 'ventas', 'facturacion'];

  /* ---------- Perfiles ---------- */
  const PROFILES = {
    mina:      { name: 'Mina sin explotar', desc: 'Hay mucho que ganar en tu operación, pero primero hay que ordenar la información y elegir bien qué atacar. Bien enfocado, aquí es donde se ven los retornos más rápidos.' },
    escalar:   { name: 'Listo para escalar', desc: 'Tienes dolores claros y bases para automatizar. El siguiente paso es un proyecto con retorno medible, no más pruebas sueltas.' },
    explorador:{ name: 'Explorador', desc: 'Todavía no hay un dolor urgente, y eso es una ventaja: puedes preparar a tu equipo para usar IA bien antes de que la necesites.' },
    afinador:  { name: 'Afinador', desc: 'Ya tienes herramientas y datos; el valor está en usarlas mejor. Capacitación y ajustes puntuales pueden multiplicar lo que ya tienes.' },
  };

  /* ---------- Cálculo ---------- */
  function compute(a) {
    const areas = a.areas || [];
    const size = { '1-10': 10, '11-50': 25, '51-200': 35, '200+': 40 }[a.tamano] || 10;
    const hrsPts = { '<5': 5, '5-20': 15, '20-50': 25, '50+': 30, nose: 15 }[a.horas] || 5;
    const potencial = Math.min(100, size + Math.min(30, areas.length * 10) + hrsPts);
    const datos = { excel: 10, basico: 25, erp: 45, mezcla: 20 }[a.datos] || 10;
    const ia = { nada: 5, individual: 20, pilotos: 30, resultados: 55 }[a.ia] || 5;
    const preparacion = Math.min(100, datos + ia);

    const hi = potencial >= 50, ready = preparacion >= 50;
    const profileKey = hi ? (ready ? 'escalar' : 'mina') : (ready ? 'afinador' : 'explorador');

    let hours = null;
    const mid = { '<5': 3, '5-20': 12, '20-50': 35, '50+': 60 }[a.horas];
    if (mid) {
      const factor = Math.min(0.45, 0.3 + areas.length * 0.05);
      const base = mid * 4.3 * factor;
      const r5 = (n) => Math.max(1, Math.round(n / 5) * 5);
      hours = [r5(base * 0.7), r5(base * 1.3)];
      if (hours[0] === hours[1]) hours[1] += 5;
    }

    // Top 3: áreas elegidas, ordenadas por impacto y facilidad (si la preparación es baja, pesa más la facilidad)
    const wEase = ready ? 1 : 1.5;
    const ranked = areas
      .map((k) => ({ k, s: PROCESSES[k].impact + PROCESSES[k].ease * wEase }))
      .sort((x, y) => y.s - x.s)
      .map((x) => x.k);
    for (const k of FALLBACK) if (ranked.length < 3 && !ranked.includes(k)) ranked.push(k);
    const top = ranked.slice(0, 3);

    const big = a.tamano && a.tamano !== '1-10';
    const decides = a.rol === 'dueno' || a.rol === 'gerente';
    const temperatura = big && decides && a.cuando === 'trimestre' ? 'caliente'
      : (big || a.cuando === 'semestre') ? 'tibio' : 'frio';

    return { potencial, preparacion, profileKey, hours, top, temperatura };
  }

  /* ---------- Medición (Meta Pixel / GA4 cuando existan) ---------- */
  function track(event, data = {}) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event, ...data });
    if (typeof window.fbq === 'function') {
      const std = { ViewContent: 1, Lead: 1, Schedule: 1 };
      window.fbq(std[event] ? 'track' : 'trackCustom', event, data);
    }
    if (typeof window.gtag === 'function') window.gtag('event', event, data);
  }

  /* ---------- Estado ---------- */
  const params = new URLSearchParams(location.search);
  const variant = VARIANTS[params.get('v')] ? params.get('v') : 'roi';
  const utm = {};
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach((k) => { if (params.get(k)) utm[k] = params.get(k); });

  const state = { i: 0, answers: {}, lead: null, result: null };

  const $ = (s) => document.querySelector(s);
  const quiz = $('#quiz'), body = $('#quiz-body'), bar = $('#progress-bar'), ptext = $('#progress-text');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // Titular según variante
  $('#hero-title').innerHTML = VARIANTS[variant].h1;
  $('#year').textContent = new Date().getFullYear();
  track('ViewContent', { content_name: 'diagnostico_ia', variant });

  /* ---------- Abrir / cerrar ---------- */
  let started = false;
  function openQuiz() {
    quiz.hidden = false;
    document.body.classList.add('locked');
    if (!started) { started = true; track('StartDiagnostic', { variant }); }
    render();
  }
  function closeQuiz() {
    if (state.result) { quiz.hidden = true; document.body.classList.remove('locked'); return; }
    if (state.i > 0 && !confirm('¿Salir del diagnóstico? Perderás tus respuestas.')) return;
    quiz.hidden = true;
    document.body.classList.remove('locked');
  }
  document.querySelectorAll('.js-start').forEach((b) => b.addEventListener('click', openQuiz));
  $('#quiz-close').addEventListener('click', closeQuiz);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !quiz.hidden) closeQuiz(); });

  function setProgress(step, total, label) {
    bar.style.width = `${Math.round((step / total) * 100)}%`;
    ptext.textContent = label;
  }

  /* ---------- Render ---------- */
  function render() {
    if (state.result) return renderResult();
    if (state.i >= QUESTIONS.length) return renderGate();
    const q = QUESTIONS[state.i];
    setProgress(state.i + 1, QUESTIONS.length + 1, `${state.i + 1} / ${QUESTIONS.length}`);
    const val = state.answers[q.id];
    let inner = '';
    if (q.type === 'text') {
      inner = `<textarea class="q-text" id="q-input" maxlength="400" placeholder="${esc(q.placeholder || '')}">${esc(val || '')}</textarea>`;
    } else {
      inner = `<div class="opts" role="group" aria-labelledby="q-title">${q.options.map(([v, l], n) => {
        const on = q.type === 'multi' ? (val || []).includes(v) : val === v;
        return `<button type="button" class="opt" data-v="${v}" aria-pressed="${on}"><span class="key">${String.fromCharCode(65 + n)}</span>${esc(l)}</button>`;
      }).join('')}</div>`;
    }
    const needsNext = q.type !== 'single';
    const nextLabel = q.type === 'text' ? (val ? 'Continuar' : 'Omitir') : 'Continuar';
    body.innerHTML = `<div class="step">
      <p class="q-kicker">PREGUNTA ${state.i + 1} DE ${QUESTIONS.length}</p>
      <h2 class="q-title" id="q-title">${esc(q.title)}</h2>
      ${q.help ? `<p class="q-help">${esc(q.help)}</p>` : '<div style="height:16px"></div>'}
      ${inner}
      <div class="q-nav">
        <button type="button" class="back" id="q-back" ${state.i === 0 ? 'hidden' : ''}>← Atrás</button>
        ${needsNext ? `<button type="button" class="btn btn-lime" id="q-next" ${q.type === 'multi' && !(val || []).length ? 'disabled' : ''}>${nextLabel} <span aria-hidden="true">→</span></button>` : ''}
      </div></div>`;

    $('#q-back').addEventListener('click', () => { state.i--; render(); });
    if (q.type === 'text') {
      const input = $('#q-input');
      const next = $('#q-next');
      input.addEventListener('input', () => {
        state.answers[q.id] = input.value.trim();
        next.firstChild.textContent = input.value.trim() ? 'Continuar ' : 'Omitir ';
      });
      next.addEventListener('click', advance);
      input.focus();
      return;
    }
    body.querySelectorAll('.opt').forEach((btn) => btn.addEventListener('click', () => {
      const v = btn.dataset.v;
      if (q.type === 'single') {
        if (state.busy) return;
        state.busy = true;
        state.answers[q.id] = v;
        body.querySelectorAll('.opt').forEach((b) => b.setAttribute('aria-pressed', b === btn));
        setTimeout(() => { state.busy = false; advance(); }, 220);
      } else {
        const arr = state.answers[q.id] = state.answers[q.id] || [];
        const at = arr.indexOf(v);
        if (at >= 0) arr.splice(at, 1);
        else if (arr.length < q.max) arr.push(v);
        body.querySelectorAll('.opt').forEach((b) => b.setAttribute('aria-pressed', arr.includes(b.dataset.v)));
        $('#q-next').disabled = !arr.length;
      }
    }));
    if (needsNext) $('#q-next').addEventListener('click', advance);
    body.querySelector('.opt').focus({ preventScroll: true });
  }

  function advance() {
    state.i++;
    quiz.scrollTo(0, 0);
    render();
  }

  // Atajos de teclado A, B, C…
  document.addEventListener('keydown', (e) => {
    if (quiz.hidden || state.result || state.i >= QUESTIONS.length) return;
    if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') return;
    const n = e.key.toUpperCase().charCodeAt(0) - 65;
    const opts = body.querySelectorAll('.opt');
    if (e.key.length === 1 && n >= 0 && n < opts.length) opts[n].click();
  });

  /* ---------- Gate ---------- */
  function renderGate() {
    setProgress(QUESTIONS.length, QUESTIONS.length + 1, 'Listo');
    const l = state.lead || {};
    body.innerHTML = `<div class="step gate">
      <p class="q-kicker">ÚLTIMO PASO</p>
      <h2>Tu diagnóstico está listo.</h2>
      <p>¿A dónde te mandamos tu Radar de IA completo? Verás el resultado aquí mismo en cuanto continúes.</p>
      <form id="gate" novalidate>
        <div class="field"><label for="f-nombre">Nombre y apellido</label><input id="f-nombre" name="nombre" autocomplete="name" required value="${esc(l.nombre || '')}" /><span class="err" id="e-nombre"></span></div>
        <div class="field"><label for="f-email">Email de trabajo</label><input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required value="${esc(l.email || '')}" /><span class="err" id="e-email"></span></div>
        <div class="field"><label for="f-empresa">Empresa</label><input id="f-empresa" name="empresa" autocomplete="organization" required value="${esc(l.empresa || '')}" /><span class="err" id="e-empresa"></span></div>
        <div class="field"><label for="f-whatsapp">WhatsApp <small>(opcional)</small></label><input id="f-whatsapp" name="whatsapp" type="tel" autocomplete="tel" inputmode="tel" placeholder="33 1234 5678" value="${esc(l.whatsapp || '')}" /></div>
        <div class="hp" aria-hidden="true"><label>No llenar<input name="website" tabindex="-1" autocomplete="off" /></label></div>
        <label class="consent"><input type="checkbox" id="f-consent" required /><span>Acepto recibir mi diagnóstico y comunicaciones de SAC. Consulta el <a href="../privacidad.html" target="_blank" rel="noopener">aviso de privacidad</a>.</span></label>
        <span class="err" id="e-consent"></span>
        <button class="btn btn-lime" type="submit" id="gate-submit">Ver mi diagnóstico <span aria-hidden="true">→</span></button>
      </form>
      <div class="q-nav"><button type="button" class="back" id="q-back">← Revisar respuestas</button></div>
    </div>`;
    $('#q-back').addEventListener('click', () => { state.i = QUESTIONS.length - 1; render(); });
    $('#gate').addEventListener('submit', onSubmit);
    $('#f-nombre').focus();
  }

  async function onSubmit(e) {
    e.preventDefault();
    const f = e.target;
    const data = {
      nombre: f.nombre.value.trim(), email: f.email.value.trim(),
      empresa: f.empresa.value.trim(), whatsapp: f.whatsapp.value.trim(),
    };
    const errs = {
      nombre: data.nombre ? '' : 'Escribe tu nombre.',
      email: /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email) ? '' : 'Revisa tu email.',
      empresa: data.empresa ? '' : 'Escribe el nombre de tu empresa.',
      consent: $('#f-consent').checked ? '' : 'Necesitamos tu autorización para enviarte el diagnóstico.',
    };
    let ok = true;
    for (const k in errs) {
      $(`#e-${k}`).textContent = errs[k];
      const input = $(`#f-${k}`);
      if (input && k !== 'consent') input.setAttribute('aria-invalid', !!errs[k]);
      if (errs[k]) ok = false;
    }
    if (!ok) return;
    if (f.website.value) return; // honeypot

    state.lead = data;
    const result = compute(state.answers);
    const payload = {
      ...data, answers: state.answers, variant, utm,
      perfil: result.profileKey, potencial: result.potencial, preparacion: result.preparacion,
      horas: result.hours, top: result.top, temperatura: result.temperatura,
      fecha: new Date().toISOString(),
    };

    const btn = $('#gate-submit');
    btn.disabled = true;
    btn.firstChild.textContent = 'Preparando tu Radar… ';
    try {
      if (HS_READY) {
        await sendToHubSpot(payload, result);
      } else {
        console.info('[Diagnóstico SAC · prototipo] Lead que se enviaría al CRM:', payload);
        try { localStorage.setItem('sac_diag_last', JSON.stringify(payload)); } catch (_) {}
      }
    } catch (err) {
      console.warn('No se pudo registrar el lead', err); // se muestra el resultado de todos modos
    }
    track('Lead', { content_name: 'diagnostico_ia', perfil: result.profileKey, temperatura: result.temperatura, variant });
    state.result = result;
    quiz.scrollTo(0, 0);
    render();
  }

  /* ---------- HubSpot ---------- */
  // Convierte las respuestas en texto legible para el registro del contacto.
  function answersText(a) {
    return QUESTIONS.map((q) => {
      let v = a[q.id];
      if (v == null || v === '' || (Array.isArray(v) && !v.length)) v = '—';
      else if (q.options) {
        const label = (x) => (q.options.find(([k]) => k === x) || [x, x])[1];
        v = Array.isArray(v) ? v.map(label).join(', ') : label(v);
      }
      return `${q.title}\n→ ${v}`;
    }).join('\n\n');
  }

  // Explica en lenguaje simple qué respuestas movieron cada puntaje (va al correo del reporte).
  function explain(a, r) {
    const label = (id, v) => { const q = QUESTIONS.find((x) => x.id === id); return ((q.options || []).find(([k]) => k === v) || [v, v])[1]; };
    const areas = (a.areas || []).map((v) => label('areas', v).toLowerCase());
    const areasTxt = areas.length ? `${areas.length === 1 ? 'un área que les quita' : areas.length + ' áreas que les quitan'} tiempo (${areas.join(', ')})` : 'sin un área crítica identificada';
    const horasTxt = { '<5': 'menos de 5 h/semana', '5-20': 'entre 5 y 20 h/semana', '20-50': 'entre 20 y 50 h/semana', '50+': 'más de 50 h/semana', nose: 'horas aún sin medir' }[a.horas] || 'horas sin dato';
    const datosTxt = { excel: 'Excel y papel', basico: 'un sistema contable o administrativo básico', erp: 'un ERP o CRM conectado', mezcla: 'una mezcla de Excel, papel y sistemas' }[a.datos] || 'sin dato';
    const iaTxt = { nada: 'todavía no han usado IA', individual: 'la IA se usa de forma individual, sin un proceso del equipo', pilotos: 'ya probaron IA pero sin resultados medibles', resultados: 'ya tienen IA funcionando con resultados' }[a.ia] || '';
    const lines = [
      `Potencial ${r.potencial}/100: equipo de ${label('tamano', a.tamano).toLowerCase()} personas, ${horasTxt} en tareas repetitivas y ${areasTxt}.`,
      `Preparación ${r.preparacion}/100: su información vive en ${datosTxt} y ${iaTxt}.`,
      `Con potencial ${r.potencial >= 50 ? 'alto' : 'bajo'} y preparación ${r.preparacion >= 50 ? 'alta' : 'baja'}, el perfil es "${PROFILES[r.profileKey].name}": ${PROFILES[r.profileKey].desc}`,
    ];
    if (r.hours) lines[2] += ` Las horas recuperables (${r.hours[0]}–${r.hours[1]} h/mes) se estiman con un 30–45 % de automatización sobre las horas que reportaste; las validamos con tu operación real en la sesión.`;
    return lines; // [potencial, preparación, perfil + horas]
  }

  const processText = (k, n) => {
    const pr = PROCESSES[k];
    return `${n + 1}) ${pr.title}. ${pr.desc}${pr.case ? ` (${pr.case}.)` : ''}`;
  };

  async function sendToHubSpot(payload, r) {
    const f = (name, value, objectTypeId = '0-1') => ({ objectTypeId, name, value: String(value) });
    const why = explain(payload.answers, r);
    const utmText = Object.entries(payload.utm).map(([k, v]) => `${k}=${v}`).join(' · ') || 'sin UTM';
    const fields = [
      ...(() => {
        const [first, ...rest] = payload.nombre.split(/\s+/);
        return rest.length ? [f('firstname', first), f('lastname', rest.join(' '))] : [f('firstname', first)];
      })(),
      f('email', payload.email),
      f('name', payload.empresa, '0-2'), // "Nombre de la empresa" del formulario = registro de Empresa
      f('sac_diag_perfil', PROFILES[r.profileKey].name),
      f('sac_diag_potencial', r.potencial),
      f('sac_diag_preparacion', r.preparacion),
      f('sac_diag_temperatura', r.temperatura),
      f('sac_diag_horas', r.hours ? `${r.hours[0]}–${r.hours[1]} h/mes` : 'No sabe'),
      f('sac_diag_top3', r.top.map(processText).join('\n\n')),
      f('sac_diag_porque', why.join('\n\n')),
      // Versiones separadas para el correo (HubSpot quita los saltos de línea al insertar una propiedad)
      f('sac_diag_porque_potencial', why[0]),
      f('sac_diag_porque_preparacion', why[1]),
      f('sac_diag_porque_perfil', why[2]),
      ...r.top.map((k, n) => f(`sac_diag_proceso${n + 1}`, processText(k, n))),
      f('sac_diag_accion', PROCESSES[r.top[0]].tomorrow),
      f('sac_diag_dolor', payload.answers.dolor || '—'),
      f('sac_diag_variante', `${payload.variant} · ${utmText}`),
      f('sac_diag_respuestas', `${answersText(payload.answers)}\n\nConsentimiento aceptado: ${payload.fecha}`),
    ];
    if (payload.whatsapp) fields.push(f('phone', payload.whatsapp));
    const hutk = (document.cookie.match(/(?:^|;\s*)hubspotutk=([^;]+)/) || [])[1];
    const body = {
      submittedAt: Date.now(),
      fields,
      context: { pageUri: location.href, pageName: document.title, ...(hutk ? { hutk } : {}) },
    };
    const { host, portalId, formId } = CONFIG.hubspot;
    const res = await fetch(`https://${host}/submissions/v3/integration/submit/${portalId}/${formId}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`HubSpot ${res.status}: ${await res.text()}`);
  }

  /* ---------- Resultado ---------- */
  function renderResult() {
    const r = state.result, p = PROFILES[r.profileKey];
    setProgress(1, 1, 'Resultado');
    const first = PROCESSES[r.top[0]];
    const hoursHtml = r.hours
      ? `<div class="hours"><span>Horas que podrías recuperar al mes (estimado)</span><strong>${r.hours[0]}–${r.hours[1]} h/mes</strong></div>`
      : `<div class="hours unknown"><span>Horas que podrías recuperar</span><strong>Te ayudamos a medirlo en la sesión</strong></div>`;
    const procs = r.top.map((k, n) => {
      const pr = PROCESSES[k];
      return `<div class="proc ${n === 0 ? 'first' : ''}">
        <div class="proc-head"><span>0${n + 1}</span><h3>${esc(pr.title)}</h3></div>
        <p>${esc(pr.desc)}</p>
        ${pr.case ? `<span class="case">${esc(pr.case)}</span>` : ''}
      </div>`;
    }).join('');
    const nombre = state.lead ? state.lead.nombre.split(' ')[0] : '';
    // Agenda con nombre y email ya escritos (parámetros de prellenado de HubSpot Meetings)
    let bookHref = CONFIG.bookingUrl;
    if (bookHref && state.lead) {
      const u = new URL(bookHref);
      const [first, ...rest] = state.lead.nombre.split(/\s+/);
      u.searchParams.set('firstname', first);
      if (rest.length) u.searchParams.set('lastname', rest.join(' '));
      u.searchParams.set('email', state.lead.email);
      bookHref = u.toString();
    }
    let embedSrc = '';
    if (bookHref) {
      const u = new URL(bookHref);
      u.searchParams.set('embed', 'true');
      embedSrc = u.toString();
    }
    body.innerHTML = `<div class="step result">
      <p class="q-kicker">TU RADAR DE IA${nombre ? ' · ' + esc(nombre.toUpperCase()) : ''}</p>
      <h2 class="q-title">Perfil: ${esc(p.name)}</h2>
      <p class="profile-desc">${esc(p.desc)}</p>
      <div class="scores">
        <div class="score"><span>POTENCIAL</span><strong>${r.potencial}</strong><b><i data-w="${r.potencial}"></i></b></div>
        <div class="score"><span>PREPARACIÓN</span><strong>${r.preparacion}</strong><b><i data-w="${r.preparacion}"></i></b></div>
      </div>
      ${hoursHtml}
      <p class="r-label">TUS 3 PROCESOS CON MÁS RETORNO</p>
      ${procs}
      <div class="tomorrow"><p class="r-label">HAZ ESTO MAÑANA</p><p>${esc(first.tomorrow)}</p></div>
      <div class="cta-box">
        <h3>¿Lo aterrizamos juntos?</h3>
        <p>En 30 minutos revisamos tu Radar, validamos los números con tu operación y te decimos por dónde empezar. Sin costo. Elige tu horario aquí abajo.</p>
        ${embedSrc
          ? `<div class="meetings-iframe-container" data-src="${esc(embedSrc)}"></div>
             <p class="book-alt">¿No se ve el calendario? <a id="book" href="${esc(bookHref)}" target="_blank" rel="noopener">Ábrelo en otra pestaña →</a></p>`
          : `<a class="btn btn-dark" id="book" href="#">Agendar 30 min <span aria-hidden="true">→</span></a>`}
      </div>
      <p class="sent">Te enviamos el reporte completo a <strong>${esc(state.lead.email)}</strong>.<br />Si no lo ves en 5 minutos, revisa tu carpeta de spam o promociones.</p>
      ${HS_READY || !/^(localhost|127\.0\.0\.1)$/.test(location.hostname) ? '' : '<p class="dev-note">Prototipo: el lead no se envía a ningún lado todavía (queda en la consola y en este navegador). Falta conectar CRM/email, la agenda y los píxeles.</p>'}
    </div>`;
    requestAnimationFrame(() => body.querySelectorAll('.score i').forEach((i) => { i.style.width = i.dataset.w + '%'; }));
    $('#book').addEventListener('click', (e) => {
      track('BookingLinkClick', { content_name: 'diagnostico_ia', perfil: r.profileKey });
      if (!CONFIG.bookingUrl) { e.preventDefault(); alert('Prototipo: aquí se abrirá el calendario.'); }
    });
    if (embedSrc) loadMeetingsEmbed();
  }

  /* ---------- Calendario de HubSpot incrustado ---------- */
  // El script oficial busca .meetings-iframe-container al cargar; se vuelve a insertar en cada render.
  function loadMeetingsEmbed() {
    const old = document.getElementById('hs-meetings-embed');
    if (old) old.remove();
    const s = document.createElement('script');
    s.id = 'hs-meetings-embed';
    s.src = 'https://static.hsappstatic.net/MeetingsEmbed/ex/MeetingsEmbedCode.js';
    s.async = true;
    document.body.appendChild(s);
  }

  // Reserva confirmada: HubSpot avisa por postMessage. Aquí sí se mide "Schedule" (cita real, no clic).
  let booked = false;
  window.addEventListener('message', (e) => {
    if (!/^https:\/\/([a-z0-9-]+\.)*hubspot\.com$/.test(e.origin)) return;
    if (!e.data || !e.data.meetingBookSucceeded || booked) return;
    booked = true;
    track('Schedule', { content_name: 'diagnostico_ia', perfil: state.result && state.result.profileKey });
  });
})();
