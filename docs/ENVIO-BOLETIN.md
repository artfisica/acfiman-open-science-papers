# Envío al Boletín de la ACFIMAN

Guía consultada el 15 de noviembre de 2026 en https://acfiman.org/boletines/ y en el número LXXXVI n.º 1 (2026). La Comisión Editorial está integrada por Deanna Marcano (editora jefe), Ismardo Bonalde y Gioconda Cunto de San Blas. Los envíos se dirigen a editora@acfiman.org.

## Lo que pide la guía

Para la evaluación basta un archivo: el manuscrito en PDF con las figuras, los cuadros y las tablas incluidos. La guía pide además que figuras y cuadros se envíen identificados por separado, de modo que adjuntamos también el paquete que genera `make export`. Si el trabajo se acepta, la revista solicita el archivo .tex con las referencias incluidas y las figuras en PDF; ese material ya está en el mismo paquete.

El manuscrito cumple los requisitos de presentación de la guía: tamaño carta a una columna, clase `article`, título, resumen de hasta 150 palabras y palabras clave en español e inglés, ubicación de los autores y autor de correspondencia, secciones numeradas hasta tres niveles, cuadros sin líneas internas ni sombreado, figuras a 160 mm en PDF, citas numéricas en orden de aparición y referencias con el formato de los ejemplos de la revista. Los ensayos del Boletín admiten opinión sustentada e información original del autor, que es el caso de ambos textos.

La guía indica que el material enviado es inédito y que se remite solo al Boletín. Los borradores están en un repositorio público porque el flujo de escritura forma parte del ejemplo que describen; la carta de presentación lo comunica a la Comisión y ofrece ajustar esa disponibilidad. El campo `preprint_disclosure` de `papers.json` registra esa decisión.

## Pasos para los dos ensayos

Los siguientes comandos dejan los dos paquetes listos a partir de la rama principal, una vez integrados estos cambios y publicado el PDF por la integración continua:

    git pull --ff-only
    python3 scripts/approve.py 02-computacion-reproducible "Arturo Sánchez Pineda"
    python3 scripts/approve.py 01-comunidades-abiertas "Arturo Sánchez Pineda" "Oscar Altuve Pabon" "Iskya García" "Estefanía Sánchez Pineda" "Ariana Moreno" "Diego Salcedo Flores"
    git commit -am "Registrar aprobaciones de los dos ensayos"
    git push
    make check STRICT=1
    make export

El resultado queda en `dist/`: una carpeta y un archivo .zip por ensayo, cada uno con `manuscript.pdf`, `main.tex` autocontenido, `figures/`, `tables/` y el manifiesto de compilación. Conviene enviar el PDF generado por la integración continua, que usa la imagen fijada, y renombrarlo para la revista, por ejemplo `SanchezPineda-entornos-reproducibles.pdf` y `SanchezPineda-et-al-hackatones-practicas-abiertas.pdf`. Cada ensayo se envía en un correo propio, con su carta.

La aprobación queda asociada al commit leído; cualquier cambio posterior en el texto o en los datos de un ensayo pide registrarla de nuevo. Con `PAPER=<directorio>` la comprobación y la exportación se limitan a un ensayo.

## Carta para el ensayo de computación

Para: editora@acfiman.org
Asunto: Envío de ensayo para el Boletín: «Entornos reproducibles para la formación en física»

Estimada Dra. Marcano y estimados miembros de la Comisión Editorial:

Reciban un cordial saludo. Les escribo para someter a la consideración del Boletín, en la categoría de ensayo, el trabajo «Entornos reproducibles para la formación en física: arquitectura, opciones de despliegue y protocolo de evaluación», del que soy autor. Adjunto el manuscrito en PDF con las figuras y los cuadros incluidos, como indica la guía para los autores, y un archivo comprimido con las figuras y los cuadros por separado y la fuente LaTeX. El texto está en tamaño carta y a una columna, con título, resumen y palabras clave en español e inglés.

El ensayo propone una arquitectura para sesiones prácticas de física basada en Git, contenedores de desarrollo, cuadernos y automatización. Compara cuatro opciones de despliegue y documenta dos experiencias docentes, el SILAFAE XV de 2024 y la CERN School of Computing celebrada en Santiago en enero de 2026, a partir de revisiones fechadas de los materiales y de los programas públicos. Creo que puede ser útil para quienes organizan formación en computación científica en las universidades venezolanas.

Quisiera comentarles con transparencia que el borrador y sus fuentes están disponibles en un repositorio público, con un portal de lectura, porque el propio flujo de escritura y compilación forma parte del ejemplo que el ensayo describe: https://github.com/artfisica/acfiman-open-science-papers. El texto es inédito y se envía únicamente al Boletín. Si la Comisión prefiere que el borrador deje de estar visible durante la evaluación, o que se presente de otra manera, lo ajustaré con mucho gusto.

En la preparación del manuscrito utilicé herramientas de asistencia (ChatGPT y Codex) como apoyo en la búsqueda documental, la organización de borradores, la revisión lingüística y el flujo de compilación. La verificación de las fuentes, los datos y las interpretaciones es mi responsabilidad.

Mi afiliación en este trabajo es Creative Commons Venezuela y Creative Commons Switzerland, capítulos que funcionan como grupos distribuidos; por eso indico Caracas y Zúrich como ubicaciones y este correo para la correspondencia. Mantengo además una relación profesional con INAIT SA, que declaro en el manuscrito.

Quedo atento a cualquier indicación de la Comisión y les agradezco de antemano su tiempo y su lectura.

Con mis mejores saludos,

Arturo Sánchez Pineda
Creative Commons Venezuela y Creative Commons Switzerland
me@arturos.ch

## Carta para el ensayo de comunidades

Para: editora@acfiman.org
Asunto: Envío de ensayo para el Boletín: «Hackatones y prácticas abiertas para construir comunidades científicas en América Latina»

Estimada Dra. Marcano y estimados miembros de la Comisión Editorial:

Reciban un cordial saludo. En nombre de mis coautores, Oscar Altuve Pabon, Iskya García, Estefanía Sánchez Pineda, Ariana Moreno y Diego Salcedo Flores, les escribo para someter a la consideración del Boletín, en la categoría de ensayo, el trabajo «Hackatones y prácticas abiertas para construir comunidades científicas en América Latina». Adjunto el manuscrito en PDF con las figuras y los cuadros incluidos, como indica la guía para los autores, y un archivo comprimido con las figuras y los cuadros por separado y la fuente LaTeX. Los seis autores hemos leído y aprobado la versión que enviamos.

El ensayo compara tres formatos de trabajo abierto en los que hemos participado: los hackatones CoAfina, el editatón Salud para todos con la OMS y la Universidad de Cornell, y la formación con datos abiertos de física en universidades venezolanas. A partir de fuentes públicas fechadas distingue inscripción, actividad, productos y continuidad, y propone decisiones de organización que pueden adaptarse a instituciones venezolanas. Uno de los antecedentes citados es un reporte publicado en Archivos Latinoamericanos de Nutrición del que soy coautor; este ensayo tiene un objetivo y un análisis propios.

Quisiera comentarles con transparencia que el borrador, sus datos y sus fuentes están disponibles en un repositorio público, con un portal de lectura, porque la conservación abierta del procedimiento forma parte de lo que el ensayo propone: https://github.com/artfisica/acfiman-open-science-papers. El texto es inédito y se envía únicamente al Boletín. Si la Comisión prefiere que el borrador deje de estar visible durante la evaluación, o que se presente de otra manera, lo ajustaremos con mucho gusto.

En la preparación del manuscrito utilizamos herramientas de asistencia (ChatGPT y Codex) como apoyo en la búsqueda documental, la organización de borradores, la revisión lingüística y el flujo de compilación. La verificación de las fuentes, los datos y las interpretaciones es responsabilidad de los autores.

Nuestras afiliaciones son los capítulos de Creative Commons en Venezuela y en Suiza, que funcionan como grupos distribuidos; por eso indicamos Caracas y Zúrich como ubicaciones y este correo para la correspondencia. El manuscrito declara los apoyos que recibieron las experiencias analizadas y mi relación profesional con INAIT SA.

Quedamos atentos a cualquier indicación de la Comisión y les agradecemos de antemano su tiempo y su lectura.

Con nuestros mejores saludos,

Arturo Sánchez Pineda, autor de correspondencia
Creative Commons Venezuela y Creative Commons Switzerland
me@arturos.ch
