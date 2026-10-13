"""Audit an equality join before summing an additive left-table measure.

Standard library only; reads CSV sources, never creates the Cartesian join.
Exit 0: declared cardinality holds; 1: violation, with evidence; 2: invalid input.
Neither a successful audit nor matching totals establishes semantic correctness.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import sys


class InputError(ValueError):
    pass


def amount(value: Fraction) -> str:
    """Exact finite base-ten string, including sums beyond Decimal precision."""
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        twos += 1
        denominator //= 2
    while denominator % 5 == 0:
        fives += 1
        denominator //= 5
    if denominator != 1:
        raise ValueError('Internal amount is not a finite decimal')
    scale = max(twos, fives)
    integer = value.numerator * 2 ** (scale - twos) * 5 ** (scale - fives)
    sign = '-' if integer < 0 else ''
    digits = str(abs(integer)).rjust(scale + 1, '0')
    if scale:
        digits = (digits[:-scale] + '.' + digits[-scale:]).rstrip('0').rstrip('.')
    return sign + digits


def read_table(path: Path, key_columns: list[str], measure: str | None = None):
    if not key_columns or len(set(key_columns)) != len(key_columns):
        raise InputError('Each side requires distinct key column names')
    raw = path.read_bytes()
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise InputError(f'{path.name}: expected UTF-8 CSV') from exc
    reader = csv.reader(io.StringIO(text, newline=''), strict=True)
    try:
        header = next(reader)
    except StopIteration as exc:
        raise InputError(f'{path.name}: missing header') from exc
    if not header or any(not name.strip() for name in header) or len(set(header)) != len(header):
        raise InputError(f'{path.name}: blank or duplicate header')
    missing = [name for name in key_columns + ([measure] if measure else []) if name not in header]
    if missing:
        raise InputError(f'{path.name}: missing columns {missing}')
    key_indices = [header.index(name) for name in key_columns]
    measure_index = header.index(measure) if measure else None
    counts, sums = {}, {}
    records = 0
    for row in reader:
        if len(row) != len(header):
            raise InputError(f'{path.name}: CSV line {reader.line_num} has {len(row)} fields; expected {len(header)}')
        key = tuple(row[index] for index in key_indices)
        if any(not part.strip() for part in key):
            raise InputError(f'{path.name}: blank key at CSV line {reader.line_num}')
        counts[key] = counts.get(key, 0) + 1
        records += 1
        if measure_index is not None:
            value = row[measure_index]
            if not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)', value):
                raise InputError(f'{path.name}: invalid plain decimal in {measure!r} at CSV line {reader.line_num}')
            sums[key] = sums.get(key, Fraction()) + Fraction(value)
    return {
        'path': str(path.resolve()), 'sha256': hashlib.sha256(raw).hexdigest(),
        'rows': records, 'key_columns': key_columns, 'counts': counts, 'sums': sums,
    }


def audit(left, right, expected: str, measure: str | None):
    lc, rc = left['counts'], right['counts']
    keys = sorted(lc.keys() | rc.keys())
    both = lc.keys() & rc.keys()
    left_only, right_only = lc.keys() - rc.keys(), rc.keys() - lc.keys()
    matched_rows = sum(lc[key] * rc[key] for key in both)
    unmatched_left = sum(lc[key] for key in left_only)
    unmatched_right = sum(rc[key] for key in right_only)
    left_unique = all(count == 1 for count in lc.values())
    right_unique = all(count == 1 for count in rc.values())
    violations = []
    if expected in ('one-to-one', 'one-to-many') and not left_unique:
        violations.append('left key is not unique')
    if expected in ('one-to-one', 'many-to-one') and not right_unique:
        violations.append('right key is not unique')
    report = {
        'schema_version': 1,
        'status': 'relationship_violation' if violations else 'cardinality_holds',
        'expected_relationship': expected,
        'violations': violations,
        'sources': {side: {name: table[name] for name in ('path', 'sha256', 'rows', 'key_columns')}
                    for side, table in [('left', left), ('right', right)]},
        'keys': {
            'left_distinct': len(lc), 'right_distinct': len(rc), 'matched_distinct': len(both),
            'left_repeated_keys': sum(count > 1 for count in lc.values()),
            'right_repeated_keys': sum(count > 1 for count in rc.values()),
            'matched_many_to_many_keys': sum(lc[key] > 1 and rc[key] > 1 for key in both),
        },
        'predicted_rows': {
            'inner': matched_rows, 'left': matched_rows + unmatched_left,
            'full': matched_rows + unmatched_left + unmatched_right,
            'unmatched_left': unmatched_left, 'unmatched_right': unmatched_right,
            'matched_left_rows_repeated_by_right': sum(lc[key] for key in both if rc[key] > 1),
        },
        'left_measure': None,
        'evidence': 'key-audit.csv',
        'limits': [
            'Keys are exact strings: no trimming, case folding or numeric coercion.',
            'Blank keys and invalid measures fail; no rows are silently dropped.',
            'The declared relationship is checked across each full source, including unmatched keys.',
            'Amounts assume the selected left measure is additive at the supplied row grain, in one unit.',
            'Cardinality does not establish correct business keys, comparable populations, eligible rows or source authority.',
            'Amounts are exact decimal strings; signed cancellation can hide monetary fanout, so inspect row counts too.',
        ],
    }
    if measure:
        ls = left['sums']
        original = sum(ls.values(), Fraction())
        matched_original = sum((ls[key] for key in both), Fraction())
        unmatched_amount = original - matched_original
        joined = sum((ls[key] * rc[key] for key in both), Fraction())
        report['left_measure'] = {
            'column': measure, 'source_total': amount(original),
            'matched_source_total': amount(matched_original), 'unmatched_left_total': amount(unmatched_amount),
            'inner_join_total': amount(joined), 'left_join_total': amount(joined + unmatched_amount),
            'duplication_excess': amount(joined - matched_original),
            'left_join_change': amount(joined + unmatched_amount - original),
        }
    evidence = []
    for key in keys:
        nl, nr = lc.get(key, 0), rc.get(key, 0)
        evidence.append({
            'key_json': json.dumps(key, ensure_ascii=False, separators=(',', ':')),
            'left_rows': nl, 'right_rows': nr,
            'inner_rows': nl * nr, 'left_join_rows': nl * max(nr, 1),
            'full_join_rows': nl * nr if nl and nr else nl + nr,
            'left_source_amount': amount(left['sums'].get(key, Fraction())) if measure else '',
            'left_inner_amount': amount(left['sums'].get(key, Fraction()) * nr) if measure else '',
            'status': 'matched' if nl and nr else ('left_only' if nl else 'right_only'),
        })
    return report, evidence


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--left', type=Path, required=True)
    parser.add_argument('--right', type=Path, required=True)
    parser.add_argument('--left-key', action='append', required=True, help='Repeat for composite keys')
    parser.add_argument('--right-key', action='append', required=True, help='Same order/arity as left keys')
    parser.add_argument('--expect', choices=['one-to-one', 'one-to-many', 'many-to-one', 'many-to-many'], required=True)
    parser.add_argument('--left-measure', help='Optional additive numeric column; plain decimal, single unit')
    parser.add_argument('--out', type=Path, required=True, help='New directory for report.json and key-audit.csv')
    args = parser.parse_args(argv)
    try:
        if len(args.left_key) != len(args.right_key):
            raise InputError('Key lists must have the same arity and semantic order')
        if args.out.exists():
            raise InputError('Output directory already exists; use a new path')
        left = read_table(args.left, args.left_key, args.left_measure)
        right = read_table(args.right, args.right_key)
        report, evidence = audit(left, right, args.expect, args.left_measure)
        args.out.mkdir(parents=True, exist_ok=False)
        fields = ['key_json', 'left_rows', 'right_rows', 'inner_rows', 'left_join_rows',
                  'full_join_rows', 'left_source_amount', 'left_inner_amount', 'status']
        with (args.out / 'key-audit.csv').open('w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(evidence)
        (args.out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'status': report['status'], 'report': str(args.out / 'report.json')}))
        return 1 if report['violations'] else 0
    except (OSError, ValueError, csv.Error) as exc:
        print(f'join_audit: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
