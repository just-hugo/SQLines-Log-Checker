"""Regression tests for the SQLines input and error-block integrity checks."""
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validator import validate, parse_blocks

UUID = (
    'ALTER TABLE GROUP1.[demo_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [demo_id];\n\n'
    '-- Failed (0 ms)\n'
    '-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed '
    'in this context, and the user-defined function or aggregate "dbo/UUIDtoSTR" could not be found.\n'
).replace('dbo/UUIDtoSTR', 'dbo/UUIDtoSTR')


def failed(sql, message, status='-- Failed (0 ms)'):
    return f'{sql}\n\n{status}\n-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]{message}\n\n'


def expected_log():
    s = ('-- SQLines Data 3.3.773 x64 - Database Migration and Validation Tool.\n'
         '-- Copyright (c) 2024 SQLines. All Rights Reserved.\n\n'
         '-- Failed DDL SQL statements executed for the target database\n\n'
         '-- Current timestamp: 2026-09-03 14:11:28.757\n\n')
    s += failed(
        'ALTER TABLE GROUP1.[demo_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [demo_id];',
        'Column "dbo" is not allowed in this context, and the user-defined function '
        'or aggregate "dbo/UUIDtoSTR" could not be found.'.replace('dbo/UUIDtoSTR', 'dbo.UUIDtoSTR')
    )
    for name in ('pbcatt_x', 'pbcatc_x', 'pbcatf_x', 'pbcatv_x', 'pbcate_x'):
        s += failed(
            f'CREATE UNIQUE INDEX [{name}] ON GROUP1.[{name}_tb] ([code]);',
            f"The operation failed because an index or statistics with name '{name}' already exists."
        )
    s += failed('CREATE INDEX [ix_cnt_diffweeks] ON GROUP1.[weeksales_post_tb] ();',
                "Incorrect syntax near ')'.")
    return s


class IntegrityTests(unittest.TestCase):
    def test_complete_log_passes_and_ignores_header_failed_ddl(self):
        result = validate(expected_log())
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['marker_count'], 7)
        self.assertEqual(result['total_blocks'], 7)
        self.assertEqual(result['incomplete_count'], 0)
        self.assertEqual(result['integrity_issues'], [])

    def test_header_missing_means_cannot_validate_even_when_errors_are_complete(self):
        log = expected_log()
        log = '\n'.join(log.splitlines()[6:]) + '\n'
        result = validate(log)
        self.assertEqual(result['status'], 'cannot_validate')
        self.assertEqual(result['marker_count'], 7)
        self.assertEqual(result['total_blocks'], 7)
        self.assertTrue(any('SQLines header' in issue for issue in result['integrity_issues']))

    def test_missing_header_line_is_rejected(self):
        log = expected_log().replace('-- Copyright (c) 2024 SQLines. All Rights Reserved.\n', '')
        result = validate(log)
        self.assertEqual(result['status'], 'cannot_validate')
        self.assertTrue(any('SQLines header' in issue for issue in result['integrity_issues']))

    def test_header_allows_varying_version_year_timestamp_and_bom(self):
        log = expected_log().replace('3.3.773', '4.2.1001').replace('2024', '2026')
        log = log.replace('2026-09-03 14:11:28.757', '2026-10-15 19:34:00')
        result = validate('\ufeff' + log)
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['marker_count'], 7)

    def test_header_in_middle_is_not_accepted(self):
        log = 'ALTER TABLE GROUP1.[x] ADD PRIMARY KEY ([id]);\n' + expected_log()
        result = validate(log)
        self.assertEqual(result['status'], 'cannot_validate')

    def test_unexpected_sql_error_is_fail_not_invalid(self):
        text = expected_log() + failed(
            'ALTER TABLE GROUP1.[category_tb_OLD] ADD PRIMARY KEY ([ca_code]);',
            "The duplicate key value is (HAY )."
        )
        result = validate(text)
        self.assertEqual(result['status'], 'fail')
        self.assertEqual(len(result['unexpected']), 1)
        self.assertEqual(result['unexpected'][0].analysis['value'], 'HAY ')

    def test_missing_expected_error_is_fail(self):
        s = expected_log().replace(
            failed('CREATE UNIQUE INDEX [pbcatt_x] ON GROUP1.[pbcatt_x_tb] ([code]);',
                   "The operation failed because an index or statistics with name 'pbcatt_x' already exists."), ''
        )
        result = validate(s)
        self.assertEqual(result['status'], 'fail')
        self.assertIn('pbcatt_x: expected 1, found 0.', result['problems'])

    def test_excess_expected_error_is_fail(self):
        s = expected_log() + failed(
            'CREATE UNIQUE INDEX [pbcatt_x] ON GROUP1.[pbcatt_x_tb] ([code]);',
            "The operation failed because an index or statistics with name 'pbcatt_x' already exists."
        )
        result = validate(s)
        self.assertEqual(result['status'], 'fail')
        self.assertIn('pbcatt_x: expected 1, found 2.', result['problems'])

    def test_truncated_last_error_message_cannot_validate(self):
        s = expected_log() + 'ALTER TABLE GROUP1.[other_tb] ADD PRIMARY KEY ([id]);\n\n-- Failed (0 ms)\n'
        result = validate(s)
        self.assertEqual(result['status'], 'cannot_validate')
        self.assertEqual(result['marker_count'], 8)
        self.assertEqual(result['total_blocks'], 7)
        self.assertEqual(result['incomplete_count'], 1)
        self.assertTrue(any('log ends' in issue for issue in result['integrity_issues']))

    def test_truncated_middle_error_not_paired_with_next_sql(self):
        s = expected_log() + (
            'ALTER TABLE GROUP1.[first_tb] ADD PRIMARY KEY ([id]);\n\n'
            '-- Failed (17 ms)\n\n'
            'ALTER TABLE GROUP1.[second_tb] ADD PRIMARY KEY ([id]);\n\n'
            '-- Failed (0 ms)\n'
            '-- [Microsoft][SQL Server]The duplicate key value is (AA).\n'
        )
        result = validate(s)
        self.assertEqual(result['status'], 'cannot_validate')
        self.assertEqual(result['incomplete_count'], 1)
        self.assertEqual(len(result['unexpected']), 1)
        self.assertIn('second_tb', result['unexpected'][0].sql)
        self.assertNotIn('first_tb', result['unexpected'][0].sql)

    def test_missing_sql_statement_cannot_validate(self):
        result = validate(expected_log() + '\n-- Failed (0 ms)\n-- [Microsoft][SQL Server]Oops.\n')
        self.assertEqual(result['status'], 'cannot_validate')
        self.assertTrue(any('SQL statement not identified' in p for p in result['integrity_issues']))

    def test_malformed_failure_marker_cannot_validate(self):
        result = validate(expected_log() + '\nCREATE INDEX [fail] ON GROUP1.[t] ([id]);\n-- Failed (??? ms)\n-- [Microsoft][SQL Server]Oops.\n')
        self.assertEqual(result['status'], 'cannot_validate')
        self.assertTrue(any('malformed failure marker' in p for p in result['integrity_issues']))

    def test_empty_and_binary_cannot_validate(self):
        self.assertEqual(validate('')['status'], 'cannot_validate')
        self.assertEqual(validate('  \n ')['status'], 'cannot_validate')
        self.assertEqual(validate('ab\x00cd')['status'], 'cannot_validate')

    def test_unrelated_text_cannot_validate(self):
        self.assertEqual(validate('just some text')['status'], 'cannot_validate')

    def test_rejected_extension_avoids_parsing(self):
        result = validate(expected_log(), input_issues=['Uploaded files must have a .sql extension.'])
        self.assertEqual(result['status'], 'cannot_validate')
        self.assertEqual(result['marker_count'], 0)
        self.assertEqual(result['total_blocks'], 0)

    def test_multiline_sql_and_original_error_are_preserved(self):
        s = expected_log() + (
            'ALTER TABLE GROUP1.[example_tb]\n'
            'ADD PRIMARY KEY ([id]);\n\n'
            '-- Failed (0 ms)\n'
            '-- [Microsoft][SQL Server]Duplicate key on multiple\n'
            '-- diagnostic lines\n'
        )
        result = validate(s)
        self.assertEqual(result['status'], 'fail')
        block = result['unexpected'][0]
        self.assertIn('ADD PRIMARY KEY ([id]);', block.sql)
        self.assertIn('-- diagnostic lines', block.raw_log)
        self.assertIn('ALTER TABLE GROUP1.[example_tb]', block.raw_log)

    def test_actual_sample_regression_when_available(self):
        sample = Path(__file__).resolve().parents[2] / 'test_sqldata_failed.sql'
        if not sample.exists():
            self.skipTest('External example log is not installed')
        result = validate(sample.read_text(encoding='utf-8'))
        self.assertEqual(result['status'], 'fail')
        self.assertEqual(result['marker_count'], 82)
        self.assertEqual(result['total_blocks'], 82)
        self.assertEqual(len(result['unexpected']), 1)
        self.assertEqual(result['incomplete_count'], 0)
        self.assertEqual(result['counts']['uuidtostr'], 75)


if __name__ == '__main__':
    unittest.main()
