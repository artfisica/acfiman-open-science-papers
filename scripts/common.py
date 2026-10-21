"""Metadata, source provenance and TeX expansion shared by build/check/export."""
from pathlib import Path
import csv, datetime, hashlib, json, re, subprocess
ROOT = Path(__file__).resolve().parents[1]
def metadata():
    return json.loads((ROOT/'papers.json').read_text())
def tex(value):
    return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in str(value))
def inputs(p):
    files = [ROOT/'papers.json', ROOT/'shared/preamble.tex', ROOT/'Makefile']
    files += list((ROOT/'scripts').glob('*.py'))
    files += list((ROOT/'.devcontainer').glob('*'))
    files += list((ROOT/'.github/workflows').glob('*.yml'))
    files += [f for f in p.rglob('*.tex') if 'build' not in f.relative_to(p).parts]
    if (p/'data/coafina-editions.csv').exists(): files.append(p/'data/coafina-editions.csv')
    # evidence.csv is editorial bookkeeping, not a typeset input.
    return sorted(set(files))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def provenance(p):
    if subprocess.check_output(['git','rev-parse','--is-shallow-repository'],cwd=ROOT,text=True).strip()=='true':
        raise SystemExit('Full source history required: run git fetch --unshallow origin.')
    paths = [str(f.relative_to(ROOT)) for f in inputs(p)]
    result = subprocess.check_output(['git','log','-1','--format=%H %ct','--',*paths],cwd=ROOT,text=True).strip()
    if not result: raise SystemExit('A source commit is required to build.')
    commit, epoch = result.split()
    dirty = bool(subprocess.check_output(['git','status','--porcelain','--',*paths],cwd=ROOT,text=True).strip())
    return {'source_commit':commit,'source_date':datetime.datetime.fromtimestamp(int(epoch),datetime.timezone.utc).date().isoformat(),'source_epoch':int(epoch),'source_dirty':dirty}
def generate(item):
    p=ROOT/'papers'/item['directory']; b=p/'build'; b.mkdir(exist_ok=True)
    info=provenance(p); m=metadata(); used=list(dict.fromkeys(a for x in item['authors'] for a in x['affiliations']))
    names=[]
    for author in item['authors']:
        markers=','.join(str(used.index(a)+1) for a in author['affiliations'])
        names.append(tex(author['name'])+r'\textsuperscript{'+markers+'}')
    lines=[', '.join(names[i:i+2]) for i in range(0,len(names),2)]
    affiliations=[]
    for i,key in enumerate(used,1):
        a=m['affiliations'][key]
        affiliations.append(r'\textsuperscript{'+str(i)+'}'+tex(a['name'])+(r' --- '+tex(a['postal_address']) if a['postal_address'] else ''))
    draft = r'\draftnotice' if item['status']=='draft' else ''
    revision=info['source_date']+' · '+info['source_commit'][:10]+(' · cambios locales' if info['source_dirty'] else '')
    contact=tex(item['corresponding_author'])
    if item['corresponding_email']: contact+='; '+tex(item['corresponding_email'])
    s=(r'\hypersetup{pdftitle={'+tex(item['title'])+r'},pdfauthor={'+tex(', '.join(a['name'] for a in item['authors']))+'}}\n'+
       r'\newcommand{\sourcerevision}{'+tex(revision)+'}\n'+r'\newcommand{\paperheading}{'+draft+r'\begin{center}'+
       r'{\LARGE\bfseries '+tex(item['title'])+r'}\par\vspace{0.6em}'+
       r'{\large\itshape '+tex(item['title_en'])+r'}\par\vspace{0.9em}'+r'\\'.join(lines)+
       r'\par\vspace{0.4em}{\small '+r'\\'.join(affiliations)+r'}\par\small Correspondencia: '+contact+
       r'\end{center}}'+'\n')
    (b/'metadata.tex').write_text(s)
    editions=p/'data/coafina-editions.csv'
    if editions.exists():
        rows=list(csv.DictReader(editions.open()))
        body=r'\begin{tabularx}{160mm}{@{}l*{6}{>{\centering\arraybackslash}X}@{}}\toprule'+'\n'
        body+=r'Año & Reportados & Inscritos & Activos & Finalizan & Países & Universidades \\'+'\n'
        for row in rows:
            body+=' & '.join(tex(row[k]) for k in ['edition','reported_students','registered','active','completed','countries','universities'])+r' \\'+'\n'
        (b/'ediciones-body.tex').write_text(body+r'\bottomrule\end{tabularx}'+'\n')
    return info

def expand(path, paper=None, stack=()):
    path=path.resolve(); paper=paper or path.parent
    if path in stack: raise ValueError('Recursive TeX input: '+str(path))
    def replace(match):
        name=match.group(1); rel=Path(name if name.endswith('.tex') else name+'.tex')
        candidate=(paper/rel).resolve()
        if not candidate.exists(): candidate=(path.parent/rel).resolve()
        return expand(candidate,paper,(*stack,path))
    return re.sub(r'\\input\{([^}]+)\}',replace,path.read_text())
