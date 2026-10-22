"""Generate the participation diagram from the same CSV as its table."""
import csv

def generate_figure(paper, build, tex):
    source=paper/'data/participation-flows.csv'
    if not source.exists(): return
    rows=list(csv.DictReader(source.open()))
    def number(s):
        if s=='ND': return None
        return float(s.lstrip('~><'))
    maximum=max(number(r[k]) or 0 for r in rows for k in ('registered','observed'))
    scale=90/max(maximum,1)
    def x(n): return 55+scale*n
    def display(s):
        return tex(s).replace(r'\textasciitilde{}',r'$\approx$').replace('>',r'$>$').replace('<',r'$<$')
    lines=[r'\begin{tikzpicture}[x=1mm,y=1mm]']
    for i,r in enumerate(rows):
        y=-i*15
        a,b=number(r['observed']),number(r['registered'])
        lines.append(r'\node[anchor=east,font=\small,align=right,text width=49mm] at (51,'+str(y)+'){'+tex(r['event'])+'};')
        if a is not None and b is not None:
            dashed=','+'dashed' if any(r[k].startswith(('~','>','<')) for k in ('observed','registered')) else ''
            lines.append(r'\draw[tinta'+dashed+'] ('+f'{x(a)},{y}) -- ({x(b)},{y});')
        for key,n in [('observed',a),('registered',b)]:
            if n is None: continue
            raw=r[key]; pos=f'({x(n)},{y})'
            if raw.startswith('>'):
                lines.append(r'\draw[tinta,-{Stealth[open]},dashed] '+pos+' -- ('+f'{x(n)+8},{y});')
                lines.append(r'\draw[tinta] ('+f'{x(n)},{y-1.5}) -- ({x(n)},{y+1.5});')
            elif raw.startswith('~'):
                lines.append(r'\draw[tinta] '+pos+' ++(0,1.4) -- ++(1.4,-1.4) -- ++(-1.4,-1.4) -- ++(-1.4,1.4) -- cycle;')
            else:
                lines.append(r'\node['+('punto' if key=='observed' else 'puntohueco')+'] at '+pos+' {};')
        label=display(r['observed'])+' / '+display(r['registered'])+'; '+display(r['ratio'])
        lines.append(r'\node[anchor=west,font=\footnotesize] at (158,'+str(y)+'){'+label+'};')
    y=-len(rows)*15+6
    lines.append(r'\draw[gris] (55,'+str(y)+') -- (153,'+str(y)+');')
    for n in range(0,int(maximum)+1,20):
        lines.append(r'\node[anchor=north,font=\footnotesize,text=gris] at ('+f'{x(n)},{y}' +'){'+str(n)+'};')
    lines.append(r'\node[anchor=north,font=\footnotesize] at (100,'+str(y-5)+'){Personas};')
    lines.append(r'\node[anchor=west,font=\footnotesize] at (55,12){Círculo lleno: actividad; vacío: inscripción; rombo: aproximación};')
    lines.append(r'\end{tikzpicture}')
    (build/'participacion-chart.tex').write_text('\n'.join(lines)+'\n')
