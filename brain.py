#!/usr/bin/env python3
"""Red Jade second brain. Python 3.10+, standard library only, no network calls."""
import argparse
import html
import json
import math
import re
import sqlite3
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

KINDS = ('experiments', 'evidence', 'lessons', 'reviews')
METRICS = ('saves_per_1000', 'shares_per_1000', 'follows_per_1000', 'retention_10s')


def utc(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('Timestamps need a timezone, for example 2026-10-31T09:00:00+10:00')
    return dt.astimezone(timezone.utc)


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def metric(row, name):
    if name == 'retention_10s':
        return next((p['fraction'] for p in row.get('retention', []) if p['second'] == 10), None)
    count = row.get(name.replace('_per_1000', ''))
    views = row.get('views')
    return 1000 * count / views if count is not None and views else None


def dashboard(payload, summary):
    def esc(value):
        return html.escape(str(value if value is not None else 'Unknown'))

    def table(headers, rows):
        return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+esc(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

    counts = [('Evidence records', len(payload['evidence'])), ('Experiments', len(payload['experiments'])), ('Lessons', len(payload['lessons'])), ('Retests', len(payload['runs']))]
    body = '<header><small>RED JADE / YOUR PRIVATE WORKSPACE</small><h1>Learn from what happened.</h1><p>Evidence, decisions and lessons you can revise.</p><p class="muted">Generated '+esc(payload['generated_at'])+'</p></header>'
    body += '<nav><a href="#lessons">Lessons</a><a href="#experiments">Experiments</a><a href="#evidence">Evidence</a><a href="context.json">Complete export</a><a href="review.md">Text review</a></nav>'
    body += '<section class="stats">'+''.join('<article><strong>'+str(count)+'</strong><span>'+name+'</span></article>' for name,count in counts)+'</section>'
    body += '<section id="lessons"><h2>What we think we know</h2><p>Statuses describe the recorded evidence. They do not prove cause and effect.</p>'
    if not payload['lessons']:
        body += '<p class="empty">No lessons yet. Review your first experiment, then register a hypothesis to test on later evidence.</p>'
    for lesson in payload['lessons']:
        status = payload['lesson_states'][lesson['id']]
        body += '<article class="lesson"><span class="badge">'+esc(status)+'</span><h3>'+esc(lesson['claim'])+'</h3><p class="muted">'+esc(lesson['id'])+'</p>'
        runs = [r for r in payload['runs'] if r['lesson_id'] == lesson['id']]
        body += table(['Run', 'Cutoff', 'Result', 'With / without feature', 'Mean difference', 'Excluded'], [(r['id'],r['as_of'],r['outcome'],f'{len(r["with_feature"])}/{len(r["without_feature"])}',r['difference'],len(r['exclusions'])) for r in runs])
        body += '<details><summary>Test rule and evidence trail</summary><pre>'+esc(json.dumps({'instrument': lesson['instrument'], 'runs': runs},indent=2))+'</pre></details></article>'
    body += '</section><section id="experiments"><h2>Work in progress</h2>'
    titles = {r['id']:r['title'] for r in payload['experiments']}
    body += table(['Experiment','State','Decision'], [(titles.get(s['id'],s['id'])+' ['+s['id']+']',s['state'],s['note'] or 'No final decision recorded') for s in payload['states']])+'</section>'
    body += '<section id="evidence"><h2>Source evidence</h2><p>Open a record to inspect its source, timeline and observed retention. Missing values remain unknown.</p>'
    for e in payload['evidence']:
        body += '<details class="record"><summary>'+esc(e['id'])+' · '+esc(e['variant'])+' · '+esc(e['observed_at'])+'</summary><p>'+esc(e['source_ref'])+'</p>'
        body += table(['Views','Saves / 1,000','Media verified'],[(e['views'],metric(e,'saves_per_1000'),e['media_verified'])])
        body += '<h3>Speech, screen and source timeline</h3>'+table(['Cut seconds','Original seconds','Speech','Screen'],[(f'{s["start"]}–{s["end"]}',f'{s["source_start"]}–{s["source_end"]}',s['speech'],s['screen']) for s in e.get('segments',[])])
        body += '<h3>Observed retention</h3>'+table(['Second','Retained fraction'],[(p['second'],p['fraction']) for p in e.get('retention',[])])+'</details>'
    body += '</section><footer>Keep this workspace private. Collection, media verification and publishing are human steps. <a href="context.json">Export your records</a>.</footer>'
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Red Jade second brain</title><style>body{max-width:1100px;margin:48px auto;padding:0 24px;background:#0e1917;color:#e3eee8;font:16px/1.6 system-ui}h1{font-size:clamp(30px,5vw,54px);line-height:1.1;margin:16px 0}h2{margin-top:42px}h3{font-size:18px}small,.muted{color:#a5beb2}a{color:#9de6bc}nav{display:flex;gap:20px;flex-wrap:wrap;border-bottom:1px solid #345044;padding:20px 0}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:28px 0}.stats article,.lesson,.record,.empty{background:#172a23;border:1px solid #345044;border-radius:12px;padding:18px;margin-bottom:14px}.stats strong{display:block;font-size:30px;color:#a4efc5}.stats span{color:#bdd3c7}.badge{display:inline-block;background:#294638;color:#b9f6ce;border-radius:20px;padding:4px 12px;font-size:13px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #345044}th{color:#a5beb2}.scroll{overflow:auto}summary{cursor:pointer;font-weight:600}details pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}details{margin-top:16px}footer{margin:48px 0;color:#a5beb2}</style></head><body>'+body+'</body></html>'


class Brain:
    def __init__(self, workspace):
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.workspace / 'brain.sqlite3')
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS records (
                kind TEXT NOT NULL, id TEXT NOT NULL, data TEXT NOT NULL,
                PRIMARY KEY(kind,id));
            CREATE TABLE IF NOT EXISTS states (
                id TEXT PRIMARY KEY, state TEXT NOT NULL, note TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY, lesson_id TEXT NOT NULL, at TEXT NOT NULL, data TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS audit (
                seq INTEGER PRIMARY KEY, at TEXT NOT NULL, action TEXT NOT NULL, data TEXT NOT NULL);
        ''')

    def close(self):
        self.db.close()

    def records(self, kind):
        return {key: json.loads(data) for key, data in self.db.execute(
            'SELECT id,data FROM records WHERE kind=? ORDER BY id', (kind,))}

    def audit(self, action, data):
        self.db.execute('INSERT INTO audit(at,action,data) VALUES(?,?,?)', (now(), action, encoded(data)))

    @staticmethod
    def validate(kind, row):
        require(isinstance(row, dict), 'Every record must be an object')
        require(isinstance(row.get('id'), str) and re.fullmatch(r'[A-Za-z0-9_-]{1,100}', row['id']), 'Use simple unique IDs: letters, numbers, _ or -')
        fields = {
            'experiments': ('title', 'objective', 'success_rule', 'created_at'),
            'evidence': ('experiment_id', 'variant', 'post_id', 'source_ref', 'platform', 'cohort', 'published_at', 'observed_at', 'labels_at'),
            'lessons': ('claim', 'created_at'),
            'reviews': ('experiment_id', 'conclusion', 'limitations', 'next_test', 'created_at'),
        }
        for field in fields[kind]:
            require(isinstance(row.get(field), str) and row[field].strip(), f'{row["id"]}: missing {field}')
        for key in ('created_at', 'published_at', 'observed_at', 'labels_at'):
            if key in row:
                utc(row[key])
        if kind == 'evidence':
            require(utc(row['published_at']) <= utc(row['observed_at']), 'Observation precedes publication')
            require(utc(row['labels_at']) <= utc(row['observed_at']), 'Label features before observing their metrics')
            require(isinstance(row.get('features'), dict) and all(isinstance(k, str) and type(v) is bool for k, v in row['features'].items()), 'features must map names to true/false')
            for key in ('views', 'saves', 'shares', 'follows'):
                require(key in row, f'{key} must be present; use null if unknown')
                require(row[key] is None or (type(row[key]) is int and row[key] >= 0), f'{key} must be a nonnegative integer or null')
            require(number(row.get('duration_seconds')) and row['duration_seconds'] > 0, 'duration_seconds must be positive')
            require(type(row.get('media_verified')) is bool, 'media_verified must be true/false')
            seen = set()
            for point in row.get('retention', []):
                require(number(point['second']) and 0 <= point['second'] <= row['duration_seconds'], 'Invalid retention timestamp')
                require(number(point['fraction']) and 0 <= point['fraction'] <= 1, 'Retention fractions must be between 0 and 1')
                require(point['second'] not in seen, 'Duplicate retention timestamp')
                seen.add(point['second'])
            for seg in row.get('segments', []):
                require(all(number(seg[k]) for k in ('start', 'end', 'source_start', 'source_end')), 'Segment times must be finite numbers')
                require(0 <= seg['start'] < seg['end'] <= row['duration_seconds'], 'Segment is outside the posted cut')
                require(0 <= seg['source_start'] < seg['source_end'], 'Invalid original-media time map')
                require(all(isinstance(seg.get(k), str) and seg[k].strip() for k in ('speech', 'screen')), 'Describe speech and screen, including silence if appropriate')
        if kind == 'lessons':
            i = row['instrument']
            for key in ('feature', 'platform', 'cohort'):
                require(isinstance(i.get(key), str) and i[key].strip(), f'Instrument needs {key}')
            require(i['metric'] in METRICS, 'Unsupported instrument metric')
            require(type(i['min_per_group']) is int and i['min_per_group'] >= 2, 'min_per_group must be at least 2; use 8 or more for real work')
            require(type(i['min_views']) is int and i['min_views'] >= 1, 'min_views must be positive')
            for key in ('target_age_hours', 'age_tolerance_hours', 'minimum_difference'):
                require(number(i[key]) and i[key] >= 0, f'{key} must be nonnegative')
            require(i['minimum_difference'] > 0, 'minimum_difference must be positive')
            require(i['direction'] in ('higher', 'lower'), 'direction must be higher or lower')
        if kind == 'reviews':
            require(isinstance(row.get('evidence_ids'), list) and len(set(row['evidence_ids'])) >= 2, 'A review needs at least two distinct evidence IDs')
            require(isinstance(row.get('edits'), list) and row['edits'], 'A review needs timestamped edits, including KEEP where appropriate')
            for edit in row['edits']:
                require(edit['action'] in ('KEEP', 'CHANGE', 'CUT'), 'Edit action must be KEEP, CHANGE or CUT')
                require(edit['method'] in ('EDIT', 'RECORD', 'NONE'), 'Edit method must be EDIT, RECORD or NONE')
                require(number(edit['start']) and number(edit['end']) and 0 <= edit['start'] < edit['end'], 'Invalid edit interval')
                require(all(isinstance(edit.get(k), str) and edit[k].strip() for k in ('reason', 'success_metric')), 'Edits need a reason and success metric')

    def ingest(self, payload):
        require(payload.get('schema_version') == 1, 'Expected schema_version: 1')
        require(set(payload) <= {'schema_version', *KINDS}, 'Unknown top-level key')
        added = 0
        with self.db:
            for kind in KINDS:
                require(isinstance(payload.get(kind, []), list), f'{kind} must be an array')
                for row in payload.get(kind, []):
                    self.validate(kind, row)
                    value = encoded(row)
                    old = self.db.execute('SELECT data FROM records WHERE kind=? AND id=?', (kind, row['id'])).fetchone()
                    if old:
                        require(old[0] == value, f'{kind}/{row["id"]} already exists with different data. Preserve history; use a new ID.')
                        continue
                    self.db.execute('INSERT INTO records VALUES(?,?,?)', (kind, row['id'], value))
                    if kind == 'experiments':
                        self.db.execute('INSERT INTO states VALUES(?,?,?)', (row['id'], 'planned', ''))
                    added += 1
            experiments, evidence = self.records('experiments'), self.records('evidence')
            sources = set()
            post_contracts = {}
            for row in evidence.values():
                require(row['experiment_id'] in experiments, f'Unknown experiment: {row["experiment_id"]}')
                key = (row['platform'], row['post_id'], utc(row['observed_at']))
                require(key not in sources, 'Same post and observation time under different IDs; duplicate snapshot rejected')
                sources.add(key)
                post = (row['platform'], row['post_id'])
                contract = (row['experiment_id'], row['variant'], row['published_at'], row['cohort'], row['features'])
                require(post not in post_contracts or post_contracts[post] == contract, 'A post cannot switch experiments, variants, cohorts or feature labels')
                post_contracts[post] = contract
            for row in experiments.values():
                if row.get('parent_id'):
                    require(row['parent_id'] in experiments and row['parent_id'] != row['id'], 'Unknown or self-referencing parent experiment')
                trail, parent = set(), row['id']
                while parent:
                    require(parent not in trail, 'Experiment parent cycle')
                    trail.add(parent)
                    parent = experiments[parent].get('parent_id')
            for row in self.records('reviews').values():
                require(row['experiment_id'] in experiments, 'Review refers to an unknown experiment')
                require(all(key in evidence and evidence[key]['experiment_id'] == row['experiment_id'] for key in row['evidence_ids']), 'Review evidence must belong to its experiment')
                for edit in row['edits']:
                    require(edit['evidence_id'] in row['evidence_ids'], 'Edit must reference reviewed evidence')
                    require(edit['end'] <= evidence[edit['evidence_id']]['duration_seconds'], 'Edit extends past the video')
            if added:
                self.audit('import', {'added': added})
        return added

    @staticmethod
    def complete_media(row):
        if not row['media_verified']:
            return False
        end = 0.0
        for seg in sorted(row.get('segments', []), key=lambda x: x['start']):
            if seg['start'] > end + 1e-6:
                return False
            end = max(end, seg['end'])
        return end >= row['duration_seconds'] - 1e-6

    def advance(self, key, target, note=''):
        old = self.db.execute('SELECT state,note FROM states WHERE id=?', (key,)).fetchone()
        require(old is not None, 'Unknown experiment')
        if old[0] == target:
            require(target != 'closed' or old[1] == note, 'Closed outcome is immutable')
            return target
        require({'planned': 'testing', 'testing': 'reviewed', 'reviewed': 'closed'}.get(old[0]) == target, 'Use planned -> testing -> reviewed -> closed. A new test gets a new experiment.')
        rows = [r for r in self.records('evidence').values() if r['experiment_id'] == key]
        if target == 'testing':
            require(len({(r['platform'], r['post_id']) for r in rows}) >= 2 and len({r['variant'] for r in rows}) >= 2, 'Testing needs two distinct posts and variants')
        if target == 'reviewed':
            reviews = [r for r in self.records('reviews').values() if r['experiment_id'] == key]
            require(reviews, 'Import an evidence-linked review first')
            chosen = max(reviews, key=lambda r: (utc(r['created_at']), r['id']))
            evidence = self.records('evidence')
            selected = [evidence[i] for i in chosen['evidence_ids']]
            require(len({r['variant'] for r in selected}) >= 2, 'Review needs both variants')
            require(all(self.complete_media(r) for r in selected), 'Review blocked: verified media and complete speech/screen/source mapping required, including the final fraction of a second')
        if target == 'closed':
            require(note.strip(), 'Record the actual decision and outcome with --note')
        with self.db:
            self.db.execute('UPDATE states SET state=?,note=? WHERE id=?', (target, note, key))
            self.audit('transition', {'experiment_id': key, 'from': old[0], 'to': target, 'note': note})
        return target

    def runs(self, lesson_id):
        return [json.loads(r[0]) for r in self.db.execute('SELECT data FROM runs WHERE lesson_id=? ORDER BY at,id', (lesson_id,))]

    def retest(self, lesson_id, run_id, as_of):
        cutoff = utc(as_of)
        as_of = cutoff.isoformat()
        old = self.db.execute('SELECT data FROM runs WHERE id=?', (run_id,)).fetchone()
        if old:
            result = json.loads(old[0])
            require(result['lesson_id'] == lesson_id and result['as_of'] == as_of, 'Run ID already used for another lesson or date')
            return result
        lessons = self.records('lessons')
        require(lesson_id in lessons, 'Unknown lesson')
        lesson = lessons[lesson_id]
        require(cutoff >= utc(lesson['created_at']), 'Retest precedes lesson creation')
        prior = self.runs(lesson_id)
        require(not prior or cutoff > utc(prior[-1]['as_of']), 'New retests must be later than previous ones; reuse the original run ID to rerun')
        used = {e for r in prior if r['outcome'] != 'insufficient' for e in r['experiment_ids']}
        qualified = [r for r in prior if r['outcome'] != 'insufficient']
        lower = utc(qualified[-1]['as_of']) if qualified else utc(lesson['created_at'])
        i = lesson['instrument']
        chosen, exclusions = {}, []
        for row in self.records('evidence').values():
            reason = None
            age = (utc(row['observed_at']) - utc(row['published_at'])).total_seconds() / 3600
            if row['platform'] != i['platform'] or row['cohort'] != i['cohort']:
                reason = 'different platform or distribution cohort'
            elif not lower <= utc(row['observed_at']) <= cutoff or (qualified and utc(row['observed_at']) == lower):
                reason = 'outside prospective observation window'
            elif row['experiment_id'] in used:
                reason = 'experiment already used in a qualified retest'
            elif abs(age - i['target_age_hours']) > i['age_tolerance_hours']:
                reason = 'different post age'
            elif i['feature'] not in row['features']:
                reason = 'feature not labelled'
            if reason:
                exclusions.append({'id': row['id'], 'reason': reason})
                continue
            # Choose nearest-age snapshot per post, then one post per experiment,
            # using identifiers, never the winning metric. Do not backfill failures.
            group = row['experiment_id']
            rank = (row['platform'], row['post_id'], abs(age-i['target_age_hours']), row['observed_at'], row['id'])
            if group not in chosen or rank < chosen[group][0]:
                if group in chosen:
                    exclusions.append({'id': chosen[group][1]['id'], 'reason': 'sibling or repeated snapshot'})
                chosen[group] = (rank, row)
            else:
                exclusions.append({'id': row['id'], 'reason': 'sibling or repeated snapshot'})
        groups = {True: [], False: []}
        for _, row in chosen.values():
            value = metric(row, i['metric'])
            if row['views'] is None or row['views'] < i['min_views'] or value is None:
                exclusions.append({'id': row['id'], 'reason': 'missing metric or insufficient views'})
                continue
            groups[row['features'][i['feature']]].append({'id': row['id'], 'experiment_id': row['experiment_id'], 'value': value})
        enough = all(len(g) >= i['min_per_group'] for g in groups.values())
        difference = None
        robust_difference = None
        outcome = 'insufficient'
        if enough:
            difference = statistics.mean(x['value'] for x in groups[True]) - statistics.mean(x['value'] for x in groups[False])
            directed = difference if i['direction'] == 'higher' else -difference
            outcome = 'supports' if directed >= i['minimum_difference'] else 'contradicts' if directed <= -i['minimum_difference'] else 'inconclusive'
            sensitivity = []
            for side in (True, False):
                for omitted in range(len(groups[side])):
                    means = {k: statistics.mean(x['value'] for n, x in enumerate(v) if k != side or n != omitted) for k, v in groups.items()}
                    sensitivity.append((means[True]-means[False]) * (1 if i['direction'] == 'higher' else -1))
            robust_difference = min(sensitivity)
            if outcome == 'supports' and robust_difference < i['minimum_difference']:
                outcome = 'inconclusive'
        selected = groups[True] + groups[False]
        result = {'id': run_id, 'lesson_id': lesson_id, 'as_of': as_of, 'outcome': outcome,
                  'difference': difference, 'minimum_leave_one_out_difference': robust_difference,
                  'metric': i['metric'], 'with_feature': groups[True],
                  'without_feature': groups[False], 'experiment_ids': sorted(x['experiment_id'] for x in selected),
                  'exclusions': exclusions, 'instrument': i}
        with self.db:
            self.db.execute('INSERT INTO runs VALUES(?,?,?,?)', (run_id, lesson_id, as_of, encoded(result)))
            self.audit('retest', result)
        return result

    def confidence(self, lesson, as_of):
        eligible = [r for r in self.runs(lesson['id']) if utc(r['as_of']) <= utc(as_of) and r['outcome'] != 'insufficient']
        streak, status = 0, 'hunch'
        for result in eligible:
            if result['outcome'] == 'supports':
                streak += 1
                status = 'supported (provisional)' if streak >= 3 else 'likely' if streak >= 2 else 'hunch'
            else:
                streak = 0
                status = 'contradicted' if result['outcome'] == 'contradicts' else 'hunch'
        last = eligible[-1]['as_of'] if eligible else lesson['created_at']
        days = (utc(as_of) - utc(last)).total_seconds() / 86400
        if days >= 90:
            return 'stale'
        if days >= 30 and status in ('likely', 'supported (provisional)'):
            return 'needs retest'
        return status

    def report(self, as_of):
        utc(as_of)
        payload = {k: list(self.records(k).values()) for k in KINDS}
        payload['generated_at'] = as_of
        payload['states'] = [{'id': r[0], 'state': r[1], 'note': r[2]} for r in self.db.execute('SELECT * FROM states ORDER BY id')]
        payload['runs'] = [json.loads(r[0]) for r in self.db.execute('SELECT data FROM runs ORDER BY at,id')]
        payload['lesson_states'] = {r['id']: self.confidence(r, as_of) for r in payload['lessons']}
        lines = ['# Second brain review', '', f'Generated: {as_of}', '',
                 'Local evidence summary. Lesson statuses are workflow labels, not statistical proof or causal conclusions.', '', '## Experiments', '']
        for state in payload['states']:
            lines.append(f'- {state["id"]}: {state["state"]}. {state["note"]}')
        lines += ['', '## Lessons', '']
        for lesson in payload['lessons']:
            status = self.confidence(lesson, as_of)
            lines += [f'- {lesson["id"]} [{status}]: {lesson["claim"]}']
            history = self.runs(lesson['id'])
            if history:
                r = history[-1]
                lines.append(f'  Latest run {r["id"]}: {r["outcome"]}; groups {len(r["with_feature"])}/{len(r["without_feature"])}; mean difference {r["difference"]}; excluded {len(r["exclusions"])}.')
        lines += ['', '## Evidence inventory', '']
        for e in payload['evidence']:
            lines.append(f'- {e["id"]}: {e["source_ref"]}; observed {e["observed_at"]}; saves/1,000 = {metric(e, "saves_per_1000")}; media complete = {self.complete_media(e)}')
        lines += ['', '## Next review', '',
                  'Read context.json for every evidence ID, timeline, review, instrument and exclusion. Inspect counterexamples and unrelated changes before adopting a lesson. Choose up to three new tests, record their success rules before collecting results, and link them to the earlier experiment.', '']
        out = self.workspace / 'reports'
        out.mkdir(exist_ok=True)
        text = '\n'.join(lines)
        (out / 'review.md').write_text(text, encoding='utf-8')
        (out / 'context.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
        (out / 'dashboard.html').write_text(dashboard(payload, text), encoding='utf-8')
        return out


def demo_payload(as_of):
    """Fictional data, three independent supporting batches and a contradiction."""
    end = utc(as_of)
    start = end - timedelta(days=24)
    data = {'schema_version': 1, 'experiments': [], 'evidence': [], 'lessons': [{
        'id': 'DEMO-lesson', 'claim': 'A direct opening is associated with more saves per 1,000 views in the fictional archive.',
        'created_at': start.isoformat(), 'instrument': {'feature': 'direct_open', 'metric': 'saves_per_1000',
        'platform': 'fictional', 'cohort': 'organic-demo', 'min_per_group': 8, 'min_views': 1000,
        'target_age_hours': 24, 'age_tolerance_hours': 2, 'minimum_difference': 5, 'direction': 'higher'}}]}
    dates = []
    for batch in range(4):
        observed = start + timedelta(days=3+batch*6)
        dates.append((observed+timedelta(hours=1)).isoformat())
        for index in range(16):
            key = f'DEMO-{batch+1}-{index+1:02}'
            direct = index < 8
            saves = (40 if direct else 20) if batch < 3 else (10 if direct else 35)
            data['experiments'].append({'id': key, 'title': 'Fictional independent concept '+key, 'objective': 'Compare openings', 'success_rule': 'Higher saves per 1,000 at 24 hours; minimum 1,000 views', 'created_at': start.isoformat()})
            data['evidence'].append({'id': key, 'experiment_id': key, 'variant': 'archive', 'post_id': key,
                'source_ref': 'fictional:'+key, 'platform': 'fictional', 'cohort': 'organic-demo',
                'published_at': (observed-timedelta(days=1)).isoformat(), 'observed_at': observed.isoformat(),
                'labels_at': (observed-timedelta(days=1,hours=1)).isoformat(), 'features': {'direct_open': direct},
                'views': 1000, 'saves': saves, 'shares': None, 'follows': None, 'duration_seconds': 12.5,
                'media_verified': False, 'segments': [], 'retention': []})
    return data, dates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', default='private/brain', help='Private data folder (default: private/brain)')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    imp = sub.add_parser('import'); imp.add_argument('file')
    adv = sub.add_parser('advance'); adv.add_argument('id'); adv.add_argument('state', choices=['testing','reviewed','closed']); adv.add_argument('--note', default='')
    rt = sub.add_parser('retest'); rt.add_argument('lesson_id'); rt.add_argument('--run-id', required=True); rt.add_argument('--as-of', required=True)
    rep = sub.add_parser('report'); rep.add_argument('--as-of', default=now())
    sub.add_parser('demo')
    args = parser.parse_args()
    brain = Brain(args.workspace)
    try:
        if args.command == 'init':
            print(f'Ready: {brain.workspace}')
        elif args.command == 'import':
            data = json.loads(Path(args.file).read_text(encoding='utf-8-sig'))
            print(f'Imported {brain.ingest(data)} new records. Identical records are reused.')
        elif args.command == 'advance':
            print(brain.advance(args.id, args.state, args.note))
        elif args.command == 'retest':
            print(json.dumps(brain.retest(args.lesson_id, args.run_id, args.as_of), indent=2))
        elif args.command == 'report':
            print(f'Report: {brain.report(args.as_of) / "dashboard.html"}')
        elif args.command == 'demo':
            require(not any(brain.records(k) for k in KINDS), 'Run demo only in an empty, separate workspace')
            data, dates = demo_payload(now())
            brain.ingest(data)
            for index, date in enumerate(dates):
                result = brain.retest('DEMO-lesson', f'DEMO-run-{index+1}', date)
                print(f'{result["id"]}: {result["outcome"]} -> {brain.confidence(data["lessons"][0], date)}')
            print(f'Report: {brain.report(now()) / "dashboard.html"}')
    except (ValueError, KeyError, TypeError, OSError, sqlite3.Error) as exc:
        parser.exit(2, f'Error: {exc}\n')
    finally:
        brain.close()


if __name__ == '__main__':
    main()
