"""Build locally and in CI using the same command. Publish only after BOTH builds pass."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
PAPERS=['01-comunidades-abiertas','02-computacion-reproducible']
selected=sys.argv[1:] or PAPERS
if any(p not in PAPERS for p in selected): raise SystemExit('Unknown paper')
# Fixed epoch avoids wall-clock-only rebuild differences. Toolchain versions remain relevant.
env=dict(os.environ, SOURCE_DATE_EPOCH='1792540800', FORCE_SOURCE_DATE='1', TZ='UTC')
staged=[]
for name in selected:
    p=ROOT/'papers'/name
    build=p/'build';build.mkdir(exist_ok=True)
    for fig in sorted((p/'figures').glob('*.tex')):
        subprocess.run(['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error','-outdir=../build',fig.name],cwd=p/'figures',env=env,check=True)
        shutil.copy2(build/(fig.stem+'.pdf'),p/'figures'/(fig.stem+'.pdf'))
    subprocess.run(['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error','-outdir=build','main.tex'],cwd=p,env=env,check=True)
    log=(build/'main.log').read_text(errors='replace')
    if any(x in log for x in ['There were undefined references','Citation `','Overfull \\hbox']):
        raise SystemExit(f'Unresolved citations/references or horizontal overflow: {name}')
    staged.append((p,build/'main.pdf'))
for p,pdf in staged:
    out=p/'pdf'/'manuscript.pdf';shutil.copy2(pdf,out)
    inputs=sorted([ROOT/'shared'/'preamble.tex']+[f for f in p.rglob('*') if f.is_file() and f.suffix in ['.tex','.csv','.json'] and 'build' not in f.parts and 'pdf' not in f.parts])
    manifest={'paper':p.name,'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'inputs':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs},'engine':subprocess.check_output(['xelatex','--version'],text=True).splitlines()[0]}
    (p/'pdf'/'build-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print(f'Built {out.relative_to(ROOT)}')
