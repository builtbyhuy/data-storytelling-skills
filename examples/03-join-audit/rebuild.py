"""Reproduce the synthetic join failure and its invoice-level correction.

The join oracle deliberately materializes row pairs instead of using the
helper's grouped multiplicity calculation. Standard library only.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import subprocess
import sys


EXAMPLE = Path(__file__).resolve().parent
REPO = EXAMPLE.parents[1]
HELPER = REPO / 'skills/business-insight-diagnosis/scripts/join_audit.py'
LEFT = EXAMPLE / 'inputs/invoice-lines.csv'
RIGHT = EXAMPLE / 'inputs/payment-allocations.csv'


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def dollars(value):
    return format(value, '.2f')


def rebuild(out):
    if out.exists():
        raise ValueError('Use a new output directory; retained evidence is never overwritten.')
    before = {str(path.relative_to(REPO)).replace('\\', '/'): file_hash(path) for path in (LEFT, RIGHT)}
    left, right = read_csv(LEFT), read_csv(RIGHT)

    inner = [(line, payment) for line in left for payment in right
             if line['invoice_id'] == payment['invoice_id']]
    left_join = []
    for line in left:
        matches = [payment for payment in right if payment['invoice_id'] == line['invoice_id']]
        left_join.extend((line, payment) for payment in matches or [None])

    source_total = sum((Decimal(row['net_amount_usd']) for row in left), Decimal(0))
    inner_total = sum((Decimal(line['net_amount_usd']) for line, _ in inner), Decimal(0))
    joined_total = sum((Decimal(line['net_amount_usd']) for line, _ in left_join), Decimal(0))
    received_total = sum((Decimal(row['received_amount_usd']) for row in right), Decimal(0))

    completed = subprocess.run([
        sys.executable, str(HELPER), '--left', str(LEFT), '--right', str(RIGHT),
        '--left-key', 'invoice_id', '--right-key', 'invoice_id',
        '--expect', 'many-to-many', '--left-measure', 'net_amount_usd',
        '--out', str(out),
    ], check=True, capture_output=True, text=True)
    report_path = out / 'report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    assert report['status'] == 'cardinality_holds'
    assert report['predicted_rows']['inner'] == len(inner) == 11
    assert report['predicted_rows']['left'] == len(left_join) == 13
    assert Decimal(report['left_measure']['source_total']) == source_total == Decimal('1200')
    assert Decimal(report['left_measure']['inner_join_total']) == inner_total == Decimal('2350')
    assert Decimal(report['left_measure']['left_join_total']) == joined_total == Decimal('2500')
    assert Decimal(report['left_measure']['duplication_excess']) == joined_total - source_total == Decimal('1300')
    assert received_total == Decimal('1050')

    # Preserve hashes and every numeric helper field; redact only machine-local paths.
    for side, path in [('left', LEFT), ('right', RIGHT)]:
        report['sources'][side]['path'] = str(path.relative_to(REPO)).replace('\\', '/')
    report_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    reconciled = []
    for invoice_id in sorted({row['invoice_id'] for row in left}):
        billed = sum((Decimal(row['net_amount_usd']) for row in left
                      if row['invoice_id'] == invoice_id), Decimal(0))
        paid = sum((Decimal(row['received_amount_usd']) for row in right
                    if row['invoice_id'] == invoice_id), Decimal(0))
        reconciled.append({'invoice_id': invoice_id, 'invoiced_usd': dollars(billed),
                           'received_usd': dollars(paid), 'outstanding_usd': dollars(billed - paid)})
    assert sum(Decimal(row['invoiced_usd']) for row in reconciled) == source_total
    assert sum(Decimal(row['received_usd']) for row in reconciled) == received_total
    assert sum(Decimal(row['outstanding_usd']) for row in reconciled) == Decimal('150')
    with (out / 'invoice-reconciliation.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['invoice_id', 'invoiced_usd', 'received_usd', 'outstanding_usd'])
        writer.writeheader()
        writer.writerows(reconciled)

    after = {str(path.relative_to(REPO)).replace('\\', '/'): file_hash(path) for path in (LEFT, RIGHT)}
    assert before == after
    verification = {
        'case': 'synthetic invoice lines joined to payment allocations',
        'helper_exit_code': completed.returncode,
        'helper_sha256': file_hash(HELPER),
        'input_sha256': before,
        'inputs_unchanged': True,
        'independent_check': 'Materialized every matching line-payment pair with a nested loop; Decimal sums use USD.',
        'checks': {
            'inner_rows': len(inner), 'left_join_rows': len(left_join),
            'source_revenue_usd': dollars(source_total),
            'inner_join_revenue_usd': dollars(inner_total),
            'left_join_revenue_usd': dollars(joined_total),
            'duplication_excess_usd': dollars(joined_total - source_total),
            'received_cash_usd': dollars(received_total),
            'outstanding_usd': dollars(source_total - received_total),
            'corrected_invoice_rows': len(reconciled),
        },
        'report_normalization': 'Only sources.left.path and sources.right.path replaced with repository-relative paths; hashes and numeric helper fields unchanged.',
        'scope': 'Checks establish these synthetic amounts and this join error, not comparative skill quality or production outcomes.',
    }
    (out / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(verification['checks']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True, help='New output directory')
    args = parser.parse_args()
    rebuild(args.out.resolve())
