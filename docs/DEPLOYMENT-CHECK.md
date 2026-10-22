# Comprobación del portal — 22 de octubre de 2026

La ejecución 39781925926, correspondiente a 67a051c00130b920ce52e9abbaafc309c51ddc5f, terminó correctamente en los tres trabajos: build, publish y deploy-pages.

https://github.com/artfisica/acfiman-open-science-papers/actions/runs/39781925926

La consulta HTTP directa del portal con parámetro único y Cache-Control: no-cache devolvió 200, el identificador 67a051c, el enlace Manifiesto y la directiva noindex. El manifiesto comunidades.json devolvió 200 y la misma revisión. El SHA-256 del PDF público descargado coincide con el manifiesto: 9ec5617480982dbaf268a0b014b969fef0c0d280c07c66399136155154e017ba.

No se reprodujo el contenido antiguo descrito en la revisión. No hay evidencia de un fallo de deploy-pages ni motivo para cambiar la estructura del workflow. No se utilizó una ventana privada: la verificación fue mediante solicitudes HTTP nuevas y consulta de los trabajos de GitHub Actions.

Los commits humanos dd33c92 y 67a051c tienen como autor Arturo Sánchez Pineda, me@arturos.ch. Los siguientes commits de PDF pertenecen a github-actions[bot]. No se detectaron nombres vacíos en esos commits. Para próximos commits se configura localmente Arturo Sánchez Pineda y 8846121+artfisica@users.noreply.github.com; no se reescribe la historia.
