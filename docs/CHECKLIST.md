# Lista editorial

Destino previsto: Boletín de la Academia de Ciencias Físicas, Matemáticas y Naturales. [Guía para autores](https://acfiman.org/boletines/), consultada el 21 de octubre de 2026. Conservamos dos ensayos con objetivos distintos: organización comunitaria y arquitectura de formación computacional.

## Antes del envío

- [ ] Confirmar con la revista compatibilidad del preprint público y modalidad de ensayo; registrar la respuesta y actualizar `editorial_policy_confirmed` en `papers.json`.
- [x] Registrar Caracas, Venezuela, y Zúrich, Suiza, como ubicaciones de los capítulos distribuidos; correspondencia: me@arturos.ch. No disponemos de dirección postal física.
- [ ] Completar financiación y declaraciones de intereses de cada manuscrito; revisar el vínculo profesional con INAIT y los apoyos históricos descritos. Cambiar `declarations_reviewed` solo tras concluir la revisión.
- [ ] Completar los resultados finales de CoAfina 2025 si se dispone de registros; su convocatoria ya tiene fuente fechada. No sustituir ND por cifras de un resumen sin denominador.
- [x] Cronología del seguimiento de Salud para todos confirmada: V2 de Cornell, 13–16 de febrero de 2023.
- [ ] Enviar a ALAN la solicitud de erratum de fecha (`docs/ERRATUM-ALAN.md`).
- [ ] Revisar todos los textos, citas, cuadros, figuras y derechos de terceros. La revisión visual y científica sigue siendo responsabilidad de los autores.
- [ ] Completar contribuciones de autoría según la información del equipo; registrar la aprobación de la versión final y su commit en `manuscript_approval`. No inferir funciones a partir de afiliaciones.
- [ ] Cambiar `status` a `ready` por manuscrito y retirar las frases editoriales pendientes del texto.
- [ ] Ejecutar `make check STRICT=1` y `make export`; inspeccionar el paquete antes de enviarlo.

## Formato

Carta, una columna, títulos y resúmenes bilingües, resúmenes de hasta 150 palabras, citas numéricas por orden de aparición. Referencias con iniciales puntuadas, revistas en cursiva y volumen en negrita. Figuras a 160 mm y tablas sin líneas internas ni sombreado. El exportador integra las fuentes en un único `main.tex` y adjunta figuras y tablas independientes. El envío puede requerir ajustes adicionales del comité editorial.

## Equipo comunitario

Orden y afiliaciones mantenidos según la configuración del proyecto:

1. Arturo Sánchez Pineda — Creative Commons Venezuela y Creative Commons Switzerland.
2. Oscar Altuve Pabon — Creative Commons Venezuela.
3. [Iskya García](https://www.linkedin.com/in/iskya-garc%C3%ADa-09454711b/) — Creative Commons Venezuela.
4. [Estefanía Sánchez Pineda](https://www.linkedin.com/in/estefan%C3%ADa-s%C3%A1nchez-pineda/) — Creative Commons Venezuela.
5. [Ariana Moreno](https://www.linkedin.com/in/ariana-moreno-9b3017219/) — Creative Commons Venezuela.
6. [Diego Salcedo Flores](https://www.linkedin.com/in/diego-salcedo-flores/) — Creative Commons Venezuela.

El ensayo de computación mantiene a Arturo como autor. Los enlaces de perfil también están en los metadatos; no se usan como evidencia científica.
