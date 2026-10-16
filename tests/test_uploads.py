"""Flask upload and paste tests (run when Flask is installed)."""
import importlib.util
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@unittest.skipUnless(importlib.util.find_spec('flask'), 'Flask not installed in test environment')
class UploadTests(unittest.TestCase):
    def setUp(self):
        import app as app_module
        self.module = app_module
        self.module._latest_result = None
        self.client = app_module.app.test_client()

    def upload(self, name, content):
        return self.client.post('/', data={'log_file': (io.BytesIO(content), name)},
                                content_type='multipart/form-data', follow_redirects=True)

    def test_reject_non_sql_extension(self):
        response = self.upload('test.log', b'ALTER TABLE t ADD PRIMARY KEY (id);')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cannot validate', response.data)
        self.assertIn(b'Uploaded files must have a .sql extension.', response.data)
        self.assertEqual(self.module._latest_result['status'], 'cannot_validate')

    def test_accept_uppercase_extension(self):
        response = self.upload('test.SQL', b'-- Failed (0 ms)\n')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Uploaded files must have a .sql extension.', response.data)
        self.assertEqual(self.module._latest_result['status'], 'cannot_validate')
        self.assertTrue(any('SQL statement not identified' in p for p in
                            self.module._latest_result['integrity_issues']))

    def test_paste_does_not_require_filename(self):
        response = self.client.post('/', data={'log_text': 'unrelated pasted text'},
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cannot validate', response.data)
        self.assertNotIn(b'Uploaded files must have a .sql extension.', response.data)

    def test_results_still_available_on_refresh(self):
        self.upload('test.txt', b'any content')
        response = self.client.get('/')
        self.assertIn(b'Cannot validate', response.data)
        self.assertIn(b'.sql extension', response.data)


if __name__ == '__main__':
    unittest.main()
