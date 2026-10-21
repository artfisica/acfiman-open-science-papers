"""Checks that matter for editing: abstract length, numeric citation order, evidence ledger."""
from pathlib import Path
import csv, re, sys
R=Path(__file__).resolve().parents[1]
errors=[]
for p in sorted((R/'papers').iterdir()):
    for lang in ['es','en']:
        t=(p/'text'/f'abstract-{lang}.tex').read_text()
        words=re.findall(r"\b[\w]+(?:[-’'][\w]+)*\b",t)
        print(p.name,lang,len(words),'words')
        if len(words)>150: errors.append(f'{p.name}: {lang} abstract exceeds 150 words')
    main=(p/'main.tex').read_text()
    body='\n'.join((p/f'{f}.tex').read_text() for f in re.findall(r'\\input\{(text/[^}]+)\}',main))
    cited=list(dict.fromkeys(k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',body) for k in group.split(',')))
    bib=(p/'references.tex').read_text()
    keys=re.findall(r'\\bibitem\{([^}]+)\}',bib)
    if cited != keys: errors.append(f'{p.name}: bibliography must follow first citation order: {cited} != {keys}')
    with (p/'data'/'evidence.csv').open() as f: rows=list(csv.DictReader(f))
    if not rows or any(not r['source'] or not r['status'] for r in rows):errors.append(f'{p.name}: incomplete evidence ledger')
    pending=sum(r['status']!='verified' for r in rows)
    print(f'  {pending} claims need author/source follow-up (allowed for a first draft).')
if errors: raise SystemExit('\n'.join(errors))
