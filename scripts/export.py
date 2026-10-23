"""Export submission-ready, self-contained TeX, PDF, figures and separate tables."""
import os, re, shutil, subprocess, sys, zipfile
from common import ROOT, metadata, expand, provenance
from table_export import table_document
subprocess.run([sys.executable,str(ROOT/'scripts/check.py'),'--strict'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],check=True,env=dict(os.environ,STRICT='1'))
for item in metadata()['papers']:
    p=ROOT/'papers'/item['directory'];d=ROOT/'dist'/p.name
    if d.exists():shutil.rmtree(d)
    (d/'figures').mkdir(parents=True);(d/'tables').mkdir()
    full=expand(p/'main.tex');full=re.sub(r'\\newcommand\{\\draftnotice\}.*?\n','',full)
    (d/'main.tex').write_text(full)
    shutil.copy2(p/'pdf/manuscript.pdf',d/'manuscript.pdf')
    shutil.copy2(p/'pdf/build-manifest.json',d/'build-manifest.json')
    for f in (p/'figures').glob('*.pdf'):shutil.copy2(f,d/'figures'/f.name)
    table_labels=re.findall(r'\\label\{(tab:[^}]+)\}',full)
    for f in (p/'tables').glob('*.tex'):
        table=expand(f,p)
        label=re.search(r'\\label\{([^}]+)\}',table)[1]
        if label not in table_labels:continue
        number=table_labels.index(label)+1
        standalone=table_document(table,number,(ROOT/'shared/preamble.tex').read_text(),(p/'build/metadata.tex').read_text(),full)
        target=d/'tables'/f.name;target.write_text(standalone)
        env=dict(os.environ,SOURCE_DATE_EPOCH=str(provenance(p)['source_epoch']),FORCE_SOURCE_DATE='1',TZ='UTC')
        subprocess.run(['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error',target.name],cwd=target.parent,env=env,check=True,stdout=subprocess.DEVNULL)
        log=target.with_suffix('.log').read_text(errors='replace')
        if any(message in log for message in ['There were undefined references','Citation `']):
            raise SystemExit(f'Unresolved references in exported table: {target}')
        for aux in target.parent.glob(f.stem+'.*'):
            if aux.suffix not in ['.tex','.pdf']:aux.unlink()
    (d/'README.txt').write_text('Submission package: compile main.tex with XeLaTeX twice. Figures and tables are supplied separately. See build-manifest.json for source provenance.\n')
    with zipfile.ZipFile(ROOT/'dist'/(p.name+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(d.rglob('*')):
            if f.is_file():z.write(f,f.relative_to(d))
    print(d)
