"""Validate, compile, then publish outputs only after all selected builds pass."""
import json, os, re, shutil, subprocess, sys
from common import ROOT, metadata, generate, inputs, sha, runtime_image
items=metadata()['papers']; names=sys.argv[1:] or [x['directory'] for x in items]
if set(names)-{x['directory'] for x in items}:raise SystemExit('Unknown paper')
subprocess.run([sys.executable,str(ROOT/'scripts/check.py')],check=True)
staged=[]
for item in items:
    if item['directory'] not in names:continue
    p=ROOT/'papers'/item['directory']; info=generate(item); b=p/'build'
    env=dict(os.environ,SOURCE_DATE_EPOCH=str(max(info['source_epoch'],info['build_epoch'])),FORCE_SOURCE_DATE='1',TZ='UTC')
    def compile_tex(file,out):
        result=subprocess.run(['latexmk','-gg','-xelatex','-interaction=nonstopmode','-halt-on-error','-outdir='+out,file.name],cwd=file.parent,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if result.returncode:
            print(result.stdout[-12000:]);raise SystemExit(f'TeX compilation failed: {file}')
    for fig in sorted((p/'figures').glob('*.tex')):
        compile_tex(fig,'../build');shutil.copy2(b/(fig.stem+'.pdf'),fig.with_suffix('.pdf'))
    compile_tex(p/'main.tex','build')
    log=(b/'main.log').read_text(errors='replace')
    if 'Output written on' not in log:raise SystemExit(f'Incomplete TeX log: {p.name}')
    if any(x in log for x in ['There were undefined references','Citation `']):raise SystemExit(f'Unresolved references: {p.name}')
    overflow=[float(x) for x in re.findall(r'Overfull \\[hv]box \((\d+(?:\.\d+)?)pt too',log)]
    if overflow:print(f'{p.name}: overflow up to {max(overflow):.2f}pt')
    if any(v>5 for v in overflow):raise SystemExit(f'Overflow exceeds 5pt: {p.name}')
    staged.append((p,info))
for p,info in staged:
    out=p/'pdf/manuscript.pdf';shutil.copy2(p/'build/main.pdf',out)
    manifest={'paper':p.name,**info,'pdf_sha256':sha(out),'inputs':{str(f.relative_to(ROOT)):sha(f) for f in inputs(p)},'engine':subprocess.check_output(['xelatex','--version'],text=True).splitlines()[0], 'configured_image':runtime_image(),'runtime':os.environ.get('PAPERS_RUNTIME','local-unpinned')}
    (p/'pdf/build-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print(f'Built {out.relative_to(ROOT)}')
