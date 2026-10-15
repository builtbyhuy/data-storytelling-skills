from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

parties, elections = [d.copy() for d in dfs]
d = elections.merge(parties[['Party_ID','Party']], left_on='Party', right_on='Party_ID', how='inner', suffixes=('_id','_name'))
s = d.groupby('Party_name', sort=True)['Delegate'].count()
h.pie(plt, s, 'Delegates by party')
