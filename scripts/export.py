"""Create self-contained editorial packages; these remain DRAFT until author review."""
from pathlib import Path
import re, shutil, zipfile
R=Path(__file__).resolve().parents[1]
def expand(path):
    text=path.read_text()
    return re.sub(r'\\input\{([^}]+)\}',lambda m: expand((path.parent/(m.group(1)+'.tex')).resolve()),text)
for p in sorted((R/'papers').iterdir()):
    d=R/'dist'/p.name
    if d.exists():shutil.rmtree(d)
    (d/'figures').mkdir(parents=True)
    (d/'main.tex').write_text(expand(p/'main.tex'))
    shutil.copy2(p/'pdf'/'manuscript.pdf',d/'manuscript.pdf')
    for f in (p/'figures').glob('*.pdf'):shutil.copy2(f,d/'figures'/f.name)
    (d/'README.txt').write_text('DRAFT for author review. XeLaTeX main.tex twice. References are embedded. Resolve the editorial checklist before submission.\n')
    with zipfile.ZipFile(R/'dist'/(p.name+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(d.rglob('*')):
            if f.is_file():z.write(f,f.relative_to(d))
    print(d)
