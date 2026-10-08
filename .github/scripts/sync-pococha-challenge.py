"""Mirror the published Sites HTML without executing remote source code."""
import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

PROJECT = 'appgprj_6ac5d38d4a1c819198d391565430e75d'
SOURCE = 'https://pococha-challenge.freefreelife2000.chatgpt.site/github-export.json'
PUBLIC = 'https://yoshi2026s.github.io/pococha-challenge/'
TARGET = Path('pococha-challenge/index.html')
STATE = Path('.github/state/pococha-challenge-sync.json')
LIMIT = 4 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url):
    request = Request(url, headers={'User-Agent': 'PocochaChallengeSync/1.0', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=30) as response:
        if response.status != 200 or urlparse(response.url).hostname != urlparse(url).hostname:
            raise ValueError('Expected an unredirected successful response from the configured host.')
        data = response.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError('Response exceeded the maximum sync payload size.')
        return data


def validate(payload):
    if payload.get('schema') != 1 or payload.get('projectId') != PROJECT or payload.get('file') != 'index.html':
        raise ValueError('Export identity or schema is invalid.')
    content = payload.get('content')
    checksum = payload.get('sha256')
    if not isinstance(content, str) or not isinstance(checksum, str) or not re.fullmatch(r'[0-9a-f]{64}', checksum):
        raise ValueError('Missing HTML or SHA-256.')
    data = content.encode('utf-8')
    if not 1000 <= len(data) <= LIMIT or digest(data) != checksum:
        raise ValueError('Export content and SHA-256 do not match.')
    required = ['<!doctype html>', '<h1>ポコチャレ解答集</h1>', f'name="pococha-sync-project" content="{PROJECT}"',
                'id="month"', 'id="departments"', 'id="sharePage"', '</html>']
    if any(value not in content for value in required):
        raise ValueError('The export is not a complete Pococha Challenge application.')
    return data, checksum


def output(name, value):
    value = str(value).lower() if isinstance(value, bool) else str(value)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write(f'{name}={value}\n')
    print(f'{name}={value}')


def public_matches(checksum):
    try:
        return digest(fetch(f'{PUBLIC}?sync={checksum}')) == checksum
    except Exception:
        return False


def sync(payload):
    data, checksum = validate(payload)
    current = TARGET.read_bytes()
    state = json.loads(STATE.read_text(encoding='utf-8'))
    if state.get('projectId') != PROJECT:
        raise ValueError('Sync baseline belongs to a different project.')
    current_checksum = digest(current)
    if current_checksum != state.get('sha256') and current_checksum != checksum:
        raise ValueError('GitHub was edited independently. Merge that change into Sites before syncing; no files were overwritten.')
    changed = current != data
    if changed:
        temporary = TARGET.with_suffix('.html.sync-tmp')
        temporary.write_bytes(data)
        temporary.replace(TARGET)
    state_changed = state.get('sha256') != checksum
    if state_changed:
        STATE.write_text(json.dumps({'schema': 1, 'projectId': PROJECT, 'sha256': checksum}, indent=2) + '\n', encoding='utf-8')
    output('changed', changed or state_changed)
    output('sha256', checksum)
    return checksum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--export-file', type=Path, help='Use a local export for validation or a controlled initial run.')
    parser.add_argument('--offline', action='store_true', help='Skip the public URL check during local validation.')
    parser.add_argument('--verify-public', action='store_true')
    args = parser.parse_args()
    if args.verify_public:
        checksum = digest(TARGET.read_bytes())
        for attempt in range(24):
            if public_matches(checksum):
                print('GitHub Pages serves the exact synchronized HTML.')
                return
            if attempt < 23:
                time.sleep(10)
        raise RuntimeError('The repository is synchronized, but GitHub Pages publication has not been confirmed.')
    payload = json.loads(args.export_file.read_text(encoding='utf-8') if args.export_file else fetch(SOURCE))
    checksum = sync(payload)
    output('rebuild', False if args.offline else not public_matches(checksum))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Sync stopped: {error}', file=sys.stderr)
        sys.exit(1)
