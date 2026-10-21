# Portal de lectura

El workflow despliega `_site/` mediante GitHub Pages después de compilar y guardar los PDF. Settings → Pages → Source debe estar en GitHub Actions. Se mantienen los permisos mínimos de Pages y el entorno `github-pages`.

Para previsualizar:

```bash
make pages
python3 -m http.server 8000 --directory _site
```

Abrir http://localhost:8000. El portal carga `papers.json` generado desde los metadatos comunes, verifica manifiestos y muestra revisión, fecha de fuentes y hash PDF. Los títulos y autores se editan solo en `papers.json` de la raíz; no en HTML ni JavaScript.

Los borradores incluyen `noindex, nofollow`. Esto solicita a los buscadores que no los indexen; no restringe el acceso público ni elimina copias existentes. En pantallas de hasta 800 px se oculta el visor integrado; «Abrir PDF» es la acción principal. Sin JavaScript quedan enlaces directos a ambos PDF. El diseño se mantiene en `web/`; el HTML es una plantilla que se sirve tras ejecutar el generador.
