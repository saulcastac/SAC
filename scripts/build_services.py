"""Generate committed, buildless service pages. Python standard library only."""
from pathlib import Path
from html import escape as e
import json
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
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
 faqs=[('¿Necesito cambiar mis sistemas actuales?','No necesariamente. Primero revisamos qué integraciones permiten tus herramientas. Si hay limitaciones, las ponemos sobre la mesa antes de proponer una solución.'),('¿Todo necesita inteligencia artificial?','No. Si una regla o una integración resuelve mejor la tarea, usamos esa opción. Incorporamos IA cuando aporta valor al proceso.'),('¿Qué pasa con los errores o las excepciones?','Definimos validaciones, permisos y puntos de revisión humana según el riesgo de cada actividad. Automatizar no elimina la necesidad de supervisar.'),('¿Cuánto cuesta y cuánto tarda?','Depende del proceso, las integraciones y el alcance. Después de entender tu necesidad, presentamos una propuesta con inversión, entregables y tiempos.')],
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
 dict(slug='acompanamiento-ia', name='Acompañamiento tecnológico', title='Acompañamiento tecnológico para empresas | SAC',
 description='Un equipo tecnológico externo para priorizar oportunidades de automatización e IA, definir un roadmap y acompañar las mejoras de tu empresa. Conoce SAC.',
 hero='La tecnología avanza todos los días. <em>Tu empresa también puede hacerlo.</em>', intro='Un equipo tecnológico externo que te ayuda a identificar oportunidades, definir prioridades y coordinar mejoras con sentido para tu negocio.', cta='Exploremos cómo trabajar juntos', kicker='CRITERIO PARA DECIDIR. CONTINUIDAD PARA AVANZAR.',
 visual=['Entender la operación', 'Definir prioridades', 'Dar seguimiento'], visual_title='Una dirección clara.<br>Un siguiente paso posible.', visual_note='Las herramientas cambian. Tus prioridades marcan el rumbo.',
 problem='No te faltan opciones. Te hace falta saber por dónde empezar.', problem_intro='Entre herramientas nuevas, pendientes internos y proveedores, es fácil invertir tiempo sin una dirección compartida.',
 problems=[('Muchas ideas, poco orden','Hay oportunidades de mejora, pero ninguna prioridad acordada.'),('Decisiones sin contexto','Elegir una herramienta se vuelve difícil cuando falta una mirada de toda la operación.'),('Iniciativas que se quedan a medias','El día a día desplaza los proyectos y nadie sostiene su seguimiento.')],
 applications=[('Diagnóstico de procesos','Entender cómo funciona la empresa y dónde hay fricción.'),('Roadmap tecnológico','Ordenar iniciativas por impacto, viabilidad y dependencias.'),('Asesoría y capacitación','Acompañar decisiones y preparar al equipo para los cambios.'),('Oportunidades de automatización','Evaluar tareas donde automatización o IA pueden aportar valor.'),('Coordinación de implementaciones','Alinear responsables, proveedores y entregables acordados.'),('Seguimiento de iniciativas','Revisar avances, obstáculos y siguientes decisiones.')],
 approach='Continuidad, con prioridades y alcance claros.', steps=[('Entendemos el punto de partida','Revisamos procesos, equipo, sistemas y objetivos de negocio.'),('Trazamos una ruta','Definimos oportunidades y una secuencia realista para abordarlas.'),('Acompañamos la ejecución','Coordinamos las iniciativas incluidas y facilitamos decisiones.'),('Revisamos y ajustamos','Damos seguimiento y actualizamos prioridades según lo aprendido.')],
 expectation='Acordamos frecuencia, responsabilidades y entregables. El desarrollo de software y las implementaciones se cotizan por alcance cuando no forman parte del acuerdo.', evidence=None,
 faqs=[('¿Necesito un equipo de tecnología interno?','No es indispensable. Podemos colaborar con dirección, responsables de área, tu equipo interno y proveedores existentes.'),('¿Incluye desarrollos ilimitados?','No. El acompañamiento tiene actividades y capacidad acordadas. Cada desarrollo o implementación se define y cotiza según su alcance.'),('¿Es lo mismo que contratar un CAIO?','Puede cubrir parte de esa función de orientación sobre IA, pero lo explicamos por lo que hacemos: ayudar a decidir, priorizar y coordinar mejoras. No todos los negocios necesitan un cargo ejecutivo adicional.'),('¿Cómo empezamos?','Con una conversación sobre tu operación y tus prioridades. A partir de ahí proponemos una forma de colaboración con objetivos, frecuencia y responsabilidades claras.')],
 contact='¿Qué necesita avanzar en tu empresa?', contact_text='Cuéntanos dónde están hoy y qué decisiones o iniciativas necesitan acompañamiento.', placeholder='Por ejemplo: tenemos varias ideas de automatización, pero necesitamos definir prioridades…'),
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

def header():
 return '''<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header" id="inicio"><div class="container nav-wrap">
<a class="brand" href="/" aria-label="SAC, ir al inicio"><span>SAC<span class="brand-dot">.</span></span><span class="brand-sub">TECHNOLOGY<br>STUDIO</span></a>
<button class="menu-toggle" type="button" aria-controls="nav-menu" aria-expanded="false" aria-label="Abrir menú"><span></span><span></span></button>
<nav class="nav" id="nav-menu" aria-label="Principal"><a href="/#soluciones">Servicios</a><a href="/#proyectos">Proyectos</a><a href="#como-trabajamos">Cómo trabajamos</a><a class="nav-cta" href="#contacto" data-cta="header">Hablemos</a></nav>
</div></header>'''

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
  return '''<section class="service-evidence theme-dark" aria-labelledby="evidence-title"><div class="container evidence-grid"><div><span class="eyebrow">EXPERIENCIA EN OPERACIÓN / VAX SOLUTIONS</span><h2 id="evidence-title">Menos trabajo manual.<br><em>Un resultado concreto.</em></h2><p>Automatizamos el procesamiento de facturas de VAX Solutions, una empresa de logística, centralizando la información y la generación de documentos y correos.</p><a class="text-link light-link" href="/#proyectos">Conoce nuestros proyectos</a></div><div class="evidence-numbers"><div><strong>250–300</strong><span>facturas procesadas diariamente</span></div><div><strong>~16 h</strong><span>semanales ahorradas</span></div><p>Resultados de este proyecto. Cada operación requiere su propia evaluación.</p></div></div></section>'''
 if d['evidence']=='rtc':
  return '''<section class="service-evidence theme-dark" aria-labelledby="evidence-title"><div class="container evidence-grid"><div><span class="eyebrow">PROYECTO REAL / RTC TRANSPORTES</span><h2 id="evidence-title">Una presencia digital<br><em>que explica su negocio.</em></h2><p>Desarrollamos un sitio corporativo para presentar los servicios de RTC Transportes y facilitar que nuevos clientes conozcan su oferta.</p><a class="text-link light-link" href="https://www.rtctransporte.com/" target="_blank" rel="noopener noreferrer">Visita RTC Transportes</a></div><div class="evidence-editorial"><span>RTC</span><p>TRANSPORTES</p><hr><p>Estrategia, contenido y desarrollo para una empresa de transporte.</p></div></div></section>'''
 return ''

def render(d):
 url=f"{ORIGIN}/servicios/{d['slug']}"
 problems=''.join(f'<article><h3>{e(t)}</h3><p>{e(p)}</p></article>' for t,p in d['problems'])
 apps=''.join(f'<div class="application-row"><h3>{e(t)}</h3><p>{e(p)}</p></div>' for t,p in d['applications'])
 steps=''.join(f'<li><h3>{e(t)}</h3><p>{e(p)}</p></li>' for t,p in d['steps'])
 faqs=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in d['faqs'])
 others=''.join(f'<a href="/servicios/{o["slug"]}">{e(o["name"])}</a>' for o in SERVICES if o!=d)
 return f'''<!doctype html>
<html lang="es-MX"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#101312">
<title>{e(d['title'])}</title><meta name="description" content="{e(d['description'])}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_MX"><meta property="og:site_name" content="SAC Technology Studio"><meta property="og:url" content="{url}"><meta property="og:title" content="{e(d['title'])}"><meta property="og:description" content="{e(d['description'])}"><meta property="og:image" content="{ORIGIN}/og-image.png"><meta property="og:image:width" content="1731"><meta property="og:image:height" content="909"><meta property="og:image:alt" content="SAC Technology Studio — Tecnología que resuelve."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{ORIGIN}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"><script src="/analytics.js" defer></script><script src="/main.js" defer></script>
</head><body class="service-page" data-service="{d['slug']}">
{header()}
<main id="contenido">
<section class="service-hero theme-dark" aria-labelledby="hero-title"><div class="container">
<nav class="service-breadcrumb" aria-label="Ruta de navegación"><a href="/">Inicio</a><span aria-hidden="true">/</span><a href="/#soluciones">Servicios</a></nav>
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
</main><footer class="footer theme-dark"><div class="container footer-top"><a href="/" class="footer-brand" aria-label="SAC, inicio">SAC<span>.</span></a><span>TECHNOLOGY STUDIO<br>DESIGNED TO SOLVE.</span><a href="#inicio" class="back-top">VOLVER ARRIBA</a></div><div class="container footer-bottom"><span>© <span id="year">2026</span> SAC. Technology Studio.</span><a href="/privacidad.html">Aviso de privacidad</a></div></footer>
</body></html>
'''

if __name__ == '__main__':
 for d in SERVICES:
  (ROOT / 'servicios' / (d['slug']+'.html')).write_text(render(d))
 # Derive the previous origin from the existing homepage, allowing repeated migrations.
 current = (ROOT/'index.html').read_text()
 match = re.search(r'property="og:image" content="(https?://[^"]+)/og-image.png"', current)
 previous = match.group(1) if match else ORIGIN
 for p in [ROOT/'index.html', ROOT/'gracias.html', ROOT/'privacidad.html']:
  text=p.read_text()
  text=text.replace(previous, ORIGIN)
  p.write_text(text)
 urls=[ORIGIN+'/',*(ORIGIN+'/servicios/'+d['slug'] for d in SERVICES),ORIGIN+'/privacidad.html']
 (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{e(u)}</loc></url>\n' for u in urls)+'</urlset>\n')
 (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+ORIGIN+'/sitemap.xml\n')
 print('Generated four service pages, sitemap and robots.txt for',ORIGIN)
