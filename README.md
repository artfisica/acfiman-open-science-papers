# Ciencia abierta y computación reproducible

Dos ensayos en preparación, mantenidos públicamente con fuentes LaTeX, datos documentales y PDF. Este es un proyecto independiente de los autores; no implica aceptación editorial.

| Ensayo | Fuentes | PDF actual |
|---|---|---|
| Comunidades científicas | [Texto](papers/01-comunidades-abiertas/main.tex) | [PDF](papers/01-comunidades-abiertas/pdf/manuscript.pdf) |
| Computación para formación en física | [Texto](papers/02-computacion-reproducible/main.tex) | [PDF](papers/02-computacion-reproducible/pdf/manuscript.pdf) |

[Portal de lectura](https://artfisica.github.io/acfiman-open-science-papers/)

## Escribir y compilar

Abrir el repositorio en Codespaces. CI y Codespaces utilizan la misma imagen TeX Live fijada por digest; la primera descarga puede tardar. No se reinstala TeX con apt en cada sesión. La imagen es Linux amd64.

Editar `papers/<artículo>/text/`, `references.tex`, `tables/` o `figures/`. Títulos, autores, afiliaciones y estado se editan **solo en `papers.json`**. Los archivos `build/metadata.tex` y `build/ediciones-body.tex` se generan automáticamente.

```bash
make all             # validar y compilar ambos
make community       # validar y compilar el ensayo comunitario
make computing       # validar y compilar el ensayo técnico
make pages           # compilar y preparar _site/
make check STRICT=1  # comprobar condiciones de envío
make export          # exige estado listo; genera dist/*.zip
```

Con MacTeX, Python 3 y Latin Modern también puede ejecutarse `make all` localmente. El manifiesto identifica ese entorno como local; las compilaciones oficiales usan la imagen fijada. [Detalles del flujo](docs/WORKFLOW.md).

## Guardar revisiones

Hacer commit de las fuentes y push. GitHub Actions valida los cambios y, en la rama predeterminada, **sobrescribe los PDF actuales mediante un commit del bot**; después despliega Pages. Cada artículo mantiene una sola ruta de PDF. Git conserva el historial. Antes de continuar, guardar los cambios propios y ejecutar `git pull --ff-only` para incorporar la actualización automática. Las propuestas de cambio solo compilan con permisos de lectura.

Cada PDF tiene un manifiesto con revisión y fecha de las fuentes, hashes de entrada y salida y motor real. Los commits que solo actualizan PDF no cambian la fecha de las fuentes. Un árbol modificado se identifica como «cambios locales». El portal muestra la revisión y el hash del PDF.

## Evidencia y envío

Cada artículo contiene `data/`, `text/`, `tables/`, `figures/`, `sources/` y `pdf/`. La tabla por edición de CoAfina se genera desde CSV; ND significa no documentado, no cero. Los registros históricos de consumo y participación que faltan se detallan en [el plan de evidencia](docs/EVIDENCE-PLAN.md).

La [lista editorial](docs/CHECKLIST.md) mantiene los requisitos pendientes. `make export` no prepara un envío mientras falten direcciones, contacto, declaraciones, revisión de evidencia o confirmación editorial de compatibilidad con el preprint público. Una [consulta a la revista](docs/EDITOR-QUERY.md) queda preparada para que los autores la envíen.

El código de automatización y del portal usa [MIT](LICENSE-CODE). Los manuscritos, datos y figuras conservan sus derechos según [RIGHTS.md](RIGHTS.md). `CITATION.cff` describe el software editorial; la autoría de cada ensayo está en `papers.json`.
