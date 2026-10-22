# Integración de la actualización del 22 de octubre de 2026

Base comprobada: 609e8a5, commit de PDF posterior a 430c6f5. El parche recibido aplica sin conflictos.

Se conservan los cuatro bloques propuestos: cronología de V2 como informe de los autores, revisión de ambos ensayos, distinción entre recuentos de participación y documentación de las tres tesis. Las fechas de defensa y tutorías de García y Di Domenico se contrastaron con los campos thesis:thesis y contributors de la API de CERN; el depósito de Altuve, con la API de Zenodo. También se contrastaron las actas EPS-HEP 2017, los 36 participantes y ocho organizadores del boletín Cornell de diciembre de 2021 y las seis firmas de la página de coordinación de Wikipedia.

La correspondencia de las cifras 49/13/22/43 con V2 se conserva como author_report, según la confirmación indicada en el paquete recibido. Los anuncios de Cornell corroboran las fechas del evento, pero no verifican por sí solos esa correspondencia. No se ha enviado una solicitud de erratum ni se ha comprobado una corrección publicada por ALAN.

Correcciones realizadas durante la integración:

- Los resúmenes presentan 42,2 % y 26,5 % como cocientes de los editatones. Se elimina el intervalo «un cuarto a tres cuartos»: una cota condicional <78 % no es un extremo observado.
- La nota del cuadro dice que se prevé solicitar la corrección, coherente con la carta todavía no enviada.
- La carta y las notas internas no afirman que los coautores ya fueron informados o aprobaron el texto.
- La tabla vacía de asignación en Wikipedia no demuestra por sí sola cómo se distribuyeron las tareas; se elimina esa inferencia.
- La comparación de ediciones se expresa como más inscripciones y menos editores activos, sin interpretación causal.

hallazgos.tex ya está eliminado en main. Se conservan las ubicaciones Caracas y Zúrich, el correo me@arturos.ch y los autores existentes. No se modifica Wikipedia, CERN ni el repositorio remoto. No se envían correos.

Pendientes: C09 sigue como author_report y C22 como pending; continúan la política editorial y las declaraciones. Completar solo las declaraciones no elimina los demás bloqueos de STRICT=1.
