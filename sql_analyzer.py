"""Conservative, best-effort extraction of diagnostics from SQLines failures."""
import re

IDENT = r'(?:\[[^\]]+(?:\]\][^\]]+)*\]|"(?:[^"]|"")+"|[A-Za-z_][\w$#@]*)'
QUALIFIED = rf'(?P<object>{IDENT}(?:\s*\.\s*{IDENT}){{0,2}})'


def _parts(value):
    tokens = re.findall(IDENT, value)
    return [s[1:-1].replace(']]', ']') if s.startswith('[') else s[1:-1].replace('""', '"') if s.startswith('"') else s for s in tokens]


def _columns(segment):
    return _parts(segment) if re.fullmatch(rf'\s*{IDENT}(?:\s*,\s*{IDENT})*\s*', segment) else []


def visible_whitespace(value):
    """Display whitespace without altering the underlying extracted value."""
    mapping = {' ': '[SPACE]', '\t': '[TAB]', '\r': '[CR]', '\n': '[LF]', '\v': '[VT]', '\f': '[FF]'}
    return ''.join(mapping.get(c, f'[U+{ord(c):04X}]' if ord(c) < 32 or ord(c) == 127 else c) for c in value)


def analyze_sql_error(sql, error):
    """Return extracted facts only; unrecognized values remain None/empty."""
    data = dict(schema=None, table=None, columns=[], operation=None,
                constraint=None, index=None, error_type=None,
                duplicate_value=None, duplicate_value_visible=None, problem=None, value=None, value_visible=None)
    sql = sql.strip()
    m = re.match(rf'^ALTER\s+TABLE\s+{QUALIFIED}\s+', sql, re.I | re.S)
    if m:
        parts = _parts(m.group('object'))
        if len(parts) >= 2:
            data['schema'] = parts[-2]
        data['table'] = parts[-1]
        rest = sql[m.end():]
        pk = re.match(rf'ADD\s+(?:CONSTRAINT\s+(?P<constraint>{IDENT})\s+)?PRIMARY\s+KEY\s*\((?P<cols>[^()]*)\)', rest, re.I | re.S)
        if pk:
            data['operation'] = 'ADD PRIMARY KEY'
            data['columns'] = _columns(pk.group('cols'))
            if pk.group('constraint'):
                data['constraint'] = _parts(pk.group('constraint'))[0]
        else:
            constraint = re.match(rf'ADD\s+CONSTRAINT\s+(?P<name>{IDENT})', rest, re.I)
            default = re.match(rf'ADD\s+DEFAULT\s+.+?\s+FOR\s+(?P<column>{IDENT})\s*;?\s*$', rest, re.I | re.S)
            alter = re.match(rf'ALTER\s+COLUMN\s+(?P<column>{IDENT})\s+', rest, re.I | re.S)
            if constraint:
                data['operation'] = 'ADD CONSTRAINT'
                data['constraint'] = _parts(constraint.group('name'))[0]
                fk = re.match(rf'ADD\s+CONSTRAINT\s+{IDENT}\s+FOREIGN\s+KEY\s*\((?P<src>[^()]*)\)\s+REFERENCES\s+(?P<target>{IDENT}(?:\s*\.\s*{IDENT}){{0,2}})\s*\((?P<dst>[^()]*)\)', rest, re.I | re.S)
                if fk:
                    data['operation'] = 'ADD FOREIGN KEY'
                    data['columns'] = _columns(fk.group('src'))
                    data['referenced_columns'] = _columns(fk.group('dst'))
                    target_parts = _parts(fk.group('target'))
                    data['referenced_table'] = target_parts[-1]
                    data['referenced_schema'] = target_parts[-2] if len(target_parts) > 1 else None
            elif default:
                data['operation'] = 'ADD DEFAULT'
                data['columns'] = _parts(default.group('column'))
            elif alter:
                data['operation'] = 'ALTER COLUMN'
                data['columns'] = _parts(alter.group('column'))
    else:
        m = re.match(rf'^CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?P<index>{IDENT})\s+ON\s+{QUALIFIED}\s*\((?P<cols>[^()]*)\)', sql, re.I | re.S)
        if m:
            parts = _parts(m.group('object'))
            data['schema'] = parts[-2] if len(parts) >= 2 else None
            data['table'] = parts[-1]
            data['index'] = _parts(m.group('index'))[0]
            data['columns'] = _columns(m.group('cols'))
            data['operation'] = 'CREATE INDEX'

    if (data['operation'] == 'ADD FOREIGN KEY' and
        re.search(r'there are no primary or candidate keys in the referenced table', error, re.I)):
        data['error_type'] = 'Missing referenced key'
        ref_table = data.get('referenced_table')
        ref_cols = data.get('referenced_columns', [])
        if ref_table and ref_cols:
            ref_name = '.'.join(filter(None, (data.get('referenced_schema'), ref_table)))
            data['problem'] = f'No matching primary or unique key on {ref_name}({", ".join(ref_cols)}).'
        else:
            data['problem'] = 'Referenced table lacks a matching primary or unique key.'
    elif re.search(r'\bduplicate key\b', error, re.I):
        data['error_type'] = 'Duplicate key'
        # SQL Server's wording is known; preserve all characters inside parentheses.
        value_match = re.search(r'\bduplicate key value is\s*\((.*?)\)\s*\.', error, re.I | re.S)
        if value_match:
            value = value_match.group(1)
            data['duplicate_value'] = value
            data['duplicate_value_visible'] = visible_whitespace(value)
            data['value'] = value
            data['value_visible'] = data['duplicate_value_visible']
        data['problem'] = 'Duplicate key value'
    elif re.search(r'\bincorrect syntax\b', error, re.I):
        data['error_type'] = 'SQL syntax error'
        data['problem'] = 'SQL syntax error'
    elif re.search(r'\balready exists\b', error, re.I):
        data['error_type'] = 'Object already exists'
        data['problem'] = 'Object already exists'

    return data
