"""Independent black-box checks for join_audit.py, using explicit tiny joins.

Usage: python test_join_audit.py PATH_TO_HELPER --workdir NEW_TEST_DIRECTORY
No third-party packages; generated sources and receipts stay in workdir.
"""
import argparse
import csv
from decimal import Decimal, localcontext
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest


HELPER = None
WORK = None


def csv_bytes(header, rows, bom=False):
    buffer = io.StringIO(newline='')
    writer = csv.writer(buffer)
    writer.writerow(header)
    writer.writerows(rows)
    return buffer.getvalue().encode('utf-8-sig' if bom else 'utf-8')


class JoinAuditTests(unittest.TestCase):
    def setUp(self):
        self.folder = WORK / self.id().split('.')[-1]
        self.folder.mkdir()
        self.number = 0

    def execute(self, left, right, expect='many-to-many', left_keys=('invoice',),
                right_keys=('invoice_ref',), measure='amount', output=None):
        self.number += 1
        run = self.folder / str(self.number)
        run.mkdir()
        left_path, right_path = run / 'invoices.csv', run / 'allocations.csv'
        left_path.write_bytes(left)
        right_path.write_bytes(right)
        out = output(run) if output else run / 'audit'
        command = [sys.executable, '-X', 'utf8', str(HELPER), '--left', str(left_path),
                   '--right', str(right_path), '--expect', expect, '--out', str(out)]
        for key in left_keys:
            command.extend(['--left-key', key])
        for key in right_keys:
            command.extend(['--right-key', key])
        if measure is not None:
            command.extend(['--left-measure', measure])
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=15)
        self.assertEqual(left_path.read_bytes(), left, 'left source changed')
        self.assertEqual(right_path.read_bytes(), right, 'right source changed')
        report = json.loads((out / 'report.json').read_text(encoding='utf-8')) if out.is_dir() and (out / 'report.json').exists() else None
        if report:
            for side, content in [('left', left), ('right', right)]:
                self.assertEqual(report['sources'][side]['sha256'], hashlib.sha256(content).hexdigest())
            with (out / 'key-audit.csv').open(encoding='utf-8', newline='') as file:
                evidence = list(csv.DictReader(file))
        else:
            evidence = None
        return result, report, evidence

    def check_case(self, invoices, allocations, expected='many-to-many',
                   left_keys=('invoice',), right_keys=('invoice_ref',),
                   left_header=('invoice', 'amount'), right_header=('invoice_ref', 'allocation'), bom=False,
                   exit_code=0, measure='amount'):
        result, report, evidence = self.execute(csv_bytes(left_header, invoices, bom),
            csv_bytes(right_header, allocations, bom), expected, left_keys, right_keys, measure)
        self.assertEqual(result.returncode, exit_code, result.stderr)
        self.assertIsNotNone(report)
        li = [left_header.index(key) for key in left_keys]
        ri = [right_header.index(key) for key in right_keys]
        leftkey = lambda row: tuple(row[index] for index in li)
        rightkey = lambda row: tuple(row[index] for index in ri)
        # Explicit nested-loop joins form the oracle; this does not use the helper's
        # group-count multiplication or amount formatting routines.
        inner = [(left, right) for left in invoices for right in allocations if leftkey(left) == rightkey(right)]
        unmatched_left = [row for row in invoices if not any(leftkey(row) == rightkey(other) for other in allocations)]
        unmatched_right = [row for row in allocations if not any(rightkey(row) == leftkey(other) for other in invoices)]
        left_join = inner + [(row, None) for row in unmatched_left]
        full_join = left_join + [(None, row) for row in unmatched_right]
        self.assertEqual(report['predicted_rows']['inner'], len(inner))
        self.assertEqual(report['predicted_rows']['left'], len(left_join))
        self.assertEqual(report['predicted_rows']['full'], len(full_join))
        self.assertEqual(report['predicted_rows']['unmatched_left'], len(unmatched_left))
        self.assertEqual(report['predicted_rows']['unmatched_right'], len(unmatched_right))
        self.assertEqual(report['sources']['left']['rows'], len(invoices))
        self.assertEqual(report['sources']['right']['rows'], len(allocations))
        evidence_by_key = {tuple(json.loads(row['key_json'])): row for row in evidence}
        expected_keys = {leftkey(row) for row in invoices} | {rightkey(row) for row in allocations}
        self.assertEqual(set(evidence_by_key), expected_keys)
        for key in expected_keys:
            item = evidence_by_key[key]
            self.assertEqual(int(item['left_rows']), sum(leftkey(row) == key for row in invoices))
            self.assertEqual(int(item['right_rows']), sum(rightkey(row) == key for row in allocations))
            self.assertEqual(int(item['inner_rows']), sum(leftkey(left) == key for left, right in inner))
            self.assertEqual(int(item['left_join_rows']), sum(leftkey(left) == key for left, right in left_join))
            self.assertEqual(int(item['full_join_rows']), sum((leftkey(left) if left is not None else rightkey(right)) == key for left, right in full_join))
        if measure is None:
            self.assertIsNone(report['left_measure'])
            return report
        with localcontext() as ctx:
            ctx.prec = 300
            ai = left_header.index(measure)
            total = lambda rows: sum((Decimal(row[ai]) for row in rows), Decimal(0))
            source = total(invoices)
            matched_source = total([row for row in invoices if row not in unmatched_left])
            inner_total = total([left for left, right in inner])
            left_total = total([left for left, right in left_join])
            for field, expected_value in {
                'source_total': source, 'matched_source_total': matched_source,
                'unmatched_left_total': total(unmatched_left), 'inner_join_total': inner_total,
                'left_join_total': left_total, 'duplication_excess': inner_total - matched_source,
                'left_join_change': left_total - source,
            }.items():
                self.assertEqual(Decimal(report['left_measure'][field]), expected_value, field)
            for key, item in evidence_by_key.items():
                self.assertEqual(Decimal(item['left_source_amount']), total([row for row in invoices if leftkey(row) == key]))
                self.assertEqual(Decimal(item['left_inner_amount']), total([left for left, right in inner if leftkey(left) == key]))
        return report

    def test_transfer_invoices_to_allocations(self):
        invoices = [('A','100.10'), ('A','-20.05'), ('B','7.25'), ('C','0'), ('D','-5.10'), ('Z','0')]
        allocations = [('A','1'), ('A','2'), ('A','3'), ('B','4'), ('E','5'), ('E','6'), ('D','7'), ('D','8')]
        report = self.check_case(invoices, allocations)
        self.assertEqual(report['keys']['matched_many_to_many_keys'], 1)

    def test_all_declared_relationships(self):
        cases = [([('A','2')], [('A','x')], 'one-to-one', 0),
                 ([('A','2')], [('A','x'), ('A','y')], 'one-to-many', 0),
                 ([('A','2'), ('A','3')], [('A','x')], 'many-to-one', 0),
                 ([('A','2'), ('A','3')], [('A','x'), ('A','y')], 'many-to-many', 0),
                 ([('A','2'), ('A','3')], [('A','x'), ('A','y')], 'one-to-one', 1),
                 ([('A','2'), ('A','3')], [('A','x')], 'one-to-many', 1),
                 ([('A','2')], [('A','x'), ('A','y')], 'many-to-one', 1)]
        for invoices, allocations, relationship, code in cases:
            with self.subTest(relationship=relationship, code=code):
                self.check_case(invoices, allocations, relationship, exit_code=code)

    def test_repeated_unmatched_keys_violate_full_table_contract(self):
        self.check_case([('A','2'), ('L','3'), ('L','4')], [('A','x')], 'one-to-many', exit_code=1)
        self.check_case([('A','2')], [('A','x'), ('R','y'), ('R','z')], 'many-to-one', exit_code=1)

    def test_composite_keys_and_explicit_reordering(self):
        self.check_case([('T1','001','10'), ('T2','001','20'), ('T1','1','30')],
            [('001','T1','a'), ('001','T1','b'), ('001','T2','c'), ('1','T1','d')],
            'one-to-many', ('tenant','invoice'), ('client','invoice_ref'),
            ('tenant','invoice','amount'), ('invoice_ref','client','allocation'))

    def test_key_arity_and_duplicate_requested_key_rejected(self):
        for left_keys, right_keys in [(('invoice','amount'), ('invoice_ref',)), (('invoice','invoice'), ('invoice_ref','allocation'))]:
            result, report, _ = self.execute(b'invoice,amount\nA,1\n', b'invoice_ref,allocation\nA,x\n', left_keys=left_keys, right_keys=right_keys)
            self.assertEqual(result.returncode, 2)
            self.assertIsNone(report)

    def test_signed_cancellation_does_not_hide_rows(self):
        report = self.check_case([('A','100'), ('B','-100'), ('C','0')],
            [('A','1'), ('A','2'), ('B','3'), ('B','4'), ('C','5'), ('C','6')], 'one-to-many')
        self.assertEqual(report['predicted_rows']['inner'], 6)
        self.assertEqual(Decimal(report['left_measure']['duplication_excess']), 0)
        self.assertEqual(report['predicted_rows']['matched_left_rows_repeated_by_right'], 3)

    def test_exact_beyond_28_digits(self):
        self.check_case([('A','10000000000000000000000000000000000000000000000.01'),
                         ('A','.000000000000000000000000000000000000000000000009'),
                         ('B','-10000000000000000000000000000000000000000000000')],
                        [('A','x'), ('A','y'), ('B','z')])

    def test_bom_raw_keys_unicode_quotes_newlines_and_literal_null_tokens(self):
        keys = ['01','1',' A','A','a','A ','NA','NULL','Hóa đơn,α','line\nbreak','quote"id']
        self.check_case([(key,str(index + 1)) for index,key in enumerate(keys)],
            [(key,'allocation') for key in reversed(keys) if key not in ['1','A ']], 'one-to-one', bom=True)

    def test_header_only_empty_sides_and_no_measure(self):
        self.check_case([], [], 'one-to-one')
        self.check_case([('A','2')], [], 'one-to-one')
        self.check_case([], [('R','r')], 'one-to-one')
        self.check_case([('A','arbitrary text')], [('A','r')], 'one-to-one', measure=None)

    def test_missing_blank_duplicate_headers_and_encoding_rejected(self):
        invalid = [b'', b'\n', b'invoice,\nA,2\n', b'invoice,invoice,amount\nA,A,2\n',
                   b'other,amount\nA,2\n', b'invoice,other\nA,2\n', b'invoice,amount\n\xff,2\n']
        for content in invalid:
            with self.subTest(content=repr(content)):
                result, report, _ = self.execute(content, b'invoice_ref,allocation\nA,x\n')
                self.assertEqual(result.returncode, 2)
                self.assertIsNone(report)

    def test_malformed_rows_and_null_keys_not_silently_dropped(self):
        invalid = [b'invoice,amount\nA\n', b'invoice,amount\nA,2,extra\n',
                   b'invoice,amount\nA,2\n\n', b'invoice,amount\n,2\n',
                   b'invoice,amount\n  ,2\n', b'invoice,amount\n"unterminated,2\n']
        for content in invalid:
            with self.subTest(content=repr(content)):
                result, report, _ = self.execute(content, b'invoice_ref,allocation\nA,x\n')
                self.assertEqual(result.returncode, 2)
                self.assertIsNone(report)
        result, report, _ = self.execute(b'invoice,amount\nA,2\n', b'invoice_ref,allocation\n,x\n')
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(report)

    def test_invalid_money_is_never_zero_filled(self):
        for value in ['', 'NaN', 'Infinity', '-inf', '1e3', '1,000', '$2', ' 2', '2 ', '--1', '.', '1/2']:
            with self.subTest(value=value):
                result, report, _ = self.execute(csv_bytes(('invoice','amount'), [('A',value)]), b'invoice_ref,allocation\nA,x\n')
                self.assertEqual(result.returncode, 2)
                self.assertIsNone(report)

    def test_existing_output_and_source_collision_preserve_files(self):
        def existing(run):
            destination = run / 'existing'
            destination.mkdir()
            (destination / 'sentinel').write_bytes(b'preserve me')
            return destination
        result, report, _ = self.execute(b'invoice,amount\nA,2\n', b'invoice_ref,allocation\nA,x\n', output=existing)
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(report)
        self.assertEqual((self.folder / '1' / 'existing' / 'sentinel').read_bytes(), b'preserve me')
        result, report, _ = self.execute(b'invoice,amount\nA,2\n', b'invoice_ref,allocation\nA,x\n', output=lambda run: run / 'invoices.csv')
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('helper', type=Path)
    parser.add_argument('--workdir', type=Path, required=True)
    args = parser.parse_args()
    HELPER, WORK = args.helper.resolve(), args.workdir.resolve()
    WORK.mkdir(parents=True, exist_ok=False)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(JoinAuditTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    receipt = {'helper_sha256': hashlib.sha256(HELPER.read_bytes()).hexdigest(),
               'oracle': 'Explicit nested-loop joins and separate high-precision Decimal sums',
               'tests_run': result.testsRun, 'success': result.wasSuccessful(),
               'failures': [{'test': str(case), 'trace': trace} for case,trace in result.failures],
               'errors': [{'test': str(case), 'trace': trace} for case,trace in result.errors]}
    (WORK / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
