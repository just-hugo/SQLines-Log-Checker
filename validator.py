"""SQLines error classification and report validation."""
import re
from log_integrity import ErrorBlock, parse_log
from sql_analyzer import analyze_sql_error

EXPECTED_INDEXES = {'pbcatt_x', 'pbcatc_x', 'pbcatf_x', 'pbcatv_x', 'pbcate_x'}
CATEGORIES = ['uuidtostr', 'pbcatt_x', 'pbcatc_x', 'pbcatf_x', 'pbcatv_x', 'pbcate_x', 'ix_cnt_diffweeks']


def parse_blocks(log_text):
    """Compatibility helper for callers using the previous parser API."""
    return parse_log(log_text).blocks


def classify_block(block):
    sql, error = block.sql.lower(), block.error.lower()
    if (re.search(r'add default\s+dbo\.uuidtostr\s*\(\s*newid\s*\(\s*\)\s*\)', sql)
        and 'column "dbo" is not allowed in this context' in error
        and 'user-defined function or aggregate' in error
        and 'could not be found' in error):
        return 'uuidtostr'
    for name in EXPECTED_INDEXES:
        if (re.search(rf'create unique index\s+\[{re.escape(name)}\]', sql)
            and f"index or statistics with name '{name}' already exists" in error):
            return name
    if re.search(r'create index\s+\[ix_cnt_diffweeks\]', sql) and "incorrect syntax near ')'" in error:
        return 'ix_cnt_diffweeks'
    return None


def validate(log_text, input_issues=None):
    """Return PASS, FAIL or CANNOT VALIDATE, preserving diagnostic details.

    Input problems (such as invalid extension) block parsing. Incomplete
    blocks permit partial findings but never a PASS/FAIL verdict.
    """
    integrity_issues = list(input_issues or [])
    counts = {name: 0 for name in CATEGORIES}

    if integrity_issues:
        return dict(status='cannot_validate', passed=False, total_blocks=0,
                    marker_count=0, incomplete_count=0, counts=counts,
                    problems=[], integrity_issues=integrity_issues, unexpected=[])

    if not log_text or not log_text.strip():
        return validate('', input_issues=['The log is empty. Upload or paste a nonempty SQLines log.'])
    if '\x00' in log_text:
        return validate('', input_issues=['The log contains binary data or unsupported NUL characters.'])

    parsed = parse_log(log_text)
    integrity_issues.extend(parsed.issues)
    unexpected = []
    for block in parsed.blocks:
        category = classify_block(block)
        if category is None:
            block.analysis = analyze_sql_error(block.sql, block.error)
            unexpected.append(block)
        else:
            counts[category] += 1

    problems = []
    if counts['uuidtostr'] == 0:
        problems.append('No UUIDtoSTR errors found.')
    for name in EXPECTED_INDEXES:
        if counts[name] != 1:
            problems.append(f'{name}: expected 1, found {counts[name]}.')
    if counts['ix_cnt_diffweeks'] != 1:
        problems.append(f'ix_cnt_diffweeks: expected 1, found {counts["ix_cnt_diffweeks"]}.')
    if unexpected:
        problems.append(f'Found {len(unexpected)} unexpected error(s).')

    status = 'cannot_validate' if integrity_issues else 'fail' if problems else 'pass'
    return dict(status=status, passed=(status == 'pass'),
                total_blocks=len(parsed.blocks), marker_count=parsed.marker_count,
                incomplete_count=parsed.incomplete_count, counts=counts,
                problems=problems, integrity_issues=integrity_issues,
                unexpected=unexpected)
