# Flujo de edición y publicación

1. Modificar fuentes y `papers.json` en Codespaces; ejecutar `make all`.
2. Revisar ambos PDF, guardar las fuentes en un commit y subirlo.
3. CI usa la misma imagen TeX Live por digest que Codespaces. Las acciones están fijadas por SHA. El job de construcción solo puede leer el repositorio.
4. En la rama predeterminada, el job `publish` verifica que la rama no avanzó, recupera los resultados y actualiza los PDF, figuras y manifiestos con un commit. Nunca fuerza un push. Un rechazo por protección de rama debe resolverse mediante la política del repositorio, no eludiéndola.
5. Pages despliega el mismo conjunto de resultados tras completar la publicación. Cada ruta contiene el PDF más reciente; el manifiesto permite identificar su contenido.
6. Guardar cambios locales y ejecutar `git pull --ff-only` antes de continuar escribiendo.

## Procedencia

El banner y el portal muestran `source_commit` y `source_date`: último commit de texto, metadatos, datos o fuentes de figuras del artículo. `build_commit` y `build_date` identifican scripts, preámbulo y configuración de compilación. `SOURCE_DATE_EPOCH` usa el mayor de ambos tiempos. Un commit del bot que solo guarda salidas no cambia esa revisión. Los manifiestos incluyen hashes de fuentes, scripts y configuración; la hoja de trabajo CoAfina incluye su CSV. El ledger editorial `evidence.csv` no se presenta como entrada de LaTeX. El motor real y el entorno declarado se registran por separado. Fijar una imagen reduce variación de herramientas, pero no garantiza por sí solo igualdad binaria en cualquier arquitectura.

Las fechas mostradas son fechas de **revisión de las fuentes**, no hora de descarga ni fecha de publicación editorial. Los cambios locales se marcan. Para actualizar el contenedor, revisar el nuevo digest y cambiarlo simultáneamente en workflow y Codespaces; `make check` comprueba esa igualdad. La imagen Debian elegida incluye Git, Python, Make y TeX Live; no se ejecuta instalación apt en CI.

## Verificación

Se comprueban longitud de resúmenes, orden y resolución de citas, etiquetas referenciadas, IDs de evidencia, metadatos de envío y paridad de contenedor. La compilación falla ante referencias sin resolver o desbordamientos mayores de 5 pt; los menores se notifican para revisión visual. `make export` exige el modo estricto y vuelve a compilar antes de empaquetar.

## Hitos opcionales

Los commits de PDF se mantienen. Para un hito revisado puede añadirse un tag y una Release, sin cambiar las rutas actuales. Antes de crearla, copiar los dos PDF a nombres distintos (`comunidades.pdf` y `computacion.pdf`) para evitar colisiones de assets, acompañados de sus manifiestos. No publicar una Release ni activar archivo externo hasta elegir el hito y revisar su contenido. El hash y la revisión del portal permiten identificar también borradores intermedios.

Codespaces construye una capa mínima sobre la misma imagen TeX fijada por digest que CI; añade el usuario no privilegiado `vscode`. No instala ni actualiza paquetes TeX. La validación estática verifica el digest común; la reconstrucción del contenedor debe comprobarse en Codespaces.

Los pendientes explícitos del texto usan `\editorialtodo{...}`. Expresiones legítimas como «pendiente de evaluación» no bloquean el envío. Una portada mutable de LA-CoNGA requiere un archivo fechado. Los informes de evento con URL propia pueden documentarse en `source-preservation.json`, con fecha, fuente corroborante citada y límites de cobertura. El control admite esta revisión explícita o una URL Wayback; avisa en borrador y bloquea en modo estricto cuando no existe ninguna. No garantiza disponibilidad futura ni confunde corroboración con una copia idéntica.

Los cuadros de ediciones y cocientes se generan desde los CSV públicos documentados. Los números aproximados y los denominadores abiertos se conservan; no se rellenan valores ausentes ni se calculan promedios entre métricas distintas.

Identidad de los próximos commits personales (configuración local, no global):

```bash
git config --local user.name "Arturo Sánchez Pineda"
git config --local user.email "me@arturos.ch"
```

No reescribimos la historia publicada. Los commits automáticos mantienen la identidad del bot.
