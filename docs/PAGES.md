# Portal de lectura

Sitio estático en español con selector de dos manuscritos, visor PDF, enlaces de
descarga y acceso al código fuente. Es independiente de ACFIMAN. No utiliza
analítica, fuentes externas ni dependencias de JavaScript.

## Activación inicial

Después de crear y subir el repositorio público `artfisica/acfiman-open-science-papers`,
activa Pages antes de subir este cambio:

```sh
gh api --method POST repos/artfisica/acfiman-open-science-papers/pages -f build_type=workflow
```

Si Pages ya estaba activado, utiliza `--method PUT` en lugar de POST para seleccionar
GitHub Actions como origen. Alternativa: Settings → Pages → Build and deployment
→ Source → GitHub Actions. El workflow necesita permiso para escribir contenidos;
las reglas de protección que prohíban el push del bot impedirán la actualización
original de los PDF y, por dependencia, el despliegue.

Consulta la dirección real con:

```sh
gh api repos/artfisica/acfiman-open-science-papers/pages --jq .html_url
```

La dirección habitual es https://artfisica.github.io/acfiman-open-science-papers/.
Los enlaces relativos también funcionan bajo la ruta de un proyecto.

## Actualizaciones

1. Edita los manuscritos y sube los cambios a `main`.
2. `build` compila los PDF, comprueba sus hashes y prepara `_site/`.
3. `publish` guarda los PDF en sus rutas habituales del repositorio.
4. `deploy-pages` publica exactamente los PDF del mismo build.

No depende de que el commit automático dispare otro workflow. Las pull requests
validan y compilan, pero no publican. Los cambios exclusivamente en Markdown o en
los PDF siguen las exclusiones del workflow original; para publicarlos usa el
botón Run workflow o `gh workflow run papers.yml`. Si avanza la rama antes de que
el bot publique, la comprobación existente detiene ese build; el siguiente build
puede publicar la revisión más reciente. No se fuerza ningún push.

Cada URL PDF muestra la versión vigente. Git conserva su historial habitual;
el sitio no crea una colección de versiones. La caché del navegador puede requerir
una recarga para mostrar un PDF recién actualizado.

## Previsualización local

Con Python 3 y los PDF ya presentes (no necesitas LaTeX para esta vista):

```sh
python3 scripts/build_pages.py
python3 -m http.server 8000 --directory _site
```

Abre http://localhost:8000. Para recompilar primero los manuscritos usa `make all`
en Codespaces. `_site/` es temporal y no se añade a Git. Edita textos/estructura en
`web/index.html`, estilos en `web/styles.css` y selección de manuscrito en
`web/app.js`. Si cambias títulos o autores, actualiza tanto HTML como JavaScript.

En navegadores móviles que no soporten el visor integrado, los enlaces Abrir PDF
y Descargar dan acceso al documento completo. Sin JavaScript hay enlaces a ambos
PDF. Para compartir la selección usa `#comunidades` o `#computacion`.
