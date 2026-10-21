# Validación de entrega — 21 de octubre de 2026

## Comprobado localmente
- Ambos manuscritos compilados con XeLaTeX/latexmk: comunidades 7 páginas; computación 8 páginas; formato carta.
- Resúmenes: comunidades 133 palabras ES / 115 EN; computación 138 ES / 125 EN. Todos dentro de 150.
- Referencias numéricas presentes y ordenadas por primera aparición; no referencias indefinidas ni desbordamientos horizontales en los logs finales.
- Páginas renderizadas y revisadas visualmente; figuras PDF separadas generadas desde TikZ, sin fotografías de terceros.
- Paquetes editoriales de `make export` compilados de forma independiente: un main.tex con secciones y bibliografía integradas, más figuras PDF.
- Configuración JSON de Codespaces/VS Code y estructura YAML del workflow analizadas.
- Lógica de publicación probada con un repositorio bare temporal: commit/push de salidas, ausencia de commit cuando no cambian, rechazo de compilación desactualizada. No se usaron credenciales ni se escribió en GitHub.

## Límites de estas comprobaciones
No se ejecutó un Codespace, no se construyó el contenedor desde cero y no se lanzó GitHub Actions remoto. La instalación apt, disponibilidad de imágenes/acciones, permisos del token y reglas de rama deben verificarse en la primera ejecución del repositorio importado. La revisión local no afirma que estas etapas remotas ya funcionaron.

La compilación no valida los hechos históricos ni cierra los pendientes de `data/evidence.csv`. El estado de borrador y las direcciones pendientes están visibles en los PDF. No se ha confirmado la política editorial de preprints. No se ha concedido una licencia global en nombre de los autores.
