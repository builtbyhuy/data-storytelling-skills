"""Recompute the four-cell comparison with exact fractions; standard library only."""
import csv
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
with (ROOT / 'data.csv').open(encoding='utf-8', newline='') as handle:
    cells = list(csv.DictReader(handle))
rates, totals = {}, {}
for team in ('A', 'B'):
    rows = [r for r in cells if r['team'] == team]
    leads = sum(int(r['eligible_leads']) for r in rows)
    wins = sum(int(r['wins']) for r in rows)
    high = next(int(r['eligible_leads']) for r in rows if r['lead_tier'] == 'High')
    totals[team] = {'eligible_leads': leads, 'wins': wins,
                    'rate': float(Fraction(wins, leads)),
                    'high_tier_share': float(Fraction(high, leads))}
    rates[team] = {r['lead_tier']: Fraction(int(r['wins']), int(r['eligible_leads'])) for r in rows}
common = {team: sum(rates[team].values()) / 2 for team in rates}
assert totals['A']['wins'] == 24 and totals['B']['wins'] == 36
assert common == {'A': Fraction(2, 5), 'B': Fraction(7, 20)}
result = {'scope': 'Synthetic four-cell fixture; observation period and coaching assignment not supplied',
          'team_totals': totals,
          'within_tier_rates': {t: {tier: float(rate) for tier, rate in d.items()} for t, d in rates.items()},
          'common_mix': {'definition': 'Hypothetical 50% High / 50% Low applied to observed rates',
                         'A': float(common['A']), 'B': float(common['B']),
                         'status': 'descriptive_standardization_not_coaching_effect'},
          'derivation': 'Aggregate=sum(wins)/sum(leads); tier=wins/leads; equal_mix=0.5*High+0.5*Low'}
(ROOT / 'calculations.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print('Team rates and equal-mix comparison reconciled.')
