'use strict';
const papers = {
  comunidades: {label: '01', title: 'Hackatones y prácticas abiertas para construir comunidades científicas en América Latina', authors: 'Oscar Altuve Pabon y Arturo Sánchez Pineda', directory: '01-comunidades-abiertas'},
  computacion: {label: '02', title: 'Entornos reproducibles y automatización para la formación en física: una experiencia de computación transversal en América Latina', authors: 'Arturo Sánchez Pineda', directory: '02-computacion-reproducible'}
};
function selectPaper() {
  const id = Object.hasOwn(papers, location.hash.slice(1)) ? location.hash.slice(1) : 'comunidades';
  const paper = papers[id];
  document.querySelectorAll('[data-paper]').forEach(link => {
    const active = link.dataset.paper === id;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'true');
    else link.removeAttribute('aria-current');
  });
  document.getElementById('reader-label').textContent = `MANUSCRITO ${paper.label}`;
  document.getElementById('reader-title').textContent = paper.title;
  document.getElementById('reader-authors').textContent = paper.authors;
  const pdf = `pdf/${id}.pdf`;
  for (const link of ['open-pdf', 'download-pdf']) document.getElementById(link).href = pdf;
  document.getElementById('source').href = `https://github.com/artfisica/acfiman-open-science-papers/tree/main/papers/${paper.directory}`;
  const viewer = document.getElementById('pdf-viewer');
  viewer.src = `${pdf}#view=FitH`;
  viewer.title = `PDF: ${paper.title}`;
  document.title = `${paper.title} · Ciencia abierta`;
}
window.addEventListener('hashchange', selectPaper);
selectPaper();
