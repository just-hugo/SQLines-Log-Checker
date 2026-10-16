import unittest
from pathlib import Path
from sql_analyzer import analyze_sql_error
from validator import validate

class AnalyzerTests(unittest.TestCase):
    def test_duplicate_key(self):
        a = analyze_sql_error('ALTER TABLE GROUP1.[category_tb_OLD] ADD PRIMARY KEY ([ca_code]);',
            "The duplicate key value is (HAY ).")
        self.assertEqual((a['schema'], a['table'], a['columns'], a['operation']),
                         ('GROUP1', 'category_tb_OLD', ['ca_code'], 'ADD PRIMARY KEY'))
        self.assertEqual(a['duplicate_value'], 'HAY ')
        self.assertEqual(a['duplicate_value_visible'], 'HAY[SPACE]')

    def test_visible_invisible_characters(self):
        from sql_analyzer import visible_whitespace
        self.assertEqual(visible_whitespace(' A\tB\nC\r\v\f '),
                         '[SPACE]A[TAB]B[LF]C[CR][VT][FF][SPACE]')

    def test_original_log_block_preserves_format(self):
        from validator import parse_blocks
        raw = ('ALTER TABLE GROUP1.[category_tb_OLD] ADD PRIMARY KEY ([ca_code]);\r\n'
               '\r\n-- Failed (0 ms)\r\n'
               '-- [Microsoft][SQL Server]The duplicate key value is (HAY ).\r\n\r\n')
        block = parse_blocks(raw)[0]
        self.assertEqual(block.raw_log, raw.rstrip('\r\n'))

    def test_index(self):
        a = analyze_sql_error('CREATE UNIQUE INDEX [ix_abc] ON GROUP1.[items] ([sku], [code]);', 'index already exists')
        self.assertEqual((a['index'], a['columns'], a['table']), ('ix_abc', ['sku', 'code'], 'items'))

    def test_unknown(self):
        a = analyze_sql_error('EXEC unknown_procedure;', 'Unexpected error')
        self.assertIsNone(a['table'])
        self.assertIsNone(a['operation'])

    def test_foreign_key_missing_referenced_key(self):
        cases = [
            ('ret_item_worklist_tb', 'fk_ret_item_work_to_vend'),
            ('ret_header_whl_tb', 'fk_ret_head_to_vendor2'),
            ('ret_manual_invc_header_tb', 'fk_ret_man_inv_hdr_to_vendor'),
        ]
        for table, constraint in cases:
            with self.subTest(table=table):
                sql = (f'ALTER TABLE GROUP1.[{table}] ADD CONSTRAINT [{constraint}] '
                       'FOREIGN KEY ([ve_code]) REFERENCES GROUP1.[vendor_tb] ([ve_code]);')
                error = ("[SQL Server]There are no primary or candidate keys in the referenced "
                         f"table 'GROUP1.vendor_tb' that match the referencing column list "
                         f"in the foreign key '{constraint}'.")
                a = analyze_sql_error(sql, error)
                self.assertEqual(a['table'], table)
                self.assertEqual(a['columns'], ['ve_code'])
                self.assertEqual(a['referenced_table'], 'vendor_tb')
                self.assertEqual(a['referenced_columns'], ['ve_code'])
                self.assertEqual(a['error_type'], 'Missing referenced key')
                self.assertEqual(a['value'], None)
                self.assertIn('GROUP1.vendor_tb(ve_code)', a['problem'])

    def test_original_log(self):
        path = Path(__file__).resolve().parents[2] / 'test_sqldata_failed.sql'
        if not path.exists():
            self.skipTest('Representative log not available')
        result = validate(path.read_text(encoding='utf-8'))
        self.assertEqual(result['total_blocks'], 82)
        self.assertEqual(result['counts']['uuidtostr'], 75)
        self.assertEqual(len(result['unexpected']), 1)
        self.assertEqual(result['unexpected'][0].analysis['duplicate_value'], 'HAY ')

if __name__ == '__main__':
    unittest.main()
