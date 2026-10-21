"""Aggregate explicitly supplied anonymized records; never infer historical cohorts."""
import argparse, csv, datetime as dt, json, statistics
p=argparse.ArgumentParser();p.add_argument('--sessions',required=True);p.add_argument('--usage',required=True);args=p.parse_args()
def read(path):
    with open(path,newline='') as f:return list(csv.DictReader(f))
sessions=read(args.sessions);usage=read(args.usage)
if not sessions and not usage:raise SystemExit('Templates contain no observations. Supply real records; no report generated.')
def number(row,key):
    value=float(row[key])
    if value<0:raise ValueError(key+' must be nonnegative')
    return value
times=[];outcomes={};missing=0
for row in sessions:
    outcome=row['outcome'];outcomes[outcome]=outcomes.get(outcome,0)+1
    if row['started_at'] and row['validated_at']:
        start=dt.datetime.fromisoformat(row['started_at']);end=dt.datetime.fromisoformat(row['validated_at'])
        if start.tzinfo is None or end.tzinfo is None:raise ValueError('Timestamps need UTC offsets')
        elapsed=(end-start).total_seconds()/60
        if elapsed<0:raise ValueError('Validation precedes start')
        times.append(elapsed)
    else:missing+=1
report={'session_records':len(sessions),'timed_records':len(times),'missing_times':missing,'outcomes':outcomes,'median_minutes':statistics.median(times) if times else None,'min_minutes':min(times) if times else None,'max_minutes':max(times) if times else None,'usage_records':len(usage),'core_hours':sum(number(r,'cores')*number(r,'active_hours') for r in usage),'storage_gb_hours':sum(number(r,'storage_gb_hours') for r in usage),'prebuild_actions_minutes':sum(number(r,'prebuild_actions_minutes') for r in usage),'cost':None,'note':'No tariff or invoice supplied; resource totals are not billed cost.'}
print(json.dumps(report,indent=2))
