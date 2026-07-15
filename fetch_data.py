#!/usr/bin/env python3
"""
fetch_data.py — Fetches Jira data for the CUBE Exec View dashboard.
Called by .github/workflows/refresh-data.yml on every scheduled run.
Requires env vars: JIRA_EMAIL, JIRA_API_TOKEN
"""
import urllib.request, json, base64, os, datetime, sys

email = os.environ['JIRA_EMAIL']
token = os.environ['JIRA_API_TOKEN']
auth  = base64.b64encode(f'{email}:{token}'.encode()).decode()

REDACTED = {
    'CPN-1114','CPN-1115','CPN-1116','CPN-1117','CPN-1118',
    'CPN-1216','CPN-1217','CPN-1224','CPN-1313',
    'CPN-1218','CPN-1219','CPN-1220','CPN-1221','CPN-1222','CPN-1225',
    'CPN-1183','CPN-1184','CPN-1185','CPN-1186','CPN-1187','CPN-1188',
    'CPN-1428','CPN-1429','CPN-1430',
    'CPN-1170','CPN-1172','CPN-1173','CPN-1174','CPN-1175',
    'CPN-1176','CPN-1177','CPN-1178','CPN-1179','CPN-1181',
    'CPN-1171','CPN-1182',
    'CPN-1230','CPN-1231','CPN-1232','CPN-1233','CPN-1234','CPN-1235',
}


def extract_panels(description):
    if not description or not isinstance(description, dict):
        return []
    panels = []

    def collect_text(node):
        if not isinstance(node, dict): return ''
        if node.get('type') == 'text': return node.get('text', '')
        if node.get('type') == 'hardBreak': return ' '
        return ' '.join(collect_text(c) for c in node.get('content', []) if c)

    def traverse(node):
        if not isinstance(node, dict): return
        if node.get('type') == 'panel':
            ptype = node.get('attrs', {}).get('panelType', 'info')
            text  = collect_text(node).strip()
            if text:
                panels.append({'type': ptype, 'text': text})
        else:
            for child in node.get('content', []):
                traverse(child)

    traverse(description)
    return panels


def fetch_jira(jql, output_file, jira_url):
    items = []
    next_page_token = None
    while True:
        body = {
            'jql': jql, 'maxResults': 100,
            'fields': ['summary','status','assignee','duedate','updated',
                       'labels','issuetype','description'],
        }
        if next_page_token:
            body['nextPageToken'] = next_page_token
        payload = json.dumps(body).encode()
        req = urllib.request.Request(
            'https://cube001.atlassian.net/rest/api/3/search/jql',
            data=payload,
            headers={
                'Authorization': f'Basic {auth}',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        for issue in data.get('issues', []):
            if issue.get('key', '') in REDACTED:
                continue
            f = issue.get('fields', {})
            items.append({
                'key':      issue.get('key', ''),
                'summary':  f.get('summary', ''),
                'status':   (f.get('status') or {}).get('name', ''),
                'assignee': (f.get('assignee') or {}).get('displayName', 'Unassigned'),
                'duedate':  f.get('duedate', '') or '',
                'reviewed': (f.get('updated') or '')[:10],
                'labels':   f.get('labels', []),
                'url':      f'https://cube001.atlassian.net/browse/{issue.get("key","")}',
                'panels':   extract_panels(f.get('description')),
            })
        next_page_token = data.get('nextPageToken')
        if not next_page_token or not data.get('issues'):
            break
    tmp = output_file + '.tmp'
    with open(tmp, 'w', newline='\n') as fh:
        json.dump({
            'updated': datetime.datetime.utcnow().isoformat() + 'Z',
            'total':   len(items),
            'jiraUrl': jira_url,
            'items':   items,
        }, fh, indent=2)
    os.replace(tmp, output_file)
    print(f'OK  {output_file}: {len(items)} items')


def fetch_jira_incidents(jql, output_file):
    items = []
    next_page_token = None
    while True:
        body = {
            'jql': jql, 'maxResults': 100,
            'fields': ['summary','status','assignee','priority',
                       'created','updated','issuetype','labels'],
        }
        if next_page_token:
            body['nextPageToken'] = next_page_token
        payload = json.dumps(body).encode()
        req = urllib.request.Request(
            'https://cube001.atlassian.net/rest/api/3/search/jql',
            data=payload,
            headers={
                'Authorization': f'Basic {auth}',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        for issue in data.get('issues', []):
            f = issue.get('fields', {})
            items.append({
                'key':       issue.get('key', ''),
                'summary':   f.get('summary', ''),
                'status':    (f.get('status') or {}).get('name', ''),
                'assignee':  (f.get('assignee') or {}).get('displayName', 'Unassigned'),
                'priority':  (f.get('priority') or {}).get('name', ''),
                'issuetype': (f.get('issuetype') or {}).get('name', ''),
                'labels':    f.get('labels', []),
                'created':   (f.get('created') or '')[:10],
                'updated':   (f.get('updated') or '')[:10],
                'url':       f'https://cube001.atlassian.net/browse/{issue.get("key","")}',
            })
        next_page_token = data.get('nextPageToken')
        if not next_page_token or not data.get('issues'):
            break
    tmp = output_file + '.tmp'
    with open(tmp, 'w', newline='\n') as fh:
        json.dump({
            'updated': datetime.datetime.utcnow().isoformat() + 'Z',
            'total':   len(items),
            'items':   items,
        }, fh, indent=2)
    os.replace(tmp, output_file)
    print(f'OK  {output_file}: {len(items)} items')


# Run all fetches independently — one failure does not block the others.
FETCHES = [
    (fetch_jira, (
        'project = CPN AND labels in ("Consumer","consumer") AND status NOT IN (Cancelled, Closed, "Not started") ORDER BY updated DESC',
        'data.json',
        'https://cube001.atlassian.net/jira/plans/7/scenarios/7/timeline?vid=183',
    )),
    (fetch_jira, (
        'project = CPN AND labels = "InfoSec" AND status NOT IN (Cancelled, Closed, "Not started") ORDER BY updated DESC',
        'data-infosec.json',
        'https://cube001.atlassian.net/jira/plans/7/scenarios/7/timeline?vid=313',
    )),
    (fetch_jira, (
        'project = CPN AND labels in ("Infra","infrastructure") AND status NOT IN (Cancelled, Closed, "Not started") ORDER BY updated DESC',
        'data-infra.json',
        'https://cube001.atlassian.net/jira/plans/7/scenarios/7/timeline?vid=315',
    )),
    (fetch_jira, (
        'project = CPN AND labels = "content" AND status NOT IN (Cancelled, Closed, "Not started") ORDER BY updated DESC',
        'data-content.json',
        'https://cube001.atlassian.net/jira/plans/7/scenarios/7/timeline?vid=183',
    )),
    (fetch_jira, (
        'project = CPN AND labels = "TechOps" AND status NOT IN (Cancelled, Closed, "Not started") ORDER BY updated DESC',
        'data-techops.json',
        'https://cube001.atlassian.net/jira/plans/7/scenarios/7/timeline?vid=317',
    )),
    (fetch_jira, (
        'project = CPN AND labels in ("intelContent","intelcpn") AND status NOT IN (Cancelled, Closed, "Not started") ORDER BY updated DESC',
        'data-midmarket.json',
        'https://cube001.atlassian.net/jira/plans/7/scenarios/7/timeline?vid=2830',
    )),
    (fetch_jira, (
        'project = CPN AND labels = "D&AI" AND status NOT IN (Cancelled, Closed, "Not started") ORDER BY updated DESC',
        'data-dataai.json',
        'https://cube001.atlassian.net/jira/plans/7/scenarios/7/timeline?vid=2831',
    )),
    (fetch_jira_incidents, (
        'project = INC AND created >= -30d ORDER BY created DESC',
        'data-esentire.json',
    )),
]


def fetch_townhall():
    """Fetch CPN-1712 description and write data-townhall.json."""
    req = urllib.request.Request(
        'https://cube001.atlassian.net/rest/api/3/issue/CPN-1712?fields=summary,description,assignee,status,updated',
        headers={
            'Authorization': f'Basic {auth}',
            'Accept': 'application/json',
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    f = data.get('fields', {})
    result = {
        'updated':     datetime.datetime.utcnow().isoformat() + 'Z',
        'key':         'CPN-1712',
        'summary':     f.get('summary', ''),
        'description': f.get('description'),
        'assignee':    (f.get('assignee') or {}).get('displayName', 'Unassigned'),
        'status':      (f.get('status') or {}).get('name', ''),
    }
    tmp = 'data-townhall.json.tmp'
    with open(tmp, 'w', newline='\n') as fh:
        json.dump(result, fh, indent=2)
    os.replace(tmp, 'data-townhall.json')
    print('OK  data-townhall.json')

failures = []

# Townhall runs separately (no args tuple)
try:
    fetch_townhall()
except Exception as e:
    print(f'FAIL data-townhall.json: {e}', file=sys.stderr)
    failures.append('data-townhall.json')

for fn, args in FETCHES:
    try:
        fn(*args)
    except Exception as e:
        out = args[1] if len(args) > 1 else args[0]
        print(f'FAIL {out}: {e}', file=sys.stderr)
        failures.append(out)

if failures:
    print(f'\n{len(failures)} fetch(es) failed: {failures}', file=sys.stderr)
    sys.exit(1)
