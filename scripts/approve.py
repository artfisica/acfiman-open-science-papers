"""Record authors' approval of a manuscript at the current commit.

Usage: python3 scripts/approve.py <paper-directory> "<author name>" ["<author name>" ...]
Run it right after committing (and pulling) the version the authors have read.
Several calls in a row are fine: pending approval records are the only uncommitted change allowed.
"""
import json, subprocess, sys
from common import ROOT
if len(sys.argv)<3: raise SystemExit(__doc__)
paper, names = sys.argv[1], sys.argv[2:]
def without_approvals(value):
    for manuscript in value['papers']:
        for author in manuscript['authors']: author.pop('manuscript_approval',None)
    return value
changed=[line[3:] for line in subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).splitlines()]
path=ROOT/'papers.json'; meta=json.loads(path.read_text())
committed=json.loads(subprocess.check_output(['git','show','HEAD:papers.json'],cwd=ROOT,text=True))
if [f for f in changed if f!='papers.json'] or without_approvals(json.loads(path.read_text()))!=without_approvals(committed):
    raise SystemExit('Commit the reviewed version first: the approval records a commit.')
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
items=[m for m in meta['papers'] if m['directory']==paper]
if not items: raise SystemExit('Unknown paper')
authors={a['name']:a for a in items[0]['authors']}
for name in names:
    if name not in authors: raise SystemExit(f'Unknown author for {paper}: {name}')
    authors[name]['manuscript_approval']={'status':'approved','approved_source_commit':revision}
    print(f'{paper}: {name} approved at {revision[:10]}')
path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('Now commit papers.json.')
