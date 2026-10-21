"""Draft checks always run; STRICT=1 additionally enforces submission readiness."""
import csv, json, os, re, sys
from common import ROOT, metadata, generate, expand, runtime_image
strict='--strict' in sys.argv or os.environ.get('STRICT')=='1'
errors=[]
meta=metadata()
for item in meta['papers']:
    p=ROOT/'papers'/item['directory']; generate(item)
    for lang in ['es','en']:
        words=re.findall(r"\b[\w]+(?:[-’'][\w]+)*\b",(p/'text'/f'abstract-{lang}.tex').read_text())
        print(p.name,lang,len(words),'words')
        if len(words)>150: errors.append(f'{p.name}: {lang} abstract exceeds 150 words')
    full=expand(p/'main.tex'); body=full.split(r'\begin{thebibliography}')[0]
    cited=list(dict.fromkeys(k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',body) for k in group.split(',')))
    keys=re.findall(r'\\bibitem\{([^}]+)\}',full)
    if cited!=keys: errors.append(f'{p.name}: references must follow citation order: {cited} != {keys}')
    labels=re.findall(r'\\label\{([^}]+)\}',body)
    refs=re.findall(r'\\(?:ref|pageref|autoref)\{([^}]+)\}',body)
    for label in set(labels)-set(refs): errors.append(f'{p.name}: unreferenced label {label}')
    for ref in set(refs)-set(labels): errors.append(f'{p.name}: undefined label {ref}')
    if len(labels)!=len(set(labels)): errors.append(f'{p.name}: duplicate labels')
    rows=list(csv.DictReader((p/'data/evidence.csv').open()))
    prefix='C' if p.name.startswith('01') else 'T'
    if [r['id'] for r in rows]!=[prefix+f'{i:02}' for i in range(1,len(rows)+1)]:errors.append(f'{p.name}: nonsequential evidence IDs')
    if not rows or any(not r['source'] or r['status'] not in ['verified','pending','author_report'] for r in rows):errors.append(f'{p.name}: incomplete evidence ledger')
    for entry in re.split(r'\\bibitem', (p/'references.tex').read_text())[1:]:
        urls=re.findall(r'\\url\{([^}]+)\}',entry)
        for url in urls:
            if url.startswith(('https://laconga.redclara.net/','http://laconga.redclara.net/')):
                archive=any(re.fullmatch(r'https://web\.archive\.org/web/\d{14}/'+re.escape(url), twin) for twin in urls)
                preservation=p/'data/source-preservation.json'
                reports=json.loads(preservation.read_text()).get('reports',{}) if preservation.exists() else {}
                record=reports.get(url,{})
                dated=(record.get('kind')=='dated_event_report' and re.fullmatch(r'\d{4}-\d{2}-\d{2}',record.get('publication_date',''))
                       and record.get('coverage') and record.get('corroborating_url') in full
                       and url.rstrip('/')!='https://laconga.redclara.net/hackathon')
                if not archive and not dated:
                    message=f'{p.name}: mutable or unreviewed source needs dated archive: {url}'
                    if strict: errors.append(message)
                    else: print('  Archive warning:',message)
    pending=[r['id'] for r in rows if r['status']!='verified']
    print('  Unresolved evidence:',', '.join(pending) or 'none')
    if item['status'] not in ['draft','ready']: errors.append(f'{p.name}: invalid status')
    if strict:
        if item['status']!='ready':errors.append(f'{p.name}: status is draft')
        # Remove command definition before checking whether the banner is invoked.
        without_definition=re.sub(r'\\newcommand\{\\draftnotice\}.*?\n','',body)
        if r'\draftnotice' in without_definition: errors.append(f'{p.name}: active draft banner')
        if pending:errors.append(f'{p.name}: unresolved evidence {pending}')
        if not item.get('corresponding_email') or '@' not in item['corresponding_email']:errors.append(f'{p.name}: missing correspondence email')
        for key in {a for person in item['authors'] for a in person['affiliations']}:
            if not meta['affiliations'][key].get('postal_address'):errors.append(f'{p.name}: missing postal address for {key}')
        for field in ['editorial_policy_confirmed','declarations_reviewed']:
            if item.get(field) is not True:errors.append(f'{p.name}: {field} not completed')
        if r'\editorialtodo{' in body:errors.append(f'{p.name}: explicit editorial TODO in manuscript')
# One immutable environment for CI and Codespaces.
image=runtime_image()
if '@sha256:' not in image or image not in (ROOT/'.github/workflows/papers.yml').read_text():errors.append('CI and Codespaces images must match by digest')
if errors:raise SystemExit('\n'.join(errors))
print('Submission checks passed.' if strict else 'Draft checks passed.')
