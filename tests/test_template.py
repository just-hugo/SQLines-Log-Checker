"""Jinja UI regression checks without requiring a running Flask server."""
import sys
import unittest
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validator import validate
from test_integrity import expected_log, failed


class TemplateTests(unittest.TestCase):
    def setUp(self):
        env = Environment(loader=FileSystemLoader(str(ROOT / 'templates')),
                          autoescape=select_autoescape(['html']))
        self.template = env.get_template('index.html')

    def render(self, result, annotations=None):
        return self.template.render(result=result, annotations=annotations or {},
                                    report_id='digest-test', shutdown_token='token-test')

    def test_initial_page_shows_input_and_no_export_controls(self):
        html = self.render(None)
        self.assertIn('id="log-form"', html)
        self.assertNotIn('id="copy-report"', html)

    def test_pass_has_export_controls_and_no_notes(self):
        html = self.render(validate(expected_log()))
        self.assertIn('Validation passed', html)
        self.assertIn('id="copy-report"', html)
        self.assertIn('id="download-report"', html)
        self.assertNotIn('class="investigation-note"', html)

    def test_error_is_expanded_until_resolved(self):
        result = validate(expected_log() + failed(
            'ALTER TABLE GROUP1.[category_tb_OLD] ADD PRIMARY KEY ([ca_code]);',
            'The duplicate key value is (HAY ).'))
        initial = self.render(result)
        self.assertIn('class="error-card" data-error-index="0" open', initial)
        self.assertIn('Investigation / resolution notes', initial)
        self.assertIn('type="checkbox" class="resolved-checkbox"', initial)
        saved = self.render(result, {'0': {'note': '<unsafe> & resolved', 'resolved': True}})
        self.assertIn('class="error-card" data-error-index="0" >', saved)
        self.assertIn('&lt;unsafe&gt; &amp; resolved', saved)
        self.assertIn('resolved-tag', saved)


if __name__ == '__main__':
    unittest.main()
