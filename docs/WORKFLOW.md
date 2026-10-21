# Del cambio al PDF

| Etapa | Lugar | Resultado |
|---|---|---|
| Escritura y revisión | Codespaces o equipo local | Cambios en LaTeX/datos/figuras |
| Control de versiones | Git/GitHub | Commit de fuentes |
| Compilación | Runner Ubuntu de GitHub Actions | Figuras PDF y dos manuscritos |
| Comprobaciones | scripts/check.py y compilador | Límites de resumen, referencias, errores de maquetación |
| Publicación en el repo | Job separado con token de escritura | Mismas rutas PDF, nuevo commit |
| Lectura | GitHub | PDF accesible sin descargar artifacts |

La compilación no valida la verdad científica. Una compilación correcta no cierra los pendientes editoriales ni convierte el borrador en publicación arbitrada.

## Ejercicio para estudiantes
1. Crear una rama y cambiar una frase de la introducción sin tocar los PDF.
2. Ejecutar `make all` y comparar el texto extraído o la vista PDF.
3. Abrir un PR; comprobar que CI valida sin escribir en la rama.
4. Integrar el PR; observar el commit posterior del bot y abrir el PDF actual.
5. Añadir una cita nueva y su entrada en el orden correcto; comprobar el verificador.
6. Introducir intencionadamente una llave LaTeX sin cerrar. La compilación debe fallar y no debe publicarse ningún PDF parcial. Reparar y volver a compilar.

El archivo build-manifest.json relaciona cada PDF con hashes de sus entradas. El historial Git relaciona esas entradas con autores y revisiones. Las ramas, el bot y los registros permiten estudiar tanto aciertos como errores.

Documentación técnica: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow
Entornos: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
