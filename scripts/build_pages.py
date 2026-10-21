"""Render the reading portal from shared metadata and current source-verified PDFs."""
import html, json, shutil
from common import ROOT, metadata, inputs, sha
OUTPUT=ROOT/'_site'
def main():
    meta=metadata(); papers={}
    for index,item in enumerate(meta['papers'],1):
        p=ROOT/'papers'/item['directory'];manifest=json.loads((p/'pdf/build-manifest.json').read_text())
        pdf=p/'pdf/manuscript.pdf'
        if not pdf.read_bytes().startswith(b'%PDF-') or sha(pdf)!=manifest['pdf_sha256']:raise SystemExit('Invalid PDF: '+p.name)
        current={str(f.relative_to(ROOT)):sha(f) for f in inputs(p)}
        if current!=manifest['inputs']:raise SystemExit('Sources changed; run make all: '+p.name)
        papers[item['slug']]={**item,'label':f'{index:02}','authors':', '.join(a['name'] for a in item['authors']),'manifest':manifest}
    if OUTPUT.exists():shutil.rmtree(OUTPUT)
    shutil.copytree(ROOT/'web',OUTPUT);(OUTPUT/'pdf').mkdir();(OUTPUT/'manifests').mkdir();(OUTPUT/'.nojekyll').touch()
    for slug,item in papers.items():
        p=ROOT/'papers'/item['directory']/'pdf'
        shutil.copy2(p/'manuscript.pdf',OUTPUT/'pdf'/f'{slug}.pdf')
        shutil.copy2(p/'build-manifest.json',OUTPUT/'manifests'/f'{slug}.json')
    (OUTPUT/'papers.json').write_text(json.dumps(papers,ensure_ascii=False,indent=2)+'\n')
    # JSON text is external, and all HTML substitutions are escaped.
    first=next(iter(papers.values()));template=(ROOT/'web/index.html').read_text()
    replacements={'TITLE':first['title'],'AUTHORS':first['authors'],'VERSION':f"Fuentes: {first['manifest']['source_date']} · {first['manifest']['source_commit'][:10]}"}
    for k,v in replacements.items():template=template.replace('{{'+k+'}}',html.escape(v))
    template=template.replace('{{ROBOTS}}','noindex, nofollow' if any(x['status']=='draft' for x in papers.values()) else 'index, follow')
    template=template.replace('{{STATUS}}','Borradores de trabajo' if any(x['status']=='draft' for x in papers.values()) else 'Manuscritos preparados para envío')
    (OUTPUT/'index.html').write_text(template)
    print('Pages ready:',OUTPUT)
if __name__=='__main__':main()
