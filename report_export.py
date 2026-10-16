"""Produce a plain-text validation and investigation report."""

from datetime import datetime

INDEX_NAMES = ('pbcatt_x', 'pbcatc_x', 'pbcatf_x', 'pbcatv_x', 'pbcate_x')


def _check_line(label, count, expected):
    valid = count >= 1 if expected == 'at least 1' else count == expected
    return f"  {label}: {count} found / {expected} required - {'OK' if valid else 'MISMATCH'}"


def build_report(result, annotations, source='Pasted log text', generated=None):
    generated = generated or datetime.now().astimezone()
    status = result['status'].upper().replace('_', ' ')
    counts = result['counts']
    lines = [
        'SQLines Log Checker - Validation Report',
        '=' * 40,
        f'Source: {source}',
        f'Generated: {generated.strftime("%Y-%m-%d %H:%M:%S %Z")}',
        f'Validation status: {status}',
        f'Failure markers found: {result["marker_count"]}',
        f'Complete failure blocks: {result["total_blocks"]}',
        f'Unexpected errors: {len(result["unexpected"])}',
        '',
        'EXPECTED ERROR CHECKS',
        '-' * 40,
    ]
    lines.append(_check_line('UUIDtoSTR default failures', counts['uuidtostr'], 'at least 1'))
    for name in INDEX_NAMES:
        lines.append(_check_line(name, counts[name], 1))
    lines.append(_check_line('ix_cnt_diffweeks', counts['ix_cnt_diffweeks'], 1))
    if result['status'] == 'pass':
        lines.append('All required expected-error patterns and counts confirmed.')
    elif result['status'] == 'cannot_validate':
        lines.append('Counts are partial or unverified; the log could not be fully validated.')
    else:
        lines.append('Expected-error checks are listed above; see any discrepancies below.')

    if result['integrity_issues']:
        lines.extend(['', 'INPUT / LOG INTEGRITY ISSUES', '-' * 40])
        lines.extend(f'- {issue}' for issue in result['integrity_issues'])

    count_problems = [p for p in result['problems'] if not (p.startswith('Found ') and ' unexpected error(s).' in p)]
    if count_problems:
        lines.extend(['', 'VALIDATION DISCREPANCIES', '-' * 40])
        lines.extend(f'- {problem}' for problem in count_problems)

    lines.extend(['', 'UNEXPECTED ERRORS', '-' * 40])
    if not result['unexpected']:
        lines.append('None found.' if result['status'] != 'cannot_validate' else 'None found among the complete blocks parsed (partial results).')
    else:
        if result['status'] == 'cannot_validate':
            lines.append('Partial findings: input could not be completely validated.')
        for i, error in enumerate(result['unexpected']):
            note = annotations.get(str(i), {})
            analysis = error.analysis or {}
            table = analysis.get('table')
            schema = analysis.get('schema')
            table_label = f'{schema}.{table}' if schema and table else table or 'Not identified'
            columns = ', '.join(analysis.get('columns') or []) or 'Not identified'
            value = analysis.get('value_visible') if analysis.get('value') is not None else 'Not applicable'
            problem = analysis.get('problem') or 'See original SQL log error below.'
            lines.extend([
                '',
                f'Unexpected error {i + 1} - {"RESOLVED" if note.get("resolved") else "UNRESOLVED"}',
                f'Table: {table_label}',
                f'Column: {columns}',
                f'Value: {value}',
                f'Problem: {problem}',
                'Investigation notes:',
                note.get('note') or '(None recorded)',
                'SQL Log Error:',
                error.raw_log or '\n\n'.join([error.sql, f'{error.status}\n{error.error}']),
            ])
    return '\n'.join(lines).rstrip() + '\n'
