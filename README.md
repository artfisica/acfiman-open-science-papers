# Ciencia abierta y computación reproducible: manuscritos ACFIMAN

Dos primeros borradores completos en español, derivados de los resúmenes ICHEP 2026 aceptados #668 y #667. Estado: **revisión de autores; no enviados al Boletín**.

| Manuscrito | Texto principal | PDF actual |
|---|---|---|
| Comunidades de ciencia abierta | [main.tex](papers/01-comunidades-abiertas/main.tex) | [Leer PDF](papers/01-comunidades-abiertas/pdf/manuscript.pdf) |
| Computación para formación en física | [main.tex](papers/02-computacion-reproducible/main.tex) | [Leer PDF](papers/02-computacion-reproducible/pdf/manuscript.pdf) |

[Comandos para crear el repositorio](docs/IMPORT.md).

## Empezar en Codespaces
1. Crear un repositorio vacío, inicialmente privado mientras se aclara la política de preprints de ACFIMAN.
2. Subir **el contenido de esta carpeta**, incluidas `.github`, `.devcontainer` y `.vscode` (no el ZIP ni una carpeta contenedora adicional).
3. Abrir Code → Codespaces → Create codespace. La instalación de TeX tarda varios minutos y necesita conexión; el contenido posterior se compila localmente sin descargar fuentes bibliográficas.
4. Editar `papers/<articulo>/text/*.tex`; cambiar metadatos en `main.tex` y referencias en `references.tex`.
5. Ejecutar `make all` y abrir el PDF desde el explorador. Ctrl/Cmd+Shift+B también construye ambos.
6. Guardar y subir cambios: `git add .`, `git commit -m "Revisar discusión"`, `git push`.
7. Actions compila. En la rama predeterminada, otro job guarda los PDF con un commit del bot. Antes de seguir editando: `git pull --ff-only` con el árbol de trabajo limpio. Si hay cambios propios, guardarlos en un commit antes del pull; no sobrescribirlos.

Cada artículo contiene `text/`, `figures/` (fuente .tex + PDF), `data/` (evidencia agregada), `sources/` (procedencia y resumen aceptado), `pdf/` (un PDF y manifiesto), `main.tex` y `references.tex`.

## Automatización y permisos
`.github/workflows/papers.yml` compila ambos artículos en pushes, PR y ejecuciones manuales. Los PR solo validan con permiso de lectura. Solo la rama predeterminada puede publicar; el job de publicación tiene `contents: write`. No necesita PAT ni secretos adicionales.

Settings → Actions → General: permitir las acciones usadas. La política de organización debe permitir `GITHUB_TOKEN` con escritura. Las reglas de la rama pueden impedir el push automático; si requieren PR para todos los commits, esta modalidad de escritura directa no funcionará sin una política compatible. No se eluden protecciones: revisar con el administrador o integrar los PDF mediante PR.

Los PDF se sobrescriben siempre en la misma ruta: no hay carpetas v1/v2 ni copias fechadas. **Git conserva versiones históricas**, como debe hacerlo un repositorio. Los artifacts son respaldo temporal de 7 días, no la única entrega. Los commits del token de GitHub no desencadenan otro push workflow; además se excluyen las rutas de salidas. Un fallo de compilación conserva los PDF anteriores. Si la rama avanza durante la compilación, se rechaza el resultado desactualizado; ejecutar de nuevo sobre la revisión actual. Nunca se fuerza el push.

## Comandos
- `make all`: verificar y compilar ambos.
- `make community` / `make computing`: compilar uno.
- `make check`: límites de resúmenes, orden de citas y registro de evidencia.
- `make export`: generar `dist/<articulo>.zip` con main.tex autocontenido, PDF y figuras para revisión editorial. Sigue siendo borrador.
- `make clean`: eliminar auxiliares; conservar PDF actuales.

En Ubuntu fuera de Codespaces: `bash scripts/install-tex.sh`. En macOS con MacTeX instalado: `make all` (se necesitan Python 3 y las fuentes Latin Modern).

## Para aprender con este repositorio
Cambiar una frase del resumen, ejecutar `make all`, abrir el PDF y revisar `git diff`. Después cambiar el diagrama en `figures/modelo.tex`, recompilar y observar que fuente, figura y manuscrito siguen conectados. No editar los PDF manualmente. Un ejercicio adicional y el diseño del flujo están en [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Fuentes y límites
Las cifras pendientes se identifican en el texto y en cada `data/evidence.csv`. No hay registros inventados de alumnos ni resultados simulados presentados como mediciones. [Revisión editorial](docs/EDITORIAL.md), [derechos](RIGHTS.md) y [validación](docs/VALIDATION.md).

Este ZIP prepara un repositorio nuevo; no modifica los repositorios de contexto ni crea uno remoto. Las configuraciones de entorno fijan Ubuntu 24.04 y la familia de acciones v4, pero apt y las etiquetas no son inmutables: la repetibilidad funcional no promete identidad binaria entre futuras versiones de TeX. El manifiesto conserva el motor y hashes de fuentes/salida.

## Portal de lectura / GitHub Pages

El portal permite seleccionar, leer y descargar ambos manuscritos. Consulta
[docs/PAGES.md](docs/PAGES.md) para activarlo y previsualizarlo. Los archivos de
`web/` definen el diseño; `scripts/build_pages.py` copia los PDF verificados.
El mismo workflow compila, actualiza los PDF del repositorio y despliega el portal.
