"""Export submission-ready, self-contained TeX, PDF, figures and separate tables."""
import os, re, shutil, subprocess, sys, zipfile
from common import ROOT, metadata, expand, provenance
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
        table=expand(f,p); table=re.sub(r'\\(?:begin|end)\{table\}(?:\[[^]]*\])?','',table)
        label=re.search(r'\\label\{([^}]+)\}',table)[1]
        number=table_labels.index(label)+1
        table=r'\setcounter{table}{'+str(number-1)+'}'+table
        standalone=r'\documentclass[11pt,letterpaper]{article}'+'\n'+(ROOT/'shared/preamble.tex').read_text()+r'\begin{document}\begin{minipage}{160mm}\makeatletter\def\@captype{table}\makeatother'+'\n'+table+r'\end{minipage}\end{document}'
        target=d/'tables'/f.name;target.write_text(standalone)
        env=dict(os.environ,SOURCE_DATE_EPOCH=str(provenance(p)['source_epoch']),FORCE_SOURCE_DATE='1',TZ='UTC')
        subprocess.run(['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error',target.name],cwd=target.parent,env=env,check=True,stdout=subprocess.DEVNULL)
        for aux in target.parent.glob(f.stem+'.*'):
            if aux.suffix not in ['.tex','.pdf']:aux.unlink()
    (d/'README.txt').write_text('Submission package: compile main.tex with XeLaTeX twice. Figures and tables are supplied separately. See build-manifest.json for source provenance.\n')
    with zipfile.ZipFile(ROOT/'dist'/(p.name+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(d.rglob('*')):
            if f.is_file():z.write(f,f.relative_to(d))
    print(d)
