"""Investigation notes persistence and plain-text export regression tests."""
import hashlib
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from notes_store import load_notes, notes_file, save_notes
from report_export import build_report
from validator import validate
from test_integrity import expected_log, failed


def validation_with_error():
    return validate(expected_log() + failed(
        'ALTER TABLE GROUP1.[category_tb_OLD] ADD PRIMARY KEY ([ca_code]);',
        'The duplicate key value is (HAY ).'
    ))


class NotesStorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = patch.dict(os.environ, {'SQLINES_NOTES_DIR': self.tmp.name})
        p.start()
        self.addCleanup(p.stop)
        self.report_id = hashlib.sha256(b'one sample log').hexdigest()

    def test_empty_notes_do_not_create_file(self):
        self.assertEqual(load_notes(self.report_id), {})
        save_notes(self.report_id, {})
        self.assertFalse(notes_file(self.report_id).exists())

    def test_save_reopen_and_preserve_whitespace(self):
        original = {'0': {'note': 'Found trailing space in HAY  \nFixed key.', 'resolved': True},
                    '1': {'note': 'Another error', 'resolved': False}}
        save_notes(self.report_id, original)
        self.assertEqual(load_notes(self.report_id), original)
        data = notes_file(self.report_id).read_text(encoding='utf-8')
        self.assertNotIn('ALTER TABLE', data)
        save_notes(self.report_id, {})
        self.assertEqual(load_notes(self.report_id), {})

    def test_reject_unsafe_report_ids(self):
        with self.assertRaises(ValueError):
            load_notes('../abc')


class ReportExportTests(unittest.TestCase):
    @staticmethod
    def build(result, notes=None):
        return build_report(result, notes or {}, 'test.sql',
                            datetime(2026, 10, 15, 20, 30, tzinfo=timezone.utc))

    def test_pass_includes_expected_counts_and_no_unexpected(self):
        result = validate(expected_log())
        self.assertEqual(result['status'], 'pass')
        report = self.build(result)
        self.assertIn('Validation status: PASS', report)
        self.assertIn('All required expected-error patterns and counts confirmed.', report)
        self.assertIn('UUIDtoSTR default failures: 1 found', report)
        for name in ('pbcatt_x', 'pbcatc_x', 'pbcatf_x', 'pbcatv_x', 'pbcate_x', 'ix_cnt_diffweeks'):
            self.assertIn(f'{name}: 1 found', report)
        self.assertIn('Unexpected errors: 0', report)
        self.assertIn('None found.', report)

    def test_unexpected_error_contains_notes_resolution_and_raw_sql(self):
        result = validation_with_error()
        self.assertEqual(result['status'], 'fail')
        report = self.build(result, {'0': {'note': 'Investigated duplicate. Fixed trailing space.', 'resolved': True}})
        self.assertIn('Unexpected error 1 - RESOLVED', report)
        self.assertIn('Table: GROUP1.category_tb_OLD', report)
        self.assertIn('Column: ca_code', report)
        self.assertIn('Value: HAY[SPACE]', report)
        self.assertIn('Investigated duplicate. Fixed trailing space.', report)
        self.assertIn('SQL Log Error:', report)
        self.assertIn('-- Failed (0 ms)', report)

    def test_unresolved_error_with_no_note(self):
        report = self.build(validation_with_error())
        self.assertIn('Unexpected error 1 - UNRESOLVED', report)
        self.assertIn('(None recorded)', report)

    def test_cannot_validate_report_explicitly_warns_partial(self):
        result = validate(expected_log() + 'ALTER TABLE GROUP1.[foo] ADD PRIMARY KEY ([id]);\n-- Failed (0 ms)\n')
        self.assertEqual(result['status'], 'cannot_validate')
        report = self.build(result)
        self.assertIn('Validation status: CANNOT VALIDATE', report)
        self.assertIn('Counts are partial or unverified', report)
        self.assertIn('INPUT / LOG INTEGRITY ISSUES', report)
        self.assertNotIn('All required expected-error patterns and counts confirmed.', report)

    def test_missing_expected_does_not_claim_all_found(self):
        result = validate(expected_log().replace(
            failed('CREATE UNIQUE INDEX [pbcatt_x] ON GROUP1.[pbcatt_x_tb] ([code]);',
                   "The operation failed because an index or statistics with name 'pbcatt_x' already exists."), ''
        ))
        report = self.build(result)
        self.assertIn('pbcatt_x: 0 found / 1 required - MISMATCH', report)
        self.assertIn('VALIDATION DISCREPANCIES', report)
        self.assertNotIn('All required expected-error patterns and counts confirmed.', report)


if __name__ == '__main__':
    unittest.main()
