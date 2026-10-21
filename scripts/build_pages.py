#!/usr/bin/env python3
"""Assemble the static reading portal from the current, verified PDF outputs."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '_site'
PAPERS = {'comunidades': '01-comunidades-abiertas', 'computacion': '02-computacion-reproducible'}

def main():
    # Verify all inputs before replacing the previous site.
    for directory in PAPERS.values():
        folder = ROOT / 'papers' / directory / 'pdf'
        pdf = (folder / 'manuscript.pdf').read_bytes()
        manifest = json.loads((folder / 'build-manifest.json').read_text())
        if not pdf.startswith(b'%PDF-') or hashlib.sha256(pdf).hexdigest() != manifest['pdf_sha256']:
            raise SystemExit(f'Invalid PDF or stale manifest: {directory}; run make all first.')
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(ROOT / 'web', OUTPUT)
    (OUTPUT / 'pdf').mkdir()
    (OUTPUT / '.nojekyll').touch()
    for slug, directory in PAPERS.items():
        shutil.copy2(ROOT / 'papers' / directory / 'pdf' / 'manuscript.pdf', OUTPUT / 'pdf' / f'{slug}.pdf')
    print(f'Pages ready: {OUTPUT}')

if __name__ == '__main__':
    main()
