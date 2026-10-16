"""Flask endpoint tests; run with Flask installed."""
import importlib.util
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from test_integrity import expected_log, failed


@unittest.skipUnless(importlib.util.find_spec('flask'), 'Flask not installed in this environment')
class InvestigationApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = patch.dict(os.environ, {'SQLINES_NOTES_DIR': self.tmp.name})
        env.start()
        self.addCleanup(env.stop)
        import app as app_module
        self.module = app_module
        self.module._latest_result = None
        self.module._latest_report_id = None
        self.client = app_module.app.test_client()

    def test_note_saved_across_refresh_and_reupload_and_used_in_report(self):
        log = expected_log() + failed(
            'ALTER TABLE GROUP1.[category_tb_OLD] ADD PRIMARY KEY ([ca_code]);',
            'The duplicate key value is (HAY ).'
        )
        upload = lambda: self.client.post('/', data={'log_file': (io.BytesIO(log.encode()), 'migration.sql')},
                                          content_type='multipart/form-data', follow_redirects=True)
        uploaded = upload()
        self.assertIn(b'Investigation / resolution notes', uploaded.data)
        self.assertIn(b'Unexpected error 1', uploaded.data)
        bad_token = self.client.post('/_investigation', json={})
        self.assertEqual(bad_token.status_code, 403)
        body = {'report_id': self.module._latest_report_id, 'index': 0,
                'note': 'Fixed the trailing space in HAY ', 'resolved': True}
        saved = self.client.post('/_investigation', json=body,
                                 headers={'X-SQLines-Shutdown-Token': self.module._shutdown_token})
        self.assertEqual(saved.status_code, 200)
        refreshed = self.client.get('/')
        self.assertIn(b'Fixed the trailing space in HAY ', refreshed.data)
        self.assertIn(b'class="error-card" data-error-index="0"', refreshed.data)
        self.assertIn(b'resolved-tag', refreshed.data)
        report = self.client.get('/_report').get_data(as_text=True)
        self.assertIn('Fixed the trailing space in HAY ', report)
        self.assertIn('Unexpected error 1 - RESOLVED', report)
        downloaded = self.client.get('/_report?download=1')
        self.assertIn('attachment;', downloaded.headers['Content-Disposition'])
        # A second analysis of the same file restores the annotations.
        self.assertIn(b'Fixed the trailing space in HAY ', upload().data)
        # Other log contents must not inherit this note.
        self.client.post('/', data={'log_text': expected_log()}, follow_redirects=True)
        self.assertNotIn('Fixed the trailing space', self.client.get('/_report').get_data(as_text=True))
        self.assertIn('Validation status: PASS', self.client.get('/_report').get_data(as_text=True))

    def test_malformed_or_stale_note_rejected(self):
        self.client.post('/', data={'log_text': expected_log()}, follow_redirects=True)
        headers = {'X-SQLines-Shutdown-Token': self.module._shutdown_token}
        invalid = self.client.post('/_investigation', headers=headers, json={
            'report_id': self.module._latest_report_id, 'index': 0, 'note': '', 'resolved': True
        })
        self.assertEqual(invalid.status_code, 409)  # no unexpected errors in a PASS log
        self.assertEqual(self.client.post('/_investigation', headers=headers, json={
            'report_id': 'invalid', 'index': 0, 'note': '', 'resolved': False
        }).status_code, 409)


if __name__ == '__main__':
    unittest.main()
