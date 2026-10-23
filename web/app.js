'use strict';
let papers;
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
  const manifest = paper.manifest;
  document.getElementById('reader-version').textContent = `Fuentes: ${manifest.source_date} · ${manifest.source_commit.slice(0, 10)}${manifest.source_dirty ? ' · cambios locales' : ''}`;
  document.getElementById('reader-hash').textContent = `PDF SHA-256: ${manifest.pdf_sha256}`;
  document.getElementById('manifest').href = `manifests/${id}.json`;
  const viewer = document.getElementById('pdf-viewer');
  if (window.matchMedia('(min-width: 801px)').matches) {
    const source = `${pdf}#view=FitH`;
    if (viewer.getAttribute('src') !== source) viewer.setAttribute('src', source);
  } else if (viewer.hasAttribute('src')) viewer.removeAttribute('src');
  viewer.title = `PDF: ${paper.title}`;
  document.title = `${paper.title} · Ciencia abierta`;
}
fetch('papers.json').then(response => { if (!response.ok) throw new Error('Metadata unavailable'); return response.json(); }).then(data => { papers = data; window.addEventListener('hashchange', selectPaper); window.addEventListener('resize', selectPaper); selectPaper(); }).catch(() => { document.getElementById('reader-version').textContent += ' · Use los enlaces directos a los PDF.'; });
