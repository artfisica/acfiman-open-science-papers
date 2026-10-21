# Crear el repositorio en tu cuenta

Este paquete no escribe en GitHub. Nombre sugerido: `acfiman-open-science-papers`.

Desde la carpeta descomprimida (la que contiene README.md, Makefile y .github):

```bash
git init -b main
git add .
git commit -m "Initial manuscripts and reproducible LaTeX workflow"
gh repo create artfisica/acfiman-open-science-papers --private --source=. --remote=origin --push
```

Requiere GitHub CLI instalado y autenticado en tu cuenta. Si el repositorio ya existe, no repetir la creación; conectar su remoto y revisar su contenido antes de subir. El nombre sugerido no fue comprobado como disponible.

Alternativa: crear el repositorio vacío desde github.com, sin README ni licencia inicial, y usar el URL que GitHub muestre:

```bash
git remote add origin https://github.com/artfisica/acfiman-open-science-papers.git
git push -u origin main
```

Después abrir Actions y comprobar la primera ejecución. Los PDF ya están incluidos; el bot los actualizará cuando cambien las fuentes. Abrir Code → Codespaces para editar. Si deseas publicar el preprint, aclarar primero la política de ACFIMAN y las licencias con los coautores; cambiar la visibilidad no requiere modificar el flujo.
