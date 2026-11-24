# Revisión de la ampliación de servicios

Fecha: 20 de noviembre de 2026. Rama: `codex/servicios-landings`.

## Comprobaciones completadas

- HTML de siete páginas: un H1 por página, sin IDs duplicados, destinos internos y assets existentes, canonical/Open Graph de las cuatro landings.
- Cuatro rutas sin extensión y recursos principales responden HTTP 200 en el servidor local que replica los rewrites exactos de `vercel.json`.
- Arquitectura Vercel: estática, raíz como output, install/build deshabilitados. No se añadió framework ni dependencias de ejecución.
- Formularios: POST nativo a FormSubmit, nombre/correo/mensaje/consentimiento obligatorios, empresa opcional, honeypot, asunto y servicio de origen, `_next` público, sin desactivar CAPTCHA. No se hicieron envíos reales.
- `node --check` para ambos scripts del navegador.
- Pruebas de runtime: ausencia de componentes opcionales, captura de UTM, analítica apagada por defecto, consentimiento/revocación, almacenamiento bloqueado, ausencia de campos personales en el contrato, retorno con envío pendiente y deduplicación, visita directa a gracias sin conversión.
- Navegador local: cuatro landings a 1440, 820 y 390 px de ancho, sin overflow horizontal y con un H1. Se inspeccionaron visualmente automatización y acompañamiento en escritorio, capacitación en tablet y móvil, desarrollo y formulario en móvil.
- Menú móvil: abrir y cerrar, actualización de `aria-expanded`, cierre con Escape. FAQ: abrir con Enter. Pestañas originales de proceso: clic y navegación con flechas. Enlace desde homepage a capacitación: navegación correcta.
- Sin mensajes de error o advertencia en consola durante la revisión de las landings, homepage, agradecimiento y privacidad.

Comandos reproducibles en README. La captura de campaña se valida con valores sintéticos en la prueba de runtime; el inspector de navegador oculta valores de campos del formulario.

## Límites y pendientes

- No se publicó ni se integró en `main`. La verificación HTTP local replica Vercel; aún falta comprobar el despliegue real de esta ampliación cuando se autorice una publicación o preview remoto.
- No se enviaron mensajes de prueba, no se resolvió CAPTCHA y no se comprobó entrega de correo o retorno real de FormSubmit. El funcionamiento del formulario existente fue confirmado por el propietario; la estructura de los nuevos conserva su integración.
- Las pruebas de pantallas son de navegador, no teléfonos físicos.
- Analítica y publicidad permanecen deshabilitadas. No se verificó proveedor externo porque no hay identificadores, adaptador ni gestor de consentimiento configurados.
- La señal futura de contacto completado refleja el retorno al agradecimiento con un intento previo, no la entrega autoritativa del correo. Ver detalles en README.

## Dirección de IA externa (rama `feat/fractional-caio`, 24 de noviembre de 2026)

- `check_site.py`: 8 páginas, 7 rutas limpias; `/direccion-ia` con `noindex`, sin canonical ni navegación, fuera del sitemap; formularios CAIO con empresa, cargo y colaboradores obligatorios y `servicio_origen=fractional-caio`. Se corrigieron anclas rotas preexistentes (`#proyectos`, `#soluciones`).
- `test_runtime.mjs`: puente de Meta con un solo `PageView`, `ViewContent` solo para la oferta CAIO, `SubmitAttempt` separado de `Lead`, nada sin consentimiento y sin datos personales.
- Chrome (headless) a 1440 y 390 px: homepage, servicio y landing con cada `utm_content` y un valor no permitido (`<img src=x>`, que deja el H1 por defecto). Sin overflow horizontal ni errores de consola.
- El generador se ejecutó dos veces sin diferencias (idempotente) y conserva la FAQ de precios de automatización y el sitemap con `/mapa-ia` y `/trabajo`.
- Pendiente: probar en un preview de Vercel, enviar un formulario real y verificar eventos con el Test Events de Meta.
