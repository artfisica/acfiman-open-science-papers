"""Metadata, source provenance and TeX expansion shared by build/check/export."""
from pathlib import Path
import csv, datetime, hashlib, json, re, subprocess
ROOT = Path(__file__).resolve().parents[1]
def metadata():
    return json.loads((ROOT/'papers.json').read_text())
def tex(value):
    return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in str(value))
def inputs(p):
    files = [ROOT/'papers.json', ROOT/'Makefile', *sorted((ROOT/'shared').glob('*.tex'))]
    files += list((ROOT/'scripts').glob('*.py'))
    files += list((ROOT/'.devcontainer').glob('*'))
    files += list((ROOT/'.github/workflows').glob('*.yml'))
    files += [f for f in p.rglob('*.tex') if 'build' not in f.relative_to(p).parts]
    # evidence.csv is editorial bookkeeping, not a typeset input.
    return sorted(set(files) | set(source_inputs(p)))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def source_inputs(p):
    # Editorial data are tracked even when not yet typeset. Generated PDFs are outputs.
    return sorted({ROOT/'papers.json', *[f for f in p.rglob('*')
        if f.is_file() and 'build' not in f.relative_to(p).parts
        and (f.suffix == '.tex' or ('data' in f.relative_to(p).parts and f.name != 'evidence.csv'))]})
def runtime_image():
    config=json.loads((ROOT/'.devcontainer/devcontainer.json').read_text())
    return config.get('image') or config['build']['args']['TEX_IMAGE']
def provenance(p):
    if subprocess.check_output(['git','rev-parse','--is-shallow-repository'],cwd=ROOT,text=True).strip()=='true':
        raise SystemExit('Full source history required: run git fetch --unshallow origin.')
    info={}
    source=source_inputs(p)
    build=sorted(set(inputs(p))-set(source))
    for kind, files in [('source',source),('build',build)]:
        paths=[str(f.relative_to(ROOT)) for f in files]
        result=subprocess.check_output(['git','log','-1','--format=%H %ct','--',*paths],cwd=ROOT,text=True).strip()
        if not result: raise SystemExit('A committed history is required to build.')
        commit,epoch=result.split()
        dirty=bool(subprocess.check_output(['git','status','--porcelain','--',*paths],cwd=ROOT,text=True).strip())
        info.update({kind+'_commit':commit,kind+'_date':datetime.datetime.fromtimestamp(int(epoch),datetime.timezone.utc).date().isoformat(),kind+'_epoch':int(epoch),kind+'_dirty':dirty})
    return info
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
    revision=info['source_date']+' \u00b7 '+info['source_commit'][:10]+(' \u00b7 cambios locales' if info['source_dirty'] else '')
    contact=tex(item['corresponding_author'])
    if item['corresponding_email']: contact+='; '+tex(item['corresponding_email'])
    # Macros semanticas: el preambulo decide la maquetacion del bloque de titulo.
    s=(r'\hypersetup{pdftitle={'+tex(item['title'])+r'},pdfauthor={'+tex(', '.join(a['name'] for a in item['authors']))+'}}\n'+
       r'\newcommand{\sourcerevision}{'+tex(revision)+'}\n'+
       r'\newcommand{\papertitle}{'+tex(item['title'])+'}\n'+
       r'\newcommand{\papertitleen}{'+tex(item['title_en'])+'}\n'+
       r'\newcommand{\papershorttitle}{'+tex(item.get('short_title') or item['title'])+'}\n'+
       r'\newcommand{\paperauthors}{'+r'\\'.join(lines)+'}\n'+
       r'\newcommand{\paperaffiliations}{'+r'\\'.join(affiliations)+'}\n'+
       r'\newcommand{\papercontact}{'+contact+'}\n'+
       r'\newcommand{\paperstatus}{'+item['status']+'}\n')
    (b/'metadata.tex').write_text(s)
    def cell(v):
        v=(v or '').strip()
        if v in ('ND',''): return r'\nd'
        out=tex(v)
        return out.replace(r'\textasciitilde{}',r'\aprox{}').replace('>',r'\mayor{}').replace('<',r'\menor{}')
    editions=p/'data/coafina-editions-public.csv'
    if editions.exists():
        rows=list(csv.DictReader(editions.open()))
        table=r'\begin{tabularx}{\linewidth}{@{}l l r r >{\RaggedRight\arraybackslash}p{30mm} Z r@{}}\toprule'+'\n'
        table+=r'\cabecera{Edición} & \cabecera{Fechas} & \cabecera{Inscritos} & \cabecera{Actividad} & \cabecera{Entregas} & \cabecera{Retos} & \cabecera{Universidades} \\\midrule'+'\n'
        def dates(row):
            import datetime
            start=datetime.date.fromisoformat(row['date_start']); end=datetime.date.fromisoformat(row['date_end'])
            return start.strftime('%d/%m')+'--'+end.strftime('%d/%m')
        for row in rows:
            if row['status']=='programado': continue
            activity=row['participated']
            if activity.startswith('ND'): activity='ND'
            university=row['registered_universities'] if row['edition']=='2022' else row['universities_event']
            university=university.split(' (')[0]
            unimark=r'\tnote{a}' if row['edition']=='2022' else ''
            entregas=row['solutions_or_teams'].replace(' soluciones evaluadas',' soluciones')
            table+=' & '.join([r'\fila{'+row['edition']+'}',dates(row),cell(row['registered'].split(' (')[0]),cell(activity),cell(entregas),cell(row['challenges'].split(' (')[0]),cell(university)+unimark])+r' \\'+'\n'
        (b/'ediciones-body.tex').write_text(table+r'\bottomrule\end{tabularx}'+'\n')
        rows=list(csv.DictReader((p/'data/participation-flows.csv').open()))
        table=r'\begin{tabularx}{\linewidth}{@{}l r r Y r@{}}\toprule'+'\n'
        table+=r'\cabecera{Evento} & \cabecera{Inscritos} & \cabecera{Recuento} & \cabecera{Umbral de actividad reportado} & \cabecera{Cociente} \\\midrule'+'\n'
        for row in rows:
            ratio=row['ratio'].replace('No calculable','ND')
            table+=' & '.join([r'\fila{'+tex(row['event'])+'}',cell(row['registered']),cell(row['observed']),tex(row['definition']),cell(ratio)])+r' \\'+'\n'
        (b/'participacion-body.tex').write_text(table+r'\bottomrule\end{tabularx}'+'\n')
    from participation_figure import generate_figure
    generate_figure(p, b, tex)
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
