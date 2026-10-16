"""Persist investigation notes without retaining SQL log content.

A SHA-256 digest of the supplied log identifies its notes. Notes and Resolved
flags are stored per-user so they survive quitting/reopening the checker.
"""

import json
import os
import tempfile
from pathlib import Path

MAX_NOTE_LENGTH = 10000


def notes_directory():
    override = os.environ.get('SQLINES_NOTES_DIR')
    if override:
        return Path(override)
    if os.name == 'nt':
        return Path(os.environ.get('LOCALAPPDATA') or Path.home() / 'AppData' / 'Local') / 'SQLinesLogChecker' / 'notes'
    if sys_platform_is_mac():
        return Path.home() / 'Library' / 'Application Support' / 'SQLinesLogChecker' / 'notes'
    return Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share')) / 'SQLinesLogChecker' / 'notes'


def sys_platform_is_mac():
    import sys
    return sys.platform == 'darwin'


def notes_file(report_id):
    if len(report_id) != 64 or any(char not in '0123456789abcdef' for char in report_id):
        raise ValueError('Invalid report identifier')
    return notes_directory() / f'{report_id}.json'


def load_notes(report_id):
    path = notes_file(report_id)
    if not path.exists():
        return {}
    stored = json.loads(path.read_text(encoding='utf-8'))
    if stored.get('version') != 1 or not isinstance(stored.get('errors'), dict):
        raise ValueError('Unrecognized notes file format')
    results = {}
    for index, entry in stored['errors'].items():
        if index.isdecimal() and isinstance(entry, dict) and isinstance(entry.get('note'), str) and type(entry.get('resolved')) is bool:
            results[index] = {'note': entry['note'], 'resolved': entry['resolved']}
    return results


def save_notes(report_id, notes):
    path = notes_file(report_id)
    if not notes:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, prefix='.notes-', suffix='.tmp', delete=False) as tmp:
            tmp_path = Path(tmp.name)
            json.dump({'version': 1, 'errors': notes}, tmp, ensure_ascii=False, indent=2)
            tmp.write('\n')
        os.replace(tmp_path, path)
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
