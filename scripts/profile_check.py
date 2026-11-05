#!/usr/bin/env python3
"""Profile self-check: every repo linked from README.md must exist, be public,
and have a green latest run of the workflow its badge points at.

Run: python3 scripts/profile_check.py   (set GITHUB_TOKEN to avoid rate limits)
Exit 0 = every claim on the page holds, 1 = something on the page is stale.
"""
import json, os, re, sys, urllib.request

README = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'README.md')
API = 'https://api.github.com'


def get(path):
    req = urllib.request.Request(API + path, headers={'Accept': 'application/vnd.github+json',
                                                       'User-Agent': 'profile-check'})
    tok = os.environ.get('GITHUB_TOKEN')
    if tok:
        req.add_header('Authorization', 'Bearer ' + tok)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main():
    text = open(README, encoding='utf-8').read()
    repos = sorted(set(re.findall(r'https://github\.com/gkmr/([\w.-]+)\)', text)) - {'gkmr'})
    badges = set(re.findall(r'github\.com/gkmr/([\w.-]+)/actions/workflows/([\w.-]+\.yml)/badge\.svg', text))
    problems = []
    for repo in repos:
        try:
            meta = get('/repos/gkmr/%s' % repo)
            if meta.get('private'):
                problems.append('%s is private but linked publicly' % repo)
        except Exception as e:
            problems.append('%s: %s' % (repo, e))
    for repo, wf in sorted(badges):
        if repo == 'gkmr':
            continue
        try:
            runs = get('/repos/gkmr/%s/actions/workflows/%s/runs?branch=main&per_page=5' % (repo, wf))['workflow_runs']
            done = [r for r in runs if r['status'] == 'completed']
            if not done:
                problems.append('%s/%s has no completed run' % (repo, wf))
            elif done[0]['conclusion'] != 'success':
                problems.append('%s/%s latest run is %s' % (repo, wf, done[0]['conclusion']))
        except Exception as e:
            problems.append('%s/%s: %s' % (repo, wf, e))
    print('checked %d repos, %d badges' % (len(repos), len(badges)))
    for p in problems:
        print('STALE: ' + p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
