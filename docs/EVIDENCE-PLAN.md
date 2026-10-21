# Evidencia por completar

## CoAfina

`coafina-editions.csv` distingue el recuento publicado de estudiantes de inscritos, activos y personas que finalizan. Para 2023 están documentados 78 estudiantes, 16 equipos, ocho países y 30 universidades. Las demás celdas siguen como ND; no se infieren a partir de invitaciones ni agregados de varias ediciones.

Para cada edición 2022–2025, incorporar un registro agregado con fechas, definiciones de actividad y finalización, denominadores, países, universidades, entregas y fuente estable. Conservar el registro original fuera del repositorio si contiene datos personales y publicar solo agregados necesarios. Las convocatorias documentan intención y calendario; no acreditan asistencia. La página principal del hackatón es mutable: recuperar la convocatoria o informe histórico de 2025 antes de marcar su evidencia como verificada.

## Salud para todos

ALAN 2026 fecha un seguimiento en 2022; el boletín de Cornell anuncia Editathon V2 para febrero de 2023. Hasta aclarar si son eventos distintos o un error de fecha, el ensayo usa las métricas de 2021 y omite el seguimiento hasta aclarar la fecha, sin combinar cohortes. El premio OMS se atribuye expresamente a lo informado por la publicación.

## Enseñanza y consumo computacional

No se conserva como resultado la afirmación de 80 estudiantes en menos de diez minutos. Para recuperarla hacen falta intervalo definido, denominador y registros de ejecución. Las cifras de costo o fallos tampoco pueden reconstruirse desde una lista de docentes.

En `papers/02-computacion-reproducible/data/` hay dos plantillas **vacías**: `sessions-template.csv` y `usage-template.csv`. Las primeras registran resultados de validación y tiempos; las segundas, recursos de máquina y almacenamiento. `scripts/summarize_usage.py` calcula agregados sin inventar registros ni convertir una estimación en factura. No subir identificadores de cuentas ni datos personales.

Las horas-núcleo se calculan como núcleos asignados por horas activas. Los GB-hora requieren integrar almacenamiento durante el tiempo que existe, incluyendo entornos detenidos y prebuilds. Añadir el uso de Actions y registrar tarifas, moneda, descuentos y fecha por separado. La factura real puede incluir cuotas y ajustes distintos de una estimación bruta. Registrar las incidencias por categorías sin atribuir a cohortes históricas los riesgos hipotéticos del cuadro del ensayo.

Para reproducir una escuela deben fijarse commit de ejercicios, digest de imagen, versión de datos, condiciones de prebuild y comando de validación. Los repositorios públicos actuales documentan materiales; no reconstruyen por sí solos sesiones pasadas.

La tabla del manuscrito resume ahora hallazgos documentados; la hoja por edición queda fuera del texto hasta completar la extracción. El ensayo no promete un inventario longitudinal completo. Véase `AUTHOR-INPUTS.md` para los datos y recuerdos concretos que aún se necesitan.
