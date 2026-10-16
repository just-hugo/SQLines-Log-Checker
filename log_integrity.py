"""Parse SQLines failure blocks and report incomplete/malformed log entries.

No end-of-log marker is assumed. A log that ends after a complete block
cannot be proven complete solely from its content.
"""

import re
from dataclasses import dataclass, field

# A broad marker finds malformed status lines as well as valid ones.
FAILED_CANDIDATE = re.compile(r"^\s*--\s*Failed(?=\s*\(|\s*$)", re.IGNORECASE)
FAILED_MARKER = re.compile(r"^\s*--\s*Failed\s*\(\s*\d+\s+ms\s*\)\s*$", re.IGNORECASE)
SQL_START = re.compile(
    r"^\s*(?:ALTER|CREATE|DROP|INSERT|UPDATE|DELETE|MERGE|TRUNCATE|"
    r"EXEC(?:UTE)?|GRANT|REVOKE|WITH|DBCC|SET|COMMENT|RENAME)\b",
    re.IGNORECASE,
)
# SQLines errors are '-- ...' comment lines, usually with an ODBC driver prefix.
ERROR_START = re.compile(r"^\s*--\s*(?:\[.+|(?:error|warning|sqlcode|sqlstate)\b)", re.IGNORECASE)

# SQLines writes these four nonempty header lines before its first error.
# Versions, copyright years, and timestamps vary between conversions.
HEADER_LINES = (
    re.compile(r"^--\s*SQLines Data\b.*-\s*Database Migration and Validation Tool\.?\s*$", re.I),
    re.compile(r"^--\s*Copyright\s*\(c\)\s*\d{4}\s+SQLines\.\s+All Rights Reserved\.?\s*$", re.I),
    re.compile(r"^--\s*Failed DDL SQL statements executed for the target database\s*$", re.I),
    re.compile(r"^--\s*Current timestamp:\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?\s*$", re.I),
)


def has_sqlines_header(lines: list[str]) -> bool:
    """Require the standard header at the start, ignoring only blank lines and a BOM."""
    meaningful = [line.lstrip('\ufeff').strip() for line in lines if line.strip('\ufeff').strip()]
    return (len(meaningful) >= len(HEADER_LINES)
            and all(pattern.fullmatch(line) for pattern, line in zip(HEADER_LINES, meaningful)))


@dataclass
class ErrorBlock:
    sql: str
    status: str
    error: str
    analysis: dict | None = None
    raw_log: str = ""


@dataclass
class ParseResult:
    blocks: list[ErrorBlock] = field(default_factory=list)
    marker_count: int = 0
    issues: list[str] = field(default_factory=list)

    @property
    def incomplete_count(self):
        return self.marker_count - len(self.blocks)


def parse_log(log_text: str) -> ParseResult:
    lines = log_text.splitlines(keepends=True)
    found = ParseResult()
    if not has_sqlines_header(lines):
        found.issues.append(
            'Missing or unrecognized SQLines header. Expected the SQLines Data '
            'identification, copyright, Failed DDL section, and current timestamp '
            'at the beginning of the log.'
        )
    cursor = 0  # first line not consumed by a previous parsed block

    for marker_idx, marker_line in enumerate(lines):
        if not FAILED_CANDIDATE.match(marker_line):
            continue

        found.marker_count += 1
        marker_number = marker_idx + 1
        if not FAILED_MARKER.fullmatch(marker_line.strip()):
            found.issues.append(f"Line {marker_number}: malformed failure marker: {marker_line.strip()}")
            cursor = marker_idx + 1
            continue

        # Find the SQL statement within this block, never reusing a statement
        # from a previous failure or from the SQLines header.
        sql_start = None
        for j in range(cursor, marker_idx):
            if SQL_START.match(lines[j]):
                sql_start = j
        sql = ''.join(lines[sql_start:marker_idx]).strip() if sql_start is not None else ''

        # A normal error starts at the next nonempty line after the marker.
        err_idx = marker_idx + 1
        while err_idx < len(lines) and not lines[err_idx].strip():
            err_idx += 1

        if err_idx >= len(lines) or not ERROR_START.match(lines[err_idx]):
            if err_idx >= len(lines):
                reason = 'the log ends before its error message'
            elif SQL_START.match(lines[err_idx]):
                reason = f'the next SQL statement starts at line {err_idx + 1}'
            elif FAILED_CANDIDATE.match(lines[err_idx]):
                reason = f'another failure marker starts at line {err_idx + 1}'
            else:
                reason = f'no recognizable error message follows (line {err_idx + 1})'
            found.issues.append(f'Line {marker_number}: incomplete error block; {reason}.')
            cursor = marker_idx + 1
            continue

        # Preserve continuation lines when SQLines splits an error across lines.
        err_end = err_idx + 1
        while err_end < len(lines):
            candidate = lines[err_end]
            if not candidate.strip() or FAILED_CANDIDATE.match(candidate) or SQL_START.match(candidate):
                break
            if not candidate.lstrip().startswith('--'):
                break
            err_end += 1

        error = ''.join(lines[err_idx:err_end]).strip()
        if not sql:
            found.issues.append(f'Line {marker_number}: incomplete error block; SQL statement not identified.')
        else:
            # The full original excerpt includes the statement, status and error.
            raw = ''.join(lines[sql_start:err_end]).rstrip('\r\n')
            found.blocks.append(ErrorBlock(sql=sql, status=marker_line.strip(),
                                           error=error, raw_log=raw))
        cursor = err_end

    if found.marker_count == 0:
        found.issues.append('No SQLines failure markers were found in the input.')
    if found.incomplete_count:
        found.issues.append(
            f'Failure accounting mismatch: {found.marker_count} failure marker(s) detected, '
            f'but only {len(found.blocks)} complete error block(s) parsed.'
        )
    return found
