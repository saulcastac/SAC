"""Generate committed, buildless service pages. Python standard library only."""
from pathlib import Path
from html import escape as e
import json
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
class Raw(str):
 """Trusted HTML authored in this file; never user input."""

def faq_html(q,a):
 return f'<details><summary>{e(q)}</summary>{a if isinstance(a,Raw) else "<p>"+e(a)+"</p>"}</details>'

ORIGIN = json.loads((ROOT / 'site-config.json').read_text())['origin'].rstrip('/')
SERVICES = [
 dict(slug='automatizacion-ia', name='Automatización e IA', title='Automatización e IA para empresas | SAC',
 description='Reduce tareas manuales y conecta procesos con automatización e inteligencia artificial a medida. Conoce el caso de VAX Solutions y conversa con SAC.',
 hero='Tu equipo tiene cosas <em>más importantes que hacer.</em>', intro='Identificamos tareas repetitivas y desarrollamos soluciones que ayudan a tu empresa a trabajar mejor. Sin complicaciones innecesarias.', cta='Descubre qué puedes automatizar', kicker='MENOS TRABAJO MANUAL. MÁS TIEMPO PARA TU NEGOCIO.',
 visual=['Documentos y datos', 'Validación y proceso', 'Operación conectada'], visual_title='De la tarea repetida<br>a un proceso que fluye.', visual_note='Cada integración parte de cómo trabaja tu empresa.',
 problem='Hay tareas que tu equipo ya no debería hacer manualmente.', problem_intro='Si una actividad se repite cada día, depende de copiar información o se detiene cuando falta una persona, vale la pena revisarla.',
 problems=[('La misma información, varias veces','Capturas datos de un correo a una hoja de cálculo y después a otro sistema.'),('El trabajo se acumula','Facturas, documentos y solicitudes compiten por el tiempo de tu equipo.'),('Los sistemas no se hablan','Cada área tiene una parte de la información. Unirla sigue siendo una tarea manual.')],
 applications=[('Documentos y facturas','Extraer información, validar campos y generar documentos con reglas definidas.'),('Correos y cotizaciones','Preparar respuestas y propuestas a partir de la información de tu operación.'),('Sistemas y bases de datos','Conectar herramientas para que los datos lleguen a donde hacen falta.'),('Agentes para operaciones internas','Consultar información y asistir tareas concretas con permisos y supervisión.'),('Actividades administrativas','Ordenar solicitudes, generar reportes y coordinar seguimientos.')],
 approach='Empezamos por una tarea concreta.', steps=[('Entendemos el proceso','Revisamos volumen, herramientas, excepciones y tiempo dedicado.'),('Elegimos dónde empezar','Priorizamos una oportunidad viable y acordamos alcance e indicadores.'),('Construimos y validamos','Probamos con escenarios de tu operación, incluidos los casos que requieren revisión humana.'),('Ponemos en marcha','Acompañamos la adopción y acordamos el seguimiento y soporte.')],
 expectation='Antes de desarrollar, conocerás qué se automatiza, qué seguirá en manos de tu equipo y cómo evaluaremos el resultado.', evidence='vax',
 faqs=[('¿Necesito cambiar mis sistemas actuales?','No necesariamente. Primero revisamos qué integraciones permiten tus herramientas. Si hay limitaciones, las ponemos sobre la mesa antes de proponer una solución.'),('¿Todo necesita inteligencia artificial?','No. Si una regla o una integración resuelve mejor la tarea, usamos esa opción. Incorporamos IA cuando aporta valor al proceso.'),('¿Qué pasa con los errores o las excepciones?','Definimos validaciones, permisos y puntos de revisión humana según el riesgo de cada actividad. Automatizar no elimina la necesidad de supervisar.'),('¿Cuánto cuesta y cuánto tarda?',Raw('<p>Trabajamos en pasos y cada uno tiene precio (MXN + IVA):</p><ul class="faq-prices"><li><strong>Diagnóstico de IA: gratis.</strong> 3 minutos en línea y, si quieres, una sesión de 30 minutos.</li><li><strong>Mapa de IA SAC: $14,900 — precio de fundador $7,900 (quedan 3 de 5).</strong> 2 semanas. Encontramos tus 3 mejores oportunidades y dejamos una mejora funcionando, con garantía de devolución. Se acredita al 100&nbsp;% si implementas con nosotros en los siguientes 60 días. <a href="/mapa-ia">Conoce el Mapa de IA</a>.</li><li><strong>Sprint de automatización: desde $45,000.</strong> De 4 a 6 semanas para automatizar un proceso de punta a punta, con precio cerrado antes de empezar. Normalmente queda entre 45 y 90 mil pesos.</li><li><strong>Acompañamiento: desde $9,900 al mes.</strong> Mantenimiento, una mejora al mes y capacitación para tu equipo.</li></ul><p>El precio exacto del Sprint sale del Mapa, cuando ya sabemos qué se automatiza, qué integraciones hacen falta y qué seguirá en manos de tu equipo. <a href="/diagnostico/">Empieza por el diagnóstico gratis</a>.</p>'))],
 contact='¿Qué tarea te está quitando tiempo?', contact_text='Cuéntanos qué se repite, con qué herramientas trabajan y dónde se atasca el proceso.', placeholder='Por ejemplo: capturamos facturas a mano y después enviamos los documentos por correo…'),
 dict(slug='capacitacion-ia', name='Capacitación en IA', title='Capacitación empresarial en IA | SAC',
 description='Talleres prácticos de inteligencia artificial para equipos de administración, ventas, operaciones y dirección. Capacitación adaptada a tu empresa con SAC.',
 hero='Tu equipo ya tiene acceso a la IA. <em>Hagamos que sepa aprovecharla.</em>', intro='Talleres prácticos y personalizados para que tu equipo use la inteligencia artificial en las tareas que ya hace todos los días.', cta='Lleva la IA a tu equipo', kicker='APRENDER. PRACTICAR. APLICAR.',
 visual=['Una tarea real', 'Práctica acompañada', 'Un equipo más capaz'], visual_title='Del “¿cómo se usa?”<br>al “esto me sirve”.', visual_note='Ejercicios de tu operación, con criterio y revisión.',
 problem='Tener una herramienta no es lo mismo que saber usarla.', problem_intro='El valor aparece cuando las personas saben qué pedir, cómo revisar una respuesta y cuándo conviene resolver la tarea de otra manera.',
 problems=[('Prueban sin un objetivo claro','Usan IA de vez en cuando, pero no encuentran cómo llevarla a sus tareas.'),('Cada persona aprende por su cuenta','Los avances quedan aislados y es difícil compartir una forma de trabajar.'),('No saben qué pueden compartir','Faltan criterios para proteger información y verificar las respuestas.')],
 applications=[('Administración','Preparar borradores, estructurar documentos y organizar información para revisión.'),('Ventas','Trabajar propuestas, preparar reuniones y adaptar mensajes con contexto del cliente.'),('Operaciones','Documentar procesos, ordenar solicitudes y convertir instrucciones en listas de trabajo.'),('Dirección','Sintetizar información, explorar escenarios y preparar preguntas para decidir mejor.')],
 approach='La capacitación empieza antes del taller.', steps=[('Conocemos al equipo','Entendemos funciones, experiencia y herramientas disponibles.'),('Elegimos tareas relevantes','Seleccionamos situaciones donde practicar tenga utilidad inmediata.'),('Aprendemos haciendo','Trabajamos con ejemplos de su operación y revisamos juntos las respuestas.'),('Dejamos herramientas prácticas','Entregamos recomendaciones y materiales para seguir aplicando lo aprendido.')],
 expectation='Acordamos participantes, objetivos, modalidad y materiales antes de empezar. Usamos ejemplos autorizados o anonimizados, sin exponer información sensible.', evidence=None,
 faqs=[('¿El equipo necesita conocimientos técnicos?','No. Adaptamos el taller al punto de partida de las personas y a sus responsabilidades. El objetivo es que puedan aplicar lo aprendido en su trabajo.'),('¿Enseñan una sola herramienta?','Seleccionamos herramientas según las tareas y el acceso que tenga tu empresa. También trabajamos criterios que sirven más allá de una plataforma.'),('¿Qué se lleva el equipo?','Ejercicios trabajados, recomendaciones de uso y materiales prácticos según el alcance acordado. Incluimos cómo revisar resultados y cuidar la información.'),('¿Qué duración y modalidad tiene?','Las definimos según los objetivos, el tamaño del grupo y el nivel de profundidad. La propuesta detalla sesiones, modalidad y herramientas o licencias necesarias.')],
 contact='¿Qué podría hacer mejor tu equipo con IA?', contact_text='Cuéntanos qué áreas participarían y qué tareas te gustaría que aprendieran a resolver.', placeholder='Por ejemplo: somos un equipo de ventas y queremos preparar mejores propuestas…'),
 dict(slug='acompanamiento-ia', name='Dirección de IA externa', custom=True),
 dict(slug='desarrollo-web', name='Desarrollo web y software', title='Desarrollo web y software a medida | SAC',
 description='Sitios corporativos, páginas de captación, aplicaciones y plataformas internas diseñadas para las necesidades de tu negocio. Desarrollo a medida con SAC.',
 hero='Una buena idea necesita algo más que verse bien. <em>Necesita funcionar.</em>', intro='Diseñamos y construimos sitios, plataformas y herramientas a medida para conectar tu negocio con sus clientes y mejorar cómo trabaja tu equipo.', cta='Cuéntanos qué quieres construir', kicker='ESTRATEGIA. DISEÑO. SOFTWARE EN OPERACIÓN.',
 visual=['Necesidad de negocio', 'Diseño y desarrollo', 'Solución en operación'], visual_title='De una necesidad<br>a una herramienta útil.', visual_note='Una experiencia clara por fuera. Una solución sólida por dentro.',
 problem='Tu negocio no siempre cabe en una plantilla.', problem_intro='A veces necesitas explicar mejor tu oferta. Otras, una herramienta que resuelva algo que los sistemas actuales no contemplan.',
 problems=[('Tu sitio no explica tu valor','La oferta es buena, pero al visitante le cuesta entender qué haces y cómo contactarte.'),('El proceso vive en hojas sueltas','La información se dispersa y el equipo depende de trabajo manual para avanzar.'),('La herramienta se quedó corta','El negocio cambió y las soluciones disponibles ya no se ajustan a tu operación.')],
 applications=[('Sitios corporativos','Una presencia digital clara para presentar tu oferta y facilitar el contacto.'),('Páginas de captación','Una propuesta enfocada y un recorrido directo para tus campañas.'),('Aplicaciones web','Funciones y flujos diseñados alrededor de las personas que los usan.'),('Plataformas internas','Centralizar información, permisos y actividades de la operación.'),('Herramientas comerciales','Apoyar cotizaciones, seguimiento y gestión según tu proceso de venta.')],
 approach='Primero definimos lo que tiene que resolver.', steps=[('Aterrizamos la necesidad','Definimos usuarios, objetivos y funciones prioritarias.'),('Diseñamos la experiencia','Ordenamos contenido, navegación y recorridos antes de desarrollar.'),('Construimos contigo','Compartimos avances y validamos las funciones acordadas.'),('Implementamos y entregamos','Realizamos pruebas y dejamos claro el uso, soporte y siguientes mejoras.')],
 expectation='Recibirás una propuesta con alcance, entregables, inversión y calendario. Acordamos también alojamiento, mantenimiento y responsabilidades para la operación.', evidence='rtc',
 faqs=[('¿Solo hacen páginas web?','También desarrollamos aplicaciones, plataformas internas y herramientas a medida. La solución depende de lo que tu negocio necesita resolver.'),('¿Pueden integrar otros sistemas?','Sí, cuando las herramientas permiten la integración. Evaluamos sus interfaces, permisos y restricciones durante la definición del proyecto.'),('¿Qué necesito para empezar?','Una idea del problema, de quién usará la solución y del resultado que buscas. Te ayudamos a convertirlo en un alcance concreto.'),('¿Incluyen mantenimiento y soporte?','Definimos el esquema en la propuesta. Aclaramos qué incluye la entrega, qué soporte se contempla y cómo se atienden mejoras posteriores.')],
 contact='¿Qué quieres poner en funcionamiento?', contact_text='Cuéntanos quién usará la solución y qué necesitas que haga por tu negocio.', placeholder='Por ejemplo: necesitamos una plataforma para centralizar cotizaciones y darles seguimiento…'),
]

def form(d):
 return f'''<form id="contact-form" action="https://formsubmit.co/saulcastac@gmail.com" method="POST" data-service="{d['slug']}">
<input type="hidden" name="_subject" value="Nueva consulta — {e(d['name'])} — SAC">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="{ORIGIN}/gracias.html">
<input type="hidden" name="servicio_origen" value="{d['slug']}">
<input type="hidden" name="landing_origen" value="/servicios/{d['slug']}">
{''.join(f'<input type="hidden" name="{key}" value="">' for key in ['utm_source','utm_medium','utm_campaign','utm_content','utm_term'])}
<input type="text" name="_honey" class="form-honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<label for="contact-name">Tu nombre</label><input id="contact-name" name="nombre" autocomplete="name" required maxlength="100">
<label for="contact-email">Correo electrónico</label><input id="contact-email" name="email" type="email" autocomplete="email" required maxlength="180">
<label for="contact-company">Empresa <span class="optional-label">(opcional)</span></label><input id="contact-company" name="empresa" autocomplete="organization" maxlength="120">
<label for="contact-message">¿Qué necesitas resolver?</label><textarea id="contact-message" name="mensaje" required maxlength="2500" rows="4" placeholder="{e(d['placeholder'])}"></textarea>
<p class="form-note">SAC SA de CV, en Zapopan, Jalisco, usará tus datos para atender esta consulta y dar seguimiento a tu proyecto. No incluyas datos sensibles ni información de pacientes. Contacto: <a href="mailto:saulcastac@gmail.com">saulcastac@gmail.com</a>.</p>
<label class="privacy-consent"><input type="checkbox" name="consentimiento" value="Acepto el aviso de privacidad y el tratamiento para atender mi consulta" required><span>He leído el <a href="/privacidad.html" target="_blank" rel="noopener">aviso de privacidad</a> y acepto el tratamiento de mis datos para atender mi consulta.</span></label>
<button class="button button-dark" type="submit">Enviar consulta</button>
<p class="form-note" id="form-status" role="status">Al continuar, FormSubmit verificará el envío para protegernos del spam.</p>
</form>'''

def evidence(d):
 if d['evidence']=='vax':
  return '''<section class="service-evidence theme-dark" aria-labelledby="evidence-title"><div class="container evidence-grid"><div><span class="eyebrow">EXPERIENCIA EN OPERACIÓN / VAX SOLUTIONS</span><h2 id="evidence-title">Menos trabajo manual.<br><em>Un resultado concreto.</em></h2><p>Automatizamos el procesamiento de facturas de VAX Solutions, una empresa de logística, centralizando la información y la generación de documentos y correos.</p><a class="text-link light-link" href="/#casos">Conoce nuestros casos</a></div><div class="evidence-numbers"><div><strong>250–300</strong><span>facturas procesadas diariamente</span></div><div><strong>~16 h</strong><span>semanales ahorradas</span></div><p>Resultados de este proyecto. Cada operación requiere su propia evaluación.</p></div></div></section>'''
 if d['evidence']=='rtc':
  return '''<section class="service-evidence theme-dark" aria-labelledby="evidence-title"><div class="container evidence-grid"><div><span class="eyebrow">PROYECTO REAL / RTC TRANSPORTES</span><h2 id="evidence-title">Una presencia digital<br><em>que explica su negocio.</em></h2><p>Desarrollamos un sitio corporativo para presentar los servicios de RTC Transportes y facilitar que nuevos clientes conozcan su oferta.</p><a class="text-link light-link" href="https://www.rtctransporte.com/" target="_blank" rel="noopener noreferrer">Visita RTC Transportes</a></div><div class="evidence-editorial"><span>RTC</span><p>TRANSPORTES</p><hr><p>Estrategia, contenido y desarrollo para una empresa de transporte.</p></div></div></section>'''
 return ''

def render(d):
 url=f"{ORIGIN}/servicios/{d['slug']}"
 problems=''.join(f'<article><h3>{e(t)}</h3><p>{e(p)}</p></article>' for t,p in d['problems'])
 apps=''.join(f'<div class="application-row"><h3>{e(t)}</h3><p>{e(p)}</p></div>' for t,p in d['applications'])
 steps=''.join(f'<li><h3>{e(t)}</h3><p>{e(p)}</p></li>' for t,p in d['steps'])
 faqs=''.join(faq_html(q,a) for q,a in d['faqs'])
 others=''.join(f'<a href="/servicios/{o["slug"]}">{e(o["name"])}</a>' for o in SERVICES if o!=d)
 return f'''<!doctype html>
<html lang="es-MX"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#101312">
<title>{e(d['title'])}</title><meta name="description" content="{e(d['description'])}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_MX"><meta property="og:site_name" content="SAC Technology Studio"><meta property="og:url" content="{url}"><meta property="og:title" content="{e(d['title'])}"><meta property="og:description" content="{e(d['description'])}"><meta property="og:image" content="{ORIGIN}/og-image.png"><meta property="og:image:width" content="1731"><meta property="og:image:height" content="909"><meta property="og:image:alt" content="SAC Technology Studio — Tecnología que resuelve."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{ORIGIN}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"><script src="/tracking.js" defer></script><script src="/analytics.js" defer></script><script src="/main.js" defer></script>
</head><body class="service-page" data-service="{d['slug']}">
{header()}
<main id="contenido">
<section class="service-hero theme-dark" aria-labelledby="hero-title"><div class="container">
<nav class="service-breadcrumb" aria-label="Ruta de navegación"><a href="/">Inicio</a><span aria-hidden="true">/</span><a href="/#empezar">Servicios</a></nav>
<div class="service-hero-grid"><div class="service-hero-copy"><p class="eyebrow">{e(d['name'])}</p><h1 id="hero-title">{d['hero']}</h1><p class="service-intro">{e(d['intro'])}</p><a class="button button-lime" href="#contacto" data-cta="hero">{e(d['cta'])}</a></div>
<div class="service-diagram" aria-label="{e('Proceso ilustrativo: '+ ' a '.join(d['visual']))}" role="img"><span class="diagram-kicker" aria-hidden="true">SAC / {e(d['name'])}</span><p class="diagram-title" aria-hidden="true">{d['visual_title']}</p><div class="diagram-flow" aria-hidden="true">{''.join(f'<span>{e(v)}</span>' for v in d['visual'])}</div><p class="diagram-note" aria-hidden="true">{e(d['visual_note'])}</p></div></div>
<p class="service-hero-foot">{e(d['kicker'])}</p>
</div></section>
<section class="service-section" aria-labelledby="problem-title"><div class="container"><div class="service-heading"><span class="section-label">EL PUNTO DE PARTIDA</span><h2 id="problem-title">{e(d['problem'])}</h2><p>{e(d['problem_intro'])}</p></div><div class="problem-columns">{problems}</div></div></section>
<section class="service-section service-applications" aria-labelledby="applications-title"><div class="container application-layout"><div class="service-heading"><span class="section-label">DE LA IDEA A LA PRÁCTICA</span><h2 id="applications-title">Así puede verse<br><em>en tu empresa.</em></h2><p>Ejemplos de lo que podemos trabajar contigo. El alcance se define a partir de tu operación.</p></div><div>{apps}</div></div></section>
{evidence(d)}
<section class="service-section theme-dark" id="como-trabajamos" aria-labelledby="approach-title"><div class="container"><div class="service-heading"><span class="eyebrow">CÓMO TRABAJAMOS</span><h2 id="approach-title">{e(d['approach'])}</h2></div><ol class="service-steps">{steps}</ol><p class="service-expectation">{e(d['expectation'])}</p></div></section>
<section class="service-section" aria-labelledby="faq-title"><div class="container faq-layout"><div class="service-heading"><span class="section-label">ANTES DE CONVERSAR</span><h2 id="faq-title">Preguntas<br><em>que vale la pena hacer.</em></h2></div><div class="service-faq">{faqs}</div></div></section>
<section class="contact-section" id="contacto" aria-labelledby="contact-title"><div class="container contact-grid"><div class="contact-copy"><span class="section-label">HABLEMOS DE TU NEGOCIO</span><h2 id="contact-title">{e(d['contact'])}</h2><p>{e(d['contact_text'])}</p><p class="contact-reassurance">Revisaremos tu mensaje y te responderemos por correo para definir el siguiente paso.</p><div class="contact-whatsapp"><a class="text-link" href="https://wa.me/524921191702?text={quote('Hola, me interesa '+d['name']+'.')}" target="_blank" rel="noopener noreferrer" data-whatsapp>Prefiero escribir por WhatsApp</a><span class="contact-whatsapp-number">+52 492 119 1702</span></div></div><div class="contact-form-wrap"><div class="contact-form-top"><strong>Cuéntanos qué necesitas.</strong></div>{form(d)}</div></div></section>
<aside class="container related-services" aria-label="Otros servicios de SAC"><p>Otras formas de trabajar juntos</p><div>{others}</div></aside>
</main><footer class="footer theme-dark"><div class="container footer-top"><a href="/" class="footer-brand" aria-label="SAC, inicio">SAC<span>.</span></a><span>TECHNOLOGY STUDIO<br>DESIGNED TO SOLVE.</span><a href="#inicio" class="back-top">VOLVER ARRIBA</a></div><div class="container footer-bottom"><span>© <span id="year">2026</span> SAC. Technology Studio.</span><a href="/privacidad.html">Aviso de privacidad</a><button type="button" data-cookie-settings hidden>Cookies</button></div></footer>
</body></html>
'''


# ---------------------------------------------------------------------------
# Dirección de IA externa (Fractional CAIO).
# One content source, three outputs: homepage section, indexable service page
# (/servicios/acompanamiento-ia) and the noindex Meta Ads landing (/direccion-ia).
# ---------------------------------------------------------------------------
CAIO = dict(
 service='fractional-caio',
 name='Dirección de IA externa',
 service_title='Dirección de IA externa (Fractional CAIO) para empresas | SAC',
 service_description='Una dirección de IA externa para tu empresa: priorizamos oportunidades, capacitamos a tu equipo y damos seguimiento cada mes. Empieza con un piloto de 90 días.',
 lp_title='Dirección de IA para tu empresa, sin contratarla de tiempo completo | SAC',
 lp_description='Trabajamos contigo para identificar oportunidades, capacitar a tu equipo y convertir la IA en mejoras reales. Empieza con un piloto de 90 días.',
 eyebrow='DIRECCIÓN DE IA EXTERNA · FRACTIONAL CAIO',
 h1=Raw('Tu empresa puede tener una dirección de inteligencia artificial. <em>Sin contratarla de tiempo completo.</em>'),
 # utm_content → H1, only for the campaign landing. Whitelisted, authored here.
 angles={
  'liderazgo': 'Tu empresa quiere usar IA. <em>¿Quién está liderando ese cambio?</em>',
  'continuidad': 'La IA no transforma una empresa <em>con un taller de dos horas.</em>',
  'direccion-externa': 'No necesitas contratar un director de IA de tiempo completo <em>para empezar a avanzar.</em>',
 },
 intro='Trabajamos contigo para identificar oportunidades, capacitar a tu equipo y convertir la IA en mejoras reales dentro de tu operación.',
 pilot='Empieza con un piloto de 90 días.',
 pilot_note='Al terminar, decides si seguimos cada mes.',
 cta='Hablemos de tu empresa',
 whatsapp_text='Hola, vi la página de dirección de IA externa y me interesa conocer el acompañamiento mensual.',
 problem_title=Raw('La IA no se implementa una vez. <em>Se trabaja todos los días.</em>'),
 problem_intro='Quizá reconozcas alguna de estas situaciones. Suelen aparecer cuando la IA llega a una empresa sin alguien que dirija su adopción.',
 problems=[
  ('Cada quien experimenta por su cuenta', 'Hay personas usando IA, pero cada una a su manera. Lo que aprende una no llega al resto del equipo.'),
  ('Las oportunidades se quedan en la lista', 'Ya identificaron qué se podría automatizar, pero nadie tiene tiempo de llevarlo a cabo.'),
  ('Herramientas compradas, poco aprovechadas', 'Se contrataron licencias o plataformas, pero falta seguimiento para que se usen de verdad.'),
 ],
 components=[
  ('Dirección y prioridades', 'Trabajamos con dirección para seleccionar qué iniciativas valen la pena.', 'Sesiones con dirección'),
  ('Roadmap de IA', 'Mantenemos una lista priorizada de oportunidades con responsables, viabilidad y resultados esperados.', 'Roadmap actualizado'),
  ('Capacitación y adopción', 'Acompañamos a colaboradores para que aprendan a aprovechar IA dentro de sus tareas cotidianas.', 'Trabajo con equipos'),
  ('Coordinación de implementaciones', 'Ayudamos a definir, supervisar y validar las mejoras tecnológicas acordadas.', 'Supervisión y validación'),
  ('Seguimiento y resultados', 'Revisamos avances, obstáculos y resultados para decidir qué sigue.', 'Revisión de avances'),
 ],
 roadmap=[('Respuestas a cotizaciones', 'Ventas', 'Alta', 'En curso'), ('Reporte semanal automático', 'Operaciones', 'Media', 'Siguiente'), ('IA en tareas de administración', 'Administración', 'Alta', 'Capacitación')],
 scope_note='El acompañamiento tiene capacidad, actividades y entregables definidos. Los desarrollos de software de mayor alcance se cotizan por separado.',
 how_title=Raw('Nos integramos a tu operación. <em>Sin agregar otra capa de complejidad.</em>'),
 moments=[
  ('Inicio', 'Conocemos el negocio, identificamos responsables y acordamos prioridades.'),
  ('Cada mes', 'Revisamos oportunidades, trabajamos con los equipos, damos seguimiento a iniciativas y coordinamos las mejoras acordadas.'),
  ('Revisión', 'Evaluamos avances, aprendizajes y próximas prioridades.'),
 ],
 month=[
  ('Semana 1', 'Prioridades con dirección', 'Revisamos avances y confirmamos en qué nos enfocamos este mes.'),
  ('Semana 2', 'Trabajo con equipos', 'Acompañamos a un área a incorporar IA en una tarea concreta.'),
  ('Semana 3', 'Seguimiento de iniciativas', 'Revisamos con responsables y proveedores las mejoras en curso.'),
  ('Semana 4', 'Reporte y siguientes pasos', 'Compartimos avances, obstáculos y la propuesta de prioridades para el siguiente mes.'),
 ],
 month_note='Ejemplo ilustrativo. La frecuencia de reuniones, las horas y los entregables se definen en la propuesta de cada empresa.',
 pilot_text='Un periodo acotado para conocer tu negocio, acordar prioridades y entregar las primeras mejoras. Al terminar, decides si continuamos con el acompañamiento mensual.',
 pilot_route=[('Días 1–30', 'Entender y priorizar'), ('Días 31–60', 'Primeras mejoras y capacitación'), ('Días 61–90', 'Medir y decidir cómo seguir')],
 pilot_terms='Ruta orientativa. El piloto se contrata con una propuesta acordada: objetivos, actividades, entregables e inversión.',
 evidence_intro='VAX Solutions, empresa de logística, forma parte de FLI Holding, el grupo empresarial donde el fundador de SAC lidera la mejora de procesos, tecnología e IA desde 2024. Ahí impulsamos dos tipos de cambio distintos.',
 adoption=[('Operaciones', 'Un gerente utiliza datos, reportes y agentes para mantenerse informado sobre las situaciones que requieren su atención.'),
           ('Administración', 'Una colaboradora utiliza IA, hojas de cálculo y Apps Script para crear sus propias automatizaciones y ayudar a sus compañeros.')],
 insight='El verdadero cambio ocurre cuando las personas empiezan a encontrar y construir soluciones por sí mismas.',
 audience=['Quieren incorporar IA, pero no saben qué priorizar.', 'Ya experimentan con herramientas, pero necesitan una estrategia de adopción.', 'No tienen un responsable interno dedicado a IA.', 'Necesitan acompañamiento para mantener el avance de sus iniciativas.'],
 audience_note='Trabajamos con tu equipo y tus proveedores actuales. No pretendemos sustituir a un CTO, CIO o área de tecnología: si ya existen, trabajamos junto a ellos; si no, te ayudamos a avanzar con IA mientras decides qué estructura necesitas.',
 pricing='Planes mensuales adaptados al tamaño de tu empresa y al nivel de acompañamiento que necesita.',
 pricing_note='Después de una primera conversación te enviamos una propuesta personalizada con alcance, actividades, entregables e inversión.',
 faqs=[
  ('¿Qué es un Fractional CAIO?', 'CAIO significa Chief AI Officer: la persona que dirige la adopción de inteligencia artificial en una empresa. “Fractional” quiere decir que la función se cubre de forma externa y parcial. En lugar de contratar a alguien de tiempo completo, cuentas con nosotros para priorizar, acompañar y dar seguimiento cada mes.'),
  ('¿En qué se diferencia de un proyecto puntual?', 'Un proyecto resuelve un problema definido y termina con la entrega. El acompañamiento mensual da continuidad: revisa prioridades, trabaja con tus equipos y coordina mejoras mes a mes. Los proyectos se pueden contratar por separado.'),
  ('¿Cómo empieza el piloto de 90 días?', 'Con una conversación sobre tu empresa. Después te enviamos una propuesta con objetivos, actividades y entregables para los primeros 90 días. Al terminar, decides si continuamos.'),
  ('¿Trabajan con nuestro equipo y proveedores actuales?', 'Sí. Colaboramos con dirección, responsables de área, tu equipo de tecnología si existe y tus proveedores. No reemplazamos a un CTO, CIO o área de tecnología.'),
  ('¿Incluye desarrollos ilimitados?', 'No. El acompañamiento tiene capacidad, actividades y entregables definidos. Los desarrollos de software de mayor alcance se cotizan por separado.'),
  ('¿Cuánto cuesta?', 'Los planes mensuales se adaptan al tamaño de tu empresa y al nivel de acompañamiento que necesita. Te enviamos una propuesta personalizada después de conocer tu operación.'),
  ('¿Puedo empezar con el diagnóstico gratis?', Raw('<p>Sí. Si prefieres explorar primero, el <a href="/diagnostico/">diagnóstico gratis</a> toma 3 minutos y te dice dónde podría haber oportunidades. No es un requisito para hablar del acompañamiento.</p>')),
 ],
 lp_faqs=4,  # the campaign landing keeps the first four questions
 contact_title='Hablemos de tu empresa.',
 contact_text='Cuéntanos qué te gustaría lograr con IA. Te respondemos por correo para agendar una conversación y, si tiene sentido, preparar una propuesta.',
 placeholder='Por ejemplo: queremos que el equipo de ventas use IA y definir qué automatizar primero…',
 home_eyebrow='SAC / FRACTIONAL CAIO',
 home_h2=Raw('Tu empresa necesita avanzar con IA. <em>No necesariamente contratar a alguien de tiempo completo.</em>'),
 home_text='Nos integramos como tu dirección externa de inteligencia artificial. Encontramos oportunidades, acompañamos a tu equipo y damos continuidad a las mejoras que realmente importan.',
 home_cta='Conoce el acompañamiento mensual',
 capabilities=['Prioridades tecnológicas claras.', 'Equipos que aprenden a utilizar IA.', 'Mejoras implementadas de manera progresiva.', 'Seguimiento de resultados.'],
)
CYCLE = ['Entender', 'Priorizar', 'Implementar', 'Medir', 'Mejorar']
SERVICE_PATH = '/servicios/acompanamiento-ia'
LP_PATH = '/direccion-ia'
H = lambda x: x if isinstance(x, Raw) else e(x)


def cycle():
 nodes = ''.join(f'<li>{e(n)}</li>' for n in CYCLE)
 return f'''<div class="caio-cycle-panel"><div class="caio-cycle-head" aria-hidden="true"><span>EVOLUCIÓN CONTINUA</span><span class="status-dot"></span></div>
<div class="caio-cycle" role="img" aria-label="Ciclo de trabajo continuo: {e(', '.join(n.lower() for n in CYCLE))}, y vuelve a empezar.">
<div class="caio-cycle-ring" aria-hidden="true"><span class="caio-cycle-runner"></span></div>
<div class="caio-cycle-center" aria-hidden="true"><small>SAC / CADA MES</small><strong>Un ciclo,<br>no un evento.</strong></div>
<ol class="caio-cycle-nodes" aria-hidden="true">{nodes}</ol></div>
<div class="caio-cycle-foot" aria-hidden="true"><span>MES 01</span><span>→</span><span>MES 02</span><span>→</span><span>MES 03</span><span>…</span></div></div>'''


def home_section():
 caps = ''.join(f'<li><span>0{i}</span>{e(c)}</li>' for i, c in enumerate(CAIO['capabilities'], 1))
 return f'''<section class="section caio-home" id="direccion-ia" aria-labelledby="caio-home-title">
      <div class="container">
        <div class="section-top"><span class="section-label">05 / OTRA FORMA DE TRABAJAR</span><span class="tiny-index">PROYECTOS PUNTUALES · ACOMPAÑAMIENTO MENSUAL ↘</span></div>
        <div class="caio-home-grid">
          <div class="caio-home-copy">
            <p class="caio-eyebrow">{e(CAIO['home_eyebrow'])}</p>
            <h2 id="caio-home-title">{H(CAIO['home_h2'])}</h2>
            <p class="caio-home-text">{e(CAIO['home_text'])}</p>
            <ul class="caio-capabilities">{caps}</ul>
            <a class="button button-dark" href="{SERVICE_PATH}" data-cta="home-caio">{e(CAIO['home_cta'])} <span aria-hidden="true">↗</span></a>
            <p class="caio-home-note">Sin promesas de automatizaciones ilimitadas: capacidad y entregables definidos desde el inicio.</p>
          </div>
          {cycle()}
        </div>
      </div>
    </section>'''


def caio_hidden(landing, subject):
 utm = ''.join(f'<input type="hidden" name="{k}" value="">' for k in ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'])
 return f'''<input type="hidden" name="_subject" value="{e(subject)}">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="{ORIGIN}/gracias.html">
<input type="hidden" name="servicio_origen" value="{CAIO['service']}">
<input type="hidden" name="modalidad" value="acompanamiento-mensual">
<input type="hidden" name="landing_origen" value="{landing}">
{utm}'''


def caio_form(landing, subject):
 roles = ['Dueño/a o socio/a', 'Director/a general', 'Director/a de área', 'Otro']
 sizes = ['1–10', '11–50', '51–200', 'Más de 200']
 opts = lambda xs: '<option value="" disabled selected>Selecciona una opción</option>' + ''.join(f'<option>{e(x)}</option>' for x in xs)
 return f'''<form id="contact-form" action="https://formsubmit.co/saulcastac@gmail.com" method="POST" data-service="{CAIO['service']}">
{caio_hidden(landing, subject)}
<input type="text" name="_honey" class="form-honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<label for="contact-name">Tu nombre</label><input id="contact-name" name="nombre" autocomplete="name" required maxlength="100">
<label for="contact-company">Empresa</label><input id="contact-company" name="empresa" autocomplete="organization" required maxlength="120">
<label for="contact-email">Correo profesional</label><input id="contact-email" name="email" type="email" autocomplete="email" required maxlength="180" placeholder="nombre@empresa.com">
<div class="caio-form-row"><div><label for="contact-role">Tu cargo</label><select id="contact-role" name="cargo" required>{opts(roles)}</select></div>
<div><label for="contact-size">Colaboradores</label><select id="contact-size" name="colaboradores" required>{opts(sizes)}</select></div></div>
<label for="contact-message">¿Qué te gustaría lograr con IA?</label><textarea id="contact-message" name="mensaje" required maxlength="2500" rows="3" placeholder="{e(CAIO['placeholder'])}"></textarea>
<p class="form-note">SAC SA de CV, en Zapopan, Jalisco, usará tus datos para atender esta consulta y preparar una propuesta. No incluyas datos sensibles. Contacto: <a href="mailto:saulcastac@gmail.com">saulcastac@gmail.com</a>.</p>
<label class="privacy-consent"><input type="checkbox" name="consentimiento" value="Acepto el aviso de privacidad y el tratamiento para atender mi consulta" required><span>He leído el <a href="/privacidad.html" target="_blank" rel="noopener">aviso de privacidad</a> y acepto el tratamiento de mis datos para atender mi consulta.</span></label>
<button class="button button-dark" type="submit">{e(CAIO['cta'])} <span aria-hidden="true">↗</span></button>
<p class="form-note" id="form-status" role="status">Al continuar, FormSubmit verificará el envío para protegernos del spam.</p>
</form>'''


def whatsapp_link(cls='text-link'):
 return f'<a class="{cls}" href="https://wa.me/524921191702?text={quote(CAIO["whatsapp_text"])}" target="_blank" rel="noopener noreferrer" data-whatsapp>Prefiero escribir por WhatsApp</a>'


def problem_section():
 items = ''.join(f'<article><span class="caio-quote-mark" aria-hidden="true">“</span><h3>{e(t)}</h3><p>{e(p)}</p></article>' for t, p in CAIO['problems'])
 return f'''<section class="service-section" aria-labelledby="problem-title"><div class="container"><div class="service-heading"><span class="section-label">EL PUNTO DE PARTIDA</span><h2 id="problem-title">{H(CAIO['problem_title'])}</h2><p>{e(CAIO['problem_intro'])}</p></div><div class="problem-columns caio-problems">{items}</div></div></section>'''


def components_section():
 c = CAIO['components']
 rows = ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td><span class="caio-pill caio-pill-{"hi" if p=="Alta" else "md"}">{e(p)}</span></td><td>{e(s)}</td></tr>' for a, b, p, s in CAIO['roadmap'])
 tag = lambda t: f'<span class="caio-tag">{e(t)}</span>'
 small = ''.join(f'<article class="caio-comp caio-comp-small"><span class="caio-comp-num">0{i}</span><h3>{e(t)}</h3><p>{e(p)}</p>{tag(g)}</article>' for i, (t, p, g) in enumerate(c[2:], 3))
 return f'''<section class="service-section caio-components" aria-labelledby="components-title"><div class="container">
<div class="service-heading"><span class="section-label">QUÉ RECIBES CADA MES</span><h2 id="components-title">Actividades concretas.<br><em>No solo estrategia.</em></h2><p>Esto es lo que hacemos contigo mientras dura el acompañamiento.</p></div>
<div class="caio-comp-grid">
<article class="caio-comp caio-comp-lead theme-dark"><span class="caio-comp-num">01</span><h3>{e(c[0][0])}</h3><p>{e(c[0][1])}</p>{tag(c[0][2])}</article>
<article class="caio-comp caio-comp-roadmap"><div><span class="caio-comp-num">02</span><h3>{e(c[1][0])}</h3><p>{e(c[1][1])}</p>{tag(c[1][2])}</div>
<figure class="caio-roadmap"><figcaption>Ejemplo ilustrativo de roadmap</figcaption><div class="caio-table-wrap"><table><thead><tr><th scope="col">Iniciativa</th><th scope="col">Responsable</th><th scope="col">Prioridad</th><th scope="col">Estado</th></tr></thead><tbody>{rows}</tbody></table></div></figure></article>
<div class="caio-comp-row">{small}</div>
</div>
<p class="caio-scope-note"><strong>Importante:</strong> {e(CAIO['scope_note'])}</p>
</div></section>'''


def how_section():
 moments = ''.join(f'<li><span class="caio-moment-num">0{i}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(CAIO['moments'], 1))
 weeks = ''.join(f'<li><span>{e(w)}</span><h4>{e(t)}</h4><p>{e(p)}</p></li>' for w, t, p in CAIO['month'])
 route = ''.join(f'<li><span>{e(d)}</span>{e(t)}</li>' for d, t in CAIO['pilot_route'])
 return f'''<section class="service-section theme-dark" id="como-trabajamos" aria-labelledby="approach-title"><div class="container">
<div class="service-heading"><span class="eyebrow">CÓMO FUNCIONA</span><h2 id="approach-title">{H(CAIO['how_title'])}</h2></div>
<ol class="caio-moments">{moments}</ol>
<div class="caio-month"><div class="caio-month-head"><h3>Así puede verse un mes</h3><span class="caio-tag caio-tag-dark">EJEMPLO ILUSTRATIVO</span></div><ol class="caio-weeks">{weeks}</ol><p class="caio-month-note">{e(CAIO['month_note'])}</p></div>
<div class="caio-pilot" id="piloto"><div><span class="eyebrow">PILOTO DE 90 DÍAS</span><h3>La forma recomendada de empezar.</h3><p>{e(CAIO['pilot_text'])}</p></div><div><ol class="caio-route">{route}</ol><p class="caio-pilot-terms">{e(CAIO['pilot_terms'])}</p></div></div>
</div></section>'''


def evidence_section():
 roles = ''.join(f'<li><span>{e(r)}</span><p>{e(t)}</p></li>' for r, t in CAIO['adoption'])
 return f'''<section class="service-evidence theme-dark caio-evidence" aria-labelledby="evidence-title"><div class="container">
<div class="caio-evidence-top"><div><span class="eyebrow">EVIDENCIA REAL / VAX SOLUTIONS</span><h2 id="evidence-title">Esto lo hacemos primero<br><em>en nuestras propias empresas.</em></h2></div><p>{e(CAIO['evidence_intro'])}</p></div>
<div class="caio-evidence-grid">
<div class="caio-ev-col"><span class="caio-ev-kicker">ADOPCIÓN / PERSONAS QUE USAN IA</span><ul class="caio-roles">{roles}</ul><p class="caio-ev-note">Roles descritos sin nombres por privacidad.</p></div>
<div class="caio-ev-col caio-ev-auto"><span class="caio-ev-kicker">AUTOMATIZACIÓN / UN PROYECTO DISTINTO</span><div class="evidence-numbers"><div><strong>250–300</strong><span>facturas procesadas al día</span></div><div><strong>~16 h</strong><span>semanales ahorradas</span></div></div><p class="caio-ev-note">Resultado de un proyecto de automatización de facturas, no de la capacitación. Cada operación requiere su propia evaluación.</p></div>
</div>
<blockquote class="caio-insight"><p>{e(CAIO['insight'])}</p></blockquote>
</div></section>'''


def audience_section():
 items = ''.join(f'<li>{e(a)}</li>' for a in CAIO['audience'])
 return f'''<section class="service-section caio-audience" aria-labelledby="audience-title"><div class="container caio-audience-grid">
<div class="service-heading"><span class="section-label">PARA QUIÉN ES</span><h2 id="audience-title">Para dueños y directores<br><em>que quieren avanzar con IA.</em></h2><p>{e(CAIO['audience_note'])}</p></div>
<div><ul class="caio-audience-list">{items}</ul>
<div class="caio-pricing"><span class="section-label">INVERSIÓN</span><p class="caio-pricing-main">{e(CAIO['pricing'])}</p><p>{e(CAIO['pricing_note'])}</p></div></div>
</div></section>'''


def faq_section(faqs):
 return f'''<section class="service-section" aria-labelledby="faq-title"><div class="container faq-layout"><div class="service-heading"><span class="section-label">ANTES DE CONVERSAR</span><h2 id="faq-title">Preguntas<br><em>que vale la pena hacer.</em></h2></div><div class="service-faq">{''.join(faq_html(q, a) for q, a in faqs)}</div></div></section>'''


def head(title, description, url, canonical, robots=''):
 return f'''<!doctype html>
<html lang="es-MX"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#101312">
{robots}<title>{e(title)}</title><meta name="description" content="{e(description)}">{f'<link rel="canonical" href="{url}">' if canonical else ''}
<meta property="og:type" content="website"><meta property="og:locale" content="es_MX"><meta property="og:site_name" content="SAC Technology Studio"><meta property="og:url" content="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:image" content="{ORIGIN}/og-image.png"><meta property="og:image:width" content="1731"><meta property="og:image:height" content="909"><meta property="og:image:alt" content="SAC Technology Studio — Tecnología que resuelve."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{ORIGIN}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"><script src="/tracking.js" defer></script><script src="/analytics.js" defer></script><script src="/main.js" defer></script>
</head>'''


FOOTER = '''<footer class="footer theme-dark"><div class="container footer-top"><a href="/" class="footer-brand" aria-label="SAC, inicio">SAC<span>.</span></a><span>TECHNOLOGY STUDIO<br>DESIGNED TO SOLVE.</span><a href="#inicio" class="back-top">VOLVER ARRIBA</a></div><div class="container footer-bottom"><span>© <span id="year">2026</span> SAC. Technology Studio.</span><a href="/privacidad.html">Aviso de privacidad</a><button type="button" data-cookie-settings hidden>Cookies</button></div></footer>'''


def render_caio_service():
 url = ORIGIN + SERVICE_PATH
 others = ''.join(f'<a href="/servicios/{o["slug"]}">{e(o["name"])}</a>' for o in SERVICES if o['slug'] != 'acompanamiento-ia')
 return f'''{head(CAIO['service_title'], CAIO['service_description'], url, True)}<body class="service-page caio-page" data-service="{CAIO['service']}">
{header(current=SERVICE_PATH)}
<main id="contenido">
<section class="service-hero theme-dark caio-hero" aria-labelledby="hero-title"><div class="container">
<nav class="service-breadcrumb" aria-label="Ruta de navegación"><a href="/">Inicio</a><span aria-hidden="true">/</span><a href="/#empezar">Servicios</a></nav>
<div class="service-hero-grid"><div class="service-hero-copy"><p class="eyebrow">{e(CAIO['eyebrow'])}</p><h1 id="hero-title">{H(CAIO['h1'])}</h1><p class="service-intro">{e(CAIO['intro'])}</p>
<p class="caio-pilot-line"><strong>{e(CAIO['pilot'])}</strong> {e(CAIO['pilot_note'])}</p>
<div class="caio-hero-actions"><a class="button button-lime" href="#contacto" data-cta="hero">{e(CAIO['cta'])} <span aria-hidden="true">↗</span></a><a class="text-link light-link" href="#como-trabajamos" data-cta="hero-secundario">Conoce cómo funciona <span aria-hidden="true">↓</span></a></div></div>
{cycle()}</div>
<p class="service-hero-foot">DIRECCIÓN · ROADMAP · CAPACITACIÓN · COORDINACIÓN · SEGUIMIENTO</p>
</div></section>
{problem_section()}
{components_section()}
{how_section()}
{evidence_section()}
{audience_section()}
{faq_section(CAIO['faqs'])}
<section class="contact-section" id="contacto" aria-labelledby="contact-title"><div class="container contact-grid"><div class="contact-copy"><span class="section-label">ACOMPAÑAMIENTO MENSUAL</span><h2 id="contact-title">{e(CAIO['contact_title'])}</h2><p>{e(CAIO['contact_text'])}</p><p class="contact-reassurance">{e(CAIO['pilot'])} {e(CAIO['pricing'])}</p><div class="contact-whatsapp">{whatsapp_link()}<span class="contact-whatsapp-number">+52 492 119 1702</span></div><p class="caio-alt-path">¿Prefieres explorar primero? <a href="/diagnostico/">Haz el diagnóstico gratis</a>.</p></div><div class="contact-form-wrap"><div class="contact-form-top"><strong>Solicita una propuesta.</strong><span>ACOMPAÑAMIENTO</span></div>{caio_form(SERVICE_PATH, 'Nueva consulta — Acompañamiento mensual (Fractional CAIO) — SAC')}</div></div></section>
<aside class="container related-services" aria-label="Otros servicios de SAC"><p>Si buscas un proyecto puntual</p><div>{others}<a href="/mapa-ia">Mapa de IA</a></div></aside>
</main>{FOOTER}
</body></html>
'''


def render_caio_lp():
 url = ORIGIN + LP_PATH
 angles = json.dumps(CAIO['angles'], ensure_ascii=False)
 return f'''{head(CAIO['lp_title'], CAIO['lp_description'], url, False, '<meta name="robots" content="noindex, follow">')}<body class="service-page caio-page caio-lp" data-service="{CAIO['service']}">
<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header lp-header" id="inicio"><div class="container nav-wrap"><span class="brand"><span>SAC<span class="brand-dot">.</span></span><span class="brand-sub">TECHNOLOGY<br>STUDIO</span></span><a class="nav-cta" href="#contacto" data-cta="header">{e(CAIO['cta'])}</a></div></header>
<main id="contenido">
<section class="service-hero theme-dark caio-hero caio-lp-hero" aria-labelledby="hero-title"><div class="container">
<div class="caio-lp-grid"><div class="service-hero-copy"><p class="eyebrow">{e(CAIO['eyebrow'])}</p><h1 id="hero-title">{H(CAIO['h1'])}</h1>
<script>(()=>{{const m={angles};const k=(new URLSearchParams(location.search).get('utm_content')||'').trim().toLowerCase();const h=document.getElementById('hero-title');if(h&&Object.prototype.hasOwnProperty.call(m,k))h.innerHTML=m[k];}})();</script>
<p class="service-intro">{e(CAIO['intro'])}</p>
<p class="caio-pilot-line"><strong>{e(CAIO['pilot'])}</strong> {e(CAIO['pilot_note'])}</p>
<ul class="caio-lp-points"><li>Priorizamos qué vale la pena hacer con IA.</li><li>Capacitamos y acompañamos a tu equipo.</li><li>Damos seguimiento a las mejoras cada mes.</li></ul>
<div class="caio-hero-actions"><a class="button button-lime caio-lp-jump" href="#contacto" data-cta="hero">{e(CAIO['cta'])} <span aria-hidden="true">↓</span></a>{whatsapp_link('text-link light-link')}</div></div>
<div class="contact-form-wrap caio-lp-form" id="contacto"><div class="contact-form-top"><strong>{e(CAIO['cta'])}.</strong><span>RESPUESTA POR CORREO</span></div>{caio_form(LP_PATH, 'Nuevo lead (Meta Ads) — Acompañamiento mensual (Fractional CAIO) — SAC')}</div></div>
</div></section>
{problem_section()}
{components_section()}
{how_section()}
{evidence_section()}
{audience_section()}
{faq_section(CAIO['faqs'][:CAIO['lp_faqs']])}
<section class="caio-lp-close" aria-labelledby="close-title"><div class="container caio-lp-close-inner"><div><span class="section-label">EL PRIMER PASO</span><h2 id="close-title">Alguien que entienda tu negocio y te ayude <em>a avanzar cada mes.</em></h2><p>{e(CAIO['pricing'])} {e(CAIO['pilot'])}</p></div><div class="caio-lp-close-actions"><a class="button button-dark" href="#contacto" data-cta="cierre">{e(CAIO['cta'])} <span aria-hidden="true">↑</span></a>{whatsapp_link()}</div></div></section>
</main>
<footer class="footer theme-dark caio-lp-footer"><div class="container footer-bottom"><span>© <span id="year">2026</span> SAC. Technology Studio · Zapopan, Jalisco.</span><a href="/privacidad.html">Aviso de privacidad</a><button type="button" data-cookie-settings hidden>Cookies</button></div></footer>
</body></html>
'''


def header(current=''):
 caio = f'<a href="{SERVICE_PATH}"{" aria-current=\"page\"" if current == SERVICE_PATH else ""}>Dirección de IA</a>'
 return f'''<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header" id="inicio"><div class="container nav-wrap">
<a class="brand" href="/" aria-label="SAC, ir al inicio"><span>SAC<span class="brand-dot">.</span></span><span class="brand-sub">TECHNOLOGY<br>STUDIO</span></a>
<button class="menu-toggle" type="button" aria-controls="nav-menu" aria-expanded="false" aria-label="Abrir menú"><span></span><span></span></button>
<nav class="nav" id="nav-menu" aria-label="Principal"><a href="/#empezar">Servicios</a><a href="/#casos">Casos</a>{caio}<a href="#como-trabajamos">Cómo trabajamos</a><a class="nav-cta" href="#contacto" data-cta="header">Hablemos</a></nav>
</div></header>'''


HOME_START, HOME_END = '<!-- caio:inicio (generado por scripts/build_services.py) -->', '<!-- caio:fin -->'

if __name__ == '__main__':
 for d in SERVICES:
  if not d.get('custom'):
   (ROOT / 'servicios' / (d['slug'] + '.html')).write_text(render(d))
 (ROOT / 'servicios' / 'acompanamiento-ia.html').write_text(render_caio_service())
 (ROOT / 'direccion-ia.html').write_text(render_caio_lp())
 # Homepage: only the block between the markers is generated.
 home = (ROOT / 'index.html').read_text()
 a, b = home.index(HOME_START), home.index(HOME_END)
 home = home[:a + len(HOME_START)] + '\n    ' + home_section() + '\n    ' + home[b:]
 (ROOT / 'index.html').write_text(home)
 # Derive the previous origin from the existing homepage, allowing repeated migrations.
 match = re.search(r'property="og:image" content="(https?://[^"]+)/og-image.png"', home)
 previous = match.group(1) if match else ORIGIN
 for p in [ROOT / 'index.html', ROOT / 'gracias.html', ROOT / 'privacidad.html']:
  text = p.read_text()
  text = text.replace(previous, ORIGIN)
  p.write_text(text)
 # The campaign landing is noindex and stays out of the sitemap.
 urls = [ORIGIN + '/', ORIGIN + '/mapa-ia', ORIGIN + '/trabajo', *(ORIGIN + '/servicios/' + d['slug'] for d in SERVICES), ORIGIN + '/privacidad.html']
 (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{e(u)}</loc></url>\n' for u in urls) + '</urlset>\n')
 (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + ORIGIN + '/sitemap.xml\n')
 print('Generated service pages, campaign landing, homepage section, sitemap and robots.txt for', ORIGIN)
