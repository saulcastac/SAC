# SAC Technology Studio

Sitio estático en HTML, CSS y JavaScript vanilla. Sin paquetes, instalación ni compilación para desplegar en Vercel. La ampliación de servicios se prepara en `codex/servicios-landings`; requiere revisión y autorización antes de integrarse a `main`.

## Páginas y rutas

| Ruta pública | Archivo |
| --- | --- |
| `/` | `index.html` |
| `/servicios/automatizacion-ia` | `servicios/automatizacion-ia.html` |
| `/servicios/capacitacion-ia` | `servicios/capacitacion-ia.html` |
| `/servicios/acompanamiento-ia` | `servicios/acompanamiento-ia.html` |
| `/servicios/desarrollo-web` | `servicios/desarrollo-web.html` |
| `/privacidad.html` | Aviso de privacidad |
| `/gracias.html` | Confirmación, excluida de buscadores con `noindex` |

`vercel.json` contiene cuatro rewrites exactos a los HTML. Permiten acceso directo y recarga en las rutas sin extensión. No hay fallback de SPA ni framework. La homepage conserva hero, proyectos, proceso, filosofía y contacto; las cuatro tarjetas enlazan a los servicios.

## Desarrollo y revisión

Desde la raíz:

```sh
python3 scripts/preview.py
```

Abrir `http://127.0.0.1:8000`. Este servidor replica los rewrites de Vercel; `python -m http.server` por sí solo no resuelve las rutas sin extensión. El servidor de revisión no procesa POST. Los formularios apuntan al FormSubmit real: no enviar datos durante QA.

Comprobaciones (con el servidor activo para la prueba HTTP):

```sh
python3 scripts/check_site.py
node --check main.js
node --check analytics.js
node scripts/test_runtime.mjs
```

`QA.md` describe lo verificado y sus límites.

## Contenido compartido y dominio

`styles.css` contiene la identidad existente y los patrones comunes de las landings. `main.js` inicializa menú, pestañas y formulario solo cuando existen sus elementos. Los HTML completos permiten leer, navegar, abrir FAQ y enviar formularios sin JavaScript; UTMs y eventos requieren JavaScript.

Las landings se generan con la biblioteca estándar de Python desde `scripts/build_services.py`. Editar allí el copy y las plantillas compartidas y ejecutar:

```sh
python3 scripts/build_services.py
```

Los HTML generados se guardan en Git y Vercel los sirve directamente; Python no es una dependencia de producción.

El origen público temporal está en `site-config.json`. Para cambiarlo, editar `origin` y ejecutar el generador. Actualiza canonical, Open Graph, imagen social, `_next`, sitemap y robots, incluida la homepage y páginas auxiliares. Los enlaces y assets internos usan rutas del mismo sitio. Revisar el diff antes de subir. No hay dominio nuevo contratado ni correo cambiado.

Cada landing tiene title, descripción, H1, canonical y Open Graph propios; se reutiliza `og-image.png` (1731 × 909), que solo descargan las plataformas al compartir, no las landings. `sitemap.xml` incluye páginas públicas y `robots.txt` señala su ubicación. Las ilustraciones son CSS y no requieren imágenes adicionales ni fuentes externas. Las animaciones respetan reduced motion.

## Contacto

El propietario confirmó que el formulario existente está activado y funciona. Todos los formularios usan POST nativo a `https://formsubmit.co/saulcastac@gmail.com`, con consentimiento obligatorio, honeypot y antispam predeterminado de FormSubmit. No se desactiva CAPTCHA ni se intercepta el envío con AJAX.

Cada formulario incluye `servicio_origen`, `landing_origen`, asunto específico y `_next` hacia la página pública de agradecimiento. Nombre, correo, mensaje y consentimiento son obligatorios; empresa es opcional. Las cinco UTMs (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`) se leen de la URL actual, se limitan a 200 caracteres y se adjuntan a la consulta. Se conservan al visitar enlaces a otros servicios; no se usan cookies ni almacenamiento persistente para la atribución. Sin JavaScript siguen funcionando formulario y servicio de origen, pero no se capturan UTMs.

WhatsApp es secundario: `+52 492 119 1702`. Las landings preparan un mensaje con el servicio de interés. No se simula un calendario de reuniones.

## Analítica: preparada, deshabilitada

`analytics.js` no carga SDKs, no contiene Pixel ID, no hace solicitudes de red ni crea cookies. Por defecto tampoco almacena datos o emite eventos. No hay banner porque no se ha activado seguimiento opcional.

Contrato preparado: `window` recibe un `CustomEvent('sac:analytics', { detail })` con:

| Evento | Significado |
| --- | --- |
| `landing_view` | Visita tras consentimiento |
| `cta_click` | Clic en CTA principal; incluye ubicación `hero` o `header` |
| `whatsapp_click` | Clic al enlace `wa.me` |
| `contact_submit` | Intento de envío que superó la validación nativa |
| `contact_completed` | Retorno a gracias con envío pendiente de la misma pestaña, dentro de 30 minutos |

Payload: `event`, `service`, `landing` (solo path), UTMs presentes y `placement` cuando corresponda. Nunca se lee el nombre, correo, empresa o mensaje para eventos. No se incluyen la URL completa ni parámetros de consulta arbitrarios.

`contact_completed` es una señal de retorno desde el flujo del formulario, no una verificación de entrega del correo. Requiere consentimiento y almacenamiento de sesión disponible; no cuenta una visita directa a gracias ni vuelve a contar al recargar. Un visitante que navegue manualmente a gracias después de intentar enviar puede producir una señal; la confirmación autoritativa requiere un backend o webhook futuro. Si el almacenamiento está bloqueado o se cambia de pestaña, no se registra esa señal.

Para activar medición en el futuro:

1. Elegir proveedor e informar finalidades, conservación y transferencias en el aviso.
2. Implementar un gestor real de consentimiento opcional, separado del consentimiento de contacto, con posibilidad de revocación.
3. Definir `window.SAC_ANALYTICS_CONFIG = { enabled: true }` **antes** de cargar `analytics.js`.
4. Solo tras consentimiento correspondiente, cargar el proveedor y conectar un adaptador al evento `sac:analytics`. Un adaptador puede traducir `contact_completed` a `Lead` de Meta, evitando duplicados.
5. En cada página, el gestor debe llamar `window.SACAnalytics.setConsent(true)` únicamente cuando tenga consentimiento válido; al rechazar o revocar, llamar con `false` y detener también el proveedor. El puente no persiste el consentimiento ni lo deduce del formulario.
6. Probar consentimiento, rechazo, revocación y deduplicación con identificadores reales autorizados, en preview.

### Meta Pixel (`tracking.js`)

`tracking.js` implementa el gestor de consentimiento y el adaptador de Meta. Se carga antes de `analytics.js` y de `diagnostico.js` en todas las páginas (también en la plantilla de `build_services.py`).

- Con `PIXEL_ID = ''` no hace nada: sin banner, sin red, sin cookies, y el botón «Cookies» del pie sigue oculto.
- Con un Pixel ID: banner con «Aceptar» y «Rechazar» del mismo peso; la elección se guarda 180 días en `localStorage` (`sac:consent:v1`) y se cambia desde cualquier `[data-cookie-settings]`. Solo al aceptar se carga `fbevents.js`; al rechazar se revoca y se borran `_fbp`/`_fbc`.
- Habilita `SAC_ANALYTICS_CONFIG` y llama `SACAnalytics.setConsent()`. Traducción: `contact_completed` → `Lead` (`content_name: contacto_<servicio>`), `whatsapp_click` → `Contact`, `cta_click` → `CTAClick`.
- Diagnóstico: `track()` usa `window.SACTrack` → `ViewContent`, `StartDiagnostic`, `Lead`, `BookingLinkClick`, `Schedule` (cita confirmada por HubSpot). Los eventos previos a la decisión quedan en cola y se envían solo si se acepta.
- Nunca se envían nombre, correo, teléfono, empresa ni respuestas. Pendiente: API de Conversiones (servidor) y deduplicación por `event_id`.

## Evidencia y privacidad

Solo se usan casos documentados: VAX Solutions (250–300 facturas diarias y aproximadamente 16 horas semanales ahorradas), RTC Transportes y plataforma de gestión clínica. No se inventan testimonios o resultados de capacitación y acompañamiento. Los resultados de VAX corresponden a ese proyecto y no son garantía para otros.

Aviso: SAC SA de CV, Zapopan, Jalisco, México; correo existente. Queda pendiente completar el domicilio proporcionado para mayor precisión. La actualización describe servicio de origen y UTMs adjuntos al contacto, y deja claro que la analítica publicitaria no está activa. Antes de activarla habrá que completar proveedor, conservación y consentimiento.

## Despliegue

Proyecto existente de Vercel: `sac-technology-studio`.

- ID: `prj_6dzateTrGZsZwh9EqmvwnUpr17aw`
- Equipo: `team_AwBkmnPtSDRBTVB5OCHO6QBw`
- Publicación estática, sin install ni build, raíz como output.
- `.vercelignore` excluye scripts, documentación y configuración de generación del paquete de despliegue.
- Publicar HTML raíz, carpeta `servicios/`, CSS, ambos JS, favicon, imagen social, sitemap, robots y configuración de Vercel juntos.

No integrar esta rama a `main` ni publicar en producción sin autorización. Una revisión local está disponible mediante el servidor de preview. Las pruebas locales de rewrites no sustituyen una comprobación final en Vercel tras aprobar el despliegue.

## Configuración pendiente

- Revisar y aprobar contenido antes de integrar.
- Validar rutas exactas y retorno de FormSubmit en un preview autorizado de Vercel; no se hicieron envíos reales durante la implementación.
- Pixel/analítica y gestor de consentimiento: sin configurar y deshabilitados.
- Dominio y correo nuevos: pospuestos por el propietario.
