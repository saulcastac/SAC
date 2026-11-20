# SAC Technology Studio

Sitio estático en HTML, CSS y JavaScript, publicado en Vercel.

## Contacto

El formulario envía por POST a FormSubmit y dirige las consultas a saulcastac@gmail.com. Incluye consentimiento obligatorio, honeypot y la verificación antispam predeterminada del servicio. El primer envío requiere activar el formulario desde el correo de confirmación de FormSubmit; después debe comprobarse la recepción de una consulta real. No requiere claves API ni backend propio.

## Contenido

Tres casos: RTC Transportes, automatización de facturación de Vax Solutions y plataforma de gestión para un consultorio de cirugía de columna. El propietario confirmó las métricas de Vax Solutions (250–300 facturas/día y aproximadamente 16 horas ahorradas/semana) y autorizó su publicación.

Aviso de privacidad en privacidad.html, con los datos proporcionados por el propietario: SAC SA de CV, Zapopan, Jalisco, México. El domicilio proporcionado solo especifica ciudad y estado; queda pendiente completar la dirección de contacto para mayor precisión.

## Desarrollo

Ejecutar `python -m http.server 8000 --bind 127.0.0.1` y abrir http://127.0.0.1:8000.

## Despliegue

Proyecto de Vercel: sac-technology-studio
ID: prj_6dzateTrGZsZwh9EqmvwnUpr17aw
Equipo: team_AwBkmnPtSDRBTVB5OCHO6QBw

Publicar únicamente index.html, styles.css, main.js, favicon.svg, privacidad.html y vercel.json. La configuración usa alojamiento estático, sin instalación ni compilación. No subir notas internas o archivos de credenciales.

## Pendientes

- Activación de FormSubmit y prueba de recepción de correo.
- Imagen para compartir (Open Graph).
- Prueba final en teléfonos reales y de todo el recorrido de contacto.
- Dominio propio y analítica cuando se definan.
